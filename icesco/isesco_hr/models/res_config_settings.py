# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    rubrique_dependent_id = fields.Many2one('hr.payroll_ma.rubrique', related='company_id.rubrique_dependent_id',
                                            required=True, readonly=False)
    age_limit = fields.Float(related='company_id.age_limit', required=True, readonly=False)
    age_limit_remboursement = fields.Float(related='company_id.age_limit_remboursement', required=True, readonly=False)
    leave_type_id = fields.Many2one('hr.leave.type',related='company_id.leave_type_id', required=True, readonly=False)

