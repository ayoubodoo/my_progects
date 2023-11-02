# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProjectTask(models.Model):
    _inherit = 'project.task'

    department_id = fields.Many2one('hr.department', string="Department")


    @api.onchange('user_id')
    def change_departement_id(self):
        for r in self:
            if r.user_id:
                r.department_id = r.user_id.employee_id.department_id
