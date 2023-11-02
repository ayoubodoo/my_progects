# -*- coding: utf-8 -*-
from odoo import models, fields, api


class DhPaysCible(models.Model):
    _name = 'dh.pays.cible'

    name = fields.Char(translate=True ,string='Name')