# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError
from . import convertion


class Payroll(models.Model):
    _inherit = 'hr.payroll_ma'

    total_net_a_payer = fields.Float(string='Total Net à payer', compute='get_total_net_a_payer')
    total_net_a_payer_vrt = fields.Float(string='Total Net à payer (virement)', compute='get_total_net_a_payer_vrt')
    total_net_a_payer_text = fields.Char(compute='change_amount')
    total_net_a_payer_vrt_text = fields.Char(compute='change_amount_vrt')
    total_bordereau_cnss = fields.Float(string='Total paiement CNSS', compute='get_total_bordereau_cnss')
    total_bordereau_cnss_text = fields.Char(compute='change_amount_cnss')
    taux_prestation_AF = fields.Float(string='AF %', compute='get_taux', default=0)
    taux_prestation_sociales = fields.Float(string='prestations sociales', compute='get_taux', default=0)
    taux_tfp = fields.Float(string='% TFP', compute='get_taux', default=0)
    taux_participation_amo = fields.Float(string='% part. AMO', compute='get_taux', default=0)
    taux_cot_amo = fields.Float(string='% cot. AMO', compute='get_taux', default=0)
    state = fields.Selection(selection=[
        ('draft', 'Brouillon'),
        ('confirmed', u'Confirmé'),
        ('paid', u'Payé'),
        ('cancelled', u'Annulé')
    ], string='Statut', readonly=True, default='draft')

    def get_taux(self):

        for rec in self:
            cot = self.env['hr.payroll_ma.cotisation'].search([('code', '=', 'allocationsFam')])
            if cot:
                rec.taux_prestation_AF = cot.tauxpatronal

            cot = self.env['hr.payroll_ma.cotisation'].search([('code', '=', 'CNSS')])
            if cot:
                rec.taux_prestation_sociales = cot.tauxpatronal + cot.tauxsalarial

            cot = self.env['hr.payroll_ma.cotisation'].search([('code', '=', 'formationPro')])
            if cot:
                rec.taux_tfp = cot.tauxpatronal

            cot = self.env['hr.payroll_ma.cotisation'].search([('code', '=', 'participationAMO')])
            if cot:
                rec.taux_participation_amo = cot.tauxpatronal

            cot = self.env['hr.payroll_ma.cotisation'].search([('code', '=', 'AMO')])
            if cot:
                rec.taux_cot_amo = cot.tauxpatronal + cot.tauxsalarial

    def get_total_bordereau_cnss(self):

        for rec in self:

            taux_plafonne = 0
            taux_non_plafonne = 0

            # On retrouve le taux plafonne
            cot = self.env['hr.payroll_ma.cotisation'].search([('code', '=', 'CNSS'),
                                                               ('company_id', '=', rec.company_id.id)])
            if cot:
                taux_plafonne = (cot.tauxsalarial + cot.tauxpatronal)

            # On retrouve les taux non plafonnés
            cot = self.env['hr.payroll_ma.cotisation'].search([('code', '=', 'allocationsFam'),
                                                               ('company_id', '=', rec.company_id.id)])
            if cot:
                taux_non_plafonne += cot.tauxpatronal

            cot = self.env['hr.payroll_ma.cotisation'].search([('code', '=', 'formationPro'),
                                                               ('company_id', '=', rec.company_id.id)])
            if cot:
                taux_non_plafonne += cot.tauxpatronal

            cot = self.env['hr.payroll_ma.cotisation'].search([('code', '=', 'participationAMO'),
                                                               ('company_id', '=', rec.company_id.id)])
            if cot:
                taux_non_plafonne += cot.tauxpatronal

            cot = self.env['hr.payroll_ma.cotisation'].search([('code', '=', 'AMO'),
                                                               ('company_id', '=', rec.company_id.id)])
            if cot:
                taux_non_plafonne += (cot.tauxsalarial + cot.tauxpatronal)

            taux_non_plafonne = taux_non_plafonne / 100
            taux_plafonne = taux_plafonne / 100

            somme_plafonnee = 0
            somme_non_plafonnee = 0
            for bul in rec.bulletin_line_ids:
                for l in bul.salary_line_ids:
                    if l.name == 'Cnss':
                        somme_plafonnee += l.base
                        somme_non_plafonnee += bul.salaire_brute_imposable

            rec.total_bordereau_cnss = (somme_non_plafonnee * taux_non_plafonne) + (somme_plafonnee * taux_plafonne)

    @api.depends('total_bordereau_cnss')
    def change_amount_cnss(self):
        self.total_bordereau_cnss_text = convertion.trad(self.total_bordereau_cnss, 'DHS').upper()
        return True

    def get_total_net_a_payer_vrt(self):
        for rec in self:
            somme = 0
            for bul in rec.bulletin_line_ids:

                if bul.employee_id.mode_reglement == 'virement':
                    somme += bul.salaire_net_a_payer

            rec.total_net_a_payer_vrt = somme

    def get_total_net_a_payer(self):
        for rec in self:
            somme = 0
            for bul in rec.bulletin_line_ids:
                somme += bul.salaire_net_a_payer

            rec.total_net_a_payer = somme

    @api.depends('total_net_a_payer')
    def change_amount(self):
        self.total_net_a_payer_text = convertion.trad(self.total_net_a_payer, 'DHS').upper()
        return True

    @api.depends('total_net_a_payer_vrt')
    def change_amount_vrt(self):
        self.total_net_a_payer_vrt_text = convertion.trad(self.total_net_a_payer_vrt, 'DHS').upper()
        return True


class bulletin(models.Model):
    _inherit = 'hr.payroll_ma.bulletin'

    salaire_base_mois = fields.Float(string='Salaire de base du mois', compute='get_base_salary')
    jrs_conges = fields.Float(string='Jours de congé', compute='get_nbr_leaves')
    conges_payes = fields.Float(string='Congés payés', compute='get_nbr_paid_leaves')
    cnss = fields.Float(string='CNSS', compute='get_cnss_employee')
    cimr_assurance_amo = fields.Float(string='CIMR/ASS/AMO', compute='get_cimr_assurance_amo')
    hsup_25 = fields.Float(string=u'Heures Sup 25%') # , compute='get_heures_sup'
    hsup_50 = fields.Float(string=u'Heures Sup 50%') # , compute='get_heures_sup'
    hsup_100 = fields.Float(string=u'Heures Sup 100%') # , compute='get_heures_sup'
    state = fields.Selection(string='State', related='id_payroll_ma.state')

    # Ajout des champs de cumul
    cumul_normal_hours = fields.Float(compute='get_cumuls', string=u'Cumul des HT', digits=(16, 2))
    cumul_work_days = fields.Float(compute='get_cumuls', string=u'Cumul des JT', digits=(16, 2))
    cumul_sbi = fields.Float(compute='get_cumuls', string='Cumul SBI', digits=(16, 2))
    cumul_base = fields.Float(compute='get_cumuls', string='Cumul base', digits=(16, 2))
    cumul_sb = fields.Float(compute='get_cumuls', string='Cumul SB', digits=(16, 2))
    cumul_sni = fields.Float(compute='get_cumuls', string='Cumul SNI', digits=(16, 2))
    cumul_sni_n_1 = fields.Float(compute='get_cumuls_n_1', string=u'Cumul SNI N-1', digits=(16, 2))
    cumul_igr = fields.Float(compute='get_cumuls', string='Cumul IR', digits=(16, 2))
    cumul_igr_n_1 = fields.Float(compute='get_cumuls_n_1', string='Cumul IR N-1', digits=(16, 2))
    cumul_igr_brut_n_1 = fields.Float(compute='get_cumuls_n_1', string='Cumul IR Brut N-1', digits=(16, 2))
    cumul_ee_cotis = fields.Float(compute='get_cumuls', string=u'Cumul Cotis employé', digits=(16, 2))
    cumul_er_cotis = fields.Float(compute='get_cumuls', string='Cumul Cotis employeur', digits=(16, 2))
    cumul_fp = fields.Float(compute='get_cumuls', string='Cumul frais professionnels', digits=(16, 2))
    cumul_avn = fields.Float(compute='get_cumuls', string=u'Cumul Avtg en nature', digits=(16, 2))
    cumul_exo = fields.Float(compute='get_cumuls', string=u'Cumul exonéré', digits=(16, 2))
    cumul_indemnites_fp = fields.Float(compute='get_cumuls', string='Cumul Indemn. frais professionnels')
    cumul_avantages = fields.Float(compute='get_cumuls', string='Cumul Avantages')

    igr_brut = fields.Float(string=u'Impot sur le revenu brut', readonly=True, digits=(16, 2))
    indemnites_frais_pro = fields.Float(string=u'Indemnités versées à titre de frais professionnels', readonly=True,
                                        digits=(16, 2))

    def get_cumuls(self):
        for res in self:
            periode = res.period_id.name.split('/')
            mois = periode[0]
            annee = periode[1]
            res.cumul_normal_hours = 0
            res.cumul_work_days = 0
            res.cumul_sbi = 0
            res.cumul_base = 0
            res.cumul_sb = 0
            res.cumul_sni = 0
            res.cumul_igr = 0
            res.cumul_ee_cotis = 0
            res.cumul_er_cotis = 0
            res.cumul_fp = 0
            res.cumul_avn = 0
            res.cumul_indemnites_fp = 0
            res.cumul_exo = 0
            res.cumul_avantages = 0

            somme_nh = 0.0
            somme_wd = 0.0
            somme_sbi = 0.0
            somme_base = 0.0
            somme_sb = 0.0
            somme_sni = 0.0
            somme_igr = 0.0
            somme_cot_ee = 0.0
            somme_cot_er = 0.0
            somme_fp = 0.0
            somme_avn = 0.0
            somme_ind_fp = 0.0
            somme_avantages = 0.0
            somme_exo = 0.0
            for j in range(1, int(mois) + 1, 1):
                valeur_mois = self.get_bulletin_cumuls(j, annee, res.employee_id.id)
                if valeur_mois:
                    somme_base += valeur_mois['salaire_base']
                    somme_nh += valeur_mois['normal_hours']
                    somme_wd += valeur_mois['working_days']
                    somme_sbi += valeur_mois['salaire_brut_imposable']
                    somme_sb += valeur_mois['salaire_brut']
                    somme_sni += valeur_mois['salaire_net_imposable']
                    somme_igr += valeur_mois['igr']
                    somme_cot_ee += valeur_mois['cotisations_employee']
                    somme_cot_er += valeur_mois['cotisations_employer']
                    somme_fp += valeur_mois['fp']
                    somme_avn += valeur_mois['avn']
                    somme_ind_fp += valeur_mois['indemnites_frais_pro']
                    somme_exo += valeur_mois['exonerations']
                    somme_avantages += valeur_mois['avantages']

            res.cumul_normal_hours = somme_nh
            res.cumul_work_days = somme_wd
            res.cumul_sbi = somme_sbi
            res.cumul_base = somme_base
            res.cumul_sb = somme_sb
            res.cumul_sni = somme_sni
            res.cumul_igr = somme_igr
            res.cumul_ee_cotis = somme_cot_ee
            res.cumul_er_cotis = somme_cot_er
            res.cumul_fp = somme_fp
            res.cumul_avn = somme_avn
            res.cumul_indemnites_fp = somme_ind_fp
            res.cumul_exo = somme_exo
            res.cumul_avantages = somme_avantages

    def get_bulletin_cumuls(self, mois, annee, employe):
        ligne_bul_paie = self.env['hr.payroll_ma.bulletin.line']
        acct_period = self.env['date.range']
        bul = self.env['hr.payroll_ma.bulletin']
        cumuls = {}
        for res in self:
            v_period = str(mois).rjust(2, '0') + "/" + str(annee)
            period = acct_period.search([('name', '=', v_period)])
            bulletin = bul.search([('period_id', '=', period.id), ('employee_id', '=', employe)])

            if bulletin:
                bul = bulletin[0]
                cumuls['normal_hours'] = bul.normal_hours
                cumuls['working_days'] = bul.working_days
                cumuls['salaire_base'] = bul.salaire_base
                cumuls['salaire_brut_imposable'] = bul.salaire_brute_imposable
                cumuls['salaire_brut'] = bul.salaire_brute
                cumuls['salaire_net_imposable'] = bul.salaire_net_imposable
                cumuls['igr'] = bul.igr
                cumuls['igr_brut'] = bul.igr_brut
                cumuls['cotisations_employee'] = bul.cotisations_employee
                cumuls['cotisations_employer'] = bul.cotisations_employer
                cumuls['indemnites_frais_pro'] = bul.indemnites_frais_pro
                cumuls['exonerations'] = bul.exoneration
                cumuls['avn'] = bul.indemnite
                cumuls['avantages'] = bul.avantage
                if bul.frais_pro < 2500:
                    cumuls['fp'] = bul.frais_pro
                else:
                    cumuls['fp'] = 2500.0
        return cumuls

    taux_anciennete = fields.Float(string=u'Taux ancienneté', digits=(16, 2))
    force_ir = fields.Float(string='Forcer IR')

    def get_frais_scolarite(self):
        for rec in self:
            rub_frais_scolarite = self.env['hr.payroll_ma.rubrique'].search([('is_scolarite', '=', True),
                                                                     ('company_id', '=', rec.company_id.id)],
                                                                    limit=1)

            if rub_frais_scolarite:
                self.env['hr.payroll_ma.bulletin.line'].search([('id_bulletin', '=', rec.id),
                                                                ('name', 'like', rub_frais_scolarite.name)]).unlink()

                school_expenses = self.env['hr.expense.school'].search([('employee_id', '=', rec.employee_id.id), ('state', '!=', 'canceled')]).filtered(lambda x: rec.period_id.date_start <= x.demand_date <= rec.period_id.date_end)

                if len(school_expenses) > 0:
                    salaire_scolarite = {
                            'name': rub_frais_scolarite.name,
                            'id_bulletin': rec.id,
                            'type': 'brute',
                            'base': sum(school_expenses.mapped('fees_total')),
                            'rate_employee': 100,
                            'subtotal_employee': sum(school_expenses.mapped('fees_total')),
                            'credit_account_id': rub_frais_scolarite.credit_account_id.id,
                            'debit_account_id': rub_frais_scolarite.debit_account_id.id,
                            'deductible': False,
                        }
                    self.env['hr.payroll_ma.bulletin.line'].create(salaire_scolarite)

    #dev kzm
    def get_heures_sup(self):
        for rec in self:
            if rec.employee_id.benifit_sup_heure == True:
                # rub_hsup_25 = self.env.ref('hr_payroll_ma.hsup_25')
                # rub_hsup_50 = self.env.ref('hr_payroll_ma.hsup_50')
                # rub_hsup_100 = self.env.ref('hr_payroll_ma.hsup_100')
                rub_hsup_25 = self.env['hr.payroll_ma.rubrique'].search([('heures_sup', '=', '25'),
                                                                         ('company_id', '=', rec.company_id.id)],
                                                                        limit=1)
                if not rub_hsup_25:
                    raise ValidationError(u"Veuillez inserer la valeur de la rubrique heure sup 25% dans la liste "
                                          u"des rubriques")
                rub_hsup_50 = self.env['hr.payroll_ma.rubrique'].search([('heures_sup', '=', '50'),
                                                                         ('company_id', '=', rec.company_id.id)],
                                                                        limit=1)
                if not rub_hsup_50:
                    raise ValidationError(
                        u"Veuillez inserer la valeur de la rubrique heure sup 50% dans la liste des rubriques")
                rub_hsup_100 = self.env['hr.payroll_ma.rubrique'].search([('heures_sup', '=', '100'),
                                                                          ('company_id', '=', rec.company_id.id)],
                                                                         limit=1)
                if not rub_hsup_100:
                    raise ValidationError(
                        u"Veuillez inserer la valeur de la rubrique heure sup 100% dans la liste des rubriques")

                # Heures Sup 25%
                lines = self.env['hr.payroll_ma.bulletin.line'].search([('id_bulletin', '=', rec.id),
                                                                        ('name', 'like', rub_hsup_25.name)])
                somme = 0
                for line in lines:
                    if line.rate_employee and line.base:
                        somme += (line.subtotal_employee * 100) / (line.rate_employee * line.base)
                rec.hsup_25 = somme
                # Heures Sup 50%
                lines = self.env['hr.payroll_ma.bulletin.line'].search([('id_bulletin', '=', rec.id),
                                                                        ('name', 'like', rub_hsup_50.name)])
                somme = 0
                for line in lines:
                    if line.rate_employee and line.base:
                        somme += (line.subtotal_employee * 100) / (line.rate_employee * line.base)

                rec.hsup_50 = somme
                # Heures Sup 100%
                lines = self.env['hr.payroll_ma.bulletin.line'].search([('id_bulletin', '=', rec.id),
                                                                        ('name', 'like', rub_hsup_100.name)])
                somme = 0
                for line in lines:
                    if line.rate_employee and line.base:
                        somme += (line.subtotal_employee * 100) / (line.rate_employee * line.base)
                rec.hsup_100 = somme

    # mehdi last version
    def get_heures_sup_auto(self):
        for rec in self:
            if rec.employee_id.benifit_sup_heure == True:
                # rub_hsup_25 = self.env.ref('hr_payroll_ma.hsup_25')
                # rub_hsup_50 = self.env.ref('hr_payroll_ma.hsup_50')
                # rub_hsup_100 = self.env.ref('hr_payroll_ma.hsup_100')
                rub_hsup_25 = self.env['hr.payroll_ma.rubrique'].search([('heures_sup', '=', '25'),
                                                                         ('company_id', '=', rec.company_id.id)],
                                                                        limit=1)

                # nouveau principe
                if len(self.env['date.trimester'].search([('periode_id', '=', rec.period_id.id)], limit=1)) > 0:
                    trimester = self.env['date.trimester'].search([('periode_id', '=', rec.period_id.id)], limit=1)
                    dh_heure_sup_25 = self.env['dh.heure.sup'].search([('employee_id', '=', rec.employee_id.id)]).filtered(
                            lambda x: (x.date_start >= trimester.date_start) and (
                                    x.date_end <= trimester.date_end))
                    dh_heure_sup_25.calcule_amount()
                    hsup_25 = sum(dh_heure_sup_25.mapped('amount_25'))
                    dh_heure_sup_50 = self.env['dh.heure.sup'].search([('employee_id', '=', rec.employee_id.id)]).filtered(
                            lambda x: (x.date_start >= trimester.date_start) and (
                                    x.date_end <= trimester.date_end))
                    dh_heure_sup_50.calcule_amount()
                    hsup_50 = sum(dh_heure_sup_50.mapped('amount_50'))
                    hsup_100 = 0
                else:
                    hsup_25 = 0
                    hsup_50 = 0
                    hsup_100 = 0

                if not rub_hsup_25:
                    raise ValidationError(u"Veuillez inserer la valeur de la rubrique heure sup 25% dans la liste "
                                          u"des rubriques")
                rub_hsup_50 = self.env['hr.payroll_ma.rubrique'].search([('heures_sup', '=', '50'),
                                                                         ('company_id', '=', rec.company_id.id)],
                                                                        limit=1)
                if not rub_hsup_50:
                    raise ValidationError(
                        u"Veuillez inserer la valeur de la rubrique heure sup 50% dans la liste des rubriques")
                rub_hsup_100 = self.env['hr.payroll_ma.rubrique'].search([('heures_sup', '=', '100'),
                                                                          ('company_id', '=', rec.company_id.id)],
                                                                         limit=1)
                if not rub_hsup_100:
                    raise ValidationError(
                        u"Veuillez inserer la valeur de la rubrique heure sup 100% dans la liste des rubriques")

                # Heures Sup 25%
                lines_25 = self.env['hr.payroll_ma.bulletin.line'].search([('id_bulletin', '=', rec.id),
                                                                        (
                                                                        'name', 'like', rub_hsup_25.name)])
                sum_25 = sum(lines_25.mapped('base'))

                if hsup_25 > 0:
                    lines_25.unlink()
                    salaire_hs_25 = {
                        'name': rub_hsup_25.name,
                        'id_bulletin': rec.id,
                        'type': 'brute',
                        'base': hsup_25 + sum_25,
                        'rate_employee': 100,
                        'subtotal_employee': hsup_25 + sum_25,
                        'credit_account_id': rub_hsup_25.credit_account_id.id,
                        'debit_account_id': rub_hsup_25.debit_account_id.id,
                        'deductible': False,
                    }
                    self.env['hr.payroll_ma.bulletin.line'].create(salaire_hs_25)

                # somme = 0
                # for line in lines:
                #     if line.rate_employee and line.base:
                #         somme += (line.subtotal_employee * 100) / (line.rate_employee * line.base)
                rec.hsup_25 = hsup_25 + sum_25
                # Heures Sup 50%
                lines_50 = self.env['hr.payroll_ma.bulletin.line'].search([('id_bulletin', '=', rec.id),
                                                                        (
                                                                        'name', 'like', rub_hsup_50.name)])

                sum_50 = sum(lines_50.mapped('base'))
                lines_50.unlink()

                if hsup_50 > 0:
                    lines_50.unlink()
                    salaire_hs_50 = {
                        'name': rub_hsup_50.name,
                        'id_bulletin': rec.id,
                        'type': 'brute',
                        'base': hsup_50 + sum_50,
                        'rate_employee': 100,
                        'subtotal_employee': hsup_50 + sum_50,
                        'credit_account_id': rub_hsup_50.credit_account_id.id,
                        'debit_account_id': rub_hsup_50.debit_account_id.id,
                        'deductible': False,
                    }
                    self.env['hr.payroll_ma.bulletin.line'].create(salaire_hs_50)
                # somme = 0
                # for line in lines:
                #     if line.rate_employee and line.base:
                #         somme += (line.subtotal_employee * 100) / (line.rate_employee * line.base)

                rec.hsup_50 = hsup_50 + sum_50
                # Heures Sup 100%
                # lines = self.env['hr.payroll_ma.bulletin.line'].search([('id_bulletin', '=', rec.id),
                #                                                         ('name', 'like',
                #                                                          rub_hsup_100.name)]).unlink()
                # somme = 0
                # for line in lines:
                #     if line.rate_employee and line.base:
                #         somme += (line.subtotal_employee * 100) / (line.rate_employee * line.base)
                rec.hsup_100 = hsup_100

    # # mehdi avant
    # def get_heures_sup_auto(self):
    #     for rec in self:
    #         # rub_hsup_25 = self.env.ref('hr_payroll_ma.hsup_25')
    #         # rub_hsup_50 = self.env.ref('hr_payroll_ma.hsup_50')
    #         # rub_hsup_100 = self.env.ref('hr_payroll_ma.hsup_100')
    #         if rec.employee_contract_id.appliquer_heure_sup == True:
    #             rub_hsup_25 = self.env['hr.payroll_ma.rubrique'].search([('heures_sup', '=', '25'),
    #                                                                      ('company_id', '=', rec.company_id.id)],
    #                                                                     limit=1)
    #
    #             # nouveau principe
    #             if len(self.env['date.trimester'].search([('periode_id', '=', rec.period_id.id)], limit=1)) > 0:
    #                 trimester = self.env['date.trimester'].search([('periode_id', '=', rec.period_id.id)], limit=1)
    #                 dh_heure_sup_25 = self.env['dh.heure.sup'].search(
    #                     [('employee_id', '=', rec.employee_id.id)]).filtered(
    #                     lambda x: (x.date_start >= trimester.date_start) and (
    #                             x.date_end <= trimester.date_end))
    #                 dh_heure_sup_25.calcule_amount()
    #                 hsup_25 = sum(dh_heure_sup_25.mapped('amount_25'))
    #
    #                 dh_heure_sup_50 = self.env['dh.heure.sup'].search(
    #                     [('employee_id', '=', rec.employee_id.id)]).filtered(
    #                     lambda x: (x.date_start >= trimester.date_start) and (
    #                             x.date_end <= trimester.date_end))
    #                 dh_heure_sup_50.calcule_amount()
    #                 hsup_50 = sum(dh_heure_sup_50.mapped('amount_50'))
    #                 hsup_100 = 0
    #             else:
    #                 hsup_25 = 0
    #                 hsup_50 = 0
    #                 hsup_100 = 0
    #
    #             if not rub_hsup_25:
    #                 raise ValidationError(u"Veuillez inserer la valeur de la rubrique heure sup 25% dans la liste "
    #                                       u"des rubriques")
    #             rub_hsup_50 = self.env['hr.payroll_ma.rubrique'].search([('heures_sup', '=', '50'),
    #                                                                      ('company_id', '=', rec.company_id.id)],
    #                                                                     limit=1)
    #             if not rub_hsup_50:
    #                 raise ValidationError(
    #                     u"Veuillez inserer la valeur de la rubrique heure sup 50% dans la liste des rubriques")
    #
    #             rub_hsup_25_50 = self.env['hr.payroll_ma.rubrique'].search([('heures_sup', '=', '2550'),
    #                                                                         ('company_id', '=', rec.company_id.id)],
    #                                                                        limit=1)
    #             if not rub_hsup_25_50:
    #                 raise ValidationError(
    #                     u"Veuillez inserer la valeur de la rubrique heure sup 50% dans la liste des rubriques")
    #
    #             rub_hsup_100 = self.env['hr.payroll_ma.rubrique'].search([('heures_sup', '=', '100'),
    #                                                                       ('company_id', '=', rec.company_id.id)],
    #                                                                      limit=1)
    #             if not rub_hsup_100:
    #                 raise ValidationError(
    #                     u"Veuillez inserer la valeur de la rubrique heure sup 100% dans la liste des rubriques")
    #
    #             # Heures Sup 25%
    #             self.env['hr.payroll_ma.bulletin.line'].search([('id_bulletin', '=', rec.id),
    #                                                             ('name', 'like', rub_hsup_25.name)]).unlink()
    #             # Heures Sup 50%
    #             self.env['hr.payroll_ma.bulletin.line'].search([('id_bulletin', '=', rec.id),
    #                                                             ('name', 'like', rub_hsup_50.name)]).unlink()
    #
    #             # Heures Sup 25+50%
    #             self.env['hr.payroll_ma.bulletin.line'].search([('id_bulletin', '=', rec.id),
    #                                                             ('name', 'like', rub_hsup_25_50.name)]).unlink()
    #
    #             if hsup_25 + hsup_50 > 0:
    #                 salaire_hs_25_50 = {
    #                     'name': rub_hsup_25_50.name,
    #                     'id_bulletin': rec.id,
    #                     'type': 'brute',
    #                     'base': hsup_25 + hsup_50,
    #                     'rate_employee': 100,
    #                     'subtotal_employee': hsup_25 + hsup_50,
    #                     'credit_account_id': rub_hsup_25_50.credit_account_id.id if rub_hsup_25_50.credit_account_id.id else self.env.ref(
    #                         "l10n_ma.1_pcg_61715").id,
    #                     'debit_account_id': rub_hsup_25_50.debit_account_id.id if rub_hsup_25_50.debit_account_id.id else self.env.ref(
    #                         "l10n_ma.1_pcg_61715").id,
    #                     'deductible': False,
    #                 }
    #                 self.env['hr.payroll_ma.bulletin.line'].create(salaire_hs_25_50)
    #
    #             # somme = 0
    #             # for line in lines:
    #             #     if line.rate_employee and line.base:
    #             #         somme += (line.subtotal_employee * 100) / (line.rate_employee * line.base)
    #             rec.hsup_25 = hsup_25
    #             # Heures Sup 50%
    #
    #             # if hsup_50 > 0:
    #             #     salaire_hs_50 = {
    #             #         'name': rub_hsup_50.name,
    #             #         'id_bulletin': rec.id,
    #             #         'type': 'brute',
    #             #         'base': hsup_50,
    #             #         'rate_employee': 100,
    #             #         'subtotal_employee': hsup_50,
    #             #         'credit_account_id': rub_hsup_50.credit_account_id.id,
    #             #         'debit_account_id': rub_hsup_50.debit_account_id.id,
    #             #         'deductible': False,
    #             #     }
    #             #     self.env['hr.payroll_ma.bulletin.line'].create(salaire_hs_50)
    #
    #             # somme = 0
    #             # for line in lines:
    #             #     if line.rate_employee and line.base:
    #             #         somme += (line.subtotal_employee * 100) / (line.rate_employee * line.base)
    #
    #             rec.hsup_50 = hsup_50
    #             # Heures Sup 100%
    #             lines = self.env['hr.payroll_ma.bulletin.line'].search([('id_bulletin', '=', rec.id),
    #                                                                     ('name', 'like', rub_hsup_100.name)]).unlink()
    #             # somme = 0
    #             # for line in lines:
    #             #     if line.rate_employee and line.base:
    #             #         somme += (line.subtotal_employee * 100) / (line.rate_employee * line.base)
    #             rec.hsup_100 = hsup_100

    @api.depends('salaire_base', 'working_days')
    def get_base_salary(self):
        for rec in self:
            rec.salaire_base_mois = rec.salaire_base * (rec.working_days / 26)

    @api.depends('salaire_net')
    def get_nbr_leaves(self):

        for rec in self:
            # rub_paid_leaves = self.env.ref('hr_payroll_ma.jrs_conges_payes')
            rub_paid_leaves = self.env['hr.payroll_ma.rubrique'].search([('jrs_conge_paye', '=', True),
                                                                         ('company_id', '=', rec.company_id.id)],
                                                                        limit=1)
            if not rub_paid_leaves:
                raise ValidationError(u"Veuillez configurer la rubrique jours congé payé dans la liste "
                                      u"des rubriques")

            lines = self.env['hr.payroll_ma.bulletin.line'].search([('id_bulletin', '=', rec.id),
                                                                    ('name', '=', rub_paid_leaves.name)])
            somme = 0

            rubrique_conge = rec.employee_contract_id.rubrique_ids.filtered(lambda x:x.date_start != False and x.date_stop != False and x.rubrique_id.jrs_conge_paye == True)
            for line in rubrique_conge:
                if (line.date_start <= rec.period_id.date_start and line.date_stop >= rec.period_id.date_start) or (line.date_start >= rec.period_id.date_start and line.date_stop <= rec.period_id.date_end):
                    somme += (line.date_stop - line.date_start).days

            rec.jrs_conges = somme

    @api.depends('salaire_net')
    def get_nbr_paid_leaves(self):

        for rec in self:

            # rub_paid_leaves = self.env.ref('hr_payroll_ma.jrs_conges_payes')
            rub_paid_leaves = self.env['hr.payroll_ma.rubrique'].search([('jrs_conge_paye', '=', True),
                                                                         ('company_id', '=', rec.company_id.id)],
                                                                        limit=1)
            if not rub_paid_leaves:
                raise ValidationError(u"Veuillez configurer la rubrique jours congé payé dans la liste "
                                      u"des rubriques")

            lines = self.env['hr.payroll_ma.bulletin.line'].search([('id_bulletin', '=', rec.id),
                                                                    ('name', '=', rub_paid_leaves.name)])

            somme = 0
            for line in lines:
                somme += line.subtotal_employee

            rec.conges_payes = somme

    @api.depends('salaire_net')
    def get_cnss_employee(self):

        for rec in self:
            lines = self.env['hr.payroll_ma.bulletin.line'].search([('id_bulletin', '=', rec.id),
                                                                    ('name', 'ilike', 'Cnss')])

            somme = 0
            for line in lines:
                somme += line.subtotal_employee
            rec.cnss = somme

    @api.depends('salaire_net')
    def get_cimr_assurance_amo(self):

        for rec in self:
            lines = self.env['hr.payroll_ma.bulletin.line'].search([('id_bulletin', '=', rec.id),
                                                                    ('name', 'in', ['CIMR', 'AMO', 'Mutuelle'])])

            somme = 0
            for line in lines:
                somme += line.subtotal_employee
            rec.cimr_assurance_amo = somme

# Rubrique
class HrRubrique(models.Model):
    _name = "hr.payroll_ma.rubrique"
    _description = "rubrique"

    name = fields.Char(string='Nom', required="True")
    code = fields.Char(string='Code', required=False, readonly=False)
    categorie = fields.Selection(selection=[('majoration', 'Majoration'),
                                            ('deduction', 'Deduction')], string=u'Catégorie', default='majoration')
    sequence = fields.Integer('Sequence', help=u"Ordre d'affichage dans le bulletin de paie", default=1)
    type = fields.Selection(selection=[('prime', 'Prime'),
                                       ('indemnite', u'Indemnité'),
                                       ('avantage', 'Avantage')], string='Type', default='prime')
    plafond = fields.Float(string=u'Plafond exonéré', default=0.0)
    formule = fields.Char(string='Formule', required=False, help='''
                    Pour les rubriques de type majoration, on utilise les variables suivantes :
                    salaire_base : Salaire de base
                    hour_base : Salaire horaire
                    normal_hours : Les heures normales
                    working_days : Jours travaillés (imposable)
        ''')
    imposable = fields.Boolean(string='Imposable', default=False)
    afficher = fields.Boolean(string='Afficher', help='Afficher cette rubrique sur le bulletin de paie', default=True)
    ir = fields.Boolean(string='IR', required=False)
    anciennete = fields.Boolean(string=u'Ancienneté')
    absence = fields.Boolean(string='Absence')
    conge = fields.Boolean(string=u'Congé')
    note = fields.Text(translate=True,string='Commentaire')
    credit_account_id = fields.Many2one('account.account', string=u'Compte de crédit')
    debit_account_id = fields.Many2one('account.account', string=u'Compte de débit')
    company_id = fields.Many2one(comodel_name='res.company', default=lambda self: self.env.company,
                                 string='Société', readonly=True, copy=False)
    is_hourly = fields.Boolean(u'Par Heure?', default=False)
    pourcentage = fields.Float(u'Pourcentage')

    heures_sup = fields.Selection([('25', '25%'), ('50', '50%'),
                                   ('100', '100%'), ('2550', '25%/50%')], string='Valeur heures sup')
    jrs_conge_paye = fields.Boolean('Jour congé payé?')

    is_grade = fields.Boolean(string="Is grade?")
    is_scolarite = fields.Boolean(string="Is scolarite?")
    line_ids = fields.One2many('hr.payroll_ma.rubrique.line', 'rubrique_id', "Lines")

# Classe : Ligne rubrique
class HrLigneRubrique(models.Model):
    _name = "hr.payroll_ma.ligne_rubrique"
    _description = "Ligne Rubrique"
    _order = 'date_start'

    #
    # def _sel_rubrique(self, cr, uid, context=None):
    #     for rec in self:
    #         obj = self.env['hr.payroll_ma.rubrique']
    #         res = obj.search([])
    #         res = [(r.id, r.name) for r in res]
    #         return res

    rubrique_id = fields.Many2one('hr.payroll_ma.rubrique', string='Rubrique', store=True)
    id_contract = fields.Many2one('hr.contract', string=u'Contrat', ondelete='cascade')
    montant = fields.Float(string='Montant')
    taux = fields.Float(string='Taux')
    period_id = fields.Many2one('date.range', domain="[('type_id.fiscal_period','=',True)]", string=u'Période')
    permanent = fields.Boolean(string='Rubrique Permanente')
    date_start = fields.Date(string=u'Date début')
    date_stop = fields.Date(string='Date fin')
    note = fields.Text(translate=True,string='Commentaire')
    montant_formule = fields.Float(string='Montant Formule', compute='compute_montant_formule')
    type_montant = fields.Selection([
        ('amount', 'Amount'),
        ('formule', 'Formule')
    ], string="", default='amount')

    @api.depends('rubrique_id')
    def compute_montant_formule(self):
        for rec in self:
            if rec.rubrique_id.formule:
                salaire_base = rec.id_contract.wage
                try:
                    rec.montant_formule = eval(str(rec.rubrique_id.formule))
                except:
                    rec.rubrique_id = False
                    raise ValidationError(_('Please enter a valid formula!'))
            else:
                rec.montant_formule = 0

    @api.constrains('date_stop')
    def _check_date(self):
        for obj in self:
            if obj.date_start > obj.date_stop:
                raise ValidationError(u'La Date début doit être inférieur à la date de fin')
            return True

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

    @api.onchange('period_id')
    def onchange_period_id(self):
        if self.period_id:
            self.date_start = self.period_id.date_start
            self.date_stop = self.period_id.date_end