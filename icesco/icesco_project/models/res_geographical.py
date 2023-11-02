# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResGeographical(models.Model):
    _name = 'res.geographical'
    _description = 'res_geographical'

    name = fields.Char(string='name')