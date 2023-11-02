# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    bp_bank_id = fields.Many2one('res.bank',related='company_id.bp_bank_id', required=True, readonly=False, string="Popular Bank")
    ab_bank_id = fields.Many2one('res.bank',related='company_id.ab_bank_id', required=True, readonly=False, string="Arab Bank")


