# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _


class Company(models.Model):
    _inherit = 'res.company'

    expense_product_id = fields.Many2one('product.product', string="Expense school product")
    administration_director_id = fields.Char(string="Director of Administration")


class ConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    expense_product_id = fields.Many2one(related='company_id.expense_product_id', string="Expense school product",
                                     readonly=False)
    administration_director_id = fields.Char(related="company_id.administration_director_id", string="Director of Administration", readonly=False)
