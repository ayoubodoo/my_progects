# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DhStrategies(models.Model):
    _name = 'dh.strategies'

    name = fields.Char(translate=True ,string='إسم')