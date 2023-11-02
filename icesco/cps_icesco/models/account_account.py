# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CpsAccountAccount(models.Model):
    _inherit = 'account.account'
    _description = 'Account Account'

    type_convertion = fields.Selection([
        ('jour', 'Cours de jour'),
        ('cloture', 'Cours de clôture'),
    ], string="Type Convertion", default='jour')
    is_fond_dedie = fields.Boolean('Compte fond dédié')