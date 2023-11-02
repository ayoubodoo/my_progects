# -*- coding: utf-8 -*-
from odoo import models, fields, api

class KeyPerformanceIndicators(models.Model):
    _name = 'key.performance.indicators'

    name = fields.Char(translate=True, string='Nom')
