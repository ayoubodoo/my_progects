# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DhSupport(models.Model):
    _name = 'dh.support'
    _description = 'Dh Support'
    _rec_name = 'name'

    name = fields.Char(translate=True,string="Name")




