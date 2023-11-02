# -*- coding: utf-8 -*-

from odoo import models, fields, api
# from .amount_to_text_fr import amount_to_text_fr
from num2words import num2words


class HrExpense(models.Model):
    _inherit = 'hr.expense'
    _description = 'Hr Expense'

    @api.depends('sheet_id', 'sheet_id.account_move_id', 'sheet_id.state')
    def _compute_state(self):
        for expense in self:
            if not expense.sheet_id or expense.sheet_id.state == 'draft':
                expense.state = "draft"
            elif expense.sheet_id.state == "cancel":
                expense.state = "refused"
            elif expense.sheet_id.state == "approve" or expense.sheet_id.state == "post" or expense.sheet_id.state == "approve_controller" or expense.sheet_id.state == "approve_director":
                expense.state = "approved"
            elif not expense.sheet_id.account_move_id:
                expense.state = "reported"
            else:
                expense.state = "done"

    def amount_in_words(self, total,currency):
        amount_to_text = num2words(total,lang='en') +'  ' + str(currency)
        return amount_to_text
    def amount_in_words_fr(self, total,currency):
        amount_to_text = num2words(total, lang='fr') +'  ' + str(currency)
        return amount_to_text
    #


    required_payment = fields.Float(string='Requierd Payement')


    passager_id = fields.Many2one('hr.employee.dependent', string="Passager")
    billeterie_id = fields.Many2one("cps.expense.billeterie", string='Billeterie')
    billeterie_count = fields.Integer(compute='compute_count')

    def compute_count(self):
        for record in self:
            record.billeterie_count = self.env['cps.expense.billeterie'].search_count(
                [('id', '=', self.billeterie_id.id)])

    def get_billeterie(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'billeterie',
            'view_mode': 'tree,form',
            'res_model': 'cps.expense.billeterie',
            'domain': [('id', '=', self.billeterie_id.id)],
            'context': "{'create': False}"
        }

class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submitted'),
        ('approve', 'Approved'),
        ('approve_controller', 'Validation Controller'),
        ('approve_director', 'Validation Director'),
        ('post', 'Posted'),
        ('done', 'Paid'),
        ('cancel', 'Refused')
    ], string='Status', index=True, readonly=True, tracking=True, copy=False, default='draft', required=True,
        help='Expense Report State')

    def action_sheet_validate_controller(self):
        for rec in self:
            rec.state = 'approve_controller'

    def action_sheet_validate_director(self):
        for rec in self:
            rec.state = 'approve_director'