# -*- coding: utf-8 -*-
from odoo import models, fields, api
class DhProject(models.Model):
    _inherit = 'project.project'
    _description = 'Project'

    # new
    name = fields.Char("Name", index=True, required=True, tracking=True, translate=True)
    sector = fields.Many2one("dh.sector", string="Sector")
    supporting_project = fields.Many2one("dh.support", string="Supporting Projects")
    project_type = fields.Many2one("dh.project.type", string="Project Type")
    country_budget_available = fields.Float(string="Country Budget Available ($)")
    budget_required_icesco = fields.Float(string="Budget required from ICESCO ($)")
    strategic_id = fields.Many2one( 'dh.strategic.objectives', string="Projects")

    translation = fields.Boolean('Translation')
    is_support_designing = fields.Boolean('Designing & printing')
    is_support_legal = fields.Boolean('Legal')
    is_support_logistics = fields.Boolean('Logistics')
    is_support_protocol = fields.Boolean('Protocol')
    is_support_finance = fields.Boolean('Finance')
    is_support_admin = fields.Boolean('Procurement')
    is_support_it = fields.Boolean('IT')
    is_support_media = fields.Boolean('Media')
    is_support_other = fields.Boolean('Other (specify)')
    # lis
    list_translation_service = fields.Many2one('dh.service.department', string="List of Translation services",
                                               domain=[("type_department", "=", 'translation')])
    list_designing_service = fields.Many2one('dh.service.department', string="List of Designing & printing  services",
                                             domain=[("type_department", "=", 'designing_printing')])
    list_legal_service = fields.Many2one('dh.service.department', string="List of Legal services",
                                         domain=[("type_department", "=", 'legal')])
    list_finance_service = fields.Many2one('dh.service.department', string="List of Finance services",
                                           domain=[("type_department", "=", 'finance')])
    list_logistics_service = fields.Many2one('dh.service.department', string="List of Logistics services",
                                             domain=[("type_department", "=", 'logistics')])
    list_admin_service = fields.Many2one('dh.service.department', string="List of Procurement services",
                                         domain=[("type_department", "=", 'procurement')])
    list_it_service = fields.Many2one('dh.service.department', string="List of IT services",
                                      domain=[("type_department", "=", 'it')])
    list_media_service = fields.Many2one('dh.service.department', string="List of Media services",
                                         domain=[("type_department", "=", 'media')])
    list_protocol_service = fields.Many2one('dh.service.department', string="List of Protocol services",
                                            domain=[("type_department", "=", 'protocol')])
    list_others_service = fields.Many2one('dh.service.department', string="List of Others services",
                                          domain=[("type_department", "=", 'others')])
    file = fields.Many2many("ir.attachment", string="File")

    language_ids = fields.Many2many('dh.lang', string='Languages of the activity', context={'active_test': False},
                                    required=False)

    def count_my_tasks(self):
        for rec in self:
            return len(rec.task_ids) # .filtered(lambda x:x.create_uid.id == self.env.uid)