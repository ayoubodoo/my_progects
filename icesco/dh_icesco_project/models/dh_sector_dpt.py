# -*- coding: utf-8 -*-
from odoo import models, fields, api


class DhSectorDpt(models.Model):
    _name = 'dh.sector.dpt'
    name = fields.Char(string="Name")

