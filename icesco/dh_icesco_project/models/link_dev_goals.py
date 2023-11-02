# -*- coding: utf-8 -*-
from odoo import models, fields, api

class LinkDevGoals(models.Model):
    _name = 'link.dev.goals'

    name = fields.Char(translate=True,string='Nom')
