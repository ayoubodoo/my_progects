import datetime as dt
import locale
import time
from datetime import timedelta, datetime
from odoo import models, fields
import base64
import io
from io import BytesIO
from odoo import models, fields, api, exceptions, _



class Reportpayement(models.TransientModel):
    _name = 'payemnt.wizard'



    account_id = fields.Many2one("account.payment")
    print = fields.Boolean("Print?",compute="_is_signatures_complets")
    type = fields.Selection([('depense_caisse', 'Pièce Dépense Caisse'),('depense_banque', 'Pièce Dépense Banque'),('virement_mad', 'Virement MAD'), ('virement_devise', 'Lettre Virement Devise'),  ('virement_salaire', 'virement des salaires avec mise à disposition'), ('compte_compte', 'Lettre virement de compte à compte'),('alimentation_carte ', 'Lettre alimentation carte bancaire')],
                            string='Type', required=True)
    signature_supperviseur_affairs_financiere = fields.Binary(string='Signature  Superviseur des affairs financières')
    signature_controlleur_financiere = fields.Binary(string='Signature Contrôleur Financier ')
    signature_dg = fields.Binary(string='Signature Directeur général')
    signature_dg_adjoint = fields.Binary(string='Signature Directeur général Adjoint')
    signature_caissier = fields.Binary(string='Signature Caissier')
    signature_benefciaire = fields.Binary(string='Signature Bénéficiaire')
    signature_res_financier = fields.Binary(string='Signature Résponsable Financier')
    senario = fields.Selection([("s1","SAF/CF/DG"),("s2","SAF/CF/DGA"),("s3","SAF/CF"),("s4","SAF/DG"),("s5","CF/DGA"),("s6","SAF/DGA"),("s7","CF/DG")])

    is_signature_supperviseur_affairs_financiere = fields.Boolean(string='Signature  Superviseur des affairs financières')
    is_signature_controlleur_financiere = fields.Boolean(string='Signature Contrôleur Financier ')
    is_signature_dg = fields.Boolean(string='Signature Directeur général')
    is_signature_dg_adjoint = fields.Boolean(string='Signature Directeur général Adjoint')
    is_signature_caissier = fields.Boolean(string='Signature Caissier')
    is_signature_benefciaire = fields.Boolean(string='Signature Bénéficiaire')
    is_signature_res_financier = fields.Boolean(string='Signature Résponsable Financier')
    @api.depends("signature_supperviseur_affairs_financiere","signature_controlleur_financiere","signature_dg","signature_dg_adjoint","signature_caissier","signature_benefciaire","signature_res_financier")
    def _is_signatures_complets(self):
        self.print = True
        account_payment = self.env['account.payment'].browse(self._context.get('active_id'))

        # if self.signature_supperviseur_affairs_financiere:
        #     if self.signature_controlleur_financiere:
        #         account_payment.signature_supperviseur_affairs_financiere = self.signature_supperviseur_affairs_financiere
        #
        #         if self.type != 'depense_caisse' and self.type != 'depense_banque':
        #             self.print = True
        #         else:
        #             if self.signature_caissier and self.signature_benefciaire and self.signature_res_financier:
        #                 self.print = True
        #                 account_payment.signature_caissier = self.signature_caissier
        #
        #         if self.signature_dg or self.signature_dg_adjoint :
        #             account_payment.signature_dg = self.signature_dg
        #             account_payment.signature_dg_adjoint = self.signature_dg_adjoint
        #
        #             if self.type != 'depense_caisse' and self.type != 'depense_banque':
        #
        #                 self.print = True
        #             else:
        #                 if self.signature_caissier and self.signature_benefciaire and self.signature_res_financier:
        #                     self.print = True
        #     if self.signature_dg_adjoint or self.signature_dg:
        #         account_payment.signature_dg = self.signature_dg
        #         account_payment.signature_dg_adjoint = self.signature_dg_adjoint
        #         if self.type != 'depense_caisse' and self.type != 'depense_banque':
        #             self.print = True
        #         else:
        #             if self.signature_caissier and self.signature_benefciaire and self.signature_res_financier:
        #                 self.print = True
            # else :
            #     raise ValidationError(_("les signatures ne sont pas completes"))

    @api.depends("signature_supperviseur_affairs_financiere", "signature_controlleur_financiere", "signature_dg",
                 "signature_dg_adjoint", "signature_caissier", "signature_benefciaire", "signature_res_financier")
    def get_signatures(self):
        account_payment = self.env['account.payment'].browse(self._context.get('active_id'))

        if self.signature_supperviseur_affairs_financiere:
                account_payment.signature_supperviseur_affairs_financiere = self.signature_supperviseur_affairs_financiere

        if self.signature_controlleur_financiere:
                account_payment.signature_controlleur_financiere = self.signature_controlleur_financiere
        if self.signature_dg_adjoint:
                account_payment.signature_dg_adjoint = self.signature_dg_adjoint
        if self.signature_dg:
                account_payment.signature_dg = self.signature_dg

        if self.signature_caissier:
                account_payment.signature_caissier = self.signature_caissier

        if self.signature_res_financier :
                    account_payment.signature_res_financier = self.signature_res_financier
        if self.signature_benefciaire :
                    account_payment.signature_benefciaire = self.signature_benefciaire


    # def is_signature_set(self):
    #     account_payment = self.env['account.payment'].browse(self._context.get('active_id'))
    # 
    #     if account_payment.signature_supperviseur_affairs_financiere :
    #         self.is_signature_supperviseur_affairs_financiere = True
    # 
    #     # if account_payment.signature_controlleur_financiere:
    #     #     self.is_signature_controlleur_financiere = True
    #     # if account_payment.signature_dg_adjoint:
    #     #
    #     #     self.is_signature_dg_adjoint = True
    #     # if account_payment.signature_dg:
    #     #     self.is_signature_dg = True
    #     #
    #     # if account_payment.signature_caissier:
    #     #     self.is_signature_caissier = True
    #     #
    #     # if account_payment.signature_res_financier :
    #     #     self.is_signature_res_financier = True
    #     # if account_payment.signature_benefciaire :
    #     #     self.is_signature_benefciaire = True


    def generate_repport(self):


        account_payment = self.env['account.payment'].browse(self._context.get('active_id'))

        account_payment.signature_supperviseur_affairs_financiere = self.signature_supperviseur_affairs_financiere
        account_payment.signature_controlleur_financiere = self.signature_controlleur_financiere
        account_payment.signature_dg = self.signature_dg
        account_payment.signature_dg_adjoint = self.signature_dg_adjoint
        account_payment.signature_caissier = self.signature_caissier
        account_payment.signature_res_financier = self.signature_res_financier
        account_payment.signature_benefciaire = self.signature_benefciaire

        if self.type == "virement_mad":
            return self.env.ref('cps_icesco.dh_virement').report_action(account_payment)
        elif self.type == "virement_devise":
            return self.env.ref('cps_icesco.dh_lettre_virement_devise').report_action(account_payment)
        elif self.type == "compte_compte":
            return self.env.ref('cps_icesco.dh_lettre_virement_compte_compte').report_action(account_payment)
        elif self.type == "virement_salaire":
            return self.env.ref('cps_icesco.dh_lettre_virement_mise_disposition').report_action(account_payment)

        elif self.type == "depense_caisse":
            return self.env.ref('cps_icesco.dh_depense_caisse').report_action(account_payment)
        elif self.type == "depense_banque":
            return self.env.ref('cps_icesco.dh_depense_banque').report_action(account_payment)
        elif self.type == "alimentation_carte":
            return self.env.ref('cps_icesco.dh_alimentation_carte_bancaire').report_action(account_payment)

