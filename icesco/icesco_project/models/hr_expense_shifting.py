# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrExpenseShifting(models.Model):
    _inherit = 'hr.expense.shifting'

    project_id = fields.Many2one('project.project', string="Project")
    hr_expense_id = fields.Many2one('hr.expense', string="Expense sheet")