# -*- coding: utf-8 -*-

from odoo import models, fields, api

class InterventionType(models.Model):
    _name = 'intervention.type'
    _description = 'Intervention Type'

    name = fields.Char(string='name')