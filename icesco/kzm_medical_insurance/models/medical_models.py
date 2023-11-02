# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta
from pprint import pprint
from datetime import date
from dateutil.relativedelta import relativedelta
from lxml import etree
import json
from itertools import groupby


class MedicalRecordBenifit(models.Model):
    _name = 'medical.record.benefit'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Medical présentation", required=True)
    refund_rate = fields.Integer(string="Refund rate", required=True)
    is_capped = fields.Boolean(string="Is capped ?")
    upper_limit = fields.Float(string="Upper limit")
    periodicities = fields.Integer(string="Periodicities")
    # currency_id = fields.Many2one ('res.currency', string="Currency")
    observation = fields.Text(translate=True,string="Observation")
    record_type = fields.Many2one('medical.record.type')
    show_cumul_date = fields.Boolean(string='Show Cumul a date')
    show_cumul_annuel = fields.Boolean(string='Show Cumul annuel')
    is_lunettes = fields.Boolean(string='Est lunettes?')
    is_dentaires = fields.Boolean(string='Est dentaires?')

class MedicalRecordType(models.Model):
    _name = 'medical.record.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Record Type", required=True)
    prestation_ids = fields.One2many('medical.record.benefit', 'record_type',
                                     string="Medical service")
    observation = fields.Text(translate=True,string="Observation")


class MedicalRecord(models.Model):
    _name = 'medical.record'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Affiliation number", required=True, default="DM")
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("in_progress", "In progress"),
            ("expired", "Expired"),
            ("canceled", "Canceled"),
        ],
        default="new",
    )

    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    departement_id = fields.Many2one('hr.department', string="Department")
    job_id = fields.Many2one('hr.job', string="Job", required=True)
    # folder_type = fields.Many2one('medical.record.type', required= True)
    beneficiaries_ids = fields.One2many('hr.employee.dependent', 'medical_id')
    mutual_contract = fields.Many2one('medical.contract', string="Mutual Contract",
                                      required=True)
    refund_request_ids = fields.One2many('medical.refund.request', 'mutual_refund_id')
    hr_expense_id = fields.Many2one('hr.expense', string="Expense sheet")

    refund_count = fields.Integer(compute='_compute_refund_count',
                                  string='Refunds Count')

    def _compute_refund_count(self):
        for r in self:
            r.refund_count = self.env['medical.refund.request'].search_count(
                [('mutual_refund_id', '=', r.id)])

    def see_medical_refunds(self):
        action = \
            self.env.ref('kzm_medical_insurance.medical_refund_request_menu_8').read()[
                0]
        action['domain'] = [('id', 'in', self.refund_request_ids.ids)]
        if self.refund_request_ids:
            action['res_id'] = self.refund_request_ids[0].id
        else:
            action['context'] = {
                'default_mutual_refund_id': self.id,
                'default_employee_id': self.employee_id.id,

            }
        print("action   : ", action)
        return action

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        for r in self:
            if r.employee_id:
                r.job_id = r.employee_id.job_id
                r.departement_id = r.employee_id.department_id

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('medical.record') or 'DM'
        vals['name'] = seq
        return super(MedicalRecord, self).create(vals)

    @api.constrains('beneficiaries_ids')
    def define_age_and_number(self):
        for r in self:
            nuber_childs = 0
            for l in r.beneficiaries_ids:
                if l.type == "child":
                    nuber_childs += 1
                    if l.age > 23:
                        raise ValidationError(
                            _("The benefeciaries can not be aged more than 23 years !"))
                    else:
                        continue
            if nuber_childs > 4:
                raise ValidationError(
                    _("The benefeciaries can not be more than four children!"))


class MedicalRefundRequest(models.Model):
    _name = 'medical.refund.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("submited", "Submitted"),
            ("verified", "verified"),
            ("arrear", "Arrear"),
            ("validated", "Validated"),
            ("refused", "Refused"),
        ],
        default="draft",
    )

    name = fields.Char(string="Number", required=True, default="DR")
    employee_id = fields.Many2one('hr.employee', required=True, string="Employee",
                                  default=lambda self: self.env['hr.employee'].search(
                                      [('user_id', '=', self.env.uid)]))
    adherent_folder = fields.Boolean(string="The request concerns a depending memeber?",
                                     required=True, default=False)
    patient_full_name = fields.Many2one('hr.employee.dependent')
    # contribution_amount = fields.Float(string="Caisse contribution amount")
    nature_of_the_disease = fields.Char(string="Disease nature", required=True)
    date = fields.Date(string="Date")
    medical_presentation_ids = fields.One2many('medical.refund.request.line',
                                               'refund_request_id')
    mutual_refund_id = fields.Many2one('medical.record', string="Medical record")
    medical_run_id = fields.Many2one('medical.refund.request.run')
    hr_expense_id = fields.Many2one('hr.expense', string="Expense sheet")
    total = fields.Float(string="Total", compute="_compute_amount")
    hr_expense_ids = fields.One2many('hr.expense', 'medical_refund_expense_id')
    today = fields.Date.today()
    total_to_refund = fields.Float(string="Total", compute="_compute_total_to_refund")
    real_total_to_refund = fields.Float(string="Total To be Refund",)
    total_arrear = fields.Float(string="Previous Arrear",
                                compute="_compute_previous_arrear")
    total_refunded = fields.Float(string="Total Refunded", store=1)
    total_refund = fields.Float(string="Total Refund", compute="_compute_total_refund")
    show_cumul_date = fields.Boolean(string='Show Cumul a date', compute='_show_cumul_date', store=True)
    show_cumul_annuel = fields.Boolean(string='Show Cumul annuel', compute='_show_cumul_annuel', store=True)

    @api.onchange('medical_presentation_ids.type_id')
    @api.depends('medical_presentation_ids.type_id')
    def _show_cumul_date(self):
        for rec in self:
            if True in rec.medical_presentation_ids.mapped('type_id').mapped('show_cumul_date'):
                rec.show_cumul_date = True
            else:
                rec.show_cumul_date = False

    @api.onchange('medical_presentation_ids.type_id')
    @api.depends('medical_presentation_ids.type_id')
    def _show_cumul_annuel(self):
        for rec in self:
            if True in rec.medical_presentation_ids.mapped('type_id').mapped('show_cumul_annuel'):
                rec.show_cumul_annuel = True
            else:
                rec.show_cumul_annuel = False

    @api.onchange('real_total_to_refund')
    def check_refunded_amount(self):
        if self.real_total_to_refund < self.total_refunded or self.real_total_to_refund > self.total_to_refund:
            raise ValidationError(_("Would you like to enter a right amount"))

    def _compute_total_refund(self):
        for rec in self:
            rec.total_refund = round(rec.total_arrear + rec.total_to_refund, 1)

    def _compute_previous_arrear(self):
        for rec in self:
            if rec.state == 'arrear':
                sum = rec.total_to_refund - rec.real_total_to_refund
                rec.total_arrear = round(sum, 1)
            else:
                rec.total_arrear = 0

    @api.depends('medical_presentation_ids')
    def _compute_total_to_refund(self):
        for r in self:
            sum = 0
            for line in r.medical_presentation_ids:
                sum += line.amount_to_refund
            r.total_to_refund = round(sum, 1)

    # difference = fields.Float(string="Difference")
    def _is_manager_default(self):
        if self.env.user.has_group('kzm_medical_insurance.medical_insurance_manager'):
            return True
        if self.env.user.has_group('kzm_medical_insurance.medical_insurance_user'):
            return False

    def _is_responsible_default(self):
        if self.env.user.has_group(
                'kzm_medical_insurance.medical_insurance_responsible') or self.env.user.has_group(
            'kzm_medical_insurance.medical_insurance_responsible'):
            return True
        else:
            return False

    is_manager = fields.Boolean("Is Manager ?", store=False,
                                default=_is_manager_default)

    is_responsible = fields.Boolean("Is Responsible ?",
                                    default=_is_responsible_default,
                                    compute='_is_responsible_compute')

    def _is_responsible_compute(self):
        for rec in self:
            if rec.env.user.has_group(
                    'kzm_medical_insurance.medical_insurance_responsible') or rec.env.user.has_group(
                'kzm_medical_insurance.medical_insurance_responsible'):
                rec.is_responsible = True
            else:
                rec.is_responsible = False

    # def _is_manager_compute(self):
    #     if self.env.user.has_group('kzm_medical_insurance.medical_insurance_user'):
    #         self.is_manager = True
    #     if self.env.user.has_group('kzm_medical_insurance.medical_insurance_manager'):
    #         self.is_manager = False

    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     res = super(MedicalRefundRequest, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
    #                                                             submenu=submenu)
    #
    #     if view_type in ['form']:  # Applies only for form view
    #         doc = etree.XML(res['arch'])
    #         for node in doc.xpath("//field"):  # All the view fields to readonly
    #             if node.get('name', 'TTTT') not in ['mutual_refund_id', 'date', 'adherent_folder', 'patient_full_name',
    #                                                 'nature_of_the_disease', 'medical_presentation_ids', 'name',
    #                                                 'total']:
    #                 modifiers = json.loads(node.get("modifiers"))
    #                 modifiers['readonly'] = [('is_manager', '=', False)]
    #                 node.set("modifiers", json.dumps(modifiers))
    #         res['arch'] = etree.tostring(doc, encoding='unicode')
    #     return res

    @api.onchange('employee_id')
    def medical_record(self):
        for r in self:
            medical = r.env['medical.record'].search(
                [('state', '=', 'in_progress'), ('employee_id', '=', r.employee_id.id)],
                limit=1)
            if medical:
                r.mutual_refund_id = medical.id
            else:
                r.mutual_refund_id = False

    @api.constrains('date', 'medical_presentation_ids')
    def check_folder_filing_date(self):
        for r in self:
            for l in r.medical_presentation_ids:
                if l.date and r.date:
                    max_date = l.date + relativedelta(months=+3)
                    if r.date > max_date:
                        raise ValidationError(
                            _(
                                "The filing date must not exceed 3 months from the date of the medical consultation"))

    def _compute_amount(self):
        for r in self:
            sum = 0
            for line in r.medical_presentation_ids:
                sum += line.amount
            r.total = sum

    expense_count = fields.Integer(compute='_compute_expense_count',
                                   string='Expense Count')

    def _compute_expense_count(self):
        for r in self:
            r.expense_count = self.env['hr.expense'].search_count(
                [('medical_refund_expense_id', '=', r.id)])

    def see_expense(self):
        action = self.env.ref('hr_expense.hr_expense_actions_my_unsubmitted').read()[0]
        action['domain'] = [('id', 'in', self.hr_expense_ids.ids)]
        # if self.hr_expense_ids:
        #     action['res_id'] = self.hr_expense_ids[0].id
        # else:
        #     action['context'] = {
        #         'default_medical_refund_expense_id': self.id,
        #         'default_employee_id': self.employee_id.id,
        #
        #     }
        print("action   : ", action)
        return action

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('medical.refund.request') or 'DR'
        vals['name'] = seq
        return super(MedicalRefundRequest, self).create(vals)

    def submit_action(self):
        self.state = 'submited'
        for line in self.medical_presentation_ids:
            line._compute_cumul_annuel()
            line.check_lunette_records()
            line.check_lunette_destaire_plafond()

    def verify_action(self):
        self.real_total_to_refund = self.total_to_refund
        self.state = 'verified'
        for line in self.medical_presentation_ids:
            line._compute_cumul_annuel()
            line.check_lunette_records()
            line.check_lunette_destaire_plafond()

    def validate_action(self):
        self.state = 'validated'
        for line in self.medical_presentation_ids:
            line._compute_cumul_annuel()
            line.check_lunette_records()
            line.check_lunette_destaire_plafond()
        # for rec in self.env['medical.refund.request']:


        template_id = self.env.ref('kzm_medical_insurance.mail_remboursement_medical')
        template_id.email_to = self.employee_id.work_email
        template_id.reply_to = self.employee_id.work_email
        template_id.email_from = 'rh@icesco.org'
        template_context = {

            'name': self.employee_id.name,

            'prenom': self.employee_id.prenom,
            'total': self.total_to_refund,
            'month': self.date.strftime('%m/%Y'),


        }
        template_id.with_context(**template_context).send_mail(self.id, force_send=True)


    def refuse_action(self):
        self.state = 'refused'

    def draft_action(self):
        self.state = 'draft'

    @api.constrains('medical_presentation_ids')
    def check_periodicity(self):
        for r in self:
            for l in r.medical_presentation_ids:
                domain = [('employee_id', '=', r.employee_id.id),
                          ('type_id', '=', l.type_id.id),
                          ('periodicity', '>', diff_month(date.today(), l.date)),
                          ('refund_request_id', '!=', r.id)]
                requests_line = r.env['medical.refund.request.line'].search(domain)
                if requests_line:
                    raise ValidationError(_("You already requested for that"))
            # if l.type_id.periodicities == 0 :
            # raise ValidationError(_("The periodicity must be different to 0 !"))


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


class MedicalRefundRequestLine(models.Model):
    _name = 'medical.refund.request.line'

    type_id = fields.Many2one('medical.record.benefit', required=True, string="Type")
    periodicity = fields.Integer(related='type_id.periodicities')
    description = fields.Char(string="Description")
    amount = fields.Float(string="Amount", required=True)
    date = fields.Date(string="Date")
    attachment_ids = fields.Many2many('ir.attachment', string="Attachments")
    refund_request_id = fields.Many2one('medical.refund.request', ondelete="cascade")
    employee_id = fields.Many2one('hr.employee',
                                  related="refund_request_id.employee_id")
    amount_to_refund = fields.Float(string="Amount To Refund",
                                    compute='set_amount_to_refund')
    patient_full_name = fields.Many2one('hr.employee.dependent',
                                        related="refund_request_id.patient_full_name")

    cumul_date = fields.Float(string='Cumul a date')
    cumul_annuel = fields.Float(string='Cumul annuel', compute='_compute_cumul_annuel', store=True)

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("submited", "Submitted"),
            ("verified", "verified"),
            ("arrear", "Arrear"),
            ("validated", "Validated"),
            ("refused", "Refused"),
        ],
        related='refund_request_id.state'
    )

    @api.depends('type_id', 'amount', 'date', 'state', 'employee_id', 'patient_full_name', 'amount_to_refund')
    def _compute_cumul_annuel(self):
        for rec in self:
            rec.cumul_annuel = 0
            if rec.type_id.id != False and rec.date != False and rec.employee_id.id != False:
                refund_annuel_type = self.env['medical.refund.request.line'].search([('employee_id', '=', rec.employee_id.id), ('patient_full_name', '=', rec.patient_full_name.id), ('type_id', '=', rec.type_id.id), ('date', '>=', datetime.strptime(rec.date.strftime('%Y-01-01'), "%Y-%m-%d")),
                         ('date', '<', datetime.strptime((rec.date + timedelta(days=365)).strftime('%Y-01-01'), "%Y-%m-%d"))]).filtered(lambda x: x.refund_request_id.state in ['submited', 'verified', 'validated', 'arrear'])
                if len(refund_annuel_type) > 0:
                    rec.cumul_annuel = sum(refund_annuel_type.mapped('amount_to_refund'))

    # difference = fields.Float(string="Difference")
    @api.depends('type_id', 'amount')
    def set_amount_to_refund(self):
        for line in self:
            amount_calculated = (line.amount * line.type_id.refund_rate) / 100
            if line.type_id.is_capped:
                line.amount_to_refund = min(amount_calculated, line.type_id.upper_limit)
            else:
                line.amount_to_refund = amount_calculated

    @api.constrains('type_id', 'date', 'employee_id', 'patient_full_name', 'state', 'refund_request_id.state')
    def check_lunette_records(self):
        for rec in self:
            if rec.type_id.is_lunettes == True:
                refund_annuel_employee_type = self.env['medical.refund.request.line'].search(
                    [('id', '!=', rec.id), ('employee_id', '=', rec.employee_id.id), ('patient_full_name', '=', rec.patient_full_name.id),
                     ('date', '>=', datetime.strptime(rec.date.strftime('%Y-01-01'), "%Y-%m-%d")),
                     ('date', '<',
                      datetime.strptime((rec.date + timedelta(days=365)).strftime('%Y-01-01'), "%Y-%m-%d"))]).filtered(
                    lambda x: x.refund_request_id.state in ['submited', 'verified', 'validated', 'arrear'] and x.refund_request_id.id != rec.refund_request_id.id and x.type_id.is_lunettes == True)
                if len(refund_annuel_employee_type) > 0:
                    raise ValidationError("Désolé, Il n'est pas possible de créer plusieurs dossiers de lunettes pour un adhérent au cours d'une même année.")

    @api.constrains('type_id', 'date', 'employee_id', 'patient_full_name', 'state', 'amount', 'amount_to_refund')
    def check_lunette_destaire_plafond(self):
        for rec in self:
            if (rec.type_id.is_lunettes == True and rec.type_id.is_capped == True) or (rec.type_id.is_dentaires == True and rec.type_id.is_capped == True):
                adherent = rec.patient_full_name.display_name if rec.patient_full_name.id != False else rec.employee_id.display_name
                if rec.amount_to_refund + sum(self.env['medical.refund.request.line'].search([('id','!=', rec.id), ('employee_id', '=', rec.employee_id.id), ('patient_full_name', '=', rec.patient_full_name.id), ('type_id', '=', rec.type_id.id), ('date', '>=', datetime.strptime(rec.date.strftime('%Y-01-01'), "%Y-%m-%d")),
                         ('date', '<', datetime.strptime((rec.date + timedelta(days=365)).strftime('%Y-01-01'), "%Y-%m-%d"))]).filtered(lambda x:x.refund_request_id.state in ['submited', 'verified', 'validated', 'arrear']).mapped('amount_to_refund')) > rec.type_id.upper_limit:
                    raise ValidationError(
                        "Désolé, Vous avez atteindre le plafond de prestation %s pour l'année %s pour l'adhérent %s. " % (rec.type_id.name, rec.date.today().year, adherent))

class MedicalRefundRequestRun(models.Model):
    _name = 'medical.refund.request.run'

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("validated", "Validated"),
        ],
        default="draft",
    )

    name = fields.Char("Number", required=True, default="LDR")
    period_id = fields.Many2one('date.range', string="period")
    date = fields.Date(string="Date", default=datetime.today())
    date_start = fields.Date(string="Start Date")
    date_end = fields.Date(string="End Date")
    refund_request_ids = fields.One2many('medical.refund.request', 'medical_run_id')
    total = fields.Float(string="Total", compute="_compute_total")
    sum_total = fields.Float(string="Total", compute="_compute_sum_total")
    actual_sold = fields.Float(string="Actual Sold")
    diffrence = fields.Float(string="Difference", compute="_compute_diff")
    sum_total_to_refund = fields.Float(string="Refunded Total",
                                       compute="_compute_sum_total_to_refund")
    sum_total_refund = fields.Float(string="Total Refund",
                                    compute="_compute_sum_total_refund")
    sum_real_total_to_refund = fields.Float(string="Total Refund",
                                            compute="_compute_sum_real_total_to_refund")
    sum_total_arrear = fields.Float(string="Arrear",
                                    compute="_compute_sum_total_arrear")

    def _compute_sum_total_to_refund(self):
        for r in self:
            sum = 0
            for line in r.refund_request_ids:
                sum += line.real_total_to_refund
            r.sum_total_to_refund = round(sum, 1)

    def _compute_sum_total(self):
        for r in self:
            sum = 0
            for line in r.refund_request_ids:
                sum += line.total
            r.sum_total = round(sum, 1)

    def _compute_sum_real_total_to_refund(self):
        for r in self:
            sum = 0
            for line in r.refund_request_ids:
                sum += line.real_total_to_refund
                # sum += line.total_refund
            r.sum_real_total_to_refund = round(sum, 1)

    def _compute_sum_total_refund(self):
        for r in self:
            sum = 0
            for line in r.refund_request_ids:
                sum += line.total_refund
                # sum += line.total_refund
            r.sum_total_refund = round(sum, 1)

    def _compute_sum_total_arrear(self):
        for r in self:
            sum = 0
            for line in r.refund_request_ids:
                sum += line.total_arrear
            r.sum_total_arrear = round(sum, 1)

    def get_prestations(self):
        dict = {}
        prestations = self.env['medical.record.benefit'].search([])
        for res in prestations:
            dict[res.id] = res.name
        return dict

    def return_grouped_requestors(self):
        for rec in self:

            employees = []
            unique_emp = []
            for line in rec.refund_request_ids:
                if line.employee_id.id not in employees:
                    filter_empl = rec.refund_request_ids.filtered(
                        lambda x: x.employee_id == line.employee_id)
                    s = 0
                    for r in filter_empl:
                        s += r.real_total_to_refund
                    unique_emp.append([line.employee_id, s,line.employee_id.bank.name])
                    employees.append(line.employee_id.id)
            """Group by Bank Account"""
            banks=[]
            unique_banks = []
            for item in unique_emp:
                li = []
                re_total_to_refund = 0
                if item[2] not in banks:

                    for i in unique_emp:
                        if i[2] == item[2]:
                            re_total_to_refund += i[1]
                            li.append(i)
                    unique_banks.append([li, re_total_to_refund])
                    banks.append(item[2])
            return unique_banks

    def get_report_values(self):
        for rec in self:
            prestations = self.env['medical.record.benefit'].search([])
            l = []
            l1 = []
            for line in rec.refund_request_ids.sorted(key=lambda x: x.employee_id.display_name):
                if line.employee_id not in l:
                    s = 0
                    for li1 in rec.refund_request_ids.sorted(key=lambda x: x.employee_id.display_name):
                        for re in li1.medical_presentation_ids:
                            if re.employee_id.id == line.employee_id.id and li1.employee_id.id == line.employee_id.id:
                                s += re.amount_to_refund
                    in_charge = []
                    in_charge1 = []
                    filter_empl = rec.refund_request_ids.filtered(
                        lambda x: x.employee_id == line.employee_id).sorted(key=lambda x: x.employee_id.display_name)
                    for li in filter_empl:
                        print(li,li.adherent_folder)
                        if li.adherent_folder:
                            charge_of = rec.refund_request_ids.filtered(lambda x: x.patient_full_name == li.patient_full_name and x.employee_id == li.employee_id)
                            # if charge_of[0].patient_full_name.name not in in_charge:
                            d = {k: 0 for k in prestations.ids}
                            for b in li.medical_presentation_ids:
                                    d[b.type_id.id] += b.amount_to_refund
                            # in_charge.append(charge_of[0].patient_full_name.name)
                            print(charge_of[0].patient_full_name.name, d)
                            in_charge1.append(
                                [charge_of[0].patient_full_name.name, d, s])
                        else:
                            """Employee in charge of himself(should not be repeated)"""
                            d1 = {k: 0 for k in prestations.ids}
                            for b in li.filtered(lambda x: x.adherent_folder != True and x.employee_id == li.employee_id).medical_presentation_ids:
                                d1[b.type_id.id] += b.amount_to_refund
                            in_charge1.append([li.employee_id.display_name, d1, s])
                    l.append(line.employee_id)
                    l1.append([line.employee_id, in_charge1])
        return l1

    def after_meeting_data(self):
        for rec in self:
            employees = []
            unique_emp = []
            for line in rec.refund_request_ids.sorted(key=lambda x: x.employee_id.display_name):
                if line.employee_id.id not in employees:
                    filter_empl = rec.refund_request_ids.filtered(
                        lambda x: x.employee_id == line.employee_id)
                    s = 0
                    arrear = 0
                    for r in filter_empl:
                        s += r.real_total_to_refund
                        arrear+=r.total_arrear

                    unique_emp.append([line.employee_id, s,arrear])
                    employees.append(line.employee_id.id)
            return unique_emp



    @api.depends('actual_sold', 'total')
    def _compute_diff(self):
        for r in self:
            r.diffrence = r.actual_sold - r.sum_total_to_refund

    # expences_ids = fields.Many2many('hr.expense', compute="_compute_expense_ids", string="Expenses", medical.contract=True)
    #
    # @api.depends('refund_request_ids')
    # def _compute_expense_ids(self):
    #     for r in self:
    #         expenses = []
    #         for expense in r.refund_request_ids:
    #             if expense.medical_run_id:
    #                 expenses.append(expense.medical_run_id.id)
    #         r.expences_ids = [(6, 0, expenses)]

    refund_count = fields.Integer(compute='_compute_refund_count',
                                  string='Refunds Count')

    def _compute_refund_count(self):
        for r in self:
            r.refund_count = self.env['medical.refund.request'].search_count(
                [('mutual_refund_id', '=', r.id)])

    def see_medical_refunds(self):
        action = \
            self.env.ref('kzm_medical_insurance.medical_refund_request_menu_8').read()[
                0]
        action['domain'] = [('id', 'in', self.refund_request_ids.ids)]
        if self.refund_request_ids:
            action['res_id'] = self.refund_request_ids[0].id
        else:
            action['context'] = {
                'default_medical_run_id': self.id,
                # 'default_employee_id': self.refund_request_ids.employee_id.id,

            }
        print("action   : ", action)
        return action

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code(
            'medical.refund.request.run') or 'LDR'
        vals['name'] = seq
        return super(MedicalRefundRequestRun, self).create(vals)

    def _compute_total(self):
        sum = 0
        for r in self:
            for line in r.refund_request_ids.medical_presentation_ids:
                sum += line.amount
            r.total = sum

    def validate_action(self):
        self.generate_expense()
        self.state = 'validated'

    def generate_expense(self):
        for r in self:
            for l in r.refund_request_ids:
                total_amount = l.real_total_to_refund - l.total_refunded
                # for line in l.medical_presentation_ids:

                # amount_calculated = (line.amount * line.type_id.refund_rate) / 100
                # limit = amount_calculated
                # print("====================", amount_calculated)
                # if line.type_id.is_capped == True:
                #     if amount_calculated < line.type_id.upper_limit:
                #         print("+++++++++++++++++", amount_calculated < line.type_id.upper_limit)
                #         limit = amount_calculated
                #     else:
                #         limit = line.type_id.upper_limit
                #         print("eeeelse", limit)
                # total_amount = total_amount + limit
                data = {
                    'name': l.name,
                    'product_id': l.env.company.expense_medical_product_id.id,
                    'employee_id': l.employee_id.id,
                    'medical_refund_expense_id': l.id,
                    'unit_amount': total_amount,
                }
                # data['expenses_ids'] = [(4, l.medical_run_id.id)]
                print("+++++++++++++++++++++++++++++++++++++++++++++++++")
                pprint(data)
                expense = self.env['hr.expense'].create(data)
                print("====================================", expense.id)
                data = {
                    'name': expense.name,
                    'employee_id': expense.employee_id.id,

                    'expense_line_ids': [(4, expense.id)],

                }
                expens_sheet = self.env['hr.expense.sheet'].create(data)
                expens_sheet.action_submit_sheet()
                expens_sheet.approve_expense_sheets()
            l.total_refunded = l.real_total_to_refund
            if l.total_to_refund != l.real_total_to_refund:
                l.write({'state': 'arrear'})
                for line in l.medical_presentation_ids:
                    line._compute_cumul_annuel()
                    line.check_lunette_records()
                    line.check_lunette_destaire_plafond()
            else:
                l.validate_action()

    def draft_action(self):
        self.state = 'draft'

    @api.onchange('period_id', 'date_start', 'date_end')
    def check_date(self):
        for r in self:
            if r.period_id:
                r.date_start = r.period_id.date_start
                r.date_end = r.period_id.date_end


class MedicalContract(models.Model):
    _name = 'medical.contract'

    name = fields.Char("Number", required=True, default="CM")
    contract_name = fields.Char("Name", required=True)
    performance_matrix_id = fields.Many2one('medical.record.type')
    employee_categ_ids = fields.One2many('hr.category.medical.line',
                                         'medical_contract_id')
    medical_record_ids = fields.One2many('medical.record', 'mutual_contract',
                                         string="Medical record")

    records_count = fields.Integer(compute='_compute_records_count',
                                   string='Records Count')

    def _compute_records_count(self):
        for r in self:
            r.records_count = self.env['medical.record'].search_count(
                [('mutual_contract', '=', r.id)])

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('medical.contract') or 'CM'
        vals['name'] = seq
        return super(MedicalContract, self).create(vals)

    def see_medical_records(self):
        action = self.env.ref('kzm_medical_insurance.medical_record_menu_8').read()[0]
        action['domain'] = [('id', 'in', self.medical_record_ids.ids)]
        if self.medical_record_ids:
            action['res_id'] = self.medical_record_ids[0].id
        else:
            action['context'] = {
                'default_mutual_contract': self.id,
                'default_employee_id': self.user_id.id,

            }
        print("action   : ", action)
        return action

    category_ids = fields.Many2many('hr.category', compute="_compute_category_ids",
                                    string="Categories", store=True)

    @api.depends('employee_categ_ids')
    def _compute_category_ids(self):
        for r in self:
            categories = []
            for category in r.employee_categ_ids:
                if category.category_id:
                    categories.append(category.category_id.id)
            r.category_ids = [(6, 0, categories)]


class HrMedicalCategoryLine(models.Model):
    _name = 'hr.category.medical.line'

    medical_contract_id = fields.Many2one('medical.contract')
    category_id = fields.Many2one('hr.category')


# class HrContractCategory(models.Model):
#     _inherit = 'hr.category'
#
#     medical_contract_id = fields.Many2one('medical.contract')


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    medical_refund_expense_id = fields.Many2one('medical.refund.request')


class HrEmployeeDependent(models.Model):
    _inherit = 'hr.employee.dependent'

    medical_record_id = fields.Many2one('medical.record')
    medical_id = fields.Many2one('medical.record')
