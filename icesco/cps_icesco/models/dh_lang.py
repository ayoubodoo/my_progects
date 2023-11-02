# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DhLang(models.Model):
    _name = 'dh.lang'
    _description = 'Languages'

    name = fields.Char(string='Name', translate=True)
    is_arabe = fields.Boolean('Is Arabe')
    is_french = fields.Boolean('Is French')
    is_english = fields.Boolean('Is English')


