# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DhOperationalPlanAbility(models.Model):
    _name = 'dh.operational.plan.ability'

    name = fields.Char(translate=True ,string='إسم')