# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class AccountAsset(models.Model):
    _inherit = 'account.asset'

    code = fields.Char(string="Code")
    taux = fields.Float(string="Taux")
    employee_id = fields.Many2one('hr.employee', string="Employée")
    num_serie = fields.Char(string='Numéro de série')
    remet_taux_zero = fields.Boolean(string="Remettre Taux A Zero", default=False)