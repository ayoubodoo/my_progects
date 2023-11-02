# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DhPerfTypeActivity(models.Model):
    _name = 'dh.perf.type.activity'

    name = fields.Char(translate=True ,string='إسم')
    category_id = fields.Many2one('dh.perf.type.activity.category', string='Category')
    task_ids = fields.One2many('project.task', 'type_activity', string='Tasks')

class DhPerfTypeActivityCategory(models.Model):
    _name = 'dh.perf.type.activity.category'

    name = fields.Char(string='name')