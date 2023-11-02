# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrEmployee(models.AbstractModel):
    _inherit = 'hr.employee.base'

    appraisal_manager_id = fields.Many2one('res.users', string="Appraisal",track_visibility='always' , domain=lambda self: [("groups_id", "=", self.env.ref("kzm_hr_appraisal.appraisal_group_evaluator").id)])

    @api.onchange('parent_id')
    def _onchange_parent_id(self):
        super(HrEmployee, self)._onchange_parent_id()
        previous_manager = self._origin.parent_id.user_id
        manager = self.parent_id.user_id
        if manager and self.appraisal_manager_id == previous_manager or not self.appraisal_manager_id:
            self.appraisal_manager_id = manager
