# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class DhInvolvedCountry(models.Model):
    _name = 'dh.involved.country'

    project_id = fields.Many2one('project.project', string='Project')
    country_id = fields.Many2one('res.partner', string='Country', domain=[('is_member_state', '=', True)])
    partner_id = fields.Char(string='Institution concerned')
    type_partner = fields.Selection([('governmental_institution', 'مؤسسة حكومية'), ('humanitarian_foundation', 'مؤسسة العمل الإنساني'), ('pays_non_membre', 'الدول غير الأعضاء'), ('pays_membre', 'الدول الأعضاء'), ('private_sector', 'القطاع الخاص')])
    project_manager_id = fields.Many2one('res.partner', string='Project manager')