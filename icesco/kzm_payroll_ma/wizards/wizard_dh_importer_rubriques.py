from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
import base64
import io
import pandas as pd


class DhImporterrubriques(models.Model):
    _name = "wizard.dh.importer.rubriques"

    attachment_id = fields.Binary("Fichier")
    payroll_id = fields.Many2one('hr.payroll_ma', string='Payroll')

    def execute(self):
        if self.attachment_id != False:
            file = base64.b64decode(self.attachment_id)
            toread = io.BytesIO()
            toread.write(file)  # pass your `decrypted` string as the argument here
            toread.seek(0)  # reset the pointer
            df = pd.read_excel(toread)
            dh_rows = len(df.index)

            # if df['produit'].value_counts()[df["produit"][i]] != len(self.picking_id.move_line_ids_without_package.filtered(lambda x: x.product_id.name == df["produit"][i])):
            #     raise ValidationError("Le nombre de lignes du fichier que vous essayez d’importer ne correspond au nombre de lignes du BL.")

            for i in range(0, dh_rows):
                for bulletin in self.payroll_id.bulletin_line_ids:
                    for_current_bulletin = False
                    if bulletin.employee_id.matricule.isdigit() == True:
                        if int(bulletin.employee_id.matricule) == df["matricule"][i]:
                            for_current_bulletin = True

                    if bulletin.employee_id.matricule.isdigit() != True:
                        if bulletin.employee_id.matricule == df["matricule"][i]:
                            for_current_bulletin = True

                    if for_current_bulletin:
                        subtotal_employee = float(df["base"][i]) * float(df["rate_employee"][i]) / 100
                        subtotal_employer = float(df["base"][i]) * float(df["rate_employer"][i]) / 100

                        if type(df["rubrique"][i]):
                            credit_account_id = self.env['account.account'].search([('code', '=', int(df["credit_account"][i]))], limit=1)
                            debit_account_id = self.env['account.account'].search([('code', '=', int(df["debit_account"][i]))], limit=1)
                            self.env['hr.payroll_ma.bulletin.line'].create(
                                {'name': df["rubrique"][i], 'type': 'brute', 'base': float(df["base"][i]),
                                 'rate_employee': float(df["rate_employee"][i]), 'subtotal_employee': subtotal_employee,
                                 'rate_employer': float(df["rate_employer"][i]), 'subtotal_employer': subtotal_employer,
                                 'credit_account_id': credit_account_id.id, 'debit_account_id': debit_account_id.id, 'id_bulletin': bulletin.id})

                        bulletin.salaire_net = bulletin.salaire_net + subtotal_employee
                        bulletin.salaire_net_a_payer = bulletin.salaire_net_a_payer + subtotal_employee

                        arrondi = 0

                        # Arrondi
                        # if dictionnaire['arrondi']://
                        if bulletin.company_id.arrondi:  #
                            arrondi = 1 - (round(bulletin.salaire_net_a_payer, 2) - int(bulletin.salaire_net_a_payer))
                            if arrondi != 1:
                                diff = bulletin.salaire_net_a_payer - int(bulletin.salaire_net_a_payer)
                                arrondi = 1 - (bulletin.salaire_net_a_payer - int(bulletin.salaire_net_a_payer))

                                if diff < 0.5:
                                    arrondi = diff * -1
                                else:
                                    arrondi = 1 - diff

                                arrondi = 1 - (bulletin.salaire_net_a_payer - int(bulletin.salaire_net_a_payer))

                                bulletin.salaire_net_a_payer += arrondi
                                self.env['hr.payroll_ma.bulletin.line'].search([('id_bulletin', '=', bulletin.id), ('name', '=', 'Arrondi')]).unlink()
                                arrondi_line = {
                                    'name': 'Arrondi',
                                    'id_bulletin': bulletin.id,
                                    'type': 'retenu',
                                    'base': arrondi,
                                    'rate_employee': 100,
                                    'subtotal_employee': arrondi,
                                    'deductible': True,
                                }
                                self.env['hr.payroll_ma.bulletin.line'].create(arrondi_line)
                            else:
                                arrondi = 0

                        bulletin.arrondi = arrondi

                        bulletin.get_cnss_employee()
                        bulletin.get_nbr_paid_leaves()
                        bulletin.get_nbr_leaves()

        self.attachment_id = False
