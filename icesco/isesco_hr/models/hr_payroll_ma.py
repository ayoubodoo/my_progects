# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrPayroll_maBulletin(models.Model):
    _inherit = 'hr.payroll_ma.bulletin'

    remaining_leaves = fields.Float(string="Remaining Leaves", related='employee_id.remaining_leaves')

    # def compute_all_lines(self):
    #     for rec_bulletin in self:
    #         if rec_bulletin.employee_id:
    #             leave_ids = self.env['hr.leave'].search(
    #                 [('state', '=', 'validate'),
    #                  ('employee_id', '=', rec_bulletin.employee_id.id),
    #                  ('holiday_status_id', '=', rec_bulletin.company_id.leave_type_id.id)])
    #
    #             allocation_ids = self.env['hr.leave.allocation'].search([
    #                 ('holiday_status_id', '=', rec_bulletin.company_id.leave_type_id.id),
    #                 ('state', '=', 'validate'),
    #                 ('employee_id', '=', rec_bulletin.employee_id.id),
    #             ])
    #             total_leave = sum([leave.number_of_days for leave in leave_ids]) if leave_ids else 0
    #             total_allocation = sum([allocation.number_of_days for allocation in allocation_ids]) if allocation_ids else 0
    #
    #             rec_bulletin.remaining_leaves = total_allocation - total_leave
    #     return super(HrPayroll_maBulletin, self).compute_all_lines()

    def get_ir(self, sbi, cotisations, logement):
        for rec in self:
            taux = 0
            somme = 0
            salaire_net_imposable = 0
            bulletin = rec
            coef = 0

            base = 0
            if rec.normal_hours:
                # base = rec.normal_hours / (dictionnaire.hour_day or 8) // 
                base = rec.normal_hours / (rec.company_id.hour_day or 8)  # 
            elif rec.working_days:
                base = rec.working_days

            # Salaire Net Imposable
            # fraispro = sbi * dictionnaire.fraispro / 100 // 
            fraispro = sbi * rec.company_id.fraispro / 100  # 
            # plafond = (dictionnaire.plafond * base) / 26 // 
            plafond = (rec.company_id.plafond * base) / 26  # 
            if fraispro < plafond:
                salaire_net_imposable = sbi - fraispro - cotisations
            else:
                salaire_net_imposable = sbi - plafond - cotisations

            # logement
            salaire_logement = salaire_net_imposable * 10 / 100
            if logement > salaire_logement:
                logement = salaire_logement
            salaire_net_imposable = salaire_net_imposable - logement
            rec.salaire_net_imposable = salaire_net_imposable


            # dictionnaire = rec.get_parametere()
            if not bulletin.employee_contract_id.ir:
                res = {
                    'salaire_net_imposable': salaire_net_imposable,
                    'taux': 0,
                    'ir_net': 0,
                    'ir_brut': 0,
                    # 'credit_account_id': dictionnaire.credit_account_id.id,// 
                    'credit_account_id': rec.company_id.credit_account_id.id,  # 
                    'frais_pro': 0,
                    'personnes': 0
                }
            else:
                base = 0
                if rec.normal_hours:
                    # base = rec.normal_hours / (dictionnaire.hour_day or 8) // 
                    base = rec.normal_hours / (rec.company_id.hour_day or 8)  # 
                elif rec.working_days:
                    base = rec.working_days

                # Salaire Net Imposable
                # fraispro = sbi * dictionnaire.fraispro / 100 // 
                fraispro = sbi * rec.company_id.fraispro / 100  # 
                # plafond = (dictionnaire.plafond * base) / 26 // 
                plafond = (rec.company_id.plafond * base) / 26  # 
                if fraispro < plafond:
                    salaire_net_imposable = sbi - fraispro - cotisations
                else:
                    salaire_net_imposable = sbi - plafond - cotisations

                # logement
                salaire_logement = salaire_net_imposable * 10 / 100
                if logement > salaire_logement:
                    logement = salaire_logement
                salaire_net_imposable = salaire_net_imposable - logement
                rec.salaire_net_imposable = salaire_net_imposable
                rec.get_cumuls()
                count_days = rec.cumul_work_days
                count_hours = rec.cumul_normal_hours

                if bulletin.employee_contract_id.type == 'mensuel' and count_days:
                    coef = 312 / count_days
                elif bulletin.employee_contract_id.type == 'horaire' and count_hours:
                    # coef = (dictionnaire.hour_month or 191) * 12 / count_hours // 
                    coef = (rec.company_id.hour_month or 191) * 12 / count_hours  # 

                new_cumul_net_imp = bulletin.cumul_sni
                cumul_coef = new_cumul_net_imp * coef

                # IR Brut
                ir_bareme = self.env['hr.payroll_ma.ir']
                ir_bareme_list = ir_bareme.search([])

                for tranche in ir_bareme_list:
                    if (cumul_coef >= tranche.debuttranche) and (cumul_coef < tranche.fintranche):
                        taux = tranche.taux
                        somme = coef and (tranche.somme / coef) or 0.0

                ir_cumul_brut = ((new_cumul_net_imp) * taux / 100) - somme

                ir_brute = ir_cumul_brut - rec.cumul_igr_brut_n_1

                # IR Net
                personnes = bulletin.employee_id.chargefam
                # if (ir_brute - (personnes * dictionnaire.charge)) < 0:// 
                if (ir_brute - (personnes * rec.company_id.charge)) < 0:  # 
                    ir_net = 0
                else:
                    # ir_net = ir_brute - (personnes * dictionnaire.charge) // 
                    ir_net = ir_brute - (personnes * rec.company_id.charge)  # 

                res = {
                    'salaire_net_imposable': salaire_net_imposable,
                    'taux': taux,
                    'ir_net': ir_net,
                    'ir_brut': ir_brute,
                    # 'credit_account_id': dictionnaire.credit_account_id.id, // 
                    'credit_account_id': rec.company_id.credit_account_id.id,  # 
                    'frais_pro': fraispro,
                    'personnes': personnes
                }
            return res



class HrPayroll_maRubrique(models.Model):
    _inherit = 'hr.payroll_ma.rubrique'

    is_grade = fields.Boolean(string="Is grade?")
    is_grade1 = fields.Boolean(string="transportation allowanc")
    line_ids = fields.One2many('hr.payroll_ma.rubrique.line', 'rubrique_id', "Lines")
    is_scolarite = fields.Boolean(string='Is scolarite?')
    is_transport = fields.Boolean(string='transportation allowance')

class HrPayroll_maLigne_rubrique(models.Model):
    _inherit = 'hr.payroll_ma.ligne_rubrique'


    @api.onchange('rubrique_id', 'type_montant')
    def onchange_rubrique_id(self):
        for rec in self:
            if rec.rubrique_id.is_hourly:
                rec.taux = rec.rubrique_id.pourcentage
            if rec.rubrique_id.is_grade and rec.id_contract.category_id:
                category_ids = rec.rubrique_id.line_ids.filtered(lambda l: l.category_id == rec.id_contract.category_id.category_id)
                if category_ids:
                    rec.montant = category_ids[0].amount
            elif rec.rubrique_id.formule:
                salaire_base = rec.id_contract.wage
                try:
                    rec.montant = eval(str(rec.rubrique_id.formule))
                except:
                    rec.rubrique_id = False
                    raise ValidationError(_('Please enter a valid formula!'))
            else:
                rec.montant = 0


class HrPayroll_maRubriqueLine(models.Model):
    _name = 'hr.payroll_ma.rubrique.line'
    _description = 'hr.payroll_ma.rubrique.line'

    category_id = fields.Many2one('hr.contract.category', string="Category")
    amount = fields.Float(string="Amount")
    rubrique_id = fields.Many2one('hr.payroll_ma.rubrique', string="Rubrique", ondelete='cascade')
