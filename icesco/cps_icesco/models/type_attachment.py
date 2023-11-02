# -*- coding: utf-8 -*-
from odoo import models, fields, api,  _
from ast import literal_eval


class TypeAttachment(models.Model):
    _name = 'type.attachment'

    name = fields.Char(string='Nom')