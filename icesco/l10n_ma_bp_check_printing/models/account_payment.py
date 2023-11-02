# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class AccountPayment(models.Model):
    _inherit = "account.payment"

    amount_add = fields.Float("AMOUNT" , compute="get_amount")

    @api.onchange('amount')
    def get_amount(self):
        for r in self:
            r.amount_add = r.amount


    def get_pb_bank_account(self):
        company = self.env.company
        bank_account = self.env['res.partner.bank'].search([('company_id', '=', company.id),
                                                            ('bank_id', '=', company.bp_bank_id.id)], limit=1)
        return bank_account.acc_number

    def get_ab_bank_account(self):
        company = self.env.company
        bank_account = self.env['res.partner.bank'].search([('company_id', '=', company.id),
                                                            ('bank_id', '=', company.ab_bank_id.id)], limit=1)
        return bank_account.acc_number