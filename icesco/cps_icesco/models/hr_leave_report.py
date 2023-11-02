# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, exceptions, _
from odoo.osv import expression
from datetime import date
from odoo.tools import date_utils

class CpsLeaveReport(models.Model):
    _inherit = "hr.leave.report"

    validity_start = fields.Date("From", related='holiday_status_id.validity_start')
    validity_stop = fields.Date("To", related='holiday_status_id.validity_stop')

    def init(self):
        tools.drop_view_if_exists(self._cr, 'hr_leave_report')

        self._cr.execute("""
            CREATE or REPLACE view hr_leave_report as (
                SELECT row_number() over(ORDER BY leaves.employee_id) as id,
                leaves.employee_id as employee_id, leaves.name as name,
                leaves.number_of_days as number_of_days, leaves.leave_type as leave_type,
                leaves.category_id as category_id, leaves.department_id as department_id,
                leaves.holiday_status_id as holiday_status_id, leaves.state as state,
                leaves.holiday_type as holiday_type, leaves.date_from as date_from,
                leaves.date_to as date_to, leaves.payslip_status as payslip_status
                from (select
                    allocation.employee_id as employee_id,
                    allocation.name as name,
                    allocation.number_of_days as number_of_days,
                    allocation.category_id as category_id,
                    allocation.department_id as department_id,
                    allocation.holiday_status_id as holiday_status_id,
                    allocation.state as state,
                    allocation.holiday_type,
                    null as date_from,
                    null as date_to,
                    FALSE as payslip_status,
                    'allocation' as leave_type
                from hr_leave_allocation as allocation
                union all select
                    request.employee_id as employee_id,
                    request.name as name,
                    (request.number_of_days * -1) as number_of_days,
                    request.category_id as category_id,
                    request.department_id as department_id,
                    request.holiday_status_id as holiday_status_id,
                    request.state as state,
                    request.holiday_type,
                    request.date_from as date_from,
                    request.date_to as date_to,
                    request.payslip_status as payslip_status,
                    'request' as leave_type
                from hr_leave as request) leaves
            );
        """)

    @api.model
    def action_time_off_analysis_current_year(self):
        domain = [('holiday_type', '=', 'employee')]

        if self.env.context.get('active_ids'):
            domain = expression.AND([
                domain,
                [('employee_id', 'in', self.env.context.get('active_ids', [])), '|', '&', ('validity_start', '>=', date_utils.start_of(fields.Date.today(), 'year')), ('validity_start', '<=', date_utils.end_of(fields.Date.today(), 'year')), '&', ('date_from', '>=', date_utils.start_of(fields.Date.today(), 'year')), ('date_from', '<=', date_utils.end_of(fields.Date.today(), 'year'))]
            ])

        return {
            'name': _('Time Off Analysis'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.leave.report',
            'view_mode': 'tree,form,pivot',
            'search_view_id': self.env.ref('hr_holidays.view_hr_holidays_filter_report').id,
            'domain': domain,
            'context': {
                'search_default_group_type': True,
                'search_default_year': True
            }
        }

    @api.model
    def action_time_off_analysis(self):
        domain = [('holiday_type', '=', 'employee')]

        if self.env.context.get('active_ids'):
            domain = expression.AND([
                domain,
                [('employee_id', 'in', self.env.context.get('active_ids', []))]
            ])

        return {
            'name': _('Time Off Analysis'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.leave.report',
            'view_mode': 'tree,form,pivot',
            'search_view_id': self.env.ref('hr_holidays.view_hr_holidays_filter_report').id,
            'domain': domain,
            'context': {
                'search_default_group_type': True,
                'search_default_year': True,
            }
        }

    # @api.model
    # def action_time_off_analysis(self):
    #
    #     domain = [('holiday_type', '=', 'employee'), ('date_from', '>=', date(date.today().year, 1, 1)),
    #                   ('date_to', '<=', date(date.today().year, 12, 31))]
    #
    #     if self.env.context.get('active_ids'):
    #         allo_ids = []
    #         leave_reports = self.env['hr.leave.report'].search([('employee_id', 'in', self.env.context.get('active_ids', [])), ('holiday_type', '=', 'employee'), ('date_from', '>=', date(date.today().year, 1, 1)),
    #              ('date_to', '<=', date(date.today().year, 12, 31))])
    #         for leave_report in leave_reports:
    #             allo_ids = allo_ids + self.env['hr.leave.report'].search(
    #                 [('employee_id', 'in', self.env.context.get('active_ids', [])), ('date_from', '=', False),
    #                  ('date_to', '=', False), ('holiday_status_id', '=', leave_report.holiday_status_id.id)]).ids
    #
    #         domain = [('id', 'in', allo_ids + leave_reports.ids)]
    #
    #     return {
    #         'name': _('Time Off Analysis'),
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'hr.leave.report',
    #         'view_mode': 'tree,form,pivot',
    #         'search_view_id': self.env.ref('hr_holidays.view_hr_holidays_filter_report').id,
    #         'domain': domain,
    #         'context': {
    #             'search_default_group_type': True,
    #             # 'search_default_year': True
    #         }
    #     }
