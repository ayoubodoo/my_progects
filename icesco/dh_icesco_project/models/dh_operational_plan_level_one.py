# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DhOperationalPlanLevelOne(models.Model):
    _name = 'dh.operational.plan.level.one'

    name = fields.Char(translate=True ,string='إسم')