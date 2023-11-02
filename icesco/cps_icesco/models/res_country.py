# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResCountry(models.Model):
    _inherit = 'res.country'

    is_member = fields.Boolean(string='ICESCO Member')