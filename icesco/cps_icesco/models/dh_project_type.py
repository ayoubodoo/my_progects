# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DhProjectType(models.Model):
    _name = 'dh.project.type'
    _description = 'Dh Project Type'
    _rec_name = 'name'

    name = fields.Char(translate=True,string="Name")








