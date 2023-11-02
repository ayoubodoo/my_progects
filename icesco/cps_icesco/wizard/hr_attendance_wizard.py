# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, _, api
from odoo.exceptions import ValidationError

class CpsHrAttendanceWizard(models.TransientModel):
    _name = "hr.attendance.wizard"

    check_in = fields.Datetime(string="Check In")
    check_out = fields.Datetime(string="Check Out")
    horaire_id = fields.Many2one('cps.hr.horaire', string='Horaire')

    def write_in_attendance(self):
        for rec in self.env['hr.attendance'].browse(self._context.get('active_ids', [])):
            if self.horaire_id.id and self.check_in and self.check_out:
                rec.write({'check_in': self.check_in, 'check_out': self.check_out, 'horaire_id': self.horaire_id.id})

            if self.horaire_id.id and self.check_in == False and self.check_out == False:
                rec.write({'horaire_id': self.horaire_id.id})
            if self.horaire_id.id and self.check_in and self.check_out == False:
                rec.write({'check_in': self.check_in, 'horaire_id': self.horaire_id.id})
            if self.horaire_id.id and self.check_in == False and self.check_out:
                rec.write({'check_out': self.check_out, 'horaire_id': self.horaire_id.id})

            if self.check_in and self.horaire_id.id == False and self.check_out == False:
                rec.write({'check_in': self.check_in})
            if self.check_in and self.horaire_id.id and self.check_out == False:
                rec.write({'check_in': self.check_in, 'horaire_id': self.horaire_id.id})
            if self.check_in and self.horaire_id.id == False and self.check_out:
                rec.write({'check_in': self.check_in, 'check_out': self.check_out})

            if self.check_out and self.horaire_id.id == False and self.check_in == False:
                rec.write({'check_out': self.check_out})
            if self.check_out and self.horaire_id.id and self.check_in == False:
                rec.write({'check_out': self.check_out, 'horaire_id': self.horaire_id.id})
            if self.check_out and self.horaire_id.id == False and self.check_in:
                rec.write({'check_out': self.check_out, 'check_in': self.check_in})