# -*- coding: utf-8 -*-
from odoo import models, fields, api
import json

class DhSubTask(models.Model):
    _name = 'dh.perf.operation'

    name = fields.Char(translate=True ,string='عملية')
    project_task_id = fields.Many2one('project.task', string='النشاط')