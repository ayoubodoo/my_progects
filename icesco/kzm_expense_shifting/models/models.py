# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning


class HrExpenseShiftingZone(models.Model):
    _name = 'hr.expense.shifting.zone'
    _description = "Shifting zone"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    name = fields.Char()


class HrExpenseShifting(models.Model):
    _name = 'hr.expense.shifting'
    _description = "Shifting expense"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    name = fields.Char(string="Reference", default='SHE')
    demand_date = fields.Date(string="Demand date", default=fields.Date.today, track_visibility='onchange')
    employee_id = fields.Many2one('hr.employee', string="Employee",
                                  default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.uid)],
                                                                                      limit=1))
    department_id = fields.Many2one('hr.department', string="Service", related='employee_id.department_id')
    job_id = fields.Many2one(related='employee_id.job_id')
    zone_id = fields.Many2one('hr.expense.shifting.zone', string='Shifting zones')
    date = fields.Date(string="Date", default=fields.Date.today, track_visibility='onchange')
    deplacement_date = fields.Date(string="Deplacement date",  track_visibility='onchange')
    days_number = fields.Integer(default=1)
    allowed_amount = fields.Float(compute='get_allowed_amount')
    currency_id = fields.Many2one('res.currency', string="Currency", compute='get_allowed_amount')
    state = fields.Selection([('draft', "Draft"),
                              ('to_approve', "To Approve"),
                              ('confirmed', "Confirmed"),
                              ('paid', "Paid"),
                              ('canceled', "Canceled")], default='draft', track_visibility='onchange')

    is_resp = fields.Boolean(compute='_compute_responsible',
                             default = lambda self: self.env.user.has_group('kzm_expense_shifting.shifting_expense_responsible'))
    hr_expense_id = fields.Many2one('hr.expense', string="Expense sheet")
    activity_number = fields.Char(string="Activity number")
    activity_name = fields.Char(string="Activity name")

    def _compute_responsible(self):
        for r in self:
            r.is_resp = self.env.user.has_group('kzm_expense_shifting.shifting_expense_responsible')

    @api.depends('employee_id', 'zone_id')
    def get_allowed_amount(self):
        for r in self:
            r.allowed_amount = 0
            r.currency_id = self.env.company.currency_id
            if r.employee_id and r.zone_id:
                if r.employee_id.category_id and r.employee_id.category_id.category_id:
                    category = r.employee_id.category_id.category_id
                    compensation = category.compensation_ids.filtered(lambda l: l.shifting_zone_id.id == r.zone_id.id)
                    if compensation:
                        r.allowed_amount = compensation.amount
                        r.currency_id = compensation.currency_id
                else:
                    raise UserError(_("%s didn't have a contract category" % r.employee_id.name))

    def approve_action(self):
        manager = self.employee_id.sudo().parent_id if self.employee_id else False
        if manager and manager.user_id:
            self.message_subscribe(partner_ids=manager.user_id.partner_id.ids)
            self.activity_schedule('kzm_expense_shifting.shifting_expense_to_approve_activity',
                                   user_id=manager.user_id.id)
            id = manager.user_id.partner_id.id
            message = """<a href="/web#model=res.partner&amp;id=%s" class="o_mail_redirect" data-oe-id="%s" data-oe-model="res.partner" target="_blank">@%s</a> <br />""" % (
                id, id, manager.user_id.partner_id.name)
            message += """A shifting expense has been submited by <strong>%s</strong>, at <strong>%s</strong>.""" % (
                self.employee_id.name, self.demand_date.strftime('%d/%m/%Y'))
            self.message_post(body=message)
        self.state = 'to_approve'
        # self.activity_update()

    def confirme_action(self):
        manager = self.department_id.sudo().manager_id if self.department_id else False
        if manager and manager.user_id:
            self.message_subscribe(partner_ids=manager.user_id.partner_id.ids)
            self.activity_feedback(['kzm_expense_shifting.shifting_expense_to_approve_activity', ])
            self.activity_schedule('kzm_expense_shifting.shifting_expense_to_validate_activity',
                                   user_id=manager.user_id.id)
            message = """<a href="/web#model=res.partner&amp;id=%s" class="o_mail_redirect" data-oe-id="%s" data-oe-model="res.partner" target="_blank">@%s</a> <br />""" % (
                manager.user_id.partner_id.id, manager.user_id.partner_id.id, manager.user_id.partner_id.name)
            message += _(
                """The shifting expense of <strong>%s</strong> has been confirmed by <strong>%s</strong> , at <strong>%s</strong>.""") % (
                           self.employee_id.name, self.employee_id.sudo().parent_id.name,
                           self.demand_date.strftime('%d/%m/%Y'))
            self.message_post(body=message)
        self.state = 'confirmed'
        self.generate_expense()

        # self.activity_update()

    def validate_action(self):
        self.state = 'paid'
        self.activity_feedback(['kzm_expense_shifting.shifting_expense_to_validate_activity', ])

    def cancel_action(self):
        self.state = 'canceled'
        self.activity_unlink(['kzm_expense_shifting.shifting_expense_to_approve_activity',
                              'kzm_expense_shifting.shifting_expense_to_validate_activity'])

    def draft_action(self):
        self.state = 'draft'

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('hr.expense.shifting') or 'SHE'
        vals['name'] = seq
        return super(HrExpenseShifting, self).create(vals)

    def generate_expense(self):
        self.hr_expense_id = self.env['hr.expense'].create({
            'name': _("Expense sheet from %s") % self.name,
            'employee_id': self.employee_id.id,
            'product_id': self.env.ref('kzm_expense_shifting.shifting_expense_product_id').id,
            'unit_amount': self.allowed_amount,
            'quantity': self.days_number,
            'currency_id': self.currency_id.id,
            'activity_number': self.activity_number,
            'activity_name': self.activity_name,
        })
        return self.hr_expense_id.action_submit_expenses()

    def see_expense(self):
        action = self.env.ref('hr_expense.hr_expense_actions_my_unsubmitted').read()[0]
        action['views'] = [(self.env.ref('hr_expense.hr_expense_view_form').id, 'form')]
        action['res_id'] = self.hr_expense_id.id
        return action

    def unlink(self):
        user = self.env.user
        if user.has_group('kzm_expense_shifting.shifting_expense_responsible'):
            for mission in self.filtered(
                    lambda mission: mission.state not in ['draft', 'to_approve', 'canceled', 'refused']):
                raise UserError(_('You cannot delete a shifting expense which is in %s state.') % (mission.state,))
            return super(HrExpenseShifting, self).unlink()
        else:
            raise UserError(_("You didn't have the right to delete shifting expense.Please contact the administrator."))



class HrContractCategory(models.Model):
    _inherit = 'hr.contract.category'

    compensation_ids = fields.One2many('icesco.daily.compensation', 'contract_category_id', string='Compensations')
    dependent_ids = fields.Many2many('hr.expense.shifting.zone', compute='update_depents', store=1)

    @api.depends('compensation_ids')
    def update_depents(self):
        for r in self:
            r.dependent_ids = False
            if r.compensation_ids:
                for line in r.compensation_ids:
                    if line.shifting_zone_id not in r.dependent_ids:
                        r.dependent_ids = [(4, line.shifting_zone_id.id)]


class DailyCompensation(models.Model):
    _name = 'icesco.daily.compensation'
    _description = "Daily compensation"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'shifting_zone_id desc'

    name = fields.Char(related='shifting_zone_id.name')
    shifting_zone_id = fields.Many2one('hr.expense.shifting.zone', string="Zone")
    amount = fields.Float()
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    contract_category_id = fields.Many2one('hr.contract.category')

class HrExpence(models.Model):
    _inherit = 'hr.expense'

    activity_number = fields.Char(string="Activity number")
    activity_name = fields.Char(string="Activity name")
