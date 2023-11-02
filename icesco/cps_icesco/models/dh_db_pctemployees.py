# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Dhpctemployees(models.Model):
    _name = 'dh.pctemployees'
    _description = 'Dh pctemployees'

    name = fields.Char(string="Name")
    value = fields.Float('Value')
    type= fields.Char(string='Type')




