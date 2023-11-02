# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DhAgreementsCategory(models.Model):
    _name = 'dh.agreement.category'

    name = fields.Char(translate=True,string='الفئة')
    agreement_international_ids = fields.One2many('dh.agreements.international', 'category', string='Agreements international')