# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    def default_leave_type(self):
        for rec in self:
            rec.leave_type_id = self.env.ref('hr_holidays.holiday_status_cl', raise_if_not_found=False)


    rubrique_dependent_id = fields.Many2one('hr.payroll_ma.rubrique', string="Rubrique dependents",
                                            required=False, readonly=False)
    age_limit = fields.Float(string="Allowed Age", required=False, readonly=False)
    age_limit_remboursement = fields.Float(string="Reimbursement age limit", required=False, readonly=False)
    leave_type_id = fields.Many2one('hr.leave.type', string="Leave Type",
                                            required=False, readonly=False)

    
