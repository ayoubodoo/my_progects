# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo.tools import float_round
from datetime import date, datetime, timedelta
from ast import literal_eval
from odoo.exceptions import ValidationError
from odoo.http import content_disposition, request, route
from dateutil.relativedelta import relativedelta

class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"

    attendance_state = fields.Selection(string="Attendance Status", compute='_compute_attendance_state',
                                        selection=[('checked_out', "Checked out"), ('checked_in', "Checked in")], store=True)

    hr_presence_state = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('conge', 'Congé'),
        ('to_define', 'To Define'),('sans_pointage', 'Sans Pointage')], compute='_compute_presence_state', default='to_define')

    dh_hr_presence_state = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('conge', 'Congé'),
        ('to_define', 'To Define'),('sans_pointage', 'Sans Pointage')], store=True)


    # @api.depends('hr_presence_state')
    # def _dh_compute_presence_state(self):
    #     for rec in self:
    #         rec.dh_hr_presence_state = rec.hr_presence_state


    def _compute_presence_state(self):
        """
        Override to include checkin/checkout in the presence state
        Attendance has the second highest priority after login
        """
        super()._compute_presence_state()
        employees = self.filtered(lambda employee: employee.hr_presence_state != 'present')
        for employee in employees:
            if employee.attendance_state == 'checked_out' and employee.hr_presence_state == 'to_define':
                employee.hr_presence_state = 'absent'
                employee.dh_hr_presence_state = 'absent'
            if len(self.env['hr.leave'].search([('employee_id', '=', employee.id)]).filtered(lambda x:x.date_from <= datetime.now() <= x.date_to)) > 0:
                employee.hr_presence_state = 'conge'
                employee.dh_hr_presence_state = 'conge'
        for employee in employees:
            if employee.attendance_state == 'checked_in':
                employee.hr_presence_state = 'present'
                employee.dh_hr_presence_state = 'present'
            if len(self.env['hr.leave'].search([('employee_id', '=', employee.id)]).filtered(
                    lambda x: x.date_from <= datetime.now() <= x.date_to)) > 0:
                employee.hr_presence_state = 'conge'
                employee.dh_hr_presence_state = 'conge'
        # for employee in employees:
        #     if employee.sans_pointage == True:
        #         employee.hr_presence_state = 'sans_pointage'
        #         employee.dh_hr_presence_state = 'sans_pointage'



        for rec in self:
            rec.dh_hr_presence_state = rec.hr_presence_state

    # @api.depends('user_id.im_status')
    # def _compute_presence_state(self):
    #     """
    #     This method is overritten in several other modules which add additional
    #     presence criterions. e.g. hr_attendance, hr_holidays
    #     """
    #     # Check on login
    #     check_login = literal_eval(
    #         self.env['ir.config_parameter'].sudo().get_param('hr.hr_presence_control_login', 'False'))
    #     for employee in self:
    #         state = 'to_define'
    #         if check_login:
    #             if employee.user_id.im_status == 'online':
    #                 state = 'present'
    #             elif employee.user_id.im_status == 'offline':
    #                 state = 'absent'
    #         if len(self.env['hr.leave'].search([('employee_id', '=', employee.id)]).filtered(lambda x:x.date_from <= datetime.now() <= x.date_to)) > 0:
    #             state = 'conge'
    #         employee.hr_presence_state = state

class HrEmployee(models.Model):
    _name = 'hr.employee'
    _inherit = ['hr.employee', 'mail.thread', 'mail.activity.mixin']

    is_translation = fields.Boolean(string='Translation',track_visibility='always')
    is_design = fields.Boolean(string='Design',track_visibility='always')
    is_legal = fields.Boolean(string='Legal',track_visibility='always')
    is_logistics = fields.Boolean('Logistics')
    is_protocol = fields.Boolean('Protocol')
    is_finance = fields.Boolean(string='Finance',track_visibility='always')
    is_admin = fields.Boolean(string='Admin',track_visibility='always')
    is_it = fields.Boolean(string='IT',track_visibility='always')
    is_media = fields.Boolean(string='Media',track_visibility='always')

    is_dg = fields.Boolean(string='DG Office',track_visibility='always')
    is_coverage = fields.Boolean(string='Coverage',track_visibility='always')
    is_dpt_participation = fields.Boolean(string='Dpt participation',track_visibility='always')

    cps_leaves_count = fields.Float('Cps Number of Time Off', compute='_cps_compute_remaining_leaves',track_visibility='always')
    cps_allocation_display = fields.Char(compute='_cps_compute_allocation_count',track_visibility='always')
    cps_allocation_used_display = fields.Char(compute='_cps_compute_total_allocation_used',track_visibility='always')
    cps_remaining_leaves = fields.Float(
        compute='_cps_compute_remaining_leaves', string='Cps Remaining Paid Time Off',track_visibility='always')
    cps_allocation_count = fields.Float('Cps Total number of days allocated.', compute='_cps_compute_allocation_count',track_visibility='always')
    cps_allocation_used_count = fields.Float('Cps Total number of days off used', compute='_cps_compute_total_allocation_used',track_visibility='always')

    #inherit

    mobile_phone = fields.Char('Work Mobile',track_visibility='always')
    work_phone = fields.Char('Work Phone',track_visibility='always')
    work_email = fields.Char('Work Email',track_visibility='always')
    work_location = fields.Char('Work Location',track_visibility='always')
    company_id = fields.Many2one('res.company', 'Company',track_visibility='always')
    department_id = fields.Many2one('hr.department', 'Department',
                                    domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",track_visibility='always')
    job_id = fields.Many2one('hr.job', 'Job Position',
                             domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",track_visibility='always')
    parent_id = fields.Many2one('hr.employee', 'Manager',
                                domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",track_visibility='always')
    address_id = fields.Many2one('res.partner', 'Work Address',
                                 domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",track_visibility='always')
    coach_id = fields.Many2one('hr.employee', 'Coach',
                               domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",track_visibility='always')
    leave_manager_id = fields.Many2one(
        'res.users', string='Time Off',
        help="User responsible of leaves approval.",track_visibility='always')
    sans_pointage = fields.Boolean(string='Sans pointage')

    resume_cv = fields.Boolean(string='cv')
    lettre_motivation = fields.Boolean(string='lettre')

    @api.constrains('name', 'prenom')
    def check_prenom_name(self):
        for rec in self:
            if len(self.env['hr.employee'].search([('id', '!=', rec.id), ('name', '=', rec.name), ('prenom', '=', rec.prenom)])) > 0:
                raise ValidationError("Vous ne pouvez pas créer un employé qui a le même nom et prénom qu'un employé existant.")

    def _group_hr_expense_user_domain(self):
        # We return the domain only if the group exists for the following reason:
        # When a group is created (at module installation), the `res.users` form view is
        # automatically modifiedto add application accesses. When modifiying the view, it
        # reads the related field `expense_manager_id` of `res.users` and retrieve its domain.
        # This is a problem because the `group_hr_expense_user` record has already been created but
        # not its associated `ir.model.data` which makes `self.env.ref(...)` fail.
        group = self.env.ref('hr_expense.group_hr_expense_team_approver', raise_if_not_found=False)
        return [('groups_id', 'in', group.ids)] if group else []
    expense_manager_id = fields.Many2one(
        'res.users', string='Expense',
        domain=_group_hr_expense_user_domain,
        help="User responsible of expense approval. Should be Expense approver.",track_visibility='always')
    resource_calendar_id = fields.Many2one('resource.calendar',
                                           domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",track_visibility='always')
    tz = fields.Selection(
        string='Timezone', related='resource_id.tz', readonly=False,
        help="This field is used in order to define in which timezone the resources will work.",track_visibility='always')
    private_email = fields.Char(related='address_home_id.email', string="Private Email", groups="hr.group_hr_user",track_visibility='always')
    phone = fields.Char(related='address_home_id.phone', related_sudo=False, readonly=False, string="Private Phone",
                        groups="hr.group_hr_user",track_visibility='always')
    # country_id = fields.Many2one(
    #     'res.country', 'Nationality (Country)', groups="hr.group_hr_user", tracking=True,track_visibility='always')

    user_id = fields.Many2one('res.users', 'User', related='resource_id.user_id', store=True, readonly=False,track_visibility='always')
    pin = fields.Char(string="PIN", groups="hr.group_hr_user", copy=False,
                      help="PIN used to Check In/Out in Kiosk Mode (if enabled in Configuration).",track_visibility='always')
    barcode = fields.Char(string="Badge ID", help="ID used for employee identification.", groups="hr.group_hr_user",
                          copy=False,track_visibility='always')

    department_racine = fields.Many2one('hr.department', department='Racine department', compute='compute_racine_department', store=True)

    @api.depends('department_id')
    def compute_racine_department(self):
        for rec in self:
            rec.department_racine = False
            if rec.department_id.parent_id.parent_id.id == False:
                rec.department_racine = rec.department_id.id
            elif rec.department_id.parent_id.parent_id.parent_id.id == False:
                rec.department_racine = rec.department_id.parent_id.id
            elif rec.department_id.parent_id.parent_id.parent_id.parent_id.id == False:
                rec.department_racine = rec.department_id.parent_id.parent_id.id
            elif rec.department_id.parent_id.parent_id.parent_id.parent_id.parent_id.id == False:
                rec.department_racine = rec.department_id.parent_id.parent_id.parent_id.id
            elif rec.department_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.id == False:
                rec.department_racine = rec.department_id.parent_id.parent_id.parent_id.parent_id.id
            elif rec.department_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.id == False:
                rec.department_racine = rec.department_id.parent_id.parent_id.parent_id.parent_id.parent_id.id
            elif rec.department_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.id == False:
                rec.department_racine = rec.department_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.id
            else:
                rec.department_racine = False

    def verify_retirement_date(self):
        for employee in self.env['hr.employee'].search([('active', '=', True), ('retirement_date', '!=', False)]):
            if employee.retirement_date > fields.Date.today():
                if int(self.env["ir.config_parameter"].sudo().get_param("cps_icesco.notif_retraite")) >=\
                        (employee.retirement_date.year - fields.Date.today().year) * 12 + (employee.retirement_date.month  - fields.Date.today().month) >= 0:
                    if len(self.env['mail.activity'].search([('user_id', '=', self.env['res.users'].search([('login', '=', 'rh@icesco.org')]).id), ('date_deadline', '=', employee.retirement_date), ('summary', 'ilike', 'date de retraite'), ('res_id', '=', employee.id)])) == 0:
                        self.env['mail.activity'].create({
                            'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                            'user_id': self.env['res.users'].search([('login', '=', 'rh@icesco.org')]).id,
                            'summary': 'date de retraite',
                            'note': 'le collaborateur suivant approche de la retraite : %s' % (employee.retirement_date),
                            'date_deadline': employee.retirement_date,
                            'res_model_id': self.env['ir.model']._get('hr.employee').id,
                            'res_id': employee.id
                        })

    def mail_notif_evaluation(self):
        if (datetime.strptime(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.date_evaluation'),'%Y-%m-%d').date() - fields.Date.today()).days == int(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.notif_evaluation')):
            template_id = self.env.ref('cps_icesco.mail_notif_evaluation')  # xml id of your email template
            for manager in self.env['hr.employee'].search([('active', '=', True)]).mapped('appraisal_manager_id'):
                template_id.email_to = manager.login
                template_id.reply_to = manager.login
                template_id.email_from = 'it@icesco.org'
                template_context = {
                    'date': self.env['ir.config_parameter'].sudo().get_param('cps_icesco.date_evaluation'),
                    'days': self.env['ir.config_parameter'].sudo().get_param('cps_icesco.notif_evaluation'),
                }
                template_id.with_context(**template_context).send_mail(self.id, force_send=True)

    def mail_notif_reevaluation(self):
        if (datetime.strptime(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.date_reevaluation'),'%Y-%m-%d').date() - fields.Date.today()).days == int(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.notif_reevaluation')):
            template_id = self.env.ref('cps_icesco.mail_notif_reevaluation')  # xml id of your email template
            for manager in self.env['hr.employee'].search([('active', '=', True)]).mapped('appraisal_manager_id'):
                template_id.email_to = manager.login
                template_id.reply_to = manager.login
                template_id.email_from = 'it@icesco.org'
                template_context = {
                    'date': self.env['ir.config_parameter'].sudo().get_param('cps_icesco.date_reevaluation'),
                    'days': self.env['ir.config_parameter'].sudo().get_param('cps_icesco.notif_reevaluation'),
                }
                template_id.with_context(**template_context).send_mail(self.id, force_send=True)


    def _cps_compute_remaining_leaves(self):
        for rec in self:
            remaining = rec._get_remaining_leaves()
            # print('remaining',remaining)
            conges = sum(self.env['hr.leave'].search([('employee_id', '=', rec.id),('date_from', '>=', date(date.today().year - 1, 1, 1)), ('date_from', '<=', date(date.today().year, 12, 31)),('state', '=', 'validate'),]).filtered(lambda x:x.holiday_status_id.allocation_type in ['fixed', 'fixed_allocation'] and x.holiday_status_id.active == True).mapped('number_of_days'))
            allocations = sum(self.env['hr.leave.allocation'].search([
                ('employee_id', '=', rec.id),
                ('create_date', '>=', date(date.today().year - 1, 1, 1)),
                ('create_date', '<=', date(date.today().year, 12, 31)),
                ('holiday_status_id.active', '=', True),
                ('state', '=', 'validate'),
            ]).mapped('number_of_days'))
            if allocations == 0:
                allocations = sum(self.env['hr.leave.allocation'].search([
                    ('employee_id', '=', rec.id),
                    ('holiday_status_id.active', '=', True),
                    ('state', '=', 'validate'),
                ]).filtered(lambda x:x.holiday_status_id.validity_start >= date(date.today().year - 1, 1, 1) and x.holiday_status_id.validity_stop <= date(date.today().year, 12, 31)).mapped('number_of_days'))
            cps_remaining = {rec.id : allocations - conges}
            # print('cps_remaining', cps_remaining)
        for employee in self:
            value = float_round(cps_remaining.get(employee.id, 0.0), precision_digits=2)
            employee.cps_leaves_count = value if value > 0 else 0
            employee.cps_remaining_leaves = value if value > 0 else 0

    def _cps_compute_allocation_count(self):
        for employee in self:
            allocations = self.env['hr.leave.allocation'].search([
                ('employee_id', '=', employee.id),
                ('create_date', '>=', date(date.today().year, 1, 1)), ('create_date', '<=', date(date.today().year, 12, 31)),
                ('holiday_status_id.active', '=', True),
                ('state', '=', 'validate'),
            ])
            employee.cps_allocation_count = float_round(sum(allocations.mapped('number_of_days')), precision_digits=2)
            employee.cps_allocation_display = "%g" % employee.cps_allocation_count

    def _cps_compute_total_allocation_used(self):
        for employee in self:
            employee.cps_allocation_used_count = float_round(employee.cps_allocation_count - employee.cps_remaining_leaves, precision_digits=2)
            employee.cps_allocation_used_display = "%g" % employee.cps_allocation_used_count

    @api.model
    def dh_attendance_scan(self, barcode):
        """ Receive a barcode scanned from the Kiosk Mode and change the attendances of corresponding employee.
            Returns either an action or a warning.
        """
        employee = self.sudo().search([('barcode', '=', barcode)], limit=1)
        if employee:
            return employee._dh_attendance_action('kzm_hr_pointeuse.dh_hr_attendance_action_kiosk_mode')
        return {'warning': _('No employee corresponding to barcode %(barcode)s') % {'barcode': barcode}}

    def _dh_attendance_action(self, next_action):
        """ Changes the attendance of the employee.
            Returns an action to the check in/out message,
            next_action defines which menu the check in/out message should return to. ("My Attendances" or "Kiosk Mode")
        """
        self.ensure_one()
        employee = self.sudo()
        last_autorisation = self.env['dh.autorisation.sortie'].search([
                ('employee_id', '=', employee.id),
            ], order='check_out desc', limit=1)
        action_message = self.env.ref('hr_attendance.hr_attendance_action_greeting_message').read()[0]
        action_message['previous_attendance_change_date'] = last_autorisation and (last_autorisation.check_out or last_autorisation.check_in) or False
        action_message['employee_name'] = employee.name
        action_message['barcode'] = employee.barcode
        action_message['next_action'] = next_action
        action_message['hours_today'] = employee.hours_today

        if employee.user_id:
            if not employee.user_id.has_group('base.group_portal'):
                modified_attendance = employee.with_user(employee.user_id)._dh_attendance_action_change()
            else:
                modified_attendance = employee._dh_attendance_action_change()
        else:
            modified_attendance = employee._dh_attendance_action_change()
        action_message['attendance'] = modified_attendance.read()[0]
        return {'action': action_message}

    def dh_attendance_manual(self, next_action, entered_pin=None):
        self.ensure_one()
        can_check_without_pin = not self.env.user.has_group('hr_attendance.group_hr_attendance_use_pin') or (self.user_id == self.env.user and entered_pin is None)
        if can_check_without_pin or entered_pin is not None and entered_pin == self.sudo().pin:
            return self._dh_attendance_action(next_action)
        return {'warning': _('Wrong PIN')}

    def _dh_attendance_action(self, next_action):
        """ Changes the attendance of the employee.
            Returns an action to the check in/out message,
            next_action defines which menu the check in/out message should return to. ("My Attendances" or "Kiosk Mode")
        """
        self.ensure_one()
        employee = self.sudo()
        action_message = self.env.ref('hr_attendance.hr_attendance_action_greeting_message').read()[0]
        action_message['previous_attendance_change_date'] = employee.last_attendance_id and (employee.last_attendance_id.check_out or employee.last_attendance_id.check_in) or False
        action_message['employee_name'] = employee.name
        action_message['barcode'] = employee.barcode
        action_message['next_action'] = next_action
        action_message['hours_today'] = employee.hours_today

        if employee.user_id:
            if not employee.user_id.has_group('base.group_portal'):
                modified_attendance = employee.with_user(employee.user_id)._dh_attendance_action_change()
            else:
                modified_attendance = employee._dh_attendance_action_change()
        else:
            modified_attendance = employee._dh_attendance_action_change()
        action_message['attendance'] = modified_attendance.read()[0]
        return {'action': action_message}

    def _dh_attendance_action_change(self):
        """ Check In/Check Out action
            Check In: create a new attendance record
            Check Out: modify check_out field of appropriate attendance record
        """

        self.ensure_one()
        action_date = fields.Datetime.now()

        autorisation_sortie = self.env['dh.autorisation.sortie'].search(
            [('employee_id', '=', self.id), ('check_in', '=', False)], order='check_out desc', limit=1)

        if len(autorisation_sortie) == 0:
            autorisation_sortie = self.env['dh.autorisation.sortie'].search([('employee_id', '=', self.id), ('check_out', '!=', False)],
                                                          order='check_out desc', limit=1)


        if len(self.env['dh.autorisation.sortie'].search(
                [('employee_id', '=', self.id)])) == 0 or (len(self.env['dh.autorisation.sortie'].search(
            [('employee_id', '=', self.id),
             ('check_out', '>=', datetime.now() - timedelta(seconds=5))])) == 0 and len(
            self.env['dh.autorisation.sortie'].search(
                [('employee_id', '=', self.id),
                 ('check_in', '>=', datetime.now() - timedelta(seconds=5))])) == 0):
            last_autorisation_sortie = self.env['dh.autorisation.sortie'].search(
                [('employee_id', '=', self.id), ('check_in', '=', False)], order='check_out desc', limit=1)
            if last_autorisation_sortie:
                last_autorisation_sortie.check_in = action_date
            else:
                vals = {
                    'employee_id': self.id,
                    'check_out': action_date,
                }

                # autorisations_this_month = self.env['dh.autorisation.sortie'].search(
                #     [('employee_id', '=', self.id), ('check_out', '>=', datetime.strptime(action_date.date().strftime('%Y-%m-01'), "%Y-%m-%d")), ('check_in', '<', datetime.strptime((action_date.date() + relativedelta(months=1)).strftime('%Y-%m-01'), "%Y-%m-%d"))])


                # if len(autorisations_this_month) == 3 or sum(autorisations_this_month.mapped('leave_hours')) >= 6:
                #     vals['dh_autorisation_to_remove'] = True

                return self.env['dh.autorisation.sortie'].create(vals)
            autorisation_sortie = last_autorisation_sortie
        return autorisation_sortie

    def _attendance_action(self, next_action):
        """ Changes the attendance of the employee.
            Returns an action to the check in/out message,
            next_action defines which menu the check in/out message should return to. ("My Attendances" or "Kiosk Mode")
        """
        self.ensure_one()
        employee = self.sudo()
        action_message = self.env.ref('hr_attendance.hr_attendance_action_greeting_message').read()[0]
        action_message['previous_attendance_change_date'] = employee.last_attendance_id and (employee.last_attendance_id.check_out or employee.last_attendance_id.check_in) or False
        action_message['employee_name'] = employee.name
        action_message['barcode'] = employee.barcode
        action_message['next_action'] = next_action
        action_message['hours_today'] = employee.hours_today

        if employee.user_id:
            if not employee.user_id.has_group('base.group_portal'):
                modified_attendance = employee.with_user(employee.user_id)._attendance_action_change()
            else:
                modified_attendance = employee._attendance_action_change()
        else:
            modified_attendance = employee._attendance_action_change()
        action_message['attendance'] = modified_attendance.read()[0]
        return {'action': action_message}

    # ATTENTION !!!!!
    def _attendance_action_change(self):
        """ Check In/Check Out action
            Check In: create a new attendance record
            Check Out: modify check_out field of appropriate attendance record
        """
        attendance = self.env['hr.attendance'].search([('employee_id', '=', self.id), ('check_out', '=', False)], limit=1)
        if len(attendance) == 0:
            attendance = self.env['hr.attendance'].search([('employee_id', '=', self.id), ('check_in', '!=', False)],
                                                          order='check_in desc', limit=1)

        if len(self.env['hr.attendance'].search(
                [('employee_id', '=', self.id)])) == 0 or (len(self.env['hr.attendance'].search(
                [('employee_id', '=', self.id),('check_out', '>=', datetime.now() - timedelta(seconds=5))])) == 0 and len(self.env['hr.attendance'].search(
                [('employee_id', '=', self.id),('check_in', '>=', datetime.now() - timedelta(seconds=5))])) == 0):
            self.ensure_one()
            action_date = fields.Datetime.now()

            horairess = self.env['cps.hr.horaire'].search([])
            horaires = []
            horaire_id = False
            blockage_pointage = False
            entree_avant_heure = False

            for horaire in horairess:
                for date in horaire.dates:
                    if action_date >= date.date_debut and action_date <= date.date_fin:
                        horaires.append(horaire)

            if len(horaires) == 0:
                horaire_id = False

            for horaire in horaires:
                check_in_horaire = datetime.strptime(horaire.horaire_debut.strftime('%H:%M:%S'), '%H:%M:%S')
                check_out_horaire = datetime.strptime(horaire.horaire_fin.strftime('%H:%M:%S'), '%H:%M:%S')
                max_horaire = datetime.strptime(horaire.horaire_max_pointage.strftime('%H:%M:%S'), '%H:%M:%S')
                date = datetime.strptime(action_date.strftime('%H:%M:%S'), '%H:%M:%S')
                if check_in_horaire <= date <= check_out_horaire:
                    blockage_pointage = True

                if date < check_in_horaire and (check_in_horaire - date).total_seconds() < float(
                    self.env['ir.config_parameter'].sudo().get_param('cps_icesco.marge_horaire')) * 3600:
                    entree_avant_heure = True

                if (max_horaire - date).total_seconds() > 0:
                    horaire_id = horaire.id
                    break
                else:
                    horaire_id = False

            if self.attendance_state != 'checked_out':
                last_attendance = self.env['hr.attendance'].search(
                    [('employee_id', '=', self.id), ('check_out', '=', False)], order='check_in desc', limit=1)
                if last_attendance.check_in.date() != action_date.date():
                    last_attendance.write({'check_out': datetime(last_attendance.check_in.date().year,
                                                                 last_attendance.check_in.date().month,
                                                                 last_attendance.check_in.date().day, 22, 59, 59)})
                    last_attendance.action_server_appliquer_horaire_one()
                    self.attendance_state = 'checked_out'

            if self.attendance_state != 'checked_in':
                vals = {
                    'employee_id': self.id,
                    'check_in': action_date,
                }
                if entree_avant_heure == True:
                    vals['checkin_anomalie'] = 'chekin_before_time'
                    # self.mail_entree_anomalie(self ,action_date)

                if self.env.user.has_group('cps_icesco.icesco_administrator_pointage') and action_date.date().weekday() not in [5, 6] and blockage_pointage == True:
                    if horaire_id == False:
                        vals['checkin_anomalie'] = 'late'

                if not self.env.user.has_group('cps_icesco.icesco_administrator_pointage') and action_date.date().weekday() not in [5, 6] and blockage_pointage == True:
                    if horaire_id == False:
                        vals['dh_to_remove'] = True
                #         raise ValidationError(_('You cannot check in because you arrive too late, please contact the responsible'))

                return self.env['hr.attendance'].create(vals)

            attendance = self.env['hr.attendance'].search([('employee_id', '=', self.id), ('check_out', '=', False)], limit=1)
            if attendance:
                attendance.check_out = action_date
                attendance.action_server_appliquer_horaire_one() # correction
            else:
                raise exceptions.UserError(
                    _('Cannot perform check out on %(empl_name)s, could not find corresponding check in. '
                      'Your attendances have probably been modified manually by human resources.') % {
                        'empl_name': self.sudo().name, })
        return attendance

    def mail_entree_anomalie(self, employee_id, action_date):
        template_id = self.env.ref('cps_icesco.mail_entree_anomalie')  # xml id of your email template
        template_id.email_to = 'rh@icesco.org'
        template_id.reply_to = 'rh@icesco.org'
        template_id.email_from = 'it@icesco.org'
        template_context = {
            'matricule': employee_id.matricule,
            'employee': employee_id.name,
            'jour': action_date.date(),
        }
        template_id.with_context(**template_context).send_mail(employee_id.id, force_send=True)

    # def call_fonction_pointage_autorisation(self, employee_id):
    #     action_date = fields.Datetime.now()
    #
    #     autorisations_this_month = self.env['dh.autorisation.sortie'].search(
    #         [('employee_id', '=', employee_id), ('check_out', '>=', datetime.strptime(action_date.date().strftime('%Y-%m-01'), "%Y-%m-%d")),
    #          ('check_in', '<', datetime.strptime((action_date.date() + relativedelta(months=1)).strftime('%Y-%m-01'), "%Y-%m-%d"))])
    #
    #     if len(autorisations_this_month) == 3 or sum(autorisations_this_month.mapped('leave_hours')) >= 6:
    #         # vals['dh_autorisation_to_remove'] = True
    #         return {'warning': _('You cannot check in because you arrive too late, please contact the responsible')}
    #
    #     return True

    def call_fonction_pointage(self):
        action_date = fields.Datetime.now()

        horairess = self.env['cps.hr.horaire'].sudo().search([])
        horaires = []
        horaire_id = False
        blockage_pointage = False

        for horaire in horairess:
            for date in horaire.dates:
                if action_date >= date.date_debut and action_date <= date.date_fin:
                    horaires.append(horaire)

        if len(horaires) == 0:
            horaire_id = False

        for horaire in horaires:
            check_in_horaire = datetime.strptime(horaire.horaire_debut.strftime('%H:%M:%S'), '%H:%M:%S')
            check_out_horaire = datetime.strptime(horaire.horaire_fin.strftime('%H:%M:%S'), '%H:%M:%S')
            max_horaire = datetime.strptime(horaire.horaire_max_pointage.strftime('%H:%M:%S'), '%H:%M:%S')
            date = datetime.strptime(action_date.strftime('%H:%M:%S'), '%H:%M:%S')
            if check_in_horaire <= date <= check_out_horaire:
                blockage_pointage = True

            if (max_horaire - date).total_seconds() > 0:
                horaire_id = horaire.id
                break
            else:
                horaire_id = False

        if not self.env.user.has_group('cps_icesco.icesco_administrator_pointage') and action_date.date().weekday() not in [5, 6] and blockage_pointage == True:
            if horaire_id == False:
                return {'warning': _('You cannot check in because you arrive too late, please contact the responsible')}

        return True

    date_cin = fields.Date(string='Date Expération CIN')
    date_exp_carte_diplomatique = fields.Date(string="Date d'xpérationcarte diplomatique")
    carte_diplomatique = fields.Char(string="Carte  diplomatique")
    date_passeport_exp = fields.Date(string="Date d'xpération passeport")
    notif_fin_contrat = fields.Integer(string='fin contrat')
    notif_fin_periode_essai = fields.Integer(string="fin période d'essai")
    notif_retraite = fields.Integer(string="Retraite")
    type_contrat = fields.Char(related='contract_id.type_id.name', string='Type de contrat')
    non_resident = fields.Boolean(string='Non Resident', default=False)

    def verify_date_cin1(self):
        for rec in self.env['hr.employee'].search([('active', '=', True)
                                                   ]):
            if rec.cin and rec.date_cin:
                s = int(self.env["ir.config_parameter"].sudo().get_param("cps_icesco.date_cin"))
                text = 'le CIN : '+ str(rec.cin) +' du collaborateur ' +str(rec.name )+' , viendra à expiration dans  ' + str(s) + ' jours'
                if int(self.env["ir.config_parameter"].sudo().get_param("cps_icesco.date_cin")) >= (
                        rec.date_cin - fields.Date.today()).days >= 0:
                    if len(self.env['mail.activity'].search(
                            [('user_id', '=', self.env['res.users'].search([('login', '=', 'rh@icesco.org')]).id),
                             ('summary', 'ilike', 'Expiration CIN'), ('res_id', '=', rec.id)])) == 0:
                        self.env['mail.activity'].create({
                            'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                            'user_id': self.env['res.users'].search([('login', '=', 'rh@icesco.org')]).id,

                            'summary': 'Expiration CIN',
                            'note': text,
                            'date_deadline': rec.date_cin,
                            'res_model_id': self.env['ir.model']._get('hr.employee').id,
                            'res_id': rec.id
                        })
    def verify_date_passeport(self):
        for rec in self.env['hr.employee'].search([('active', '=', True)
                                                   ]):
            if rec.passport_id and rec.date_passeport_exp:
                s = int(self.env["ir.config_parameter"].sudo().get_param("cps_icesco.date_cin"))
                text = 'le passeport : '+ str(rec.cin) +' du collaborateur ' +str(rec.name )+' , viendra à expiration dans  ' + str(s) + ' jours'
                if int(self.env["ir.config_parameter"].sudo().get_param("cps_icesco.date_cin")) >= (
                        rec.date_passeport_exp - fields.Date.today()).days >= 0:
                    if len(self.env['mail.activity'].search(
                            [('user_id', '=', self.env['res.users'].search([('login', '=', 'rh@icesco.org')]).id),
                             ('summary', 'ilike', 'Expiration passeport'), ('res_id', '=', rec.id)])) == 0:
                        self.env['mail.activity'].create({
                            'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                            'user_id': self.env['res.users'].search([('login', '=', 'rh@icesco.org')]).id,

                            'summary': 'Expiration passeport',
                            'note': text,
                            'date_deadline': rec.date_passeport_exp,
                            'res_model_id': self.env['ir.model']._get('hr.employee').id,
                            'res_id': rec.id
                        })
    def verify_date_carte_diplomatique(self):
        for rec in self.env['hr.employee'].search([('active', '=', True)
                                                   ]):
            if rec.carte_diplomatique and rec.date_exp_carte_diplomatique:
                s = int(self.env["ir.config_parameter"].sudo().get_param("cps_icesco.date_cin"))
                text = 'la catrte diplomatique  : '+ str(rec.carte_diplomatique) +' du collaborateur ' +str(rec.name )+' , viendra à expiration dans  ' + str(s) + ' jours'
                if int(self.env["ir.config_parameter"].sudo().get_param("cps_icesco.date_cin")) >= (
                        rec.date_exp_carte_diplomatique - fields.Date.today()).days >= 0:
                    if len(self.env['mail.activity'].search(
                            [('user_id', '=', self.env['res.users'].search([('login', '=', 'rh@icesco.org')]).id),
                             ('summary', 'ilike', 'Expiration carte diplomatique'), ('res_id', '=', rec.id)])) == 0:
                        self.env['mail.activity'].create({
                            'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                            'user_id': self.env['res.users'].search([('login', '=', 'rh@icesco.org')]).id,

                            'summary': 'Expiration carte diplomatique',
                            'note': text,
                            'date_deadline': rec.date_exp_carte_diplomatique,
                            'res_model_id': self.env['ir.model']._get('hr.employee').id,
                            'res_id': rec.id
                        })

    def dh_allocation_employee(self):
        for rec in self:
            allocations = []
            for allocation in self.env['hr.leave.allocation'].search([('state', '=', 'validate'), ('employee_id', '=', rec.id)]).mapped('holiday_status_id'):
                if sum(self.env['hr.leave.allocation'].search([('state', '=', 'validate'),('employee_id', '=', rec.id), ('holiday_status_id', '=', allocation.id)]).mapped('number_of_days_display')) - sum(self.env['hr.leave'].search([('state', '=', 'validate'), ('employee_id', '=', rec.id), ('holiday_status_id', '=', allocation.id)]).mapped('number_of_days_display')) > 0:
                    allocations.append({'type_allocation': allocation.name, 'days': sum(self.env['hr.leave.allocation'].search([('state', '=', 'validate'), ('employee_id', '=', rec.id), ('holiday_status_id', '=', allocation.id)]).mapped('number_of_days_display')) - sum(self.env['hr.leave'].search([('state', '=', 'validate'), ('employee_id', '=', rec.id), ('holiday_status_id', '=', allocation.id)]).mapped('number_of_days_display')),'balance_leave': sum(self.env['hr.leave.allocation'].search([('state', '=', 'validate'),('employee_id', '=', rec.id), ('holiday_status_id', '=', allocation.id)]).mapped('number_of_days_display'))})


            rec.emergency_leave = 7 - sum(self.env['hr.leave'].search([('state', '=', 'validate'),('holiday_status_id.is_urgent', '=', True), ('employee_id', '=', rec.id), ]).filtered(lambda x: datetime(date.today().year, 12, 31) >= x.date_from >= datetime( date.today().year, 1, 1) or datetime(date.today().year, 1, 1) <= x.date_to <= datetime(date.today().year, 12, 31)).mapped('number_of_days'))
            rec.sum= sum(self.env['hr.leave'].search([('state', '=', 'validate'),('holiday_status_id.is_urgent', '=', True), ('employee_id', '=', rec.id), ]).filtered(lambda x: datetime(date.today().year, 12, 31) >= x.date_from >= datetime( date.today().year, 1, 1) or datetime(date.today().year, 1, 1) <= x.date_to <= datetime(date.today().year, 12, 31)).mapped('number_of_days'))


            if len(allocations) > 0 or rec.emergency_leave > 0 :
                template_id = self.env.ref('cps_icesco.mail_allocation_employee')  # xml id of your email template
                template_id.email_to = rec.work_email
                template_id.reply_to = rec.work_email
                template_id.email_from = 'rh@icesco.org'
                template_context = {
                    'allocations': allocations,
                    'emergency_leave':  rec.emergency_leave,
                    'today': date.today()
                }
                template_id.with_context(**template_context).send_mail(rec.id, force_send=True)

    def atteindre_plafond_type_mutuelle(self):
        for prestation in self.env['medical.record.benefit'].search([('is_capped', '=', True)]):
            for employee in self.env['medical.refund.request.line'].search([('date', '>=', datetime.strptime(date.today().strftime('%Y-01-01'), "%Y-%m-%d")),
                     ('date', '<', datetime.strptime((date.today() + timedelta(days=365)).strftime('%Y-01-01'), "%Y-%m-%d"))]).filtered(lambda x:x.refund_request_id.state in ['submited', 'verified', 'validated', 'arrear']).mapped('employee_id'):
                if sum(self.env['medical.refund.request.line'].search([('employee_id', '=', employee.id), ('patient_full_name', '=', False), ('type_id', '=', prestation.id), ('date', '>=', datetime.strptime(date.today().strftime('%Y-01-01'), "%Y-%m-%d")),
                     ('date', '<', datetime.strptime((date.today() + timedelta(days=365)).strftime('%Y-01-01'), "%Y-%m-%d"))]).filtered(lambda x:x.refund_request_id.state in ['submited', 'verified', 'validated', 'arrear']).mapped('amount_to_refund')) >= prestation.upper_limit:
                    if len(self.env['mail.activity'].search(
                            [('res_id', '=', employee.id),
                             ('summary', 'ilike', 'Employée Atteindre plafond mutuelle'),
                             ('note', 'ilike', "<p>L'employée %s atteindre le plafond de prestation %s pour l'année %s.</p>" % (employee.display_name, prestation.name, date.today().year))])) == 0:
                        self.env['mail.activity'].create({
                                    'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                                    'user_id': self.env['res.users'].search([('login', '=', 'rh@icesco.org')]).id,
                                    'summary': 'Employée Atteindre plafond mutuelle',
                                    'note': "<p>L'employée %s atteindre le plafond de prestation %s pour l'année %s.</p>" % (employee.display_name, prestation.name, date.today().year),
                                    'res_model_id': self.env['ir.model']._get('hr.employee').id,
                                    'res_id': employee.id
                                })

            for dependent in self.env['medical.refund.request.line'].search([('date', '>=', datetime.strptime(date.today().strftime('%Y-01-01'), "%Y-%m-%d")),
                     ('date', '<', datetime.strptime((date.today() + timedelta(days=365)).strftime('%Y-01-01'), "%Y-%m-%d"))]).filtered(lambda x:x.refund_request_id.state in ['submited', 'verified', 'validated', 'arrear']).mapped('employee_id').mapped('dependent_ids'):
                if sum(self.env['medical.refund.request.line'].search([('employee_id', '=', dependent.employee_id.id), ('patient_full_name', '=', dependent.id), ('type_id', '=', prestation.id), ('date', '>=', datetime.strptime(date.today().strftime('%Y-01-01'), "%Y-%m-%d")),
                     ('date', '<', datetime.strptime((date.today() + timedelta(days=365)).strftime('%Y-01-01'), "%Y-%m-%d"))]).filtered(lambda x:x.refund_request_id.state in ['submited', 'verified', 'validated', 'arrear']).mapped('amount_to_refund')) >= prestation.upper_limit:
                    if len(self.env['mail.activity'].search(
                            [('res_id', '=', dependent.employee_id.id),
                             ('summary', 'ilike', 'Adhérent Atteindre plafond mutuelle'),
                             ('note', 'ilike', "<p>L'adhérent %s atteindre le plafond de prestation %s pour l'année %s.</p>" % (dependent.name ,prestation.name, date.today().year))])) == 0:
                        self.env['mail.activity'].create({
                                    'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                                    'user_id': self.env['res.users'].search([('login', '=', 'rh@icesco.org')]).id,
                                    'summary': 'Adhérent Atteindre plafond mutuelle',
                                    'note': "<p>L'adhérent %s atteindre le plafond de prestation %s pour l'année %s.</p>" % (dependent.name ,prestation.name, date.today().year),
                                    'res_model_id': self.env['ir.model']._get('hr.employee').id,
                                    'res_id': dependent.employee_id.id
                                })

    # def verify_date_cin(self):
    #     first_user = False
    #     remain_user_ids = []
    #     i = 0
    #     for user1 in self.env['res.users'].search(
    #             [("groups_id", "=", self.env.ref("hr.group_hr_manager").id)]):
    #         if user1.has_group('hr_contract.group_hr_contract_manager') and i == 0:
    #             first_user = user1[0]
    #             i = i + 1
    #
    #     self.mailmessage(event.id, 'cps_icesco.mail_event_informations', 'events@icesco.org', 'cabdg@icesco.org', '',
    #                      False)
    #     if 'dg_approval' in vals:
    #         if vals['dg_approval']:
    #             self.mailmessage(event.id, 'cps_icesco.mail_event_validation', 'events@icesco.org', 'dg@icesco.org', '',
    #                              self.env['hr.employee'].search([('is_dg', '=', True)]))
    #     if 'deadline_delivery' in vals:
    #         if vals['deadline_delivery']:
    #             for user in self.env['res.users'].search(
    #                     [("groups_id", "=", self.env.ref("cps_icesco.icesco_confirm_event").id)]):
    #                 self.env['mail.activity'].create({
    #                     'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
    #                     'user_id': user.id,
    #                     'summary': 'The deadline of delivery',
    #                     'note': 'The deadline of delivery to this event is : %s' % (event.deadline_delivery),
    #                     'date_deadline': event.deadline_delivery.date(),
    #                     'res_model_id': self.env['ir.model']._get('event.event').id,
    #                     'res_id': event.id
    #                 })
    #     return event

    # def generate_employees(self, vals):
    #     event = super(dhHrPayroll_ma, self).create(vals)
    #     for rec in self:
    #         employee_obj = self.env['hr.employee']
    #         obj_contract = self.env['hr.contract']
    #         employees = employee_obj.search([('active', '=', True), ('employee_externe', '=', False),
    #                                          ('date', '<=', rec.date_end),
    #                                          ('company_id', '=', rec.company_id.id),
    #                                          ])
    #
    #         if rec.state == 'draft':
    #             sql = '''
    #                DELETE from hr_payroll_ma_bulletin where id_payroll_ma = %s
    #                    '''
    #             self.env.cr.execute(sql, (rec.id,))
    #
    #         for employee in employees:
    #             contract = obj_contract.search([('employee_id', '=', employee.id),
    #                                             ('state', 'in', ('pending', 'open'))], order='date_start', limit=1)
    #             if contract:
    #                 line = {
    #                     'employee_id': employee.id,
    #                     'employee_contract_id': contract.id,
    #                     'working_days': contract.working_days_per_month,
    #                     'normal_hours': contract.monthly_hour_number,
    #                     'hour_base': contract.hour_salary,
    #                     'salaire_base': contract.wage,
    #                     'id_payroll_ma': rec.id,
    #                     'period_id': rec.period_id.id,
    #                     'date_start': rec.date_start,
    #                     'date_end': rec.date_end,
    #                     'date_salary': rec.date_salary,
    #                     'taux_anciennete': employee.anciennete and self.env['hr.payroll_ma.bulletin'].calc_seniority(
    #                         employee.date, rec.date_end, type_employe=employee.type_employe, wk_days=0) or 0.0
    #
    #                 }
    #                 self.env['hr.payroll_ma.bulletin'].create(line)
    #         for user in self.env['hr.employee'].search([('non_resident', '=', True), ('date.year', '=', date.today().year),('date.month', '=', date.today().month)]):
    #             self.env['mail.activity'].create({
    #                 'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
    #                 'user_id': user.id,
    #                 'summary': 'The deadline of delivery',
    #                 'note': 'The following employees must have a facility allowance:  : %s' % (user.name),
    #                 # 'date_deadline': event.deadline_delivery.date(),
    #                 'res_model_id': self.env['ir.model']._get('hr.payroll_ma.bulletin').id,
    #                 'res_id': event.id
    #             })
    #             # return event
    #
    #
    #     return True
    def send_emails(self):
        for r in self:
            r.bulletin_line_ids.send_emails()
    def filter_residents(self):
        for r in self:
            employees_non_rside = self.env['hr.employee'].search([('non_resident', '=',True),('date.year', '=',date.today().year),('date.month', '=',date.today().month)])
            print('employees_non_rside',employees_non_rside)


class dhHrPayroll_ma(models.Model):
    _name = 'hr.payroll_ma'
    _inherit = ['hr.payroll_ma', 'mail.thread', 'mail.activity.mixin']
    # def send_emails(self):
    #     for r in self:
    #         r.bulletin_line_ids.send_emails()
    # def filter_residents(self):
    #     for r in self:
    #         employees_non_rside = self.env['hr.employee'].search([('non_resident', '=',True),('date.year', '=',date.today().year),('date.month', '=',date.today().month)])
    #         print('employees_non_rside',employees_non_rside)


class HrPayroll_maBulletinResidence(models.Model):
    _name = 'hr.payroll_ma.bulletin'
    _inherit = ['hr.payroll_ma.bulletin','mail.thread', 'mail.activity.mixin']


    # def send_emails(self):
    #     template = self.env.ref('kzm_payslip_email.notif_hr_payroll_ma_bulletin', False)
    #     for bulletin in self:
    #         if bulletin.employee_id.non_resident == False and bulletin.employee_id.date:
    #
    #             content, content_type = self.env.ref('kzm_payroll_ma.bulletin_paie_id').render_qweb_pdf(
    #                 bulletin.id)
    #             bulletin_paie_att = self.env['ir.attachment'].create({
    #                 'name': 'Bulletin %s.pdf' %  bulletin.period_id.name,
    #                 'type': 'binary',
    #                 'datas': base64.encodestring(content),
    #                 'res_model': 'hr.payroll_ma.bulletin',
    #                 'res_id': bulletin.id,
    #                 'mimetype': 'application/x-pdf'
    #             })
    #
    #             email_values = {
    #                 'email_to': bulletin.employee_id.work_email,
    #                 'attachment_ids':[(6, 0, [bulletin_paie_att.id])]
    #             }
    #             self.env['mail.template'].browse(template.id).send_mail(bulletin.id, email_values=email_values,
    #                                                                     force_send=False, raise_exception=True)


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    multiple_users = fields.Many2many('res.users', store=True)

    # Add this function inside
    @api.model
    def create(self, vals):
        assigned_user_id = vals['user_id']
        assigned_user_name = self.env['res.users'].browse(vals['user_id']).name
        vals['display_name'] = assigned_user_name
        res = super(MailActivity, self).create(vals)
        if 'multiple_users' in vals and vals['multiple_users']:
            related_user_ids = self.env['res.users'].search([('id', 'in', vals['multiple_users'][0][2])], order='id')
            for each in related_user_ids:
                if each.name != assigned_user_name:
                    vals['user_id'] = each.id
                    vals['display_name'] = each.name
                    res = super(MailActivity, self).create(vals)
        return res