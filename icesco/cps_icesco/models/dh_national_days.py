# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DhnationalDays(models.Model):
    _name = 'dh.national.days'
    _description = 'national Days'
    _rec_name = 'name'

    name = fields.Char(string="Name")
    date = fields.Char(string="Date")
    partner_id = fields.Many2one('res.partner', string='national days')