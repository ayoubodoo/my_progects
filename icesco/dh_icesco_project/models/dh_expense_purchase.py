# -*- coding: utf-8 -*-
from odoo import models, fields, api


class DHExpensePurchase(models.Model):
    _name = 'dh.expense.purchase'

    name = fields.Char(string='Name')
    expense_ids = fields.Many2many('hr.expense', string='Expenses', compute='compute_expenses')
    purchase_ids = fields.Many2many('purchase.order', string='Purchases', compute='compute_purchases')
    amount_expenses = fields.Float(string='Amount Expenses', compute='compute_expenses', store=True) # المصروفات
    amount_purchases = fields.Float(string='Amount Purchases', compute='compute_purchases', store=True) # المشتريات
    amount_expenses_purchases = fields.Float(string='Amount Total', compute='compute_amount_total', store=True) # المجموع

    def compute_expenses(self):
        for rec in self:
            rec.expense_ids = [(4, expense.id) for expense in self.env['hr.expense'].search([('task_id', '=', False), ('state', 'in', ['approved', 'done'])])]
            rec.amount_expenses = sum(rec.expense_ids.filtered(lambda x:x.state in ['approved', 'done']).mapped('total_amount'))

    def compute_purchases(self):
        for rec in self:
            rec.purchase_ids = [(4, purchase.id) for purchase in self.env['purchase.order'].search([('task_id', '=', False), ('state', 'in', ['purchase', 'done'])])]
            rec.amount_purchases = sum(rec.purchase_ids.filtered(lambda x:x.state in ['purchase', 'done']).mapped('amount_total'))

    @api.depends('amount_expenses', 'amount_purchases')
    def compute_amount_total(self):
        for rec in self:
            rec.amount_expenses_purchases = rec.amount_expenses + rec.amount_purchases

    def recalcule_expenses_purchasess(self):
        for rec in self:
            rec.compute_expenses()
            rec.compute_purchases()

class DhDhPurchases(models.Model):
    _inherit = 'purchase.order'

    def open_line(self):
        return {
            'name': 'Purchases',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'purchase.order',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target': 'current'
        }

class DhDhHrExpense(models.Model):
    _inherit = 'hr.expense'

    def open_line(self):
        return {
            'name': 'Expenses',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hr.expense',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'target': 'current'
        }