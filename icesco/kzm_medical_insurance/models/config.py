# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _


class ConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def _default_product_id(self):
        try:
            return self.env.ref('kzm_medical_insurance.expense_medical_product_id').id
        except ValueError:
            return False

    expense_medical_product_id = fields.Many2one(related='company_id.expense_medical_product_id', string="Expense medical product",
                                     readonly=False, default=_default_product_id)

class Company(models.Model):
    _inherit = 'res.company'

    expense_medical_product_id = fields.Many2one('product.product', string="Expense medical product")
