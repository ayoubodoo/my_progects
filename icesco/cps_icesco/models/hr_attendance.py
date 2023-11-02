# # -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from odoo.tools import format_datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_round
from datetime import date, datetime, timedelta
import locale


class CpsHrAttendance(models.Model):

    _inherit = 'hr.attendance'
    matricule = fields.Char(string=_("Matricule"), store=True, related='employee_id.matricule')
    # matricule = fields.Char(related="employee_id.matricule", string='Matricule', store=True)
    # equipe = fields.Selection([('A', 'A'), ('B', 'B'), ('FM', 'FM'), ('FA', 'FA')], string='Equipe salarié', related="employee_id.equipe", store=True)
    horaire_id = fields.Many2one('cps.hr.horaire', 'Horaire')
    # checkin_horaire = fields.Datetime(related="horaire_id.horaire_debut", string='Horaire entrée')
    checkin_corriged = fields.Datetime('Entrée orig.')
    checkin_anomalie = fields.Selection(string='An. Entrée', selection=[('chekin_before_time', 'Entrée avant heure'), ('late', 'Retard'), ('abnormal_checkin', 'Entrée anormale'), ('absence', 'absence'), ('normal', 'Normal')])
    # checkout_horaire = fields.Datetime(related="horaire_id.horaire_fin", string='Horaire sortie')
    checkout_corriged = fields.Datetime('Sortie orig.')
    checkout_anomalie = fields.Selection(string='An. Sortie', selection=[('chekout_before_time', 'Sortie avant heure'), ('chekout_after_time', 'Sortie aprés heure'), ('abnormal_checkout', 'Sortie anormale'), ('absence', 'absence'), ('normal', 'Normal')])
    correction_id = fields.Many2one('cps.hr.correction', 'N° Correction')
    hn = fields.Float('HN')
    h_25 = fields.Float('H25')
    h_50 = fields.Float('H50')
    h_100 = fields.Float('H100')
    is_absent = fields.Boolean('Est absent')
    is_duree_pause = fields.Boolean('Est pause', default=True)
    deactive_50_100 = fields.Boolean('Désactiver 50% et 100%', default=False)
    jour_ferie = fields.Boolean('Jour Férie', default=False)
    pointage_double = fields.Boolean('Pointage Double', compute='_compute_pointage_double', store=True)
    pointage_est_corriger = fields.Boolean('Est Corrige')
    sans_pointage= fields.Boolean(string=_("Sans Pointage"), store=True, related='employee_id.sans_pointage')
    dh_to_remove = fields.Boolean(string='To remove', store=True)
    jour = fields.Char(string='Jour',compute='_get_jour')


    def get_action_normal(self):
        return str(self.env.ref('hr_attendance.hr_attendance_action_kiosk_mode').id)

    def get_action_autorisation_sortie(self):
        return str(self.env.ref('kzm_hr_pointeuse.dh_hr_attendance_action_kiosk_mode').id)

    # def set_locale(locale_):
    #     locale.setlocale(category=locale.LC_ALL, locale=locale_)

    @api.depends('check_in')
    def _get_jour(self):
        for rec in self:
            rec.jour = rec.check_in.strftime('%A')
            if rec.jour == 'Monday':
                rec.jour = 'Lundi'
            elif rec.jour == 'Tuesday':
                rec.jour = 'Mardi'
            elif rec.jour == 'Wednesday':
                rec.jour = 'Mercredi'
            elif rec.jour == 'Thursday':
                rec.jour = 'Jeudi'
            elif rec.jour == 'Friday':
                rec.jour = 'Vendredi'
            elif rec.jour == 'Friday':
                rec.jour = 'Vendredi'
            elif rec.jour == 'Saturday':
                rec.jour = 'Samedi'
            elif rec.jour == 'Sunday':
                rec.jour = 'Dimanche'




    def action_marquer_un_pointage_corrige(self):
        for rec in self.env['hr.attendance'].browse(self._context.get('active_ids', [])):
            if rec.pointage_est_corriger == False:
                rec.write({'pointage_est_corriger': True})

    def action_marquer_un_pointage_non_corrige(self):
        for rec in self.env['hr.attendance'].browse(self._context.get('active_ids', [])):
            if rec.pointage_est_corriger == True:
                rec.write({'pointage_est_corriger': False})

    # @api.constrains('check_in', 'check_out', 'employee_id')
    # def _check_validity(self):
    #     """ Verifies the validity of the attendance record compared to the others from the same employee.
    #         For the same employee we must have :
    #             * maximum 1 "open" attendance record (without check_out)
    #             * no overlapping time slices with previous employee records
    #     """
    #     for attendance in self:
    #         # we take the latest attendance before our check_in time and check it doesn't overlap with ours
    #         last_attendance_before_check_in = self.env['hr.attendance'].search([
    #             ('employee_id', '=', attendance.employee_id.id),
    #             ('check_in', '<=', attendance.check_in),
    #             ('id', '!=', attendance.id),
    #         ], order='check_in desc', limit=1)
    #         if last_attendance_before_check_in and last_attendance_before_check_in.check_out and last_attendance_before_check_in.check_out > attendance.check_in:
    #             raise exceptions.ValidationError(_("Cannot create new attendance record for %(empl_name)s, the employee was already checked in on %(datetime)s") % {
    #                 'empl_name': attendance.employee_id.name,
    #                 'datetime': format_datetime(self.env, attendance.check_in, dt_format=False),
    #             })
    #
    #         if not attendance.check_out:
    #             # if our attendance is "open" (no check_out), we verify there is no other "open" attendance
    #             no_check_out_attendances = self.env['hr.attendance'].search([
    #                 ('employee_id', '=', attendance.employee_id.id),
    #                 ('check_out', '=', False),
    #                 ('id', '!=', attendance.id),
    #             ], order='check_in desc', limit=1)
    #             # if no_check_out_attendances:
    #             #     raise exceptions.ValidationError(_("Cannot create new attendance record for %(empl_name)s, the employee hasn't checked out since %(datetime)s") % {
    #             #         'empl_name': attendance.employee_id.name,
    #             #         'datetime': format_datetime(self.env, no_check_out_attendances.check_in, dt_format=False),
    #             #     })
    #
    #         if attendance.check_out:
    #             # we verify that the latest attendance with check_in time before our check_out time
    #             # is the same as the one before our check_in time computed before, otherwise it overlaps
    #             last_attendance_before_check_out = self.env['hr.attendance'].search([
    #                 ('employee_id', '=', attendance.employee_id.id),
    #                 ('check_in', '<', attendance.check_out),
    #                 ('id', '!=', attendance.id),
    #             ], order='check_in desc', limit=1)
    #             if last_attendance_before_check_out and last_attendance_before_check_in != last_attendance_before_check_out:
    #                 raise exceptions.ValidationError(_("Cannot create new attendance record for %(empl_name)s, the employee was already checked in on %(datetime)s") % {
    #                     'empl_name': attendance.employee_id.name,
    #                     'datetime': format_datetime(self.env, last_attendance_before_check_out.check_in, dt_format=False),
    #                 })


    @api.depends('check_in', 'employee_id')
    def _compute_pointage_double(self):
        for rec in self:
            if len(rec.env['hr.attendance'].search([('employee_id', '=', rec.employee_id.id), ('check_in', '<', rec.check_in), ('check_in', '>=', datetime.combine(rec.check_in.date(), datetime.min.time())), ('check_in', '<=', datetime.combine((rec.check_in.date() + timedelta(days=1)), datetime.min.time()))])) > 0:
                rec.pointage_double = True
                for attendance in rec.env['hr.attendance'].search(
                    [('employee_id', '=', rec.employee_id.id), ('check_in', '<', rec.check_in),
                     ('check_in', '>=', datetime.combine(rec.check_in.date(), datetime.min.time())), ('check_in', '<=',
                                                                                                      datetime.combine((rec.check_in.date() + timedelta(days=1)),datetime.min.time()))]):
                    attendance.pointage_double = True
            else:
                rec.pointage_double = False

    @api.onchange('horaire_id')
    def change_anomalie(self):
        for rec in self:
            if rec.horaire_id.id == False:
                rec.checkin_anomalie = False
                rec.checkout_anomalie = False

    # def action_deactive_50_100(self):
    #     for rec in self.env['hr.attendance'].browse(self._context.get('active_ids', [])):
    #         if rec.deactive_50_100 == False:
    #             rec.write({'deactive_50_100': True})
    #
    # def action_active_50_100(self):
    #     for rec in self.env['hr.attendance'].browse(self._context.get('active_ids', [])):
    #         if rec.deactive_50_100:
    #             rec.write({'deactive_50_100': False})

    def action_active_jour_ferie(self):
        for rec in self.env['hr.attendance'].browse(self._context.get('active_ids', [])):
            if rec.jour_ferie == False:
                rec.write({'jour_ferie': True})

    def action_deactive_jour_ferie(self):
        for rec in self.env['hr.attendance'].browse(self._context.get('active_ids', [])):
            if rec.jour_ferie:
                rec.write({'jour_ferie': False})

    def change_state_is_duree_pause_true(self):
        for rec in self.env['hr.attendance'].browse(self._context.get('active_ids', [])):
            if rec.is_duree_pause == False:
                rec.write({'is_duree_pause': True})
                rec._compute_worked_hours()

    def change_state_is_duree_pause_false(self):
        for rec in self.env['hr.attendance'].browse(self._context.get('active_ids', [])):
            if rec.is_duree_pause == True:
                rec.write({'is_duree_pause': False})
                rec._compute_worked_hours()

    @api.model
    def create(self, values):
        jour_ferie = False
        if 'check_in' in values.keys():
            if self.env['hr.employee'].search([('id', '=', values['employee_id'])]).contract_id.filtered(
                    lambda x: x.state == 'open'):
                for leave in self.env['hr.employee'].search([('id', '=', values['employee_id'])]).contract_id.filtered(
                        lambda x: x.state == 'open').resource_calendar_id.global_leave_ids:
                    if leave.date_from.date() <= datetime.fromisoformat(
                            str(values['check_in'])).date() and leave.date_to.date() >= datetime.fromisoformat(
                        str(values['check_in'])).date():
                        jour_ferie = True
            else:
                for leave in self.env['resource.calendar.leaves'].search([('resource_id', '=', False)]):
                    if leave.date_from.date() <= datetime.fromisoformat(
                            str(values['check_in'])).date() and leave.date_to.date() >= datetime.fromisoformat(
                        str(values['check_in'])).date():
                        jour_ferie = True

            if datetime.fromisoformat(str(values['check_in'])).date().weekday() == 6:
                jour_ferie = True

        values['jour_ferie'] = jour_ferie
        attendance = super(CpsHrAttendance, self).create(values)
        return attendance

    @api.depends('check_in', 'check_out', 'is_duree_pause', 'jour_ferie', 'horaire_id') # 'deactive_50_100',
    def _compute_worked_hours(self):
        for attendance in self:
            # nouveau principe
            jour_ferie = False
            if attendance.check_out:
                delta = attendance.check_out - attendance.check_in
                work_hours = delta.total_seconds() / 3600.0
                attendance.worked_hours = work_hours

            for leave in self.env['resource.calendar.leaves'].search([('resource_id', '=', False)]):
                if leave.date_from.date() <= datetime.fromisoformat(
                        str(attendance.check_in)).date() and leave.date_to.date() >= datetime.fromisoformat(
                    str(attendance.check_in)).date():
                    jour_ferie = True

            if attendance.check_in.date().weekday() in [5, 6] or jour_ferie == True:
                if attendance.check_out:
                    delta_h50 = attendance.check_out - attendance.check_in
                    if delta_h50.total_seconds() / 3600.0 > 0:
                        attendance.h_50 = delta_h50.total_seconds() / 3600.0
                        attendance.h_25 = 0
                    else:
                        attendance.h_50 = 0
                        attendance.h_25 = 0
            else:
                if attendance.check_out and attendance.horaire_id:

                    delta_debut_fin_h25 = attendance.horaire_id.horaire_fin_h25.date() - attendance.horaire_id.horaire_debut_h25.date()
                    delta_debut_fin_h50 = attendance.horaire_id.horaire_fin_h50.date() - attendance.horaire_id.horaire_debut_h50.date()

                    horaire_debut = attendance.horaire_id.horaire_debut.replace(year=attendance.check_in.year, month=attendance.check_in.month, day=attendance.check_in.day)
                    horaire_fin = attendance.horaire_id.horaire_fin.replace(year=attendance.check_in.year, month=attendance.check_in.month, day=attendance.check_in.day)
                    horaire_debut_h25 = attendance.horaire_id.horaire_debut_h25.replace(year=attendance.check_in.year, month=attendance.check_in.month, day=attendance.check_in.day)
                    horaire_fin_h25 = attendance.horaire_id.horaire_fin_h25.replace(year=attendance.check_in.year, month=attendance.check_in.month, day=attendance.check_in.day) + timedelta(days=delta_debut_fin_h25.days)
                    horaire_debut_h50 = attendance.horaire_id.horaire_debut_h50.replace(year=attendance.check_in.year, month=attendance.check_in.month, day=attendance.check_in.day)
                    horaire_fin_h50 = attendance.horaire_id.horaire_fin_h50.replace(year=attendance.check_in.year, month=attendance.check_in.month, day=attendance.check_in.day) + timedelta(days=delta_debut_fin_h50.days)

                    if attendance.check_out >= horaire_fin:
                        delta_hn = horaire_fin - attendance.check_in
                    elif attendance.check_out < horaire_fin:
                        delta_hn = attendance.check_out - attendance.check_in
                    else:
                        delta_hn = 0

                    if attendance.check_in <= horaire_debut_h25 and attendance.check_out >= horaire_fin_h25:
                        delta_h25 = horaire_fin_h25 - horaire_debut_h25
                    elif attendance.check_in > horaire_debut_h25 and attendance.check_out >= horaire_fin_h25:
                        delta_h25 = horaire_fin_h25 - attendance.check_in
                    elif attendance.check_in <= horaire_debut_h25 and attendance.check_out < horaire_fin_h25:
                        delta_h25 = attendance.check_out - horaire_debut_h25
                    elif attendance.check_in > horaire_debut_h25 and attendance.check_out < horaire_fin_h25:
                        delta_h25 = attendance.check_out - attendance.check_in
                    else:
                        delta_h25 = 0

                    if attendance.check_in <= horaire_debut_h50 and attendance.check_out >= horaire_fin_h50:
                        delta_h50 = horaire_fin_h50 - horaire_debut_h50
                    elif attendance.check_in > horaire_debut_h50 and attendance.check_out >= horaire_fin_h50:
                        delta_h50 = horaire_fin_h50 - attendance.check_in
                    elif attendance.check_in <= horaire_debut_h50 and attendance.check_out < horaire_fin_h50:
                        delta_h50 = attendance.check_out - horaire_debut_h50
                    elif attendance.check_in > horaire_debut_h50 and attendance.check_out < horaire_fin_h50:
                        delta_h50 = attendance.check_out - attendance.check_in
                    else:
                        delta_h50 = 0

                    if delta.total_seconds() / 3600.0 > 0:
                        attendance.worked_hours = delta.total_seconds() / 3600.0
                    else:
                        attendance.worked_hours = 0

                    if delta_hn.total_seconds() / 3600.0 > 0:
                        attendance.hn = delta_hn.total_seconds() / 3600.0
                    else:
                        attendance.hn = 0

                    if delta_h25.total_seconds() / 3600.0 > 0:
                        attendance.h_25 = delta_h25.total_seconds() / 3600.0
                    else:
                        attendance.h_25 = 0

                    if delta_h50.total_seconds() / 3600.0 > 0:
                        attendance.h_50 = delta_h50.total_seconds() / 3600.0
                    else:
                        attendance.h_50 = 0

            # ancienne principe

            # Holiday = False
            # if attendance.jour_ferie == True:
            #     Holiday = True
            # print('weekday', attendance.check_in.date().weekday())
            # if attendance.check_in.date().weekday() != 6 and Holiday != True: #or attendance.deactive_50_100 == True
            #     attendance.h_50 = 0
            #     attendance.h_100 = 0
            #     if attendance.check_out:
            #         delta = attendance.check_out - attendance.check_in
            #         work_hours = delta.total_seconds() / 3600.0
            #         decimal_part = work_hours % 1
            #         if decimal_part < 1 and decimal_part >= 0.75:
            #             work_hours = int(work_hours) + 1
            #         if decimal_part < 0.75 and decimal_part > 0.25:
            #             work_hours = int(work_hours) + 0.5
            #         if decimal_part <= 0.25 and decimal_part > 0:
            #             work_hours = int(work_hours)
            #         # attendance.worked_hours = delta.total_seconds() / 3600.0
            #         attendance.worked_hours = work_hours
            #         attendance.hn = attendance.worked_hours
            #         print('attendance.worked_hours-------------------------', attendance.worked_hours % 2)
            #         decimal_value = (attendance.worked_hours % 2)
            #         if decimal_value > 1:
            #             if decimal_value - 1 < 0.25:
            #                 attendance.hn = attendance.worked_hours - (decimal_value - 1) + 0
            #             elif decimal_value - 1 < 0.5:
            #                 attendance.hn = attendance.worked_hours - (decimal_value - 1) + 0.25
            #             elif decimal_value - 1 < 0.75:
            #                 attendance.hn = attendance.worked_hours - (decimal_value - 1) + 0.5
            #             elif decimal_value - 1 >= 0.75:
            #                 attendance.hn = attendance.worked_hours - (decimal_value - 1) + 0.75
            #         if attendance.is_duree_pause:
            #             # if len(attendance.correction_id) > 0:
            #             if len(attendance.horaire_id) > 0:
            #                 print('attendance.horaire_id.duree_pause----------------------------------------',
            #                       attendance.horaire_id.duree_pause)
            #                 if attendance.hn > 4:
            #                     attendance.hn -= attendance.horaire_id.duree_pause
            #             else:
            #                 if attendance.hn > 4:
            #                     attendance.hn -= 0.5
            #         attendance.h_25 = 0
            #         if attendance.hn > 10:
            #             attendance.h_25 = attendance.hn - 10
            #             attendance.hn = 10
            #     else:
            #         attendance.worked_hours = False
            # else:
            #     if attendance.jour_ferie == True:
            #         attendance.hn = 0
            #         attendance.h_25 = 0
            #         if attendance.check_out:
            #             delta = attendance.check_out - attendance.check_in
            #             work_hours = delta.total_seconds() / 3600.0
            #             decimal_part = work_hours % 1
            #             if decimal_part < 1 and decimal_part >= 0.75:
            #                 work_hours = int(work_hours) + 1
            #             if decimal_part < 0.75 and decimal_part > 0.25:
            #                 work_hours = int(work_hours) + 0.5
            #             if decimal_part <= 0.25 and decimal_part > 0:
            #                 work_hours = int(work_hours)
            #             attendance.worked_hours = work_hours
            #             # attendance.worked_hours = delta.total_seconds() / 3600.0
            #             attendance.h_50 = attendance.worked_hours
            #             # print('attendance.worked_hours-------------------------', attendance.worked_hours % 2)
            #             decimal_value = (attendance.worked_hours % 2)
            #             if decimal_value > 1:
            #                 if decimal_value - 1 < 0.25:
            #                     attendance.h_50 = attendance.worked_hours - (decimal_value - 1) + 0
            #                 elif decimal_value - 1 < 0.5:
            #                     attendance.h_50 = attendance.worked_hours - (decimal_value - 1) + 0.25
            #                 elif decimal_value - 1 < 0.75:
            #                     attendance.h_50 = attendance.worked_hours - (decimal_value - 1) + 0.5
            #                 elif decimal_value - 1 >= 0.75:
            #                     attendance.h_50 = attendance.worked_hours - (decimal_value - 1) + 0.75
            #             if attendance.is_duree_pause:
            #                 # if len(attendance.correction_id) > 0:
            #                 if len(attendance.horaire_id) > 0:
            #                     # print('attendance.horaire_id.duree_pause----------------------------------------',
            #                     #       attendance.horaire_id.duree_pause)
            #                     if attendance.h_50 > 4:
            #                         attendance.h_50 -= attendance.horaire_id.duree_pause
            #                 else:
            #                     if attendance.h_50 > 4:
            #                         attendance.h_50 -= 0.5
            #             attendance.h_100 = 0
            #             if attendance.h_50 > 10:
            #                 attendance.h_100 = attendance.h_50 - 10
            #                 attendance.h_50 = 10
            #         else:
            #             attendance.worked_hours = False
            #     else:
            #         attendance.h_50 = 0
            #         attendance.h_100 = 0
            #         if attendance.check_out:
            #             delta = attendance.check_out - attendance.check_in
            #             work_hours = delta.total_seconds() / 3600.0
            #             decimal_part = work_hours % 1
            #             if decimal_part < 1 and decimal_part >= 0.75:
            #                 work_hours = int(work_hours) + 1
            #             if decimal_part < 0.75 and decimal_part > 0.25:
            #                 work_hours = int(work_hours) + 0.5
            #             if decimal_part <= 0.25 and decimal_part > 0:
            #                 work_hours = int(work_hours)
            #             # attendance.worked_hours = delta.total_seconds() / 3600.0
            #             attendance.worked_hours = work_hours
            #             attendance.hn = attendance.worked_hours
            #             # print('attendance.worked_hours-------------------------', attendance.worked_hours % 2)
            #             decimal_value = (attendance.worked_hours % 2)
            #             if decimal_value > 1:
            #                 if decimal_value - 1 < 0.25:
            #                     attendance.hn = attendance.worked_hours - (decimal_value - 1) + 0
            #                 elif decimal_value - 1 < 0.5:
            #                     attendance.hn = attendance.worked_hours - (decimal_value - 1) + 0.25
            #                 elif decimal_value - 1 < 0.75:
            #                     attendance.hn = attendance.worked_hours - (decimal_value - 1) + 0.5
            #                 elif decimal_value - 1 >= 0.75:
            #                     attendance.hn = attendance.worked_hours - (decimal_value - 1) + 0.75
            #             if attendance.is_duree_pause:
            #                 # if len(attendance.correction_id) > 0:
            #                 if len(attendance.horaire_id) > 0:
            #                     # print('attendance.horaire_id.duree_pause----------------------------------------',
            #                     #       attendance.horaire_id.duree_pause)
            #                     if attendance.hn > 4:
            #                         attendance.hn -= attendance.horaire_id.duree_pause
            #                 else:
            #                     if attendance.hn > 4:
            #                         attendance.hn -= 0.5
            #             attendance.h_25 = 0
            #             if attendance.hn > 10:
            #                 attendance.h_25 = attendance.hn - 10
            #                 attendance.hn = 10
            #         else:
            #             attendance.worked_hours = False


    def write(self, values):
        jour_ferie = False
        if 'check_in' in values.keys():
            if self.env['hr.employee'].search([('id', '=', self.employee_id.id)]).contract_id.filtered(
                    lambda x: x.state == 'open'):
                for leave in self.env['hr.employee'].search([('id', '=', self.employee_id.id)]).contract_id.filtered(
                        lambda x: x.state == 'open').resource_calendar_id.global_leave_ids:
                    if leave.date_from.date() <= datetime.fromisoformat(
                            str(values['check_in'])).date() and leave.date_to.date() >= datetime.fromisoformat(
                        str(values['check_in'])).date():
                        jour_ferie = True
            else:
                for leave in self.env['resource.calendar.leaves'].search([('resource_id', '=', False)]):
                    if leave.date_from.date() <= datetime.fromisoformat(
                            str(values['check_in'])).date() and leave.date_to.date() >= datetime.fromisoformat(
                        str(values['check_in'])).date():
                        jour_ferie = True

            if datetime.fromisoformat(str(values['check_in'])).date().weekday() == 6:
                jour_ferie = True

            values['jour_ferie'] = jour_ferie
        attendance = super(CpsHrAttendance, self).write(values)
        if 'is_absent' in values:
            if values['is_absent']:
                self.employee_id.is_absents=True
        if 'check_in' in values:
            if values['check_in']:
                if self.check_in!=False:
                    self.pointage_est_corriger=True
        if 'check_out' in values:
            if values['check_out']:
                if self.check_out != False:
                    self.pointage_est_corriger=True
        return attendance

    def action_appliquer_horaire(self):

        check_in = datetime.strptime(self.correction_id.date_correction.strftime('%Y-%m-%d') + " " + self.horaire_id.horaire_debut.strftime('%H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        check_out = datetime.strptime(self.correction_id.date_correction.strftime('%Y-%m-%d') + " " + self.horaire_id.horaire_fin.strftime('%H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        # print ('check_out--------------------------------', check_out)
        if datetime.strptime(self.horaire_id.horaire_fin.strftime('%Y-%m-%d'), '%Y-%m-%d') == datetime.strptime(self.horaire_id.horaire_debut.strftime('%Y-%m-%d'), '%Y-%m-%d'):
            day_out_horaire = datetime.strptime(self.correction_id.date_correction.strftime('%Y-%m-%d'), '%Y-%m-%d') + timedelta(days=1)
            check_out = datetime.strptime(day_out_horaire.strftime('%Y-%m-%d') + " " + self.horaire_id.horaire_fin.strftime('%H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        self.write({'pointage_est_corriger': True ,'check_in': check_in, 'check_out': check_out})
        # self.correction_id.action_appliquer_horaire()

    def sortie_automatique_pointage(self):
       for attendance in self.env['hr.attendance'].search([('check_out', '=', False), ('check_in', '>=', ((fields.Date.today()-timedelta(days=1)).strftime('%Y-%m-%d 00:00:00'))), ('check_in', '<=', ((fields.Date.today()-timedelta(days=0)).strftime('%Y-%m-%d 00:00:00')))]):
           attendance.write({'check_out': datetime(attendance.check_in.date().year,
                                                        attendance.check_in.date().month,
                                                        attendance.check_in.date().day, 22, 59, 59)})

    def correction_pointage_all(self):
        horairess = self.env['cps.hr.horaire'].search([])
        horaires = []
        for attendance in self.env['hr.attendance'].search([('create_date', '>=', ((fields.Date.today()-timedelta(days=1)).strftime('%Y-%m-%d 00:00:00'))), ('create_date', '<=', ((fields.Date.today()-timedelta(days=0)).strftime('%Y-%m-%d 00:00:00')))]):
            if attendance.worked_hours>0:
                for horaire in horairess:
                    for date in horaire.dates:
                        if attendance.check_in >= date.date_debut and attendance.check_out <= date.date_fin:
                            horaires.append(horaire)

                if len(horaires) == 0:
                    attendance.horaire_id = False

                for horaire in horaires:
                    check_in = datetime.strptime(attendance.checkin_corriged.strftime('%H:%M:%S'),
                                                 '%H:%M:%S') if attendance.checkin_corriged else datetime.strptime(
                        attendance.check_in.strftime('%H:%M:%S'), '%H:%M:%S')
                    check_in_horaire = datetime.strptime(horaire.horaire_debut.strftime('%H:%M:%S'), '%H:%M:%S')
                    check_out = datetime.strptime(attendance.checkout_corriged.strftime('%H:%M:%S'),
                                                  '%H:%M:%S') if attendance.checkout_corriged else datetime.strptime(
                        attendance.check_out.strftime('%H:%M:%S'), '%H:%M:%S')
                    check_out_horaire = datetime.strptime(horaire.horaire_fin.strftime('%H:%M:%S'),'%H:%M:%S')
                    if ((check_in-check_in_horaire).total_seconds()>-float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.marge_horaire')) * 3600 and (check_in-check_in_horaire).total_seconds()<float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.marge_horaire')) * 3600):
                        attendance.horaire_id= horaire.id
                        break
                    else:
                        attendance.horaire_id = False

                if attendance.horaire_id:
                    # attendance.horaire_id=attendance.horaire_id.id
                    check_in_modified = None
                    check_out_modified = None
                    attendance.checkin_anomalie=""
                    attendance.checkout_anomalie=""
                    if attendance.checkin_corriged:
                        attendance.write({'pointage_est_corriger': True ,'check_in' : attendance.checkin_corriged})
                    if attendance.check_in:
                        check_in = datetime.strptime(attendance.check_in.strftime('%H:%M:%S'), '%H:%M:%S')# + timedelta(hours=1)
                        check_in_horaire = datetime.strptime(attendance.horaire_id.horaire_debut.strftime('%H:%M:%S'),'%H:%M:%S')# + timedelta(hours=1)
                        diff_in = (check_in-check_in_horaire).total_seconds()/60
                        if not attendance.checkin_corriged:
                            attendance.checkin_corriged = attendance.check_in
                        check_in_modified = attendance.check_in
                        if diff_in < -float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.marge_horaire')) * 3600:
                            attendance.checkin_anomalie= "chekin_before_time"
                        # if diff_in >= float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.marge_horaire')) * 3600:
                        #     attendance.checkin_anomalie= "late"
                        if diff_in >= 0 and diff_in <= float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.retard_time')) * 60:
                            attendance.checkin_anomalie = "normal"
                        # if diff_in > float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.retard_time')) * 60 and diff_in < float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.marge_horaire')) * 3600:
                        #     attendance.checkin_anomalie = "late"
                        if diff_in < 0 and diff_in>=-float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.marge_horaire')) * 3600:
                            if attendance.check_in!=attendance.horaire_id.horaire_debut:
                                check_in_modified= datetime.strptime(attendance.check_in.strftime('%Y-%m-%d') + " " + attendance.horaire_id.horaire_debut.strftime('%H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                            attendance.checkin_anomalie= "chekin_before_time"
                    if attendance.check_out:
                        horaire_j_plus_1 = True
                        if datetime.strptime(attendance.horaire_id.horaire_fin.strftime('%Y-%m-%d'),'%Y-%m-%d') == datetime.strptime(attendance.horaire_id.horaire_debut.strftime('%Y-%m-%d'), '%Y-%m-%d'):
                            horaire_j_plus_1 =False
                        if not horaire_j_plus_1:
                            check_out_horaire = datetime.strptime(attendance.check_in.strftime('%Y-%m-%d') + " " + attendance.horaire_id.horaire_fin.strftime('%H:%M:%S'),'%Y-%m-%d %H:%M:%S')# + timedelta(hours=1)
                        else:
                            day_out_horaire = datetime.strptime(attendance.check_in.strftime('%Y-%m-%d'),'%Y-%m-%d') + timedelta(days=1)
                            check_out_horaire = datetime.strptime(day_out_horaire.strftime('%Y-%m-%d') + " " + attendance.horaire_id.horaire_fin.strftime('%H:%M:%S'),'%Y-%m-%d %H:%M:%S')# + timedelta(hours=1)
                        check_out = datetime.strptime(attendance.check_out.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S') #+ timedelta(hours=1)
                        diff_out = (check_out-check_out_horaire).total_seconds()/60
                        if not attendance.checkout_corriged:
                            attendance.checkout_corriged = attendance.check_out
                        check_out_modified = attendance.check_out
                        if diff_out<0:
                            attendance.checkout_anomalie= "chekout_before_time"
                        if diff_out==0:
                            attendance.checkout_anomalie= "normal"
                        if diff_out>0 and diff_out<=float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.marge_horaire')) * 3600:
                            attendance.checkout_anomalie= "chekout_after_time"
                            if not horaire_j_plus_1:
                                check_out_modified= datetime.strptime(attendance.check_out.strftime('%Y-%m-%d') + " " + attendance.horaire_id.horaire_fin.strftime('%H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                            else:
                                day_out = datetime.strptime(attendance.check_in.strftime('%Y-%m-%d'),'%Y-%m-%d') + timedelta(days=1)
                                check_out_modified = datetime.strptime(day_out.strftime('%Y-%m-%d') + " " + attendance.horaire_id.horaire_fin.strftime('%H:%M:%S'),'%Y-%m-%d %H:%M:%S')
                        if diff_out>float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.marge_horaire')) * 3600:
                            attendance.checkout_anomalie= "chekout_after_time"
                    if check_in_modified and check_out_modified:
                        attendance.write({'pointage_est_corriger': True ,'check_in' : check_in_modified})
                else:
                    attendance.horaire_id = False
                    # attendance.checkin_corriged = False
                    # attendance.checkout_corriged = False
                    attendance.checkin_anomalie = False
                    attendance.checkout_anomalie = False
            # else:
            #     # print('absence----------------!!!!')
            #     attendance.checkin_anomalie = "absence"
            #     attendance.checkout_anomalie = "absence"
            attendance._compute_worked_hours()

    def action_server_appliquer_horaire(self):
        horairess = self.env['cps.hr.horaire'].search([])
        horaires = []

        # for attendance in self.attendance_ids:
        for attendance in self.env['hr.attendance'].search([('id', 'in', self._context.get('active_ids'))]):

            attendance._compute_worked_hours()


            if attendance.worked_hours>0:
                for horaire in horairess:
                    for date in horaire.dates:
                        if attendance.check_in >= date.date_debut and attendance.check_out <= date.date_fin:
                            horaires.append(horaire)

                if len(horaires) == 0:
                    attendance.horaire_id = False

                for horaire in horaires:
                    check_in = datetime.strptime(attendance.checkin_corriged.strftime('%H:%M:%S'),
                                                 '%H:%M:%S') if attendance.checkin_corriged else datetime.strptime(
                        attendance.check_in.strftime('%H:%M:%S'), '%H:%M:%S')
                    check_in_horaire = datetime.strptime(horaire.horaire_debut.strftime('%H:%M:%S'), '%H:%M:%S')
                    check_out = datetime.strptime(attendance.checkout_corriged.strftime('%H:%M:%S'),
                                                  '%H:%M:%S') if attendance.checkout_corriged else datetime.strptime(
                        attendance.check_out.strftime('%H:%M:%S'), '%H:%M:%S')
                    check_out_horaire = datetime.strptime(horaire.horaire_fin.strftime('%H:%M:%S'),'%H:%M:%S')
                    if ((check_in-check_in_horaire).total_seconds()>-float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.marge_horaire')) * 3600 and (check_in-check_in_horaire).total_seconds()<float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.marge_horaire')) * 3600):
                        attendance.horaire_id= horaire.id
                        break
                    else:
                        attendance.horaire_id = False

                if attendance.horaire_id:
                    # attendance.horaire_id=attendance.horaire_id.id
                    check_in_modified = None
                    check_out_modified = None
                    attendance.checkin_anomalie=""
                    attendance.checkout_anomalie=""
                    if attendance.checkin_corriged:
                        attendance.write({'pointage_est_corriger': True ,'check_in' : attendance.checkin_corriged})
                    if attendance.check_in:
                        check_in = datetime.strptime(attendance.check_in.strftime('%H:%M:%S'), '%H:%M:%S')# + timedelta(hours=1)
                        check_in_horaire = datetime.strptime(attendance.horaire_id.horaire_debut.strftime('%H:%M:%S'),'%H:%M:%S')# + timedelta(hours=1)
                        diff_in = (check_in-check_in_horaire).total_seconds()/60
                        if not attendance.checkin_corriged:
                            attendance.checkin_corriged = attendance.check_in
                        check_in_modified = attendance.check_in
                        if diff_in < -float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.marge_horaire')) * 3600:
                            attendance.checkin_anomalie= "chekin_before_time"
                        # if diff_in >= float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.marge_horaire')) * 3600:
                        #     attendance.checkin_anomalie= "late"
                        if diff_in >= 0 and diff_in <= float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.retard_time')) * 60:
                            attendance.checkin_anomalie = "normal"
                        # if diff_in > float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.retard_time')) * 60 and diff_in < float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.marge_horaire')) * 3600:
                        #     attendance.checkin_anomalie = "late"
                        if diff_in < 0 and diff_in>=-float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.marge_horaire')) * 3600:
                            if attendance.check_in!=attendance.horaire_id.horaire_debut:
                                check_in_modified= datetime.strptime(attendance.check_in.strftime('%Y-%m-%d') + " " + attendance.horaire_id.horaire_debut.strftime('%H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                            attendance.checkin_anomalie= "chekin_before_time"
                    if attendance.check_out:
                        horaire_j_plus_1 = True
                        if datetime.strptime(attendance.horaire_id.horaire_fin.strftime('%Y-%m-%d'),'%Y-%m-%d') == datetime.strptime(attendance.horaire_id.horaire_debut.strftime('%Y-%m-%d'), '%Y-%m-%d'):
                            horaire_j_plus_1 =False
                        if not horaire_j_plus_1:
                            check_out_horaire = datetime.strptime(attendance.check_in.strftime('%Y-%m-%d') + " " + attendance.horaire_id.horaire_fin.strftime('%H:%M:%S'),'%Y-%m-%d %H:%M:%S')# + timedelta(hours=1)
                        else:
                            day_out_horaire = datetime.strptime(attendance.check_in.strftime('%Y-%m-%d'),'%Y-%m-%d') + timedelta(days=1)
                            check_out_horaire = datetime.strptime(day_out_horaire.strftime('%Y-%m-%d') + " " + attendance.horaire_id.horaire_fin.strftime('%H:%M:%S'),'%Y-%m-%d %H:%M:%S')# + timedelta(hours=1)
                        check_out = datetime.strptime(attendance.check_out.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S') #+ timedelta(hours=1)
                        diff_out = (check_out-check_out_horaire).total_seconds()/60
                        if not attendance.checkout_corriged:
                            attendance.checkout_corriged = attendance.check_out
                        check_out_modified = attendance.check_out
                        if diff_out<0:
                            attendance.checkout_anomalie= "chekout_before_time"
                        if diff_out==0:
                            attendance.checkout_anomalie= "normal"
                        if diff_out>0 and diff_out<=float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.marge_horaire')) * 3600:
                            attendance.checkout_anomalie= "chekout_after_time"
                            if not horaire_j_plus_1:
                                check_out_modified= datetime.strptime(attendance.check_out.strftime('%Y-%m-%d') + " " + attendance.horaire_id.horaire_fin.strftime('%H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                            else:
                                day_out = datetime.strptime(attendance.check_in.strftime('%Y-%m-%d'),'%Y-%m-%d') + timedelta(days=1)
                                check_out_modified = datetime.strptime(day_out.strftime('%Y-%m-%d') + " " + attendance.horaire_id.horaire_fin.strftime('%H:%M:%S'),'%Y-%m-%d %H:%M:%S')
                        if diff_out>float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.marge_horaire')) * 3600:
                            attendance.checkout_anomalie= "chekout_after_time"
                    if check_in_modified and check_out_modified:
                        attendance.write({'pointage_est_corriger': True ,'check_in' : check_in_modified})
                else:
                    attendance.horaire_id = False
                    # attendance.checkin_corriged = False
                    # attendance.checkout_corriged = False
                    attendance.checkin_anomalie = False
                    attendance.checkout_anomalie = False
            # else:
            #     # print('absence----------------!!!!')
            #     attendance.checkin_anomalie = "absence"
            #     attendance.checkout_anomalie = "absence"
            attendance._compute_worked_hours()

    def action_server_appliquer_horaire_one(self):
        horairess = self.env['cps.hr.horaire'].search([])
        horaires = []

        # for attendance in self.attendance_ids:
        for attendance in self.env['hr.attendance'].search([('id', '=', self.id)]):

            attendance._compute_worked_hours()

            if attendance.worked_hours>0:
                for horaire in horairess:
                    for date in horaire.dates:
                        if attendance.check_in >= date.date_debut and attendance.check_out <= date.date_fin:
                            horaires.append(horaire)

                if len(horaires) == 0:
                    attendance.horaire_id = False

                for horaire in horaires:
                    check_in = datetime.strptime(attendance.checkin_corriged.strftime('%H:%M:%S'),
                                                 '%H:%M:%S') if attendance.checkin_corriged else datetime.strptime(
                        attendance.check_in.strftime('%H:%M:%S'), '%H:%M:%S')
                    check_in_horaire = datetime.strptime(horaire.horaire_debut.strftime('%H:%M:%S'), '%H:%M:%S')
                    check_out = datetime.strptime(attendance.checkout_corriged.strftime('%H:%M:%S'),
                                                  '%H:%M:%S') if attendance.checkout_corriged else datetime.strptime(
                        attendance.check_out.strftime('%H:%M:%S'), '%H:%M:%S')
                    check_out_horaire = datetime.strptime(horaire.horaire_fin.strftime('%H:%M:%S'),'%H:%M:%S')
                    if ((check_in-check_in_horaire).total_seconds()>-float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.marge_horaire')) * 3600 and (check_in-check_in_horaire).total_seconds()<float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.marge_horaire')) * 3600):
                        attendance.horaire_id= horaire.id
                        break
                    else:
                        attendance.horaire_id = False

                if attendance.horaire_id:
                    # attendance.horaire_id=attendance.horaire_id.id
                    check_in_modified = None
                    check_out_modified = None
                    attendance.checkin_anomalie=""
                    attendance.checkout_anomalie=""
                    if attendance.checkin_corriged:
                        attendance.write({'pointage_est_corriger': True ,'check_in' : attendance.checkin_corriged})
                    if attendance.check_in:
                        check_in = datetime.strptime(attendance.check_in.strftime('%H:%M:%S'), '%H:%M:%S')# + timedelta(hours=1)
                        check_in_horaire = datetime.strptime(attendance.horaire_id.horaire_debut.strftime('%H:%M:%S'),'%H:%M:%S')# + timedelta(hours=1)
                        diff_in = (check_in-check_in_horaire).total_seconds()/60
                        if not attendance.checkin_corriged:
                            attendance.checkin_corriged = attendance.check_in
                        check_in_modified = attendance.check_in
                        if diff_in < -float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.marge_horaire')) * 3600:
                            attendance.checkin_anomalie= "chekin_before_time"
                        # if diff_in >= float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.marge_horaire')) * 3600:
                        #     attendance.checkin_anomalie= "late"
                        if diff_in >= 0 and diff_in <= float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.retard_time')) * 60:
                            attendance.checkin_anomalie = "normal"
                        # if diff_in > float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.retard_time')) * 60 and diff_in < float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.marge_horaire')) * 3600:
                        #     attendance.checkin_anomalie = "late"
                        if diff_in < 0 and diff_in>=-float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.marge_horaire')) * 3600:
                            if attendance.check_in!=attendance.horaire_id.horaire_debut:
                                check_in_modified= datetime.strptime(attendance.check_in.strftime('%Y-%m-%d') + " " + attendance.horaire_id.horaire_debut.strftime('%H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                            attendance.checkin_anomalie= "chekin_before_time"
                    if attendance.check_out:
                        horaire_j_plus_1 = True
                        if datetime.strptime(attendance.horaire_id.horaire_fin.strftime('%Y-%m-%d'),'%Y-%m-%d') == datetime.strptime(attendance.horaire_id.horaire_debut.strftime('%Y-%m-%d'), '%Y-%m-%d'):
                            horaire_j_plus_1 =False
                        if not horaire_j_plus_1:
                            check_out_horaire = datetime.strptime(attendance.check_in.strftime('%Y-%m-%d') + " " + attendance.horaire_id.horaire_fin.strftime('%H:%M:%S'),'%Y-%m-%d %H:%M:%S')# + timedelta(hours=1)
                        else:
                            day_out_horaire = datetime.strptime(attendance.check_in.strftime('%Y-%m-%d'),'%Y-%m-%d') + timedelta(days=1)
                            check_out_horaire = datetime.strptime(day_out_horaire.strftime('%Y-%m-%d') + " " + attendance.horaire_id.horaire_fin.strftime('%H:%M:%S'),'%Y-%m-%d %H:%M:%S')# + timedelta(hours=1)
                        check_out = datetime.strptime(attendance.check_out.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S') #+ timedelta(hours=1)
                        diff_out = (check_out-check_out_horaire).total_seconds()/60
                        if not attendance.checkout_corriged:
                            attendance.checkout_corriged = attendance.check_out
                        check_out_modified = attendance.check_out
                        if diff_out<0:
                            attendance.checkout_anomalie= "chekout_before_time"
                            # self.mail_sortie_anomalie(attendance.employee_id, attendance.check_out)
                        if diff_out==0:
                            attendance.checkout_anomalie= "normal"
                        if diff_out>0 and diff_out<=float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.marge_horaire')) * 3600:
                            attendance.checkout_anomalie= "chekout_after_time"

                            if not horaire_j_plus_1:
                                check_out_modified= datetime.strptime(attendance.check_out.strftime('%Y-%m-%d') + " " + attendance.horaire_id.horaire_fin.strftime('%H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                            else:
                                day_out = datetime.strptime(attendance.check_in.strftime('%Y-%m-%d'),'%Y-%m-%d') + timedelta(days=1)
                                check_out_modified = datetime.strptime(day_out.strftime('%Y-%m-%d') + " " + attendance.horaire_id.horaire_fin.strftime('%H:%M:%S'),'%Y-%m-%d %H:%M:%S')
                        if diff_out>float(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.marge_horaire')) * 3600:
                            attendance.checkout_anomalie= "chekout_after_time"

                    if check_in_modified and check_out_modified:
                        attendance.write({'pointage_est_corriger': True ,'check_in' : check_in_modified})
                else:
                    attendance.horaire_id = False
                    # attendance.checkin_corriged = False
                    # attendance.checkout_corriged = False
                    attendance.checkin_anomalie = False
                    attendance.checkout_anomalie = False
            # else:
            #     # print('absence----------------!!!!')
            #     attendance.checkin_anomalie = "absence"
            #     attendance.checkout_anomalie = "absence"
            attendance._compute_worked_hours()

    def remove_pointage(self):
        self.unlink()