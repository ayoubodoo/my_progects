# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime
import requests

class DhAwards(models.Model):
    _name = 'dh.awards'

    name = fields.Char(translate=True ,string='الجائزة ')
    date = fields.Date(store=True,string='Launch year')


    annee = fields.Selection(
        selection='years_selection',
        string="السنة",
    )
    pays_id = fields.Many2one('res.partner', store=True, string='الدولة')
    direction_id = fields.Many2one('dh.directions', store=True, string='Administration concerned')
    def years_selection(self):
        year_list = []
        for y in range(datetime.now().year - 90, datetime.now().year + 15):
            year_list.append((str(y), str(y)))
        return year_list
class DhDirectionS(models.Model):
    _name = 'dh.directions'

    name = fields.Char(translate=True ,string='Name')


