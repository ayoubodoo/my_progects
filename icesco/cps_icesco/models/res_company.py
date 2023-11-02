# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = 'res.company'

    image_presence = fields.Binary('Image presence', help="Image presence")