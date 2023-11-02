# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DhStandardGovernmentSystem(models.Model):
    _name = 'dh.government.system'

    name = fields.Char(string='إسم')