# -*- coding: utf-8 -*-
from odoo import models, fields, api

class RisksAddressing(models.Model):
    _name = 'risks.addressing'

    name = fields.Char(translate=True,string='Nom')
