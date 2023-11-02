# -*- coding: utf-8 -*-
import time
from dateutil.relativedelta import relativedelta
from datetime import date, datetime
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

class HrLoanType(models.Model):
    _name = "hr.loan.type"
    _description = "Loan Types"

    name = fields.Char('Name', size=128, required=True)
    code = fields.Char('Code', size=32, required=True)


class hrLoan(models.Model):
    _name = 'hr.loan'
    _description = 'Loan & Advance'

    def _loan_done(self):
        for loan in self:
            done = False
            for line in loan.line_ids:
                if not line.paid:
                    done = False
                    break
                else:
                    done = True
            if done:
                loan.write({'state': 'done'})
            loan.done = done

    def default_is_user(self):
        if self.env.user.has_group('kzm_payroll_ma.group_hr_payroll_user') and not self.env.user.has_group(
                'kzm_payroll_ma.group_hr_payroll_manager') and not self.env.user.has_group(
            'kzm_payroll_ma.group_hr_payroll_settings'):
            return True
        else:
            return False

    def _default_employee(self):
        return self.env.user.employee_id

    name = fields.Char('Name', size=128, required=True, )
    employee_id = fields.Many2one('hr.employee', 'Employee', required=True, default=_default_employee)
    loan_company = fields.Char('Laon Company', size=128, required=False, )
    date = fields.Date('Date', required=False, default=lambda *a: time.strftime("%Y-%m-%d"))
    date_start = fields.Date('Date Start', required=True, )
    type_id = fields.Many2one('hr.loan.type', 'Loan Type', required=True, )
    loan_amount = fields.Float('Loan Amount', digits=(12, 2), required=True, )
    duration = fields.Integer('Duration(Mounth)', required=True, )
    int_untaxed = fields.Float('untaxed Interest rate %', digits=(12, 2), )
    interest_tax = fields.Float('Tax %', digits=(12, 2), )
    int_taxed = fields.Float('Taxed Interest rate %', digits=(12, 2), required=True, )
    term_amount = fields.Float('Term Amount', digits=(12, 2), readonly=True)
    balance = fields.Float('Balance', digits=(12, 2), )
    line_ids = fields.One2many('hr.loan.line', 'loan_id', 'Laon lines', required=False, )
    notes = fields.Text(translate=True,string='Notes')
    principal_home = fields.Boolean('Principal Home Loan', default=False)
    done = fields.Boolean(compute='_loan_done', string='Done')
    is_user = fields.Boolean(string="Is User", compute='compute_is_user', default=default_is_user)
    approbation_date = fields.Date(string="Approbation Date", )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submited', 'Submited'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('closed', 'Closed'),
    ], "State", readonly=True, select=True, default='draft')

    def loan_submit(self):
        for rec in self:
            rec.write({'state': 'submited'})

    def reset_to_draft(self):
        for rec in self:
            rec.write({'state': 'draft'})
            rec.approbation_date = False

    def loan_close(self):
        for rec in self:
            rec.write({'state': 'closed'})

    def loan_reject(self):
        for rec in self:
            rec.write({'state': 'rejected'})
            rec.approbation_date = False

    @api.constrains('principal_home')
    def _check_unique_principal_home(self):
        for id in self:
            empl = id.employee_id
            if len(id.search([('employee_id', '=', empl.id),('principal_home', '=', True)])) > 1:
                raise ValidationError(_("Warning! Employee shoud have one principal home loan."))

    @api.constrains('date', 'date_start')
    def _check_dates(self):
        for loan in self.read(['date', 'date_start']):
            if loan['date'] and loan['date_start'] and loan['date'] > loan['date_start']:
                raise ValidationError(_("Error! Loan date request must be less than loan date start."))

    _sql_constraints = [
        ('CHECK_POSITIV_DURATION', 'CHECK(duration > 0)', 'Incorrect duration value!'),
        ('CHECK_POSITIV_AMOUNT', 'CHECK(loan_amount > 0)', 'Incorrect loan amount value!'),
    ]

    @api.onchange('interest_tax', 'int_untaxed')
    def onchange_interest(self):
        for loan in self:
            if loan.int_untaxed:
                loan.int_taxed = loan.int_untaxed * (1 + (loan.interest_tax / 100.0))

    def get_line(self):
        lines = []
        A = 0.0
        capital = 0.0
        self.line_ids.unlink()

        d = self.duration
        k = krd = self.loan_amount
        i = self.int_untaxed / 100.0 / 12.0
        t = self.interest_tax / 100.0
        T = self.int_taxed / 100.0 / 12.0
        date_start = self.date_start
        if not T:
            A = d and (k / d) or 0.0
        else:
            try:
                A = k * (T / (1 - (1 / (1 + T) ** d)))
            except ZeroDivisionError:
                pass
        for num in range(1, d + 1):
            krd = krd - capital
            int_amount = krd * i
            tax = int_amount * t
            capital = A - int_amount - tax
            # line_date =  datetime.strptime(date_start,'%Y-%m-%d') + relativedelta(months=+num-1)
            line_date = date_start + relativedelta(months=+num - 1)
            vals = {
                'number': num,
                'line_date': line_date.strftime('%Y-%m-%d'),
                'krd': krd,
                'int_amount': int_amount,
                'tax_amount': tax,
                'capital_amount': capital,
                'total_amount': A,
            }
            lines.append((0, 0, vals))
        self.write({'line_ids': lines, 'term_amount': A})

    def loan_confirm(self):
        for loan in self:
            loan.get_line()
            loan.state = 'approved'
            loan.approbation_date = fields.Date.today()

    def compute_is_user(self):
        for rec in self:
            if rec.env.user.has_group('kzm_payroll_ma.group_hr_payroll_user') and not rec.env.user.has_group(
                    'kzm_payroll_ma.group_hr_payroll_manager') and not rec.env.user.has_group(
                'kzm_payroll_ma.group_hr_payroll_settings'):
                rec.is_user = True
            else:
                rec.is_user = False


class HrLoanLine(models.Model):
    _name = "hr.loan.line"
    _description = "Loan Lines"

    number = fields.Integer('Number', required=True, readonly=True)
    loan_id = fields.Many2one('hr.loan', 'Loan', required=False, ondelete='cascade')
    employee_id = fields.Many2one('hr.employee', related='loan_id.employee_id', string="Employee")
    line_date = fields.Date('Term Date', readonly=True)
    krd = fields.Float('KRD', digits=(12, 2), readonly=True)
    int_amount = fields.Float('Interest Amount', digits=(12, 2), readonly=True)
    capital_amount = fields.Float('Capital Amount', digits=(12, 2), readonly=True)
    tax_amount = fields.Float('Tax Amount', digits=(12, 2), readonly=True)
    total_amount = fields.Float('Line Amount', digits=(12, 2), readonly=True)
    paid = fields.Boolean('Paid', required=False, default=False)


class HrPayrollMaBulletin(models.Model):
    _inherit = "hr.payroll_ma.bulletin"

    def compute_all_lines(self):
        for rec in self:
            # dictionnaire = self.get_parametere()
            id_bulletin = rec.id
            bulletin = rec
            if not bulletin.period_id:
                rec.period_id = bulletin.id_payroll_ma.period_id.id

            sql = ''' DELETE from hr_payroll_ma_bulletin_line where id_bulletin = %s '''
            self.env.cr.execute(sql, (id_bulletin,))

            # par cps
            if bulletin.salaire_base > 0:
                salaire_base = bulletin.salaire_base
            else:
                salaire_base = bulletin.employee_contract_id.wage


            normal_hours = bulletin.normal_hours
            hour_base = bulletin.hour_base
            working_days = bulletin.working_days

            salaire_base_worked = 0
            salaire_brute = 0
            salaire_brute_imposable = 0
            salaire_net = 0
            salaire_net_imposable = 0
            cotisations_employee = 0
            cotisations_employer = 0
            prime = 0
            indemnite = 0
            avantage = 0
            exoneration = 0
            prime_anciennete = 0
            deduction = 0
            logement = bulletin.employee_id.logement
            frais_pro = 0
            personne = 0
            absence = 0
            arrondi = 0
            min = 0

            # Salaire de base
            if salaire_base:
                absence += salaire_base - (salaire_base * (bulletin.working_days / 26))
                salaire_base_line = {
                    'name': 'Salaire de base',
                    'id_bulletin': id_bulletin,
                    'type': 'brute',
                    'base': round(salaire_base, 2),
                    'rate_employee': round((bulletin.working_days / 26) * 100, 2),
                    'subtotal_employee': round(salaire_base * (bulletin.working_days / 26), 2),
                    'deductible': False,
                }
                salaire_base_worked += salaire_base * (bulletin.working_days / 26)
                self.env['hr.payroll_ma.bulletin.line'].create(salaire_base_line)

            elif hour_base:
                normale_hours_line = {
                    'name': 'Heures normales',
                    'id_bulletin': id_bulletin,
                    'type': 'brute',
                    'base': normal_hours,
                    'rate_employee': hour_base,
                    'subtotal_employee': normal_hours * hour_base,
                    'deductible': False,
                }
                salaire_base_worked += hour_base * round(normal_hours, 2)
                self.env['hr.payroll_ma.bulletin.line'].create(normale_hours_line)
            # Rubriques majoration
            sql = '''
                            SELECT  l.montant,l.type_montant,l.taux,r.name,r.categorie,r.type,r.formule,r.afficher,r.sequence,r.imposable,
                                    r.plafond,r.ir,r.anciennete,r.absence,r.id,r.conge,r.credit_account_id, r.debit_account_id, r.is_hourly
                            FROM    hr_payroll_ma_ligne_rubrique l
                                    LEFT JOIN hr_payroll_ma_rubrique r on (l.rubrique_id=r.id)
                            WHERE
                                    l.id_contract=%s
                                    AND (l.permanent=True OR l.date_start <= %s and l.date_stop >= %s OR l.date_start >= %s and l.date_stop <= %s)
                        order by r.sequence
                        '''
            self.env.cr.execute(sql, (bulletin.employee_contract_id.id,
                                      bulletin.period_id.date_start, bulletin.period_id.date_start,
                                      bulletin.period_id.date_start, bulletin.period_id.date_end,
                                      ))
            rubriques = self.env.cr.dictfetchall()
            ir = salaire_base_worked
            anciennete = 0
            for rubrique in rubriques:
                if rubrique['categorie'] == 'majoration':
                    # 5 lignes suivant c'était commenter dans ce code
                    if rubrique['type_montant'] == 'formule':
                        if rubrique['formule']:
                            try:
                                rubrique['montant'] = eval(str(rubrique['formule']))
                            except Exception as e:
                                raise ValidationError(_('Formule Error : %s ' % (e)))

                    # actualisation montant jours chômés payés & jours congés payés
                    taux = rubrique['taux']
                    montant = rubrique['montant']
                    # Rubriques par heure: Heures sup
                    if rubrique['is_hourly']:
                        if bulletin.employee_contract_id.hour_salary > 0:
                            taux_horaire = bulletin.employee_contract_id.hour_salary
                        elif bulletin.employee_contract_id.monthly_hour_number > 0:
                            taux_horaire = bulletin.salaire_base / bulletin.employee_contract_id.monthly_hour_number or 1
                        else:
                            taux_horaire = bulletin.salaire_base / 191

                        # Montant=Nb heure
                        # Taux: Par exemple: Heures sup 25%:  25%--125%
                        montant = montant * taux_horaire * taux / 100

                    if rubrique['conge']:
                        # taux = rubrique['taux']
                        # montant = 0
                        # par cps
                        taux = 100
                        montant = rubrique['montant']
                    if rubrique['absence'] and not rubrique['conge']:
                        if bulletin.employee_contract_id.type == "mensuel":
                            taux = bulletin.working_days / 26
                            montant = rubrique['montant'] * taux
                        else:
                            if bulletin.normal_hours < 191:
                                min = bulletin.normal_hours
                            else:
                                min = 191
                            # min = min(int(bulletin.normal_hours), 191)
                            taux = min / 191
                            montant = rubrique['montant'] * taux

                        taux = taux * 100
                        absence += rubrique['montant'] - montant
                    if rubrique['anciennete'] and not rubrique['conge']:
                        anciennete += montant

                    # IR
                    if rubrique['ir'] and not rubrique['conge']:
                        if rubrique['plafond'] == 0:
                            ir += montant
                        elif montant <= rubrique['plafond']:
                            ir += montant
                        elif montant > rubrique['plafond']:
                            if rubrique['plafond']:
                                ir += montant - rubrique['plafond']
                            else:
                                ir += montant
                    # Cotisations
                    if not rubrique['imposable'] and not rubrique['conge']:
                        if rubrique['plafond'] == 0:
                            exoneration += montant
                        elif montant <= rubrique['plafond']:
                            exoneration += montant
                        elif montant > rubrique['plafond']:
                            exoneration += rubrique['plafond']

                    if rubrique['type'] == 'prime' and not rubrique['conge']:
                        prime += montant
                    elif rubrique['type'] == 'indemnite' and not rubrique['conge']:
                        indemnite += montant
                    elif rubrique['type'] == 'avantage' and not rubrique['conge']:
                        avantage += montant
                    majoration_line = {
                        'name': rubrique['name'],
                        'id_bulletin': id_bulletin,
                        'type': 'brute',
                        'base': rubrique['montant'],
                        'rate_employee': taux,
                        'subtotal_employee': montant,
                        'deductible': False,
                        'afficher': rubrique['afficher'],
                        # 'rubrique_id': rubrique['id'],
                        'credit_account_id': rubrique['credit_account_id'] or False,
                        'debit_account_id': rubrique['debit_account_id'] or False
                    }
                    rub_hsup_25 = self.env['hr.payroll_ma.rubrique'].search([('heures_sup', '=', '25'),
                                                                             ('company_id', '=', rec.company_id.id)],
                                                                            limit=1)
                    rub_hsup_50 = self.env['hr.payroll_ma.rubrique'].search([('heures_sup', '=', '50'),
                                                                             ('company_id', '=', rec.company_id.id)],
                                                                            limit=1)
                    rub_hsup_100 = self.env['hr.payroll_ma.rubrique'].search([('heures_sup', '=', '100'),
                                                                              ('company_id', '=', rec.company_id.id)],
                                                                             limit=1)
                    rub_hsup_25_50 = self.env['hr.payroll_ma.rubrique'].search([('heures_sup', '=', '2550'),
                                                                                ('company_id', '=', rec.company_id.id)],
                                                                               limit=1)
                    if (majoration_line['name'] not in [rub_hsup_25.name, rub_hsup_50.name, rub_hsup_100.name,
                                                     rub_hsup_25_50.name]) or (
                            majoration_line['name'] in [rub_hsup_25.name, rub_hsup_50.name, rub_hsup_100.name,
                                                     rub_hsup_25_50.name] and bulletin.employee_id.benifit_sup_heure == True):
                        self.env['hr.payroll_ma.bulletin.line'].create(majoration_line)

            # Ancienneté
            prime_anciennete = (salaire_base_worked + anciennete) * rec.taux_anciennete / 100
            if rec.taux_anciennete:
                anciennete_line = {
                    'name': 'Prime anciennete',
                    'id_bulletin': id_bulletin,
                    'type': 'brute',
                    'base': (salaire_base_worked + anciennete),
                    'rate_employee': rec.taux_anciennete,
                    'subtotal_employee': prime_anciennete,
                    'deductible': False,
                }
                self.env['hr.payroll_ma.bulletin.line'].create(anciennete_line)
            # Cotisations
            salaire_brute = salaire_base_worked + prime + indemnite + avantage + prime_anciennete
            salaire_brute_imposable = salaire_brute - exoneration
            cotisations = bulletin.employee_contract_id.cotisation.cotisation_ids
            base = 0
            if bulletin.employee_id.affilie:
                for cot in cotisations:
                    if cot.plafonee and salaire_brute_imposable >= cot.plafond:
                        base = cot.plafond
                    else:
                        base = salaire_brute_imposable
                    cotisation_line = {
                        'name': cot.name,
                        'id_bulletin': id_bulletin,
                        'type': 'cotisation',
                        'base': base,
                        'rate_employee': cot.tauxsalarial,
                        'rate_employer': cot.tauxpatronal,
                        'subtotal_employee': base * cot.tauxsalarial / 100,
                        'subtotal_employer': base * cot.tauxpatronal / 100,
                        'credit_account_id': cot.credit_account_id.id,
                        'debit_account_id': cot.debit_account_id.id,
                        # 'credit_account_id': cot.credit_account_id(bulletin.company_id).id,
                        # 'debit_account_id': cot.debit_account_id(bulletin.company_id).id,
                        'deductible': True,
                    }
                    cotisations_employee += base * cot.tauxsalarial / 100
                    cotisations_employer += base * cot.tauxpatronal / 100
                    self.env['hr.payroll_ma.bulletin.line'].create(cotisation_line)

            cotisations_employee, cotisations_employer = rec.prepare_cotisation(cotisations_employee,
                                                                                cotisations_employer)

            # Impot sur le revenu
            res = rec.get_ir(ir + prime_anciennete, cotisations_employee, logement)
            res['ir_net'] = self.force_ir if self.force_ir else res['ir_net']
            if not res['ir_net'] == 0:
                ir_line = {
                    'name': 'Impot sur le revenu',
                    'id_bulletin': id_bulletin,
                    'type': 'cotisation',
                    'base': res['salaire_net_imposable'],
                    'rate_employee': res['taux'],
                    'subtotal_employee': res['ir_net'],
                    'credit_account_id': res['credit_account_id'],
                    'debit_account_id': res['credit_account_id'],
                    'deductible': True,
                }
                self.env['hr.payroll_ma.bulletin.line'].create(ir_line)

            # Rubriques Deduction add compte #Nait
            for rubrique in rubriques:
                if rubrique['categorie'] == 'deduction':
                    deduction += rubrique['montant']
                    deduction_line = {
                        'name': rubrique['name'],
                        'id_bulletin': id_bulletin,
                        'type': 'retenu',
                        'base': rubrique['montant'],
                        'rate_employee': 100,
                        'subtotal_employee': rubrique['montant'],
                        'deductible': True,
                        'afficher': rubrique['afficher'],
                        'credit_account_id': rubrique['credit_account_id'] or False,
                        'debit_account_id': rubrique['debit_account_id'] or False
                    }
                    self.env['hr.payroll_ma.bulletin.line'].create(deduction_line)
            salaire_net = salaire_brute - res['ir_net'] - cotisations_employee

            deduction_net = rec.prepare_salaire_net(salaire_net)
            salaire_net -= deduction_net

            salaire_net_a_payer = salaire_brute - deduction - res['ir_net'] - cotisations_employee - deduction_net

            rec.get_frais_scolarite()

            rec.get_heures_sup_auto()

            # Arrondi
            # if dictionnaire['arrondi']:// 
            if rec.company_id.arrondi:  # 
                arrondi = 1 - (round(salaire_net_a_payer, 2) - int(salaire_net_a_payer))
                if arrondi != 1:
                    diff = salaire_net_a_payer - int(salaire_net_a_payer)
                    arrondi = 1 - (salaire_net_a_payer - int(salaire_net_a_payer))

                    if diff < 0.5:
                        arrondi = diff * -1
                    else:
                        arrondi = 1 - diff

                    arrondi = 1 - (salaire_net_a_payer - int(salaire_net_a_payer))

                    salaire_net_a_payer += arrondi
                    arrondi_line = {
                        'name': 'Arrondi',
                        'id_bulletin': id_bulletin,
                        'type': 'retenu',
                        'base': arrondi,
                        'rate_employee': 100,
                        'subtotal_employee': arrondi,
                        'deductible': True,
                    }
                    self.env['hr.payroll_ma.bulletin.line'].create(arrondi_line)
                else:
                    arrondi = 0

            rec.salaire = salaire_base
            rec.salaire_brute = salaire_brute
            rec.salaire_brute_imposable = salaire_brute_imposable
            rec.salaire_net = salaire_net
            rec.salaire_net_a_payer = salaire_net_a_payer
            rec.salaire_net_imposable = res['salaire_net_imposable']
            rec.cotisations_employee = cotisations_employee
            rec.cotisations_employer = cotisations_employer
            rec.igr = res['ir_net']
            rec.igr_brut = res['ir_brut']
            rec.prime = prime
            rec.indemnite = indemnite
            rec.avantage = avantage
            rec.deduction = deduction
            rec.prime_anciennete = prime_anciennete
            rec.exoneration = exoneration
            rec.absence = absence
            rec.frais_pro = res['frais_pro']
            rec.personnes = res['personnes']
            rec.arrondi = arrondi
            rec.logement = bulletin.employee_id.logement

            rec.get_cnss_employee()
            rec.get_nbr_paid_leaves()
            rec.get_nbr_leaves()