# -*- coding: utf-8 -*-
from odoo import models, fields, api


class DhIndicatorResultType(models.Model):
    _name = 'dh.indicator.result.type'

    name = fields.Char(string='إسم')