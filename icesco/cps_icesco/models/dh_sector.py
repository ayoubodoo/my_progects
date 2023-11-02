# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DhSector(models.Model):
    _name = 'dh.sector'
    _description = 'Dh Sector'
    _rec_name = 'name'

    name = fields.Char(string="Name")
