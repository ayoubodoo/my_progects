# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from .amount_to_text_fr import amount_to_text_fr


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    amount_to_text = fields.Text(string='Total TTC',
                                 store=True, readonly=True, compute='_amount_in_words')

    @api.depends('amount_total')
    def _amount_in_words(self):
        for r in self:
            r.amount_to_text = amount_to_text_fr(r.amount_total, r.company_id.currency_id.symbol)

