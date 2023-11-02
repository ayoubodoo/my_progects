# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class Department(models.Model):

    _inherit = 'hr.department'
    
    name = fields.Char(translate=True,string='Name')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Compte analytique')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Tags analytique')
