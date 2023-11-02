# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import datetime

class DhHeureSup(models.Model):
    _name = "dh.heure.sup"

    employee_id = fields.Many2one('hr.employee', string='Employee')
    date_start = fields.Date(string='Date Start') # lundi 7:30
    date_end = fields.Date(string='Date end') # lundi 7:30
    h_25 = fields.Float('H25')
    h_50 = fields.Float('H50')
    amount_25 = fields.Float('Amount H25')
    amount_50 = fields.Float('Amount H50')
    attendance_ids = fields.Many2many('hr.attendance', string='Présences')

    def calcule_amount(self):
        for rec in self:
            salaire_per_hour = 0
            bulletin = rec.env['hr.payroll_ma.bulletin'].search([('employee_id', '=', rec.employee_id.id)]).filtered(
                lambda x: (x.period_id.date_start <= rec.date_start <= x.period_id.date_end) and (
                        x.period_id.date_start <= rec.date_end <= x.period_id.date_end))

            if bulletin.employee_contract_id.resource_calendar_id.hours_per_day != 0:
                if len(bulletin) > 0:
                    salaire_per_hour = (
                                                   bulletin.salaire_base / bulletin.employee_contract_id.working_days_per_month) / bulletin.employee_contract_id.resource_calendar_id.hours_per_day
                else:
                    salaire_per_hour = (
                                                   rec.employee_id.contract_id.wage / bulletin.employee_contract_id.working_days_per_month) / bulletin.employee_contract_id.resource_calendar_id.hours_per_day

            rec.amount_25 = rec.h_25 * 1.25 * salaire_per_hour
            rec.amount_50 = rec.h_50 * 1.5 * salaire_per_hour

    def action_attendances_button(self):
        for rec in self:
            return {
                "name": "Présences",
                'view_mode': 'tree',
                'view_type': 'tree',
                "res_model": "hr.attendance",
                "type": "ir.actions.act_window",
                # "context": context,
                'views': [(self.env.ref("hr_attendance.view_attendance_tree").id, 'list')],
                "domain": [("id", "in", rec.attendance_ids.ids)],
            }

    def cron_week_heure_sup(self):
        for attendance in self.env['hr.attendance'].search(
                [('check_in', '!=', False), ('check_out', '!=', False), ('hn', '>', 7)]).filtered(
            lambda x: (x.check_in > datetime.datetime.now() - datetime.timedelta(days=7)) and (
                    x.check_out < datetime.datetime.now())):
            attendance.action_server_appliquer_horaire_one()

        for employee in self.env['hr.attendance'].search([('check_in', '!=', False), ('check_out', '!=', False), ('hn', '>', 7)]).filtered(lambda x: (x.check_in > datetime.datetime.now() - datetime.timedelta(days=7)) and (x.check_out < datetime.datetime.now())).mapped('employee_id'):
            if sum(self.env['hr.attendance'].search([('employee_id', '=', employee.id), ('check_in', '!=', False), ('check_out', '!=', False),('hn', '>', 7)]).filtered(lambda x: (x.check_in > datetime.datetime.now() - datetime.timedelta(days=7)) and (x.check_out < datetime.datetime.now())).mapped('worked_hours')) > 33:
                sum_heure_sup_25 = sum(self.env['hr.attendance'].search([('employee_id', '=', employee.id), ('check_in', '!=', False), ('check_out', '!=', False),('hn', '>', 7)]).filtered(lambda x: (x.check_in > datetime.datetime.now() - datetime.timedelta(days=7)) and (x.check_out < datetime.datetime.now())).mapped('h_25'))
                sum_heure_sup_50 = sum(self.env['hr.attendance'].search([('employee_id', '=', employee.id), ('check_in', '!=', False), ('check_out', '!=', False),('hn', '>', 7)]).filtered(lambda x: (x.check_in > datetime.datetime.now() - datetime.timedelta(days=7)) and (x.check_out < datetime.datetime.now())).mapped('h_50'))
                sum_worked_hours = sum(self.env['hr.attendance'].search([('employee_id', '=', employee.id), ('check_in', '!=', False), ('check_out', '!=', False),('hn', '>', 7)]).filtered(lambda x: (x.check_in > datetime.datetime.now() - datetime.timedelta(days=7)) and (x.check_out < datetime.datetime.now())).mapped('worked_hours'))

                get_heure_sup_25 = 0
                get_heure_sup_50 = 0

                reste_hours_sup = sum_worked_hours - 33

                if sum_heure_sup_50 >= reste_hours_sup:
                    get_heure_sup_50 = reste_hours_sup
                else:
                    get_heure_sup_50 = sum_heure_sup_50
                    reste_hours_sup = reste_hours_sup - sum_heure_sup_50

                if sum_heure_sup_25 >= reste_hours_sup:
                    get_heure_sup_25 = reste_hours_sup
                else:
                    get_heure_sup_25 = sum_heure_sup_25

                self.env['dh.heure.sup'].create({'employee_id': employee.id, 'date_start': (datetime.datetime.now() - datetime.timedelta(days=7)).date(),'date_end': (datetime.datetime.now()).date(), 'h_25': get_heure_sup_25,'h_50': get_heure_sup_50,'attendance_ids': [(4, attendance.id) for attendance in self.env['hr.attendance'].search([('employee_id', '=', employee.id),('check_in', '!=', False),('check_out', '!=', False)]).filtered(lambda x: (x.check_in > datetime.datetime.now() - datetime.timedelta(days=7)) and (x.check_out < datetime.datetime.now()))]})
