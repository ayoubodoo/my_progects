# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DhMoyensTransport(models.Model):
    _name = 'dh.moyen.transport'

    name = fields.Char(string="Name")
