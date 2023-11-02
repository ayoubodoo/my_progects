# -*- coding: utf-8 -*-
from odoo import models, fields, api

class NonsectorProgrammes(models.Model):
    _name = 'non.sector.programmes'

    name = fields.Char(string='Nom',translate=True)
    task_ids = fields.One2many('project.task', 'non_sector_programmes_id', string='Tasks')
