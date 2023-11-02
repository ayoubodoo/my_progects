# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DhServiceDepartment(models.Model):
    _name = 'dh.service.department'
    _description = 'Dh Service Department'

    name = fields.Char(string='Name')
    department_id = fields.Many2one('hr.department', string='Department')
    type_department = fields.Selection(string='Type Department',
                                       selection=[('translation', 'Translation'),
                                                  ('designing_printing', 'Designing & printing'), ('legal', 'Legal'),
                                                  ('finance', 'Finance'), ('logistics', 'Logistics'),
                                                  ('procurement', 'Procurement'), ('it', 'IT'), ('media', 'Media'),
                                                  ('protocol', 'Protocol'), ('others', 'Others')], related='department_id.type_department')


