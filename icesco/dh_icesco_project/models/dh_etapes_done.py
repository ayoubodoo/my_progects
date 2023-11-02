# -*- coding: utf-8 -*-
from odoo import models, fields, api


class DhEtapesDone(models.Model):
    _name = 'dh.etapes.done'

    name = fields.Char(translate=True,string='إسم')