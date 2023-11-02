# # -*- coding: utf-8 -*-
import base64
from odoo.tools.float_utils import float_compare
from odoo import models, fields, api, exceptions, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import date, datetime, timedelta
from odoo.exceptions import UserError, ValidationError
import json
from dateutil.relativedelta import relativedelta
from odoo.addons.resource.models.resource_mixin import timezone_datetime
from collections import defaultdict
from pytz import timezone, UTC


class CpsHrLeave(models.Model):
    _name = 'cps.hr.leave'
    _rec_name = 'date_absence'

    date_absence = fields.Date('Journée Absence')
    # equipe = fields.Selection([('A', 'A'), ('B', 'B'), ('FM', 'FM'), ('FA', 'FA')], string='Equipe salarié')
    leave_lines = fields.One2many('cps.hr.leave.line', 'leave_id', string="Employee")
    state = fields.Selection(
        selection=[("draft", "Brouillon"), ("valide", "Valider")],
        string="Status",
        default="draft",
        readonly=True,
    )

    def action_filter_attendances(self):
        self.leave_lines = False
        # if self.equipe != False:
        #     employees = self.env['hr.employee'].search([('equipe', '=', self.equipe)])
        # else:
        employees = self.env['hr.employee'].search([('sans_pointage', '=', False)])

        colis = []
        for employee in employees:
            trouve = False
            for attendance in employee.attendance_ids.filtered(
                    lambda a: a.check_in.strftime('%Y-%m-%d') == self.date_absence.strftime('%Y-%m-%d')):
                print('Mat', employee.matricule, '  pointage--------------------', attendance.check_in)
                trouve = True
            if trouve == False:
                count = len(self.env['hr.leave'].search(
                    [('date_from', '<=', self.date_absence), ('date_to', '>=', self.date_absence),
                     ('employee_id', '=', employee.id), ('state', '=', 'validate')]))
                if count == 0:
                    colis.append((0, 0, {'leave_id': self.id, 'employee_id': employee.id}))
        self.leave_lines = colis

    def action_valider_absence(self):
        for leave_line in self.leave_lines:
            if len(leave_line.leave_type) > 0:
                leave = self.env['hr.leave'].create({
                    'holiday_type': 'employee',
                    'employee_id': leave_line.employee_id.id,
                    'request_date_from': self.date_absence,
                    'request_date_to': self.date_absence,
                    'date_from': self.date_absence,
                    'date_to': self.date_absence,
                    # 'request_hour_from': str(leave_line.horaire_id.horaire_debut.hour + 1),
                    # 'request_hour_to': str(leave_line.horaire_id.horaire_fin.hour + 1),
                    # 'date_from': str(self.date_absence.strftime('%Y-%m-%d')) + " " + str(
                    #     leave_line.horaire_id.horaire_debut.strftime('%H:%M:%S')),
                    # 'date_to': str(self.date_absence.strftime('%Y-%m-%d')) + " " + str(
                    #     leave_line.horaire_id.horaire_fin.strftime('%H:%M:%S')),
                    'request_unit_hours': False,
                    'number_of_days': 1,
                    'holiday_status_id': leave_line.leave_type.id,
                    'cps_hr_leave_id': self.id
                })
                leave.action_approve()
                leave.action_validate()
        self.state = 'valide'


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    # holiday_status_id = fields.Many2one(
    #     "hr.leave.type", string="Time Off Type", required=True, readonly=True,
    #     states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]},
    #     domain=[('valid', '=', True)])

    # moyens_transport_id = fields.Many2one("dh.moyen.transport",string="Mean of Transport")



    rest_leave = fields.Float(string='jours restants', compute='_get_rest_leave')

    # @api.depends('holiday_status_id','employee_id','number_of_days')
    # def _get_rest_leave(self):
    #
    #     for p in self:
    #         p.rest_leave = False
    #         for rec in self.env['hr.leave'].filtered(lambda x:x.holiday_status_id.allocation_type != 'no'):
    #
    #             print('rr')
    #             for line in self.env.env['hr.leave.allocation'].filtered(lambda x:x.employee_id.id == rec.employee_id.id and x.holiday_status_id.id == rec.holiday_status_id.id ):
    #                 if line.number_of_days_display and rec.number_of_days:
    #                     rec.rest_leave = line.number_of_days_display - rec.number_of_days
    #                     print('test1',line.number_of_days_display)
    #                     print('test2',rec.number_of_days)

    @api.depends('holiday_status_id', 'employee_id', 'number_of_days', 'state')
    def _get_rest_leave(self):
        for rec in self:
            rec.rest_leave = 0
            if rec.holiday_status_id.allocation_type != 'no':
                # if rec.request_date_from.year == fields.Date.today().year:


                rec.rest_leave = sum(self.env['hr.leave.allocation'].search(
                        [('state', '=', 'validate'), ('employee_id', '=', rec.employee_id.id),
                         ('holiday_status_id', '=', rec.holiday_status_id.id)]).filtered(
                        lambda r: r.holiday_status_id.validity_start.year == fields.Date.today().year or r.holiday_status_id.validity_start.year ==  fields.Date.today().year -1 or r.holiday_status_id.validity_start == False).mapped(
                        'number_of_days_display'))- sum(self.env['hr.leave'].search(
                        [('state', '=', 'validate'), ('employee_id', '=', rec.employee_id.id),
                         ('holiday_status_id', '=', rec.holiday_status_id.id)]).filtered(
                        lambda r: r.request_date_from.year == fields.Date.today().year or r.request_date_from.year ==  fields.Date.today().year -1).mapped(
                        'number_of_days_display'))
                print("rest_leave", rec.rest_leave)


    cps_hr_leave_id = fields.Many2one('cps.hr.leave', string='cps hr leave')

    # def mail_unjusify_abscence_gestionnaire(self):
    #     abscence_non_just = []
    #     for rec in self.env['hr.leave'].search([]).filtered(lambda x:x.holiday_status_id.unpaid == True):
    #         template_id = self.env.ref('cps_icesco.mail_unjusify_abscence_gestionnaire')  # xml id of your email template
    #         template_id.email_to = rec.employee_id.parent_id.work_email
    #         template_id.reply_to = rec.employee_id.parent_id.work_email
    #         template_id.email_from = 'it@icesco.org'
    #         template_context = {
    #             'name': rec.employee_id.name,
    #             'prenom': rec.employee_id.prenom,
    #             'heure': rec.cps_hr_leave_id.date_absence,
    #         }
    #         template_id.with_context(**template_context).send_mail(self.id, force_send=True)
    #         abscence_non_just.append(rec)
    # def mail_unjusify_abscence_employees(self):
    #     employee_abscence = []
    #     for rec in self.env['hr.leave'].search([]).filtered(lambda x:x.holiday_status_id.unpaid == True):
    #         template_id = self.env.ref('cps_icesco.mail_unjusify_abscence_employees')  # xml id of your email template
    #         template_id.email_to = rec.employee_id.work_email
    #         template_id.reply_to = rec.employee_id.work_email
    #         template_id.email_from = 'rh@icesco.org'
    #         template_context = {
    #             'name': rec.employee_id.name,
    #             'prenom': rec.employee_id.prenom,
    #             'heure': rec.cps_hr_leave_id.date_absence,
    #         }
    #         template_id.with_context(**template_context).send_mail(self.id, force_send=True)
    #         employee_abscence.append(rec)
    #     for employee in employee_abscence:
    #         template_id = self.env.ref('cps_icesco.mail_unjusify_abscence_gestionnaire')  # xml id of your email template
    #         template_id.email_to = employee.employee_id.parent_id.work_email
    #         template_id.reply_to = employee.employee_id.parent_id.work_email
    #         template_id.email_from = 'rh@icesco.org'
    #         template_context = {
    #             'name': employee.employee_id.name,
    #             'prenom': employee.employee_id.prenom,
    #             'heure': employee.cps_hr_leave_id.date_absence,
    #         }
    #         template_id.with_context(**template_context).send_mail(self.id, force_send=True)

    def get_by_manager(self, vals, expId):
        # return next(x for x in vals if x['manager_id'] == expId)
        return [d for d in vals if d["manager_id"] == expId]

    def mail_unjusify_abscence_employees(self):
        employee_abscence = []
        employee_abscence_time = []
        managers = []
        for rec in self.env['hr.leave'].search([]).filtered(
                lambda x: x.holiday_status_id.unpaid == True and x.date_from.date() <= date.today() and x.date_to.date() >= date.today()):
            template_id = self.env.ref('cps_icesco.mail_unjusify_abscence_employees')  # xml id of your email template
            template_id.email_to = rec.employee_id.work_email
            template_id.reply_to = rec.employee_id.work_email
            template_id.email_from = 'rh@icesco.org'
            template_context = {
                'name': rec.employee_id.name,
                'prenom': rec.employee_id.prenom,
                'date': date.today(),
                'start_day': rec.date_from.date(),
                'end_day': rec.date_to.date(),
                # 'retard_time': rec.check_in - selected_horaire.horaire_debut if selected_horaire else 0
            }
            template_id.with_context(**template_context).send_mail(self.id, force_send=True)
            # template_id.send_mail(self.id, force_send=True)
            employee_abscence.append(rec.employee_id)
            employee_abscence_time.append(
                {'manager_id': rec.employee_id.parent_id, 'leave': rec, 'date_from': rec.date_from.date(),
                 'date_to': rec.date_to.date(), 'employee': rec.employee_id})

        for emp in employee_abscence:
            if emp.parent_id not in managers:
                managers.append(emp.parent_id)

        for manager in managers:
            template_id = self.env.ref(
                'cps_icesco.mail_unjusify_abscence_gestionnaire')  # xml id of your email template
            template_id.email_to = manager.work_email
            template_id.reply_to = manager.work_email
            template_id.email_from = 'rh@icesco.org'
            template_context = {
                # 'name': manager.name,
                # 'prenom': manager.prenom,
                'date': date.today(),
                'employee_abscence': self.get_by_manager(employee_abscence_time, manager)
            }
            template_id.with_context(**template_context).send_mail(self.id, force_send=True)

    @api.constrains('holiday_status_id', 'request_date_from', 'request_date_to')
    def check_conge_urgent(self):
        for rec in self:
            if rec.holiday_status_id.is_urgent == True:
                if rec.number_of_days > 2:
                    raise UserError(_('You cannot operate more than 2 days in a single urgent leave.'))

                time_offs_urgent = self.env['hr.leave'].search(
                    [('id', '!=', rec.id), ('employee_id', '=', rec.employee_id.id),
                     ('state', 'not in', ['cancel', 'refuse'])]).filtered(
                    lambda x: x.holiday_status_id.is_urgent == True)  # ('state', '=', 'validate')

                time_offs_urgent_fusion = self.env['hr.leave'].search(
                    [('id', '!=', rec.id), ('employee_id', '=', rec.employee_id.id),
                     ('state', 'not in', ['cancel', 'refuse']), ('number_of_days', '=', 2)]).filtered(
                    lambda x: x.holiday_status_id.is_urgent == True and  x.date_from >= datetime(rec.date_from.year , 1, 1) and x.date_to <= datetime(
                                rec.date_to.year, 12, 31))

                time_offs_urgent_current_year = time_offs_urgent.filtered(
                    lambda x: datetime(date.today().year, 12, 31) >= x.date_from >= datetime(
                        date.today().year, 1, 1) or datetime(date.today().year, 1, 1) <= x.date_to <= datetime(
                        date.today().year, 12, 31))

                time_offs_day_before = self.env['hr.leave'].search(
                    [('id', '!=', rec.id), ('employee_id', '=', rec.employee_id.id),
                     ('state', 'not in', ['cancel', 'refuse'])]).filtered(
                    lambda x: x.date_from.date() <= rec.date_from.date() - timedelta(
                        days=1) and x.date_to.date() >= rec.date_from.date() - timedelta(days=1) and x.holiday_status_id.payed == True)

                time_offs_day_after = self.env['hr.leave'].search(
                    [('id', '!=', rec.id), ('employee_id', '=', rec.employee_id.id),
                     ('state', 'not in', ['cancel', 'refuse'])]).filtered(
                    lambda x: x.date_from.date() <= rec.date_to.date() + timedelta(
                        days=1) and x.date_to.date() >= rec.date_to.date() + timedelta(days=1) and x.holiday_status_id.payed == True)

                if len(time_offs_day_before) > 0 or len(time_offs_day_after) > 0:
                    raise ValidationError(
                        "Il n'est pas possible de combiner un congé d'urgence avec un congé prévu à l'avance.")

                if rec.number_of_days == 2:
                    if len(time_offs_urgent_fusion) == 1:
                        raise UserError(_('You have the right to merge 2 days only once a year.'))

                if time_offs_urgent_current_year:
                    if sum(time_offs_urgent_current_year.mapped('number_of_days')) >= 7:
                        raise UserError(_('The employee has exceeded 7 urgent leave days in the current year.'))
            else:
                if rec.holiday_status_id.payed == True:
                    time_offs_day_before = self.env['hr.leave'].search(
                        [('id', '!=', rec.id), ('employee_id', '=', rec.employee_id.id),
                         ('state', 'not in', ['cancel', 'refuse'])]).filtered(
                        lambda x: x.date_from.date() <= rec.date_from.date() - timedelta(
                            days=1) and x.date_to.date() >= rec.date_from.date() - timedelta(days=1) and x.holiday_status_id.is_urgent == True)

                    time_offs_day_after = self.env['hr.leave'].search(
                        [('id', '!=', rec.id), ('employee_id', '=', rec.employee_id.id),
                         ('state', 'not in', ['cancel', 'refuse'])]).filtered(
                        lambda x: x.date_from.date() <= rec.date_to.date() + timedelta(
                            days=1) and x.date_to.date() >= rec.date_to.date() + timedelta(days=1) and x.holiday_status_id.is_urgent == True)

                    if len(time_offs_day_before) > 0 or len(time_offs_day_after) > 0:
                        raise ValidationError(
                            "Il n'est pas possible de combiner un congé avec un congé d'urgence prévu à l'avance.")

    def activity_update(self):
        to_clean, to_do = self.env['hr.leave'], self.env['hr.leave']
        for holiday in self:
            start = UTC.localize(holiday.date_from).astimezone(timezone(holiday.employee_id.tz or 'UTC'))
            end = UTC.localize(holiday.date_to).astimezone(timezone(holiday.employee_id.tz or 'UTC'))
            note = _('New %s Request created by %s from %s to %s') % (
            holiday.holiday_status_id.name, holiday.create_uid.name, start, end)
            if holiday.state == 'draft':
                to_clean |= holiday

            # d'aprés icesco -> ne pas envoiyer mail dans la création de congé
            # elif holiday.state == 'confirm':
            #     holiday.activity_schedule(
            #         'hr_holidays.mail_act_leave_approval',
            #         note=note,
            #         user_id=holiday.sudo()._get_responsible_for_approval().id or self.env.user.id)
            #
            #     # sent email to employee (mehdi)
            #     context = self._context
            #     current_uid = context.get('uid')
            #     user_id = self.env['res.users'].sudo().browse(current_uid)
            #
            #     # responsable type de congé
            #     responsable_email_to = holiday.holiday_status_id.responsible_id.partner_id.email
            #
            #     # employee de congé
            #     employee_email_to = holiday.employee_id.work_email
            #
            #     template_id = self.env['ir.model.data'].get_object_reference('cps_icesco',
            #                                                                  'email_template_confirme')[
            #         1]
            #     email_template_obj = self.env['mail.template'].browse(template_id)
            #     if template_id:
            #         # to responsible
            #         values = email_template_obj.generate_email(self.id, fields=None)
            #         values['email_from'] = user_id.partner_id.email
            #         values['email_to'] = responsable_email_to
            #         values['author_id'] = user_id.partner_id.id
            #         values['res_id'] = False  # self.res_id
            #         values['model'] = False  # self.res_model
            #         mail_mail_obj = self.env['mail.mail']
            #         msg_id = mail_mail_obj.create(values)
            #         if msg_id:
            #             mail_mail_obj.send([msg_id])
            #             msg_id.sudo().send()
            #
            #         # to employee
            #         values = email_template_obj.generate_email(self.id, fields=None)
            #         values['email_from'] = user_id.partner_id.email
            #         values['email_to'] = employee_email_to
            #         values['author_id'] = user_id.partner_id.id
            #         values['res_id'] = False  # self.res_id
            #         values['model'] = False  # self.res_model
            #         mail_mail_obj = self.env['mail.mail']
            #         msg_id = mail_mail_obj.create(values)
            #         if msg_id:
            #             mail_mail_obj.send([msg_id])
            #             msg_id.sudo().send()

            # elif holiday.state == 'validate1':
            #     holiday.activity_feedback(['hr_holidays.mail_act_leave_approval'])
            #     holiday.activity_schedule(
            #         'hr_holidays.mail_act_leave_second_approval',
            #         note=note,
            #         user_id=holiday.sudo()._get_responsible_for_approval().id or self.env.user.id)
            #
            #     # sent email to employee (mehdi)
            #     context = self._context
            #     current_uid = context.get('uid')
            #     user_id = self.env['res.users'].sudo().browse(current_uid)
            #
            #     # responsable type de congé
            #     responsable_email_to = holiday.holiday_status_id.responsible_id.partner_id.email
            #
            #     # employee de congé
            #     employee_email_to = holiday.employee_id.work_email
            #
            #     template_id = self.env['ir.model.data'].get_object_reference('cps_icesco',
            #                                                                  'email_template_validate1')[
            #         1]
            #     email_template_obj = self.env['mail.template'].browse(template_id)
            #     if template_id and holiday.holiday_status_id.is_urgent == False and holiday.holiday_status_id.payed == True:
            #         # to responsible
            #         values = email_template_obj.generate_email(self.id, fields=None)
            #         values['email_from'] = user_id.partner_id.email
            #         values['email_to'] = responsable_email_to
            #         values['author_id'] = user_id.partner_id.id
            #         values['res_id'] = False  # self.res_id
            #         values['model'] = False  # self.res_model
            #         mail_mail_obj = self.env['mail.mail']
            #         msg_id = mail_mail_obj.create(values)
            #         if msg_id:
            #             mail_mail_obj.send([msg_id])
            #             msg_id.sudo().send()
            #
            #         # to employee
            #         if employee_email_to:
            #             values = email_template_obj.generate_email(self.id, fields=None)
            #             values['email_from'] = user_id.partner_id.email
            #             values['email_to'] = employee_email_to
            #             values['author_id'] = user_id.partner_id.id
            #             values['res_id'] = False  # self.res_id
            #             values['model'] = False  # self.res_model
            #             mail_mail_obj = self.env['mail.mail']
            #             msg_id = mail_mail_obj.create(values)
            #             if msg_id:
            #                 mail_mail_obj.send([msg_id])
            #                 msg_id.sudo().send()
            #
            #         # to manager
            #         values = email_template_obj.generate_email(self.id, fields=None)
            #         values['email_from'] = user_id.partner_id.email
            #         values['email_to'] = 'nabuzuhri@icesco.org'
            #         values['author_id'] = user_id.partner_id.id
            #         values['res_id'] = False  # self.res_id
            #         values['model'] = False  # self.res_model
            #         mail_mail_obj = self.env['mail.mail']
            #         msg_id = mail_mail_obj.create(values)
            #         if msg_id:
            #             mail_mail_obj.send([msg_id])
            #             msg_id.sudo().send()
            #
            #         # to hr
            #         values = email_template_obj.generate_email(self.id, fields=None)
            #         values['email_from'] = user_id.partner_id.email
            #         values['email_to'] = 'rh@icesco.org'
            #         values['author_id'] = user_id.partner_id.id
            #         values['res_id'] = False  # self.res_id
            #         values['model'] = False  # self.res_model
            #         mail_mail_obj = self.env['mail.mail']
            #         msg_id = mail_mail_obj.create(values)
            #         if msg_id:
            #             mail_mail_obj.send([msg_id])
            #             msg_id.sudo().send()

            if holiday.state == 'validate':
                to_do |= holiday

                # sent email to employee (mehdi)
                context = self._context
                current_uid = context.get('uid')
                user_id = self.env['res.users'].sudo().browse(current_uid)

                # responsable type de congé
                responsable_email_to = holiday.holiday_status_id.responsible_id.partner_id.email

                # employee de congé
                employee_email_to = holiday.employee_id.work_email

                template_id = self.env['ir.model.data'].get_object_reference('cps_icesco',
                                                                             'email_template_validate')[
                    1]
                email_template_obj = self.env['mail.template'].browse(template_id)
                if template_id and holiday.holiday_status_id.is_urgent == False and holiday.holiday_status_id.payed == True:
                    # for rec in self.env['hr.leave'].browse(self._context.get('active_ids', [])):
                    content, content_type = self.env.ref('cps_icesco.dh_report_leaves').render_qweb_pdf(
                        self.id)
                    leave_infos = self.env['ir.attachment'].create({
                        'name': 'leave %s.pdf' % self.name,
                        'type': 'binary',
                        'datas': base64.encodestring(content),
                        'res_model': 'hr.leave',
                        'res_id': self.id,
                        'mimetype': 'application/x-pdf'
                    })
                    # # to responsible
                    # values = email_template_obj.generate_email(self.id, fields=None)
                    #
                    # values['email_from'] = user_id.partner_id.email
                    # values['email_from'] = user_id.partner_id.email
                    # values['email_to'] = responsable_email_to
                    # values['email_cc'] = 'rh@icesco.org'
                    #
                    # values['author_id'] = user_id.partner_id.id
                    # values['res_id'] = False  # self.res_id
                    # values['model'] = False  # self.res_model
                    # values['attachment_ids'] = [(4, leave_infos.id)]  # self.res_model
                    # mail_mail_obj = self.env['mail.mail']
                    # msg_id = mail_mail_obj.create(values)
                    # if msg_id:
                    #     mail_mail_obj.send([msg_id])
                    #     msg_id.sudo().send()

                    # to employee
                    if employee_email_to:
                        values = email_template_obj.generate_email(self.id, fields=None)
                        values['email_from'] = user_id.partner_id.email
                        values['email_to'] = employee_email_to
                        values['author_id'] = user_id.partner_id.id
                        values['res_id'] = False  # self.res_id
                        values['model'] = False  # self.res_model
                        values['attachment_ids'] = [(4, leave_infos.id)]
                        mail_mail_obj = self.env['mail.mail']
                        msg_id = mail_mail_obj.create(values)
                        if msg_id:
                            mail_mail_obj.send([msg_id])
                            msg_id.sudo().send()

                    # # to manager
                    # values = email_template_obj.generate_email(self.id, fields=None)
                    #
                    # values['email_from'] = user_id.partner_id.email
                    # values['email_from'] = user_id.partner_id.email
                    # values['email_to'] = 'nabuzuhri@icesco.org'
                    # values['author_id'] = user_id.partner_id.id
                    # values['res_id'] = False  # self.res_id
                    # values['model'] = False  # self.res_model
                    # values['attachment_ids'] = [(4, leave_infos.id)]  # self.res_model
                    # mail_mail_obj = self.env['mail.mail']
                    # msg_id = mail_mail_obj.create(values)
                    # if msg_id:
                    #     mail_mail_obj.send([msg_id])
                    #     msg_id.sudo().send()

                    # to hr
                    values = email_template_obj.generate_email(self.id, fields=None)
                    values['email_from'] = user_id.partner_id.email
                    values['email_to'] = 'rh@icesco.org'
                    values['author_id'] = user_id.partner_id.id
                    values['res_id'] = False  # self.res_id
                    values['model'] = False  # self.res_model
                    values['attachment_ids'] = [(4, leave_infos.id)]
                    mail_mail_obj = self.env['mail.mail']
                    msg_id = mail_mail_obj.create(values)
                    if msg_id:
                        mail_mail_obj.send([msg_id])
                        msg_id.sudo().send()

            # elif holiday.state == 'refuse':
            #     to_clean |= holiday
            #
            #     # sent email to employee (mehdi)
            #     context = self._context
            #     current_uid = context.get('uid')
            #     user_id = self.env['res.users'].sudo().browse(current_uid)
            #
            #     # responsable type de congé
            #     responsable_email_to = holiday.holiday_status_id.responsible_id.partner_id.email
            #
            #     # employee de congé
            #     employee_email_to = holiday.employee_id.work_email
            #
            #     template_id = self.env['ir.model.data'].get_object_reference('cps_icesco',
            #                                                                  'email_template_refuse')[
            #         1]
            #     email_template_obj = self.env['mail.template'].browse(template_id)
            #     if template_id and holiday.holiday_status_id.is_urgent == False and holiday.holiday_status_id.payed == True:
            #         # to responsible
            #         values = email_template_obj.generate_email(self.id, fields=None)
            #         values['email_from'] = user_id.partner_id.email
            #         values['email_to'] = responsable_email_to
            #         values['author_id'] = user_id.partner_id.id
            #         values['res_id'] = False  # self.res_id
            #         values['model'] = False  # self.res_model
            #         mail_mail_obj = self.env['mail.mail']
            #         msg_id = mail_mail_obj.create(values)
            #         if msg_id:
            #             mail_mail_obj.send([msg_id])
            #             msg_id.sudo().send()
            #
            #         # to employee
            #         if employee_email_to:
            #             values = email_template_obj.generate_email(self.id, fields=None)
            #             values['email_from'] = user_id.partner_id.email
            #             values['email_to'] = employee_email_to
            #             values['author_id'] = user_id.partner_id.id
            #             values['res_id'] = False  # self.res_id
            #             values['model'] = False  # self.res_model
            #             mail_mail_obj = self.env['mail.mail']
            #             msg_id = mail_mail_obj.create(values)
            #             if msg_id:
            #                 mail_mail_obj.send([msg_id])
            #                 msg_id.sudo().send()
            #
            #         # to manager
            #         values = email_template_obj.generate_email(self.id, fields=None)
            #         values['email_from'] = user_id.partner_id.email
            #         values['email_to'] = 'nabuzuhri@icesco.org'
            #         values['author_id'] = user_id.partner_id.id
            #         values['res_id'] = False  # self.res_id
            #         values['model'] = False  # self.res_model
            #         mail_mail_obj = self.env['mail.mail']
            #         msg_id = mail_mail_obj.create(values)
            #         if msg_id:
            #             mail_mail_obj.send([msg_id])
            #             msg_id.sudo().send()
            #
            #         # to hr
            #         values = email_template_obj.generate_email(self.id, fields=None)
            #         values['email_from'] = user_id.partner_id.email
            #         values['email_to'] = 'rh@icesco.org'
            #         values['author_id'] = user_id.partner_id.id
            #         values['res_id'] = False  # self.res_id
            #         values['model'] = False  # self.res_model
            #         mail_mail_obj = self.env['mail.mail']
            #         msg_id = mail_mail_obj.create(values)
            #         if msg_id:
            #             mail_mail_obj.send([msg_id])
            #             msg_id.sudo().send()
        if to_clean:
            to_clean.activity_unlink(
                ['hr_holidays.mail_act_leave_approval', 'hr_holidays.mail_act_leave_second_approval'])
        if to_do:
            to_do.activity_feedback(
                ['hr_holidays.mail_act_leave_approval', 'hr_holidays.mail_act_leave_second_approval'])

    def is_free_date(self, odoo_date):
        if odoo_date:
            dt = fields.Datetime.from_string(odoo_date)
            dt = fields.Date.to_string(dt.date())
            free_days = self.env['specific.holidays'].search([('end_date','>=', dt),('start_date','<=', dt)])
            if len(free_days)>0:
                return True
        return False

    def _get_number_of_days(self, date_from, date_to, employee_id):
        """ If an employee is currently working full time but requests a leave next month
            where he has a new contract working only 3 days/week. This should be taken into
            account when computing the number of days for the leave (2 weeks leave = 6 days).
            Override this method to get number of days according to the contract's calendar
            at the time of the leave.
        """
        days = super(HrLeave, self)._get_number_of_days(date_from, date_to, employee_id)
        if employee_id:
            delta = date_to - date_from
            free_day = 0
            for day in range(delta.days + 1):
                if self.is_free_date(date_from + timedelta(days=day)) == True:
                    free_day += 1

            if free_day > 0:
                employee = self.env['hr.employee'].browse(employee_id)
                return {'days': ((date_to - date_from).days + 1 - free_day), 'hours': ((date_to - date_from).days + 1 - free_day) * 8}
            else:
                if self.holiday_status_id.is_maternite == True or self.holiday_status_id.is_maladie == True:
                    employee = self.env['hr.employee'].browse(employee_id)
                    return {'days': ((date_to - date_from).days + 1), 'hours': ((date_to - date_from).days + 1) * 8}
                else:
                    employee = self.env['hr.employee'].browse(employee_id)
                    # Use sudo otherwise base users can't compute number of days
                    contracts = employee.sudo()._get_contracts(date_from, date_to, states=['open'])
                    contracts |= employee.sudo()._get_incoming_contracts(date_from, date_to)
                    calendar = contracts[
                               :1].resource_calendar_id if contracts else None  # Note: if len(contracts)>1, the leave creation will crash because of unicity constaint
                    return employee._get_work_days_data_batch(date_from, date_to, calendar=calendar)[employee.id]

        return days

    @api.onchange('date_from', 'date_to', 'employee_id', 'holiday_status_id')
    def _onchange_leave_dates(self):
        if self.date_from and self.date_to:
            self.number_of_days = self._get_number_of_days(self.date_from, self.date_to, self.employee_id.id)['days']
        else:
            self.number_of_days = 0


class DhHrAttandance1(models.Model):
    _inherit = 'hr.attendance'

    # cps_hr_leave_id = fields.Many2one('cps.hr.leave', string='cps hr leave')
    # def mail_unjusify_retard_gestionnaire(self):
    #     employee_retard = []
    #     for rec in self.env['hr.attendance'].search([]).filtered(lambda x:x.checkin_anomalie == 'late'):
    #         template_id = self.env.ref('cps_icesco.mail_unjusify_retard_gestionnaire')  # xml id of your email template
    #         template_id.email_to = rec.employee_id.parent_id.work_email
    #         template_id.reply_to = rec.employee_id.parent_id.work_email
    #         template_id.email_from = 'it@icesco.org'
    #         template_id.send_mail(self.id, force_send=True)
    #         employee_retard.append(rec)

    def mail_hours_number(self):
        list1 = []
        worked_hours = 0
        yesterday = (datetime.today() - timedelta(days=1)).date()
        day_f = ((datetime.today() - timedelta(days=3)).date()).strftime('%A')
        today = (datetime.today()).date()
        for rec in self.env['hr.attendance'].search([]).filtered(lambda x: x.check_in.date() == yesterday):
            if rec.checkin_corriged:
                day_w = (rec.checkin_corriged.date()).weekday()
                day = rec.checkin_corriged.date()
                check_in = rec.checkin_corriged
                if rec.checkout_corriged:
                    delta = rec.checkout_corriged - rec.checkin_corriged
                    worked_hours = delta.total_seconds() / 3600.0
                    if day_w in [0, 1, 2, 3]:
                        if worked_hours < 7:
                            list1.append({'employee': rec.employee_id, 'worked_hours': round(worked_hours, 2),
                                          'check_in': rec.checkin_corriged, 'check_out': rec.checkout_corriged})
                elif rec.check_out:
                    delta = rec.checkout_corriged - rec.check_out
                    worked_hours = delta.total_seconds() / 3600.0
                    if day_w in [0, 1, 2, 3]:
                        if worked_hours < 7:
                            list1.append({'employee': rec.employee_id, 'worked_hours': round(worked_hours, 2),
                                          'check_in': rec.checkin_corriged, 'check_out': rec.check_out})

            elif rec.check_in:
                day = rec.check_in.date()
                day_w = (rec.check_in.date()).weekday()
                check_in = rec.check_in

                if rec.checkout_corriged:
                    check_out = rec.checkout_corriged

                    delta = rec.checkout_corriged - rec.check_in
                    worked_hours = delta.total_seconds() / 3600.0
                    if day_w in [0, 1, 2, 3]:
                        if worked_hours < 7:
                            list1.append({'employee': rec.employee_id, 'worked_hours': round(worked_hours, 2),
                                          'check_in': rec.check_in, 'check_out': rec.checkout_corriged})

                elif rec.check_out:
                    check_out = rec.check_out

                    delta = rec.check_out - rec.check_in
                    worked_hours = delta.total_seconds() / 3600.0
                    if day_w in [0, 1, 2, 3]:
                        if worked_hours < 7:
                            list1.append({'employee': rec.employee_id, 'worked_hours': round(worked_hours, 2),
                                          'check_in': rec.check_in, 'check_out': rec.check_out})

            # if rec.checkout_corriged:
            #     delta = rec.checkout_corriged - rec.checkin_corriged
            #     worked_hours = delta.total_seconds() / 3600.0
            #     if rec.jour in ('Lundi', 'Mardi', 'Mercredi', 'Jeudi'):
            #         if worked_hours < 7:
            #             list1.append({'employee': rec.employee_id,'worked_hours': round(worked_hours, 2),'check_in':rec.checkin_corriged,'check_out':rec.checkout_corriged})
        if len(list1) > 0:
            template_id = self.env.ref('cps_icesco.mail_hours_number_model1')  # xml id of your email template
            template_id.email_to = 'rh@icesco.org'
            template_id.email_cc = 'nabuzuhri@icesco.org'

            template_id.reply_to = 'rh@icesco.org'
            template_id.email_from = 'it@icesco.org'
            template_context = {

                'name': rec.employee_id.name,
                'check_in': check_in,
                'check_out': check_out,
                'prenom': rec.employee_id.prenom,
                'worked_hours': worked_hours,
                'list1': list1,
                'day': day,

            }
            template_id.with_context(**template_context).send_mail(self.id, force_send=True)
            for line in list1:
                template_id = self.env.ref('cps_icesco.mail_hours_number_model12')  # xml id of your email template
                template_id.email_to = line['employee'].work_email
                template_id.email_cc = line['employee'].parent_id.work_email
                # template_id.email_to = line.employee.work_email
                # template_id.reply_to = line.employee.work_email
                template_id.email_from = 'it@icesco.org'
                template_context = {

                    # 'name': line.employee.name,
                    # 'check_in': rec.check_in,
                    # 'check_out': rec.check_out,
                    # 'prenom': line.employee.prenom,
                    # 'worked_hours': rec.worked_hours,
                    # 'list1': list1,
                    # 'day': rec.check_in.date(),

                }
                template_id.with_context(**template_context).send_mail(self.id, force_send=True)

    def mail_hours_number2(self):
        list2 = []
        worked_hours = 0

        today = (datetime.today()).date()
        this_month = datetime.today().strftime("%M")
        day_f = ((datetime.today() - timedelta(days=3)).date()).weekday()
        day_3 = ((datetime.today() - timedelta(days=3)).date())
        today = (datetime.today()).date()
        if day_f == 4:

            # for rec in self.env['hr.attendance'].search([]).filtered(lambda x: x.jour == 'Mercredi' and x.check_in.strftime("%M") == this_month):
            for rec in self.env['hr.attendance'].search([]).filtered(lambda x: x.check_in.date() == day_3):

                if rec.checkin_corriged:
                    day = rec.checkin_corriged.date()
                    check_in = rec.checkin_corriged

                    if rec.checkout_corriged:
                        delta = rec.checkout_corriged - rec.checkin_corriged
                        worked_hours = delta.total_seconds() / 3600.0
                        if worked_hours < 5:
                            list2.append({'employee': rec.employee_id, 'worked_hours': round(worked_hours, 2),
                                          'check_in': rec.checkin_corriged, 'check_out': rec.checkout_corriged})
                    elif rec.check_out:
                        delta = rec.checkout_corriged - rec.check_out
                        worked_hours = delta.total_seconds() / 3600.0
                        if worked_hours < 5:
                            list2.append({'employee': rec.employee_id, 'worked_hours': round(worked_hours, 2),
                                          'check_in': rec.checkin_corriged, 'check_out': rec.checkout_corriged})

                elif rec.check_in:
                    day = rec.check_in.date()
                    check_in = rec.check_in

                    if rec.checkout_corriged:
                        check_out = rec.checkout_corriged

                        delta = rec.checkout_corriged - rec.check_in
                        worked_hours = delta.total_seconds() / 3600.0

                        if worked_hours < 5:
                            list2.append({'employee': rec.employee_id, 'worked_hours': round(worked_hours, 2),
                                          'check_in': rec.checkin_corriged, 'check_out': rec.checkout_corriged})
                    elif rec.check_out:
                        check_out = rec.check_out
                        delta = rec.check_out - rec.check_in
                        worked_hours = delta.total_seconds() / 3600.0

                        if worked_hours < 5:
                            list2.append({'employee': rec.employee_id, 'worked_hours': round(worked_hours, 2),
                                          'check_in': rec.checkin_corriged, 'check_out': rec.checkout_corriged})

                if len(list2) > 0:
                    template_id = self.env.ref(
                        'cps_icesco.mail_hours_number_model2')  # xml id of your email template
                    template_id.email_to = 'rh@icesco.org'
                    template_id.reply_to = 'rh@icesco.org'
                    template_id.email_cc = 'nabuzuhri@icesco.org'
                    template_id.email_from = 'it@icesco.org'
                    template_context = {
                        'list2': list2,
                        'day': day,
                        'name': rec.employee_id.name,
                        'check_in': check_in,
                        'check_out': check_out,
                        'prenom': rec.employee_id.prenom,
                        'worked_hours': worked_hours,

                    }
                    template_id.with_context(**template_context).send_mail(self.id, force_send=True)
                    for line in list2:
                        template_id = self.env.ref('cps_icesco.mail_hours_number_model12')  # xml id of your email template
                        template_id.email_to = line['employee'].work_email
                        template_id.email_cc = line['employee'].parent_id.work_email

                        # template_id.email_to = line.employee.work_email
                        # template_id.reply_to = line.employee.work_email
                        template_id.email_from = 'it@icesco.org'
                        template_context = {

                            # 'name': line.employee.name,
                            # 'check_in': rec.check_in,
                            # 'check_out': rec.check_out,
                            # 'prenom': line.employee.prenom,
                            # 'worked_hours': rec.worked_hours,
                            # 'list1': list1,
                            # 'day': rec.check_in.date(),

                        }
                        template_id.with_context(**template_context).send_mail(self.id, force_send=True)
    def mail_sortie_anomalie(self, employee_id, action_date):

        template_id = self.env.ref('cps_icesco.mail_sortie_anomalie')  # xml id of your email template
        template_id.email_to = 'rh@icesco.org'
        template_id.reply_to = 'rh@icesco.org'
        template_id.email_from = 'it@icesco.org'
        template_context = {
            'matricule': employee_id.matricule,
            'employee': employee_id.name,
            'jour': action_date.date(),
        }
        template_id.with_context(**template_context).send_mail(employee_id.id, force_send=True)

    def get_by_manager(self, vals, expId):
        # return next(x for x in vals if x['manager_id'] == expId)
        return [d for d in vals if d["manager_id"] == expId]

    def mail_unjusify_retard_employees(self):
        employee_retard = []
        employee_retard_time = []
        managers = []
        yesterday = (datetime.today() - timedelta(days=1)).date()
        # print('0000', self.env['hr.attendance'].search([]).filtered(lambda x:x.checkin_anomalie == 'late' and x.check_in.date() == date.today()))
        for rec in self.env['hr.attendance'].search([]).filtered(
                lambda x: x.checkin_anomalie == 'late' and x.check_in.date() == date.today()):  # date.today()
            selected_horaire = False
            for horaire in self.env['cps.hr.horaire'].search([]).filtered(
                    lambda x: datetime.strptime(x.horaire_debut.strftime('%H:%M:%S'), '%H:%M:%S') <= datetime.strptime(
                            rec.check_in.strftime('%H:%M:%S'), '%H:%M:%S') and datetime.strptime(
                            x.horaire_fin.strftime('%H:%M:%S'), '%H:%M:%S') >= datetime.strptime(
                            rec.check_in.strftime('%H:%M:%S'), '%H:%M:%S')):
                if selected_horaire:
                    if (datetime.strptime(rec.check_in.strftime('%H:%M:%S'), '%H:%M:%S') - datetime.strptime(
                            horaire.horaire_debut.strftime('%H:%M:%S'), '%H:%M:%S')).total_seconds() / 3600 < (
                            datetime.strptime(rec.check_in.strftime('%H:%M:%S'), '%H:%M:%S') - datetime.strptime(
                            selected_horaire.horaire_debut.strftime('%H:%M:%S'), '%H:%M:%S')).total_seconds() / 3600:
                        selected_horaire = horaire
                else:
                    selected_horaire = horaire

            template_id = self.env.ref('cps_icesco.mail_retard_employees')  # xml id of your email template
            template_id.email_to = rec.employee_id.work_email
            template_id.reply_to = rec.employee_id.work_email
            template_id.email_from = 'rh@icesco.org'
            template_context = {
                'name': rec.employee_id.name,
                'prenom': rec.employee_id.prenom,
                'checkin': rec.check_in,
                'day': rec.check_in.date(),
                'retard_time': str(timedelta(hours=(datetime.strptime(rec.check_in.strftime('%H:%M:%S'),
                                                                      '%H:%M:%S') - datetime.strptime(
                    selected_horaire.horaire_debut.strftime('%H:%M:%S'),
                    '%H:%M:%S')).total_seconds() / 3600 if selected_horaire else 0))
            }
            template_id.with_context(**template_context).send_mail(self.id, force_send=True)
            # template_id.send_mail(self.id, force_send=True)
            employee_retard.append(rec.employee_id)
            employee_retard_time.append({'manager_id': rec.employee_id.parent_id, 'employee': rec.employee_id,
                                         'retard_time': str(timedelta(hours=(datetime.strptime(
                                             rec.check_in.strftime('%H:%M:%S'), '%H:%M:%S') - datetime.strptime(
                                             selected_horaire.horaire_debut.strftime('%H:%M:%S'),
                                             '%H:%M:%S')).total_seconds() / 3600 if selected_horaire else 0))})

        for emp in employee_retard:
            if emp.parent_id not in managers:
                managers.append(emp.parent_id)

        for manager in managers:
            template_id = self.env.ref('cps_icesco.mail_unjusify_retard_gestionnaire')  # xml id of your email template
            template_id.email_to = manager.work_email
            template_id.reply_to = manager.work_email
            template_id.email_from = 'rh@icesco.org'
            template_context = {
                # 'name': manager.name,
                # 'prenom': manager.prenom,
                'day': date.today(),
                'employees_retard': self.get_by_manager(employee_retard_time, manager)
            }
            template_id.with_context(**template_context).send_mail(self.id, force_send=True)

        # for employee in employee_retard:
        #     template_id = self.env.ref(
        #         'cps_icesco.mail_unjusify_retard_gestionnaire')  # xml id of your email template
        #     template_id.email_to = employee.parent_id.work_email
        #     template_id.reply_to = employee.parent_id.work_email
        #     template_id.email_from = 'rh@icesco.org'
        #     template_context = {
        #         'name': rec.name,
        #         'prenom': rec.prenom,
        #         'day': rec.check_in.date(),
        #     }
        #     template_id.with_context(**template_context).send_mail(self.id, force_send=True)

    def mail_hr_day_retard_employees(self):
        employee_retard_time = []
        managers = []

        for rec in self.env['hr.attendance'].search([]).filtered(
                lambda x: x.checkin_anomalie == 'late' and x.check_in.date() == date.today()):
            selected_horaire = False
            for horaire in self.env['cps.hr.horaire'].search([]).filtered(
                    lambda x: datetime.strptime(x.horaire_debut.strftime('%H:%M:%S'), '%H:%M:%S') <= datetime.strptime(
                            rec.check_in.strftime('%H:%M:%S'), '%H:%M:%S') and datetime.strptime(
                            x.horaire_fin.strftime('%H:%M:%S'), '%H:%M:%S') >= datetime.strptime(
                            rec.check_in.strftime('%H:%M:%S'), '%H:%M:%S')):
                if selected_horaire:
                    if (datetime.strptime(rec.check_in.strftime('%H:%M:%S'), '%H:%M:%S') - datetime.strptime(
                            horaire.horaire_debut.strftime('%H:%M:%S'), '%H:%M:%S')).total_seconds() / 3600 < (
                            datetime.strptime(rec.check_in.strftime('%H:%M:%S'), '%H:%M:%S') - datetime.strptime(
                            selected_horaire.horaire_debut.strftime('%H:%M:%S'), '%H:%M:%S')).total_seconds() / 3600:
                        selected_horaire = horaire
                else:
                    selected_horaire = horaire

            # template_id.send_mail(self.id, force_send=True)
            employee_retard_time.append({'employee': rec.employee_id, 'retard_time': str(timedelta(hours=(
                                                                                                                     datetime.strptime(
                                                                                                                         rec.check_in.strftime(
                                                                                                                             '%H:%M:%S'),
                                                                                                                         '%H:%M:%S') - datetime.strptime(
                                                                                                                 selected_horaire.horaire_debut.strftime(
                                                                                                                     '%H:%M:%S'),
                                                                                                                 '%H:%M:%S')).total_seconds() / 3600 if selected_horaire else 0))})

        if len(employee_retard_time) > 0:
            # rh
            template_id = self.env.ref('cps_icesco.mail_hr_retard_gestionnaire')  # xml id of your email template
            template_id.email_to = 'rh@icesco.org'
            template_id.reply_to = 'rh@icesco.org'
            template_id.email_from = 'it@icesco.org'
            template_context = {
                'day': date.today(),
                'employees_retard': employee_retard_time
            }
            template_id.with_context(**template_context).send_mail(self.id, force_send=True)

            # nidal
            template_id = self.env.ref('cps_icesco.mail_hr_retard_gestionnaire')  # xml id of your email template
            template_id.email_to = 'nabuzuhri@icesco.org'
            template_id.reply_to = 'nabuzuhri@icesco.org'
            template_id.email_from = 'it@icesco.org'
            template_context = {
                'day': date.today(),
                'employees_retard': employee_retard_time
            }
            template_id.with_context(**template_context).send_mail(self.id, force_send=True)

    def mail_hr_week_retard_employees(self):
        employee_retard_time = []
        managers = []

        for rec in self.env['hr.attendance'].search([]).filtered(
                lambda x: x.checkin_anomalie == 'late' and date.today() - timedelta(
                        days=7) < x.check_in.date() <= date.today()):
            selected_horaire = False
            for horaire in self.env['cps.hr.horaire'].search([]).filtered(
                    lambda x: datetime.strptime(x.horaire_debut.strftime('%H:%M:%S'), '%H:%M:%S') <= datetime.strptime(
                            rec.check_in.strftime('%H:%M:%S'), '%H:%M:%S') and datetime.strptime(
                            x.horaire_fin.strftime('%H:%M:%S'), '%H:%M:%S') >= datetime.strptime(
                            rec.check_in.strftime('%H:%M:%S'), '%H:%M:%S')):
                if selected_horaire:
                    if (datetime.strptime(rec.check_in.strftime('%H:%M:%S'), '%H:%M:%S') - datetime.strptime(
                            horaire.horaire_debut.strftime('%H:%M:%S'), '%H:%M:%S')).total_seconds() / 3600 < (
                            datetime.strptime(rec.check_in.strftime('%H:%M:%S'), '%H:%M:%S') - datetime.strptime(
                            selected_horaire.horaire_debut.strftime('%H:%M:%S'), '%H:%M:%S')).total_seconds() / 3600:
                        selected_horaire = horaire
                else:
                    selected_horaire = horaire

            # template_id.send_mail(self.id, force_send=True)
            employee_retard_time.append({'jour': rec.check_in.date(), 'employee': rec.employee_id, 'retard_time': str(
                timedelta(hours=(datetime.strptime(rec.check_in.strftime('%H:%M:%S'), '%H:%M:%S') - datetime.strptime(
                    selected_horaire.horaire_debut.strftime('%H:%M:%S'),
                    '%H:%M:%S')).total_seconds() / 3600 if selected_horaire else 0))})

        if len(employee_retard_time) > 0:
            # to rh
            template_id = self.env.ref('cps_icesco.mail_hr_week_retard_gestionnaire')  # xml id of your email template
            template_id.email_to = 'rh@icesco.org'
            template_id.reply_to = 'rh@icesco.org'
            template_id.email_from = 'it@icesco.org'
            template_context = {
                'employees_retard': employee_retard_time
            }
            template_id.with_context(**template_context).send_mail(self.id, force_send=True)

            # to nidal
            template_id = self.env.ref('cps_icesco.mail_hr_week_retard_gestionnaire')  # xml id of your email template
            template_id.email_to = 'nabuzuhri@icesco.org'
            template_id.reply_to = 'nabuzuhri@icesco.org'
            template_id.email_from = 'it@icesco.org'
            template_context = {
                'employees_retard': employee_retard_time
            }
            template_id.with_context(**template_context).send_mail(self.id, force_send=True)

    def mail_hr_month_retard_employees(self):
        employee_retard_time = []
        managers = []

        for rec in self.env['hr.attendance'].search([]).filtered(
                lambda x: x.checkin_anomalie == 'late' and date.today() - relativedelta(
                        months=+1) < x.check_in.date() <= date.today()):
            selected_horaire = False
            for horaire in self.env['cps.hr.horaire'].search([]).filtered(
                    lambda x: datetime.strptime(x.horaire_debut.strftime('%H:%M:%S'), '%H:%M:%S') <= datetime.strptime(
                            rec.check_in.strftime('%H:%M:%S'), '%H:%M:%S') and datetime.strptime(
                            x.horaire_fin.strftime('%H:%M:%S'), '%H:%M:%S') >= datetime.strptime(
                            rec.check_in.strftime('%H:%M:%S'), '%H:%M:%S')):
                if selected_horaire:
                    if (datetime.strptime(rec.check_in.strftime('%H:%M:%S'), '%H:%M:%S') - datetime.strptime(
                            horaire.horaire_debut.strftime('%H:%M:%S'), '%H:%M:%S')).total_seconds() / 3600 < (
                            datetime.strptime(rec.check_in.strftime('%H:%M:%S'), '%H:%M:%S') - datetime.strptime(
                            selected_horaire.horaire_debut.strftime('%H:%M:%S'), '%H:%M:%S')).total_seconds() / 3600:
                        selected_horaire = horaire
                else:
                    selected_horaire = horaire

            # template_id.send_mail(self.id, force_send=True)
            employee_retard_time.append({'jour': rec.check_in.date(), 'employee': rec.employee_id, 'retard_time': str(
                timedelta(hours=(datetime.strptime(rec.check_in.strftime('%H:%M:%S'), '%H:%M:%S') - datetime.strptime(
                    selected_horaire.horaire_debut.strftime('%H:%M:%S'),
                    '%H:%M:%S')).total_seconds() / 3600 if selected_horaire else 0))})

        if len(employee_retard_time) > 0:
            # to rh
            template_id = self.env.ref('cps_icesco.mail_hr_month_retard_gestionnaire')  # xml id of your email template
            template_id.email_to = 'rh@icesco.org'
            template_id.reply_to = 'rh@icesco.org'
            template_id.email_from = 'it@icesco.org'
            template_context = {
                'employees_retard': employee_retard_time
            }
            template_id.with_context(**template_context).send_mail(self.id, force_send=True)

            # to nidal
            template_id = self.env.ref('cps_icesco.mail_hr_month_retard_gestionnaire')  # xml id of your email template
            template_id.email_to = 'nabuzuhri@icesco.org'
            template_id.reply_to = 'nabuzuhri@icesco.org'
            template_id.email_from = 'it@icesco.org'
            template_context = {
                'employees_retard': employee_retard_time
            }
            template_id.with_context(**template_context).send_mail(self.id, force_send=True)

    def action_validate(self):
        current_employee = self.env.user.employee_id
        if any(holiday.state not in ['confirm', 'validate1', 'validate'] for holiday in self):
            raise UserError(_('Time off request must be confirmed in order to approve it.'))

        self.write({'state': 'validate'})
        self.filtered(lambda holiday: holiday.validation_type == 'both').write(
            {'second_approver_id': current_employee.id})
        self.filtered(lambda holiday: holiday.validation_type != 'both').write(
            {'first_approver_id': current_employee.id})

        for holiday in self.filtered(lambda holiday: holiday.holiday_type != 'employee'):
            if holiday.holiday_type == 'category':
                employees = holiday.category_id.employee_ids
            elif holiday.holiday_type == 'company':
                employees = self.env['hr.employee'].search([('company_id', '=', holiday.mode_company_id.id)])
            else:
                employees = holiday.department_id.member_ids

            conflicting_leaves = self.env['hr.leave'].with_context(
                tracking_disable=True,
                mail_activity_automation_skip=True,
                leave_fast_create=True
            ).search([
                ('date_from', '<=', holiday.date_to),
                ('date_to', '>', holiday.date_from),
                ('state', 'not in', ['cancel', 'refuse']),
                ('holiday_type', '=', 'employee'),
                ('employee_id', 'in', employees.ids)])

            if conflicting_leaves:
                # YTI: More complex use cases could be managed in master
                if holiday.leave_type_request_unit != 'day' or any(
                        l.leave_type_request_unit == 'hour' for l in conflicting_leaves):
                    raise ValidationError(_('You can not have 2 leaves that overlaps on the same day.'))

                # keep track of conflicting leaves states before refusal
                target_states = {l.id: l.state for l in conflicting_leaves}
                conflicting_leaves.action_refuse()
                split_leaves_vals = []
                for conflicting_leave in conflicting_leaves:
                    if conflicting_leave.leave_type_request_unit == 'half_day' and conflicting_leave.request_unit_half:
                        continue

                    # Leaves in days
                    if conflicting_leave.date_from < holiday.date_from:
                        before_leave_vals = conflicting_leave.copy_data({
                            'date_from': conflicting_leave.date_from.date(),
                            'date_to': holiday.date_from.date() + timedelta(days=-1),
                            'state': target_states[conflicting_leave.id],
                        })[0]
                        before_leave = self.env['hr.leave'].new(before_leave_vals)
                        before_leave._onchange_request_parameters()
                        # Could happen for part-time contract, that time off is not necessary
                        # anymore.
                        # Imagine you work on monday-wednesday-friday only.
                        # You take a time off on friday.
                        # We create a company time off on friday.
                        # By looking at the last attendance before the company time off
                        # start date to compute the date_to, you would have a date_from > date_to.
                        # Just don't create the leave at that time. That's the reason why we use
                        # new instead of create. As the leave is not actually created yet, the sql
                        # constraint didn't check date_from < date_to yet.
                        if before_leave.date_from < before_leave.date_to:
                            split_leaves_vals.append(before_leave._convert_to_write(before_leave._cache))
                    if conflicting_leave.date_to > holiday.date_to:
                        after_leave_vals = conflicting_leave.copy_data({
                            'date_from': holiday.date_to.date() + timedelta(days=1),
                            'date_to': conflicting_leave.date_to.date(),
                            'state': target_states[conflicting_leave.id],
                        })[0]
                        after_leave = self.env['hr.leave'].new(after_leave_vals)
                        after_leave._onchange_request_parameters()
                        # Could happen for part-time contract, that time off is not necessary
                        # anymore.
                        if after_leave.date_from < after_leave.date_to:
                            split_leaves_vals.append(after_leave._convert_to_write(after_leave._cache))

                split_leaves = self.env['hr.leave'].with_context(
                    tracking_disable=True,
                    mail_activity_automation_skip=True,
                    leave_fast_create=True,
                    leave_skip_state_check=True
                ).create(split_leaves_vals)

                split_leaves.filtered(lambda l: l.state in 'validate')._validate_leave_request()

            values = holiday._prepare_employees_holiday_values(employees)
            leaves = self.env['hr.leave'].with_context(
                tracking_disable=True,
                mail_activity_automation_skip=True,
                leave_fast_create=True,
                leave_skip_state_check=True,
            ).create(values)

            leaves._validate_leave_request()

        employee_requests = self.filtered(lambda hol: hol.holiday_type == 'employee')
        employee_requests._validate_leave_request()
        if not self.env.context.get('leave_fast_create'):
            employee_requests.filtered(lambda holiday: holiday.validation_type != 'no_validation').activity_update()
        return True