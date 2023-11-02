# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from itertools import groupby

class ProductProduct(models.Model):
    _inherit = 'product.product'

    articles_qty = fields.Integer(string="Quantity")


class OutOfStockWizard(models.TransientModel):
    _name = 'account.payment.check.wizard'
    _description = "Account payment check wizard"

    bank = fields.Selection([
        ('popular_bank', 'Popular Bank'),
        ('arab_bank', 'Arab Bank'),
    ])
    payment_id = fields.Many2one('account.payment')

    def print_report(self):
        if self.bank == 'popular_bank':
            return self.env.ref('l10n_ma_bp_check_printing.print_pb_check_report_action').report_action(self.payment_id)
        if self.bank == 'arab_bank':
            return self.env.ref('l10n_ma_bp_check_printing.print_ab_check_report_action').report_action(self.payment_id)


