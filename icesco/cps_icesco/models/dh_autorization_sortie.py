# # -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import date, datetime, timedelta
from odoo.exceptions import UserError, ValidationError
import json
from dateutil.relativedelta import relativedelta

class DHAutorizationSortie(models.Model):

    _name = 'dh.autorisation.sortie'

    employee_id = fields.Many2one('hr.employee', string='Employée', required=True)
    department_id = fields.Many2one('hr.department', string='Département', related='employee_id.department_id')
    check_out = fields.Datetime('Check Out', required=True)
    check_in = fields.Datetime('Check In')
    motif = fields.Char(string='Motif')
    leave_hours = fields.Float(string='Durée', compute='_compute_leave_hours', store=True, readonly=True)
    # dh_autorisation_to_remove = fields.Boolean(string='To remove', store=True)

    @api.model
    def create(self, vals):
        print('type vals', vals['check_out'])
        autorisations_this_month = self.env['dh.autorisation.sortie'].search(
            [('employee_id', '=', vals['employee_id']), ('check_out', '>=', datetime.strptime(vals['check_out'].strftime('%Y-%m-01'), "%Y-%m-%d")),
             ('check_in', '<', datetime.strptime((vals['check_out'].date() + relativedelta(months=1)).strftime('%Y-%m-01'), "%Y-%m-%d"))])

        if len(autorisations_this_month) == 3 or sum(autorisations_this_month.mapped('leave_hours')) >= 6:
            raise ValidationError("Vous ne pouvez pas enregistrer votre sortie car vous avez atteint le nombre maximal d'autorisations de sortie allouées pour ce mois. Merci.")

        res = super(DHAutorizationSortie, self).create(vals)
        return res


    @api.depends('check_in', 'check_out')
    def _compute_leave_hours(self):
        for attendance in self:
            if attendance.check_in:
                delta = attendance.check_in - attendance.check_out
                attendance.leave_hours = delta.total_seconds() / 3600.0
            else:
                attendance.leave_hours = False