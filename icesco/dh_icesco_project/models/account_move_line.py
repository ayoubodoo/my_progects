# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    type_partenaire = fields.Selection([('institution_gouv_etat_member', 'مؤسسة حكومية'),
                                        ('institution_gouv_etat_non_member', 'مؤسسة العمل الإنساني'),
                                        ('organisation_mondiale_rare', 'الدول غير الأعضاء'),
                                        ('organisation_locale', 'الدول الأعضاء'),
                                        ('organisation_regional', 'القطاع الخاص')], related='partner_id.type_partenaire', store=True)

    task_id = fields.Many2one('project.task', string='Task')