# encoding: utf-8

from odoo import models, api, fields, _


class AccountTax(models.Model):
    _inherit = 'account.tax'

    @api.onchange('name')
    def get_the_description(self):
        for o in self:
            if '%' in o.name:
                o.description = o.name.split('%')[0] + '%'

    @api.model
    def update_descriptions(self):
        records = self.env['account.tax'].search([])
        records.get_the_description()
