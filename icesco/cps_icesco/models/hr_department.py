# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api, _


class Department(models.Model):
    _inherit = 'hr.department'
    _order = 'seq'
    seq = fields.Char(required=False, readonly=True, copy=False)

    service_ids = fields.One2many('dh.service.department', 'department_id', string='Services')
    type_department = fields.Selection(string='Type Department',
                                       selection=[('translation', 'Translation'), ('designing_printing', 'Designing & printing'), ('legal', 'Legal'), ('finance', 'Finance'), ('logistics', 'Logistics'), ('procurement', 'Procurement'), ('it', 'IT'), ('media', 'Media'), ('protocol', 'Protocol'), ('others', 'Others')],
                                       default='others')

    @api.model
    def create(self, vals):
        if vals.get('seq', _('New')) == _('New'):
            vals['seq'] = self.env['ir.sequence'].next_by_code(
                'sequence_departements.hr.department') or _(
                'New')
        return super(Department, self).create(vals)