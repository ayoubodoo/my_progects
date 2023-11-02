# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = "res.company"

    account_digit = fields.Integer(string="Account digits", default=0)


class AccountDigits(models.TransientModel):
    _inherit = "res.config.settings"

    account_digit = fields.Integer(string="Account digits", related='company_id.account_digit', readonly=False)

    def update_account_code_digit(self):
        for local in self:
            records = self.env['account.account'].search([])
            for l in records:
                if l.company_id:
                    nDigit = l.company_id.account_digit
                    if len(l.code) < nDigit:
                        l.code = l.code.ljust(nDigit, '0')


class AccountAccount(models.Model):
    _inherit = "account.account"

    def update_account_code_digit(self):
        for l in self:
            if l.company_id:
                nDigit = l.company_id.account_digit
                if len(l.code) < nDigit:
                    l.code = l.code.ljust(nDigit, '0')
