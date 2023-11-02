# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, _, api
from odoo.exceptions import ValidationError
from odoo.exceptions import ValidationError
class CpsHrAttendanceEmployeeWizard(models.TransientModel):
    _name = "hr.attendance.employee.wizard"


    employee_id = fields.Many2one('hr.employee', string="Employee")

    def write_in_attendance(self):
        count = len(self.env['hr.attendance'].search([('id', 'in', self._context.get('active_ids'))]).mapped('employee_id'))
        if count > 1:
            raise ValidationError("Il faut selectionné même employée")
        else:
            for rec in self.env['hr.attendance'].browse(self._context.get('active_ids', [])):

                if self.employee_id.id:
                    rec.write({'employee_id': self.employee_id.id})

