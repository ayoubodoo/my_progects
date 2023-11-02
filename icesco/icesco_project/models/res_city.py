# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCity(models.Model):
    _name = 'res.city'
    _description = 'City'

    name = fields.Char(string="Name", required=True, translate=True)
