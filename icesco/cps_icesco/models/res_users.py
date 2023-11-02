# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    is_translation = fields.Boolean(string='Translation')
    is_design = fields.Boolean(string='Design')
    is_legal = fields.Boolean(string='Legal')
    is_logistics = fields.Boolean('Logistics')
    is_protocol = fields.Boolean('Protocol')
    is_finance = fields.Boolean(string='Finance')
    is_admin = fields.Boolean(string='Admin')
    is_it = fields.Boolean(string='IT')
    is_media = fields.Boolean(string='Media')

    is_dg = fields.Boolean(string='DG Office')
    is_coverage = fields.Boolean(string='Coverage')
    is_dpt_participation = fields.Boolean(string='Dpt participation')
    image_presence = fields.Binary('Image presence', help="Image presence")