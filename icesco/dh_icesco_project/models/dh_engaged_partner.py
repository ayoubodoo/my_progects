# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class DhEngagedPartner(models.Model):
    _name = 'dh.engaged.partner'

    project_id = fields.Many2one('project.project', string='Project')
    type_partner = fields.Selection([('governmental_institution', 'مؤسسة حكومية'), ('humanitarian_foundation', 'مؤسسة العمل الإنساني'), ('pays_non_membre', 'الدول غير الأعضاء'), ('pays_membre', 'الدول الأعضاء'), ('private_sector', 'القطاع الخاص')])
    type_organisation = fields.Char(string='Type Organisation')
    organisation = fields.Char(string='Organisation')
    project_manager_id = fields.Many2one('res.partner', string='Project manager')