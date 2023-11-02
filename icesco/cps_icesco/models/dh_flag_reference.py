# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DhFlagsReference(models.Model):
    _name = 'dh.flag.reference'
    _description = 'Flags Reference'

    partner_id = fields.Many2one('res.partner',string='flag réference')
    hex = fields.Char(string='HEX')
    rgb = fields.Integer(string='RGB')










