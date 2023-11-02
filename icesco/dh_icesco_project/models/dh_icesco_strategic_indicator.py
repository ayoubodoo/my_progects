# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DhIcescoStrategicIndicator(models.Model):
    _name = 'dh.icesco.strategic.indicator'

    name = fields.Char(string='إسم')
    pilliar_id = fields.Many2one('dh.pilliar', string='المحور')