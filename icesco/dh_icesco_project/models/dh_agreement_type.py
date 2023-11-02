# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DhAgreementsType(models.Model):
    _name = 'dh.agreement.type'

    name = fields.Char(string='نوع')
    agreement_international_ids = fields.One2many('dh.agreements.international', 'type_agr', string='Agreements international')