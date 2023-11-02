# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CpsHrExpense(models.Model):
    _name = 'cps.hr.expense'
    _description = 'Cps Hr Expense'



    product_id = fields.Many2one('product.product', required=True)
    billeterie_id = fields.Many2one("cps.expense.billeterie", string='Billeterie', required=True)
    date = fields.Date("Date", related='billeterie_id.date')
    employee_id = fields.Many2one('hr.employee', string="Employé", related='billeterie_id.employee_id')
    passager_id = fields.Many2one('hr.employee.dependent', string="Passager")
    payment_mode = fields.Selection([
        ("own_account", "Employee (to reimburse)"),
        ("company_account", "Company")
    ], default='own_account',
        string="Payé par")
    montant = fields.Float(string="Montant Total")