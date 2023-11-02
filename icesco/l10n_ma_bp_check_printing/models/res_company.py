# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ResCompany(models.Model):
    _inherit = "res.company"

    bp_bank_id = fields.Many2one('res.bank', string="Popular Bank")
    ab_bank_id = fields.Many2one('res.bank', string="Arab Bank")

