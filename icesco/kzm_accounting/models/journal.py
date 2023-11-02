# -*- coding: utf-8 -*-

from odoo import models, api, fields, _


class AccountJournal(models.Model):
    _inherit = "account.journal"

    update_posted = fields.Boolean(string='Allow Cancelling Entries', default=True,
                                   help="Check this box if you want to allow the cancellation the entries"
                                        " related to this journal or of the invoice related to this journal")

    @api.model
    def update_update_posted(self):
        records = self.env['account.journal'].search([])
        for rec in records:
            rec.update_posted = True
