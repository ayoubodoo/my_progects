# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import fields, models, api, _


class HrAbsence(models.Model):
    _name = 'hr.absence'
    _description = 'CPS HR Pointeuse Absence'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string="Employee", store=True)
    matricule = fields.Char(string=_("Matricule"), store=True, related='employee_id.matricule')
    # matricule_pointeuse = fields.Char(string=_("Matricule (P)"), required=False)
    date = fields.Date("Date")

    # company_id = fields.Many2one(comodel_name="res.company",
    #                              string=_("Company"), related='machine_id.company_id', store=True)

    @api.model
    def generate_absence(self):
        vals = []
        employee_ids = self.env['hr.employee'].search([])
        for employee in employee_ids:
            if employee.resource_calendar_id:
                if any(int(line.dayofweek) == datetime.today().weekday() for line in
                       employee.resource_calendar_id.attendance_ids):
                    resource = self.env['resource.calendar.leaves'].search([
                        ('holiday_id.employee_id', '=', employee.id),
                        ('date_from', '<=', datetime.today()),
                        ('date_to', '>=', datetime.today()),
                    ])
                    if not resource:
                        attendance = self.env['hr.attendance'].search(['&', ('employee_id', '=', employee.id),
                                                                       '|', '&', ('check_in', '>=',
                                                                                  datetime.today().replace(hour=00,
                                                                                                           minute=00)),
                                                                       ('check_in', '<=',
                                                                        datetime.today().replace(hour=23, minute=59)),
                                                                       '&', ('check_out', '>=',
                                                                             datetime.today().replace(hour=23,
                                                                                                      minute=59)),
                                                                       ('check_out', '<=',
                                                                        datetime.today().replace(hour=23, minute=59))
                                                                       ])
                        absence = self.env['hr.absence'].search(
                            [('employee_id', '=', employee.id), ('date', '=', datetime.today())])

                        if not attendance and not absence:
                            vals.append({
                                'employee_id': employee.id,
                                'date': datetime.today(),
                            })
        self.env['hr.absence'].create(vals)
