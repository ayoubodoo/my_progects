# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning
from datetime import datetime
import base64

class HrExpenseSchool(models.Model):
    _name = 'hr.expense.school'
    _description = "School expense"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'


    def expense_school_mailmessage(self):
        for rec in self.env['hr.expense.school'].search([]).filtered(lambda r: r.demand_date.year == fields.Date.today().year):
            template_id = self.env.ref('kzm_expense_school.mail_expenses_school_informations')  # xml id of your email template
            employee_id = rec.employee_id
            attachmentss = []
            content, content_type = self.env.ref('kzm_expense_school.school_fees_expense').render_qweb_pdf(
                self.env['hr.expense.school'].search([('id', '=', rec.id)]).id)
            expense_school_infos = self.env['ir.attachment'].create({
                'name': 'Rapport %s.pdf' % self.env['hr.expense.school'].search([('id', '=', rec.id)]).name,
                'type': 'binary',
                'datas': base64.encodestring(content),
                'res_model': 'hr.expense.school',
                'res_id': self.env['hr.expense.school'].search([('id', '=', rec.id)]).id,
                'mimetype': 'application/x-pdf'
            })
            attachmentss.append(expense_school_infos.id)

            template_id.email_to = employee_id.work_email
            template_id.reply_to = employee_id.work_email
            template_id.email_from = 'it@icesco.org'
            template_context = {
                'name': self.env['hr.expense.school'].search([('id', '=', rec.id)]).name,
            }
            template_id.with_context(**template_context).send_mail(rec.id, force_send=True, email_values={
                'attachment_ids': expense_school_infos})


    def get_salaire_brut(self):
        if self.employee_id and self.employee_id.sudo().contract_id:
            current_month = self.demand_date.month
            current_year = self.demand_date.year
            bulletins = self.env['hr.payroll_ma.bulletin'].search([('employee_id', '=', self.employee_id.id)],
                                                                  order="date_start asc")
            bulletin = False
            for b in bulletins:
                same_month = b.period_id.date_start.month == current_month and b.period_id.date_end.month == current_month
                same_year = b.period_id.date_start.year == current_year and b.period_id.date_end.year == current_year
                if same_year and same_month:
                    bulletin = b
                    break
                bulletin = b

            if bulletin:
                rubrique_13_total = 0
                rubrique_13_name = self.env['hr.payroll_ma.rubrique'].search([('is_13th_month', '=', True)]).mapped(
                    'name')
                for line in bulletin.salary_line_ids:
                    if line.name in rubrique_13_name:
                        rubrique_13_total += line.subtotal_employee
                salaire_brut = bulletin.salaire_brute - rubrique_13_total
            else:
                contract = self.employee_id.sudo().contract_id
                primes = 0
                for rubrique in contract.rubrique_ids:
                    if not rubrique.rubrique_id.is_13th_month:
                        primes += rubrique.montant if rubrique.montant > 0 else contract.wage

                cotisations = 0
                for cotisation in contract.cotisation.cotisation_ids:
                    cotisations += contract.wage * (cotisation.tauxsalarial + cotisation.tauxpatronal) / 100

                salaire_brut = contract.wage + primes - cotisations

                if not self.employee_id.category_id.category_id:
                    raise UserError("Employee %s didn't have a contract category" % self.employee_id.name)

            return salaire_brut
        return 0

    name = fields.Char(string="Reference", default='ES')
    demand_date = fields.Date(string="Demand date", default=fields.Date.today, track_visibility='onchange')
    employee_id = fields.Many2one('hr.employee', string="Employee",
                                  default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)],
                                                                                      limit=1))
    department_id = fields.Many2one('hr.department', string="Service", related='employee_id.department_id')
    job_id = fields.Many2one(related='employee_id.job_id')
    fees_total = fields.Float("Fees total", compute='get_total_fees')
    max_refund_amount = fields.Float('Max refund amount', compute='get_max_refund_amount')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    expense_line_ids = fields.One2many('hr.expense.school.line', 'expense_id', string='Lines')
    state = fields.Selection([('draft', "Draft"),
                              ('to_approve', "To Approve"),
                              ('confirmed', "Confirmed"),
                              ('paid', "Paid"),
                              ('canceled', "Canceled")], default='draft', track_visibility='onchange')

    is_resp = fields.Boolean("Is Responsible?", compute='_compute_responsible',
                             default = lambda self: self.env.user.has_group('kzm_expense_school.school_expense_responsible'))
    hr_expense_id = fields.Many2one('hr.expense', string="Expense sheet")
    dependent_ids = fields.Many2many('hr.employee.dependent', compute='update_depents', store=1)
    number_of_months = fields.Integer(string="Number of months")
    employee_annual_salary = fields.Float("Employee Annual Salary", compute='get_annual_salary')
    academic_year = fields.Char("Academic Year")
    note = fields.Text('Note')
    salaire_brut = fields.Float(string="Salaire", default=get_salaire_brut)

    def get_administration_director(self):
        return self.env.company.sudo().administration_director_id

    @api.depends('employee_id', 'salaire_brut')
    def get_annual_salary(self):
        for r in self:
            # r.employee_annual_salary = 12 * r.get_salaire_brut()
            r.employee_annual_salary = r.salaire_brut * 12 * r.number_of_months / 10 # ce base sur le salaire manuel saisie

    def _compute_responsible(self):
        for r in self:
            r.is_resp = self.env.user.has_group('kzm_expense_school.school_expense_responsible')

    @api.depends('expense_line_ids')
    def get_total_fees(self):
        for r in self:
            r.fees_total = 0
            if r.expense_line_ids:
                for l in r.expense_line_ids:
                     r.fees_total = sum([l.subtotal*0.75 for l in r.expense_line_ids]) * l.rate

    @api.depends('employee_id','number_of_months', 'salaire_brut')
    def get_max_refund_amount(self):
        for r in self:

            # r.max_refund_amount = r.number_of_months * r.get_salaire_brut() * r.employee_id.category_id.category_id.scholarship_refund / 100
            r.max_refund_amount = (r.salaire_brut * 12 * r.number_of_months / 10) * r.employee_id.category_id.category_id.scholarship_refund / 100 # ce base sur le salaire manuel saisie

    def approve_action(self):
        manager = self.employee_id.sudo().parent_id if self.employee_id else False
        if manager and manager.user_id:
            self.message_subscribe(partner_ids=manager.user_id.partner_id.ids)
            self.activity_schedule('kzm_expense_school.school_expense_to_approve_activity',
                                   user_id=manager.user_id.id)
            id = manager.user_id.partner_id.id
            message = """<a href="/web#model=res.partner&amp;id=%s" class="o_mail_redirect" data-oe-id="%s" data-oe-model="res.partner" target="_blank">@%s</a> <br />""" % (
                id, id, manager.user_id.partner_id.name)
            message += """A school expense has been submited by <strong>%s</strong>, at <strong>%s</strong>.""" % (
                self.employee_id.name, self.demand_date.strftime('%d/%m/%Y'))
            self.message_post(body=message)
        self.state = 'to_approve'
        # self.activity_update()

    def confirme_action(self):
        manager = self.department_id.sudo().manager_id if self.department_id else False
        if manager and manager.user_id:
            self.message_subscribe(partner_ids=manager.user_id.partner_id.ids)
            self.activity_feedback(['kzm_expense_school.school_expense_to_approve_activity', ])
            self.activity_schedule('kzm_expense_school.school_expense_to_validate_activity',
                                   user_id=manager.user_id.id)
            message = """<a href="/web#model=res.partner&amp;id=%s" class="o_mail_redirect" data-oe-id="%s" data-oe-model="res.partner" target="_blank">@%s</a> <br />""" % (
                manager.user_id.partner_id.id, manager.user_id.partner_id.id, manager.user_id.partner_id.name)
            message += _(
                """The school expense of <strong>%s</strong> has been confirmed by <strong>%s</strong> , at <strong>%s</strong>.""") % (
                           self.employee_id.name, self.employee_id.sudo().parent_id.name,
                           self.demand_date.strftime('%d/%m/%Y'))
            self.message_post(body=message)
        self.state = 'confirmed'
        self.generate_expense()

        # self.activity_update()

    def validate_action(self):
        self.state = 'paid'
        self.activity_feedback(['kzm_expense_school.school_expense_to_validate_activity', ])

    def cancel_action(self):
        self.state = 'canceled'
        self.activity_unlink(['kzm_expense_school.school_expense_to_approve_activity',
                              'kzm_expense_school.school_expense_to_validate_activity'])

    def draft_action(self):
        self.state = 'draft'

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('hr.expense.school') or 'SE'
        vals['name'] = seq
        return super(HrExpenseSchool, self).create(vals)

    def generate_expense(self):
        amount = min(self.fees_total, self.max_refund_amount)
        # print(self.env.company.expense_product_id.id)
        self.hr_expense_id = self.env['hr.expense'].create({
            'name': _("Expense sheet from %s") % self.name,
            'employee_id': self.employee_id.id,
            'product_id': self.env.company.expense_product_id.id,
            'unit_amount': amount,
        })
        return self.hr_expense_id.action_submit_expenses()

    def see_expense(self):
        action = self.env.ref('hr_expense.hr_expense_actions_my_unsubmitted').read()[0]
        action['views'] = [(self.env.ref('hr_expense.hr_expense_view_form').id, 'form')]
        action['res_id'] = self.hr_expense_id.id
        return action

    def unlink(self):
        user = self.env.user
        if user.has_group('kzm_expense_school.school_expense_responsible'):
            for mission in self.filtered(
                    lambda mission: mission.state not in ['draft', 'to_approve', 'canceled', 'refused']):
                raise UserError(_('You cannot delete a school expense which is in %s state.') % (mission.state,))
            return super(HrExpenseSchool, self).unlink()
        else:
            raise UserError(_("You didn't have the right to delete school expense.Please contact the administrator."))

    @api.depends('expense_line_ids')
    def update_depents(self):
        for r in self:
            if r.expense_line_ids:
                for line in r.expense_line_ids:
                    if line.dependent_id not in r.dependent_ids:
                        r.dependent_ids = [(4, line.dependent_id.id)]
                    else:
                        r.dependent_ids = False
            else:
                r.dependent_ids = False


class HrExpenseSchoolLine(models.Model):
    _name = 'hr.expense.school.line'
    _description = "School expense lines"

    expense_id = fields.Many2one('hr.expense.school', string='Expense')
    employee_id = fields.Many2one(related='expense_id.employee_id', store=1)
    dependent_id = fields.Many2one('hr.employee.dependent', string="Dependents", )
    inscription_fees = fields.Float('Inscription fees')
    schoolarship_fees = fields.Float('Scholarship fees')
    document_ids = fields.Many2many('ir.attachment', string="Documents")
    subtotal = fields.Float('Subtotal', compute='get_subtotal')
    rate = fields.Float(string="Rate", default=1)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)

    @api.depends('inscription_fees', 'schoolarship_fees')
    def get_subtotal(self):
        for r in self:
            r.subtotal = r.inscription_fees + r.schoolarship_fees


class HrContractCategory(models.Model):
    _inherit = 'hr.contract.category'

    scholarship_refund = fields.Float('(%) Scholarship refund')
