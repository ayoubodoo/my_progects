# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CpsExpenseType(models.Model):
    _name = 'cps.expense.type'
    _description = 'Cps expense type'

    name = fields.Char(translate=True,string='Nom', required=True)
    product_ids = fields.Many2many('product.product', string='Articles', required=True)
