# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tests import Form
from odoo.exceptions import ValidationError
from datetime import datetime
import base64

class EventEvent(models.Model):

    _inherit = 'event.event'
    #General
    deptartment_id = fields.Many2one('hr.department', 'Presented by', required=True)
    event_related = fields.Char('Event name', required=True)
    location = fields.Selection([('icesco', 'ICESCO'), ('external', 'External'), ('online', 'Online')], 'Implementation location')
    location_required = fields.Char('Implementation location')
    room_id = fields.Many2one('cps.event.room','Room')
    country = fields.Many2one('res.country', 'Country')
    city = fields.Char('City')
    location_name = fields.Char('Location')
    #Event / Project details
    initiative = fields.Selection([('icesco_plan', 'Part of ICESCO plan'), ('new', 'New proposed activity'), ('cooperation', 'Cooperation agreement')], string='The Initiative is', required=True)
    initiative_required = fields.Char('Initiative required')
    frequency = fields.Selection([('first', 'First time'), ('regular', 'Regular activity'), ('continuity', 'Continuity of previous collaboration')], string='The frequency of this initiative', required=True)
    frequency_required = fields.Char('Frequency required')
    member_state_id = fields.Many2one('res.country','Member state', domain=[('is_member', '=', True)])
    external_member_state = fields.Many2one('res.country', string='Member state', domain=[('is_member', '=', True)])
    non_member_state_id = fields.Many2one('res.country', string='Non member states', domain=[('is_member', '=', False)])
    external_non_member_state = fields.Many2one('res.country', string='Non member states', domain=[('is_member', '=', False)])
    partners = fields.Char('Partners')
    dg_approval = fields.Boolean('DG Approval')
    is_dg_participation = fields.Boolean('DG participation', default=False)
    is_dpt_participation = fields.Boolean('Sector/Department participation')
    is_external_expert = fields.Boolean('Hire External Expert')
    is_dg_participation_required = fields.Boolean('DG Participation required')
    dg_initiative_required = fields.Char('Initiative required', required=True)
    provider = fields.Char(string='Provider')
    is_sponsorship_available = fields.Boolean('Sponsorship Available')
    is_estimated_budget = fields.Boolean('Estimated Budget')
    is_ioc_organization = fields.Boolean('OIC Organizations')
    is_un_organization = fields.Boolean('UN Organizations')
    is_au_organization = fields.Boolean('AU Organizations')
    is_al_organization = fields.Boolean('AL Organizations')
    list_oic_organization = fields.Many2one('res.partner', string="List of OIC Organizations", domain=[("is_ioc_organization", "=", True)])
    list_un_organization = fields.Many2one('res.partner', string="List of UN Organizations", domain=[("is_un_organization", "=", True)])
    list_au_organization = fields.Many2one('res.partner', string="List of AU Organizations", domain=[("is_au_organization", "=", True)])
    list_al_organization = fields.Many2one('res.partner', string="List of AL Organizations", domain=[("is_al_organization", "=", True)])
    list_translation_service = fields.Many2one('dh.service.department', string="List of Translation services",
                                            domain=[("type_department", "=", 'translation')])
    list_designing_service = fields.Many2one('dh.service.department', string="List of Designing & printing  services",
                                           domain=[("type_department", "=", 'designing_printing')])
    list_legal_service = fields.Many2one('dh.service.department', string="List of Legal services",
                                           domain=[("type_department", "=", 'legal')])
    list_finance_service = fields.Many2one('dh.service.department', string="List of Finance services",
                                           domain=[("type_department", "=", 'finance')])
    list_logistics_service = fields.Many2one('dh.service.department', string="List of Logistics services",
                                           domain=[("type_department", "=", 'logistics')])
    list_admin_service = fields.Many2one('dh.service.department', string="List of Procurement services",
                                             domain=[("type_department", "=", 'procurement')])
    list_it_service = fields.Many2one('dh.service.department', string="List of IT services",
                                         domain=[("type_department", "=", 'it')])
    list_media_service = fields.Many2one('dh.service.department', string="List of Media services",
                                      domain=[("type_department", "=", 'media')])
    list_protocol_service = fields.Many2one('dh.service.department', string="List of Protocol services",
                                         domain=[("type_department", "=", 'protocol')])
    list_others_service = fields.Many2one('dh.service.department', string="List of Others services",
                                            domain=[("type_department", "=", 'others')])
    others_organization = fields.Char(string='Others')
    budget = fields.Monetary('Estimated Budget')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    #DG Participation information
    dg_participation = fields.Selection([('no', 'No Participation'), ('visit', 'Visit (In Person)'), ('opening', 'Opening/ Closing address (In Person)'), ('recorded', 'Recorded Video (Virtual)'), ('video', 'Video Conference (Virtual)')], string='Participation level required for DG participation')
    dg_participation_required = fields.Boolean('DG participation required')
    is_dg_visit = fields.Boolean('Visit')
    is_dg_event = fields.Boolean('Event')
    is_dg_recorded = fields.Boolean('Recorded Video')
    is_dg_video = fields.Boolean('Video Conference')
    is_opening = fields.Boolean('Opening')
    is_closing = fields.Boolean('Closing')
    is_panel = fields.Boolean('Panel')
    is_many_presidents = fields.Boolean('A+: Two or more Presidents')
    is_one_president = fields.Boolean('A: One President')
    is_many_ministers = fields.Boolean('B+: Prime Minister orover Two ministers')
    is_one_minister = fields.Boolean('B: OneMinister')
    is_professionals = fields.Boolean('C: Professionals')
    key_people_meet = fields.Char('Key People to meet')
    deadline_delivery = fields.Datetime('Deadline of Delivery')
    duration_video = fields.Integer('Duration Video')
    agenda_topics = fields.Char('Agenda Topics')
    conference_link = fields.Char('Conference link')
    speech_topic = fields.Char('Speech topic')
    speech_points = fields.Char('Key points')
    speech_duration = fields.Integer('Speech duration (in minutes)')
    date_speech = fields.Datetime('Speech date')
    participation_level = fields.Selection([('a+', 'A+: Two or more Presidents'), ('a', 'A: One President'), ('b+', 'B+: Prime Minister or over Two ministers'), ('b', 'B: One Minister'), ('c', 'C: Professionals')], string='Participation level required for DG participation')
    participation_level_required = fields.Char('Participation level required')
    is_partnership_govenmental = fields.Boolean('A: Governmental organization')
    is_partnership_international = fields.Boolean('B: International Organization')
    is_partnership_nonorganization = fields.Boolean('C: Non-Governmental Organization')
    is_partnership_others = fields.Boolean('D: Others Organization')
    state_engagement = fields.Selection([('none', 'Not defined'),('high', 'High: Over 6 times in the same year'), ('medium', 'Medium: Between 3 to 6 times in the same year'), ('low', 'Low: Less than 3 times in the same year')], string='State member engagement with ICESCO this year', compute='_compute_state_engagement')
    project_id = fields.Many2one('project.project', string='Projet')
    task_id = fields.Many2one('project.task', string='Projet')
    state = fields.Selection(selection_add=[('draft', 'Unapproved'),('postponed', 'Postponed'), ('delegated', 'Delegated'), ('modified', 'Modified'), ('confirm', 'Approved')])

    @api.constrains('room_id')
    def check_reserve_room(self):
        for rec in self:
            event_reserved = rec.env['event.event'].search([('room_id', '=', rec.room_id.id), ('id', '!=', rec.id)]).filtered(lambda x:rec.date_begin <= x.date_begin <= rec.date_end or rec.date_begin <= x.date_end <= rec.date_end)
            if len(event_reserved) > 0 and rec.location == 'icesco' and rec.room_id.id != False:
                raise ValidationError("The room %s is already reserved in this date for the event %s" % (rec.room_id.name, event_reserved[0].name))

    @api.depends('member_state_id', 'date_begin')
    def _compute_state_engagement(self):
        for rec in self:
            if rec.member_state_id.id != False:
                count_engagement = len(self.env['event.event'].search([('member_state_id', '=', rec.member_state_id.id)]).filtered(lambda x:x.date_begin.year == fields.Date.today().year))
            else:
                count_engagement = 0
            if count_engagement > 6:
                rec.state_engagement = 'high'
            elif 3 <= count_engagement <= 6:
                rec.state_engagement = 'medium'
            elif 1 <= count_engagement < 3:
                rec.state_engagement = 'low'
            else:
                rec.state_engagement = 'none'

    def _compute_state_engagement_return(self, member_state_id):
        for rec in self:
            if member_state_id != False:
                count_engagement = len(self.env['event.event'].search([('member_state_id', '=', member_state_id)]).filtered(lambda x:x.date_begin.year == fields.Date.today().year))
            else:
                count_engagement = 0
            if count_engagement > 6:
                state_engagement = 'high'
            elif 3 <= count_engagement <= 6:
                state_engagement = 'medium'
            elif 1 <= count_engagement < 3:
                state_engagement = 'low'
            else:
                state_engagement = 'none'

            return state_engagement

    state_engagement_required = fields.Char('State engagement required')
    #Financial Coverage by Stakeholders
    is_coverage_airflight = fields.Boolean('Airflight')
    is_coverage_diem = fields.Boolean('Per Diem')
    is_coverage_accomodation = fields.Boolean('Accommodatiom')
    is_coverage_localtransport = fields.Boolean('Local Transportation')
    coverage_persons = fields.Integer('Coverage for Number person', required=True)
    coverage_persons_airflight = fields.Integer('Coverage airflight for', required=True)
    coverage_persons_por_diem = fields.Integer('Coverage Por Diem for', required=True)
    coverage_persons_accomodation = fields.Integer('Coverage Accomodation for', required=True)
    coverage_persons_local_transportation = fields.Integer('Coverage Local Transortation for', required=True)
    is_increase_competitiveness = fields.Boolean('Increase ICESCO competitiveness')
    is_increase_fundraising = fields.Boolean('Receive fundraising/sponsorship')
    is_increase_partnership = fields.Boolean('Initiate new partnership')
    is_increase_services = fields.Boolean('Provide Services for a State Member')
    is_increase_services_expertise = fields.Boolean('Provide technical expertise/   consultations')
    is_increase_services_capacity = fields.Boolean('Capacity building')
    is_increase_services_practice = fields.Boolean('Sharing a best practice')
    is_increase_services_collaboration = fields.Boolean('Enhance mutual collaboration')
    is_support_translation = fields.Boolean('Enhance mutual collaboration')

    translation = fields.Boolean('Translation')
    is_support_designing = fields.Boolean('Designing & printing')
    is_support_legal = fields.Boolean('Legal')
    is_support_logistics = fields.Boolean('Logistics')
    is_support_protocol = fields.Boolean('Protocol')
    is_support_finance = fields.Boolean('Finance')
    is_support_admin = fields.Boolean('Procurement')
    is_support_it = fields.Boolean('IT')
    is_support_media = fields.Boolean('Media')
    is_support_other = fields.Boolean('Other supports (specify)')
    services_other = fields.Char('Other services (specify)')
    suppliers_for = fields.Char('Suppliers for')
    sponsors_for = fields.Char('Sponsors for')
    attach_invitation_id = fields.Many2many(comodel_name="ir.attachment", relation="m2m_ir_invistation_rel", column1="m2m_id",  column2="attachment_id", string="Invitation")
    attach_note_id = fields.Many2many(comodel_name="ir.attachment", relation="m2m_ir_note_rel", column1="m2m_id",  column2="attachment_id", string="Event / project Concept Note")
    attach_participants_id = fields.Many2many(comodel_name="ir.attachment", relation="m2m_ir_participants_rel", column1="m2m_id",  column2="attachment_id", string="Attendees / Participants")
    attach_external_export = fields.Many2many(comodel_name="ir.attachment", relation="m2m_ir_external_export_rel", column1="m2m_id",  column2="attachment_id", string="Attachement Hire External Expert")

    dg_approved = fields.Boolean('Approved')
    dg_postponed = fields.Boolean('Postponed')
    dg_delegated = fields.Boolean('Delegated')
    dg_modified = fields.Boolean('Modified')
    postponed_date = fields.Date(string='Proposed date')
    delegation = fields.Char(string='Delegation')
    modified_budget = fields.Boolean(string='Budget')
    modified_program = fields.Boolean(string='Program')
    modified_attendees = fields.Boolean(string='List of attendees')

    @api.onchange('dg_approval','is_dg_participation','is_dpt_participation')
    def onchange_dg_initiative(self):
        if self.dg_approval == True or self.is_dg_participation == True or self.is_dpt_participation == True:
            self.dg_initiative_required='OK'
        else:
            self.dg_initiative_required=''

    # def testt(self):
    #     self.mailmessage(self.id, 'cps_icesco.mail_event_informations', 'events@icesco.org', 'cabdg@icesco.org', '',
    #                      self.env['hr.employee'].search([('is_dg', '=', True)]))

    @api.model
    def create(self, vals):
        event = super(EventEvent, self).create(vals)



        dg_contact = self.env['res.partner'].search([('email', '=', 'it@icesco.org')], limit=1)
        registration = self.env['event.registration'].sudo().create({'partner_id': dg_contact.id, 'name': dg_contact.name, 'email': dg_contact.email, 'event_id': event.id})
        registration.sudo().confirm_registration()

        self.mailmessage(event.id, 'cps_icesco.mail_event_informations', 'events@icesco.org', 'cabdg@icesco.org', '', False)
        if 'dg_approval' in vals:
            if vals['dg_approval']:
                self.mailmessage(event.id, 'cps_icesco.mail_event_validation', 'events@icesco.org', 'dg@icesco.org', '', self.env['hr.employee'].search([('is_dg', '=', True)]))
        if 'deadline_delivery' in vals:
            if vals['deadline_delivery']:
                for user in self.env['res.users'].search([("groups_id", "=", self.env.ref("cps_icesco.icesco_confirm_event").id)]):
                    self.env['mail.activity'].create({
                        'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                        'user_id': user.id,
                        'summary': 'The deadline of delivery',
                        'note': 'The deadline of delivery to this event is : %s' % (event.deadline_delivery),
                        'date_deadline': event.deadline_delivery.date(),
                        'res_model_id': self.env['ir.model']._get('event.event').id,
                        'res_id': event.id
                    })
        return event

    def write(self, vals):
        if 'dg_approval' in vals:
            if vals['dg_approval']:
                self.mailmessage(self.id, 'cps_icesco.mail_event_validation', 'events@icesco.org', 'dg@icesco.org', '', self.env['hr.employee'].search([('is_dg', '=', True)]))
        if vals.get("state", False):
            if vals['state'] == 'confirm':
                self.mailmessage(self.id, 'cps_icesco.mail_event_participation', 'events@icesco.org', 'dg@icesco.org', '', self.env['hr.employee'].search([('is_dg', '=', True)]))
                if self.is_dpt_participation:
                    self.mailmessage(self.id, 'cps_icesco.mail_event_participation_department', 'events@icesco.org', self.deptartment_id.manager_id.work_email, '', self.deptartment_id.manager_id)
                if self.translation:
                        self.mailmessage(self.id, 'cps_icesco.mail_event_support', 'events@icesco.org', 'translation@icesco.org', 'Translation', False)
                if self.is_support_designing:
                        self.mailmessage(self.id, 'cps_icesco.mail_event_support', 'events@icesco.org', 'design@icesco.org','Design & printing', False)
                if self.is_support_legal:
                        self.mailmessage(self.id, 'cps_icesco.mail_event_support', 'events@icesco.org', 'legal@icesco.org','Legal', False)
                if self.is_support_finance:
                        self.mailmessage(self.id, 'cps_icesco.mail_event_support', 'events@icesco.org', 'finance@icesco.org','Finance', False)
                if self.is_support_admin:
                        self.mailmessage(self.id, 'cps_icesco.mail_event_support', 'events@icesco.org', 'admin@icesco.org', 'Admin', False)
                if self.is_support_it:
                        self.mailmessage(self.id, 'cps_icesco.mail_event_support', 'events@icesco.org', 'it@icesco.org', 'IT', False)
                if self.is_support_media:
                        self.mailmessage(self.id, 'cps_icesco.mail_event_support', 'events@icesco.org', 'media@icesco.org', 'Media', False)
                if self.is_coverage_airflight or self.is_coverage_diem or self.is_coverage_accomodation or self.is_coverage_localtransport:
                    self.mailmessage(self.id, 'cps_icesco.mail_event_coverage', 'events@icesco.org', 'coverage@icesco.org', '', False)
        if vals.get("dg_postponed", False):
            if vals["dg_postponed"]:
                vals["state"] = 'postponed'
                # self.mailmessage(self.id, 'cps_icesco.mail_event_informations', 'events@icesco.org', 'cabdg@icesco.org',
                #                  '', self.env['hr.employee'].search([('is_dg', '=', True)]))
        if vals.get("dg_delegated", False):
            if vals["dg_delegated"]:
                vals["state"] = 'delegated'
                # self.mailmessage(self.id, 'cps_icesco.mail_event_informations', 'events@icesco.org', 'cabdg@icesco.org',
                #                  '', self.env['hr.employee'].search([('is_dg', '=', True)]))
        if vals.get("dg_modified", False):
            if vals["dg_modified"]:
                vals["state"] = 'modified'
                # self.mailmessage(self.id, 'cps_icesco.mail_event_informations', 'events@icesco.org', 'cabdg@icesco.org',
                #                  '', self.env['hr.employee'].search([('is_dg', '=', True)]))
        if vals.get("dg_approved", False):
            if vals["dg_approved"]:
                self.button_confirm()
        res = super(EventEvent, self).write(vals)
        if vals.get("dg_postponed", False):
            if vals["dg_postponed"]:
                self.mailmessage(self.id, 'cps_icesco.mail_event_informations', 'events@icesco.org', self.create_uid.email,
                                 '', False)
                for user in self.env['res.users'].search([("groups_id", "=", self.env.ref("cps_icesco.icesco_confirm_event").id)]):
                    self.mailmessage(self.id, 'cps_icesco.mail_event_informations', 'events@icesco.org',
                                     user.partner_id.email, '', False)
        if vals.get("dg_delegated", False):
            if vals["dg_delegated"]:
                self.mailmessage(self.id, 'cps_icesco.mail_event_informations', 'events@icesco.org', self.create_uid.email,
                                 '', False)
                for user in self.env['res.users'].search([("groups_id", "=", self.env.ref("cps_icesco.icesco_confirm_event").id)]):
                    self.mailmessage(self.id, 'cps_icesco.mail_event_informations', 'events@icesco.org',
                                     user.partner_id.email, '', False)
        if vals.get("dg_modified", False):
            if vals["dg_modified"]:
                self.mailmessage(self.id, 'cps_icesco.mail_event_informations', 'events@icesco.org', self.create_uid.email,
                                 '', False)
                for user in self.env['res.users'].search([("groups_id", "=", self.env.ref("cps_icesco.icesco_confirm_event").id)]):
                    self.mailmessage(self.id, 'cps_icesco.mail_event_informations', 'events@icesco.org',
                                     user.partner_id.email, '', False)
        # if vals.get("deadline_delivery", False):
        #     if vals['deadline_delivery']:
        #         for user in self.env['res.users'].search([("groups_id", "=", self.env.ref("cps_icesco.icesco_confirm_event").id)]):
        #             self.env['mail.activity'].create({
        #                 'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
        #                 'user_id': user.id,
        #                 'summary': 'The deadline of delivery',
        #                 'note': 'The deadline of delivery to this event is : %s' % (vals['deadline_delivery']),
        #                 'date_deadline': datetime.fromisoformat(vals['deadline_delivery']).date(),
        #                 'res_model_id': self.env['ir.model']._get('event.event').id,
        #                 'res_id': self.id
        #             })
        return res

    def mailmessage(self, id, template, email_from, email_to, department, users):
        template_id = self.env.ref(template)  # xml id of your email template
        attachmentss = []
        content, content_type = self.env.ref('cps_icesco.cps_report_event_infos').render_qweb_pdf(
            self.env['event.event'].search([('id', '=', id)]).id)
        event_infos = self.env['ir.attachment'].create({
            'name': 'Event %s.pdf' % self.env['event.event'].search([('id', '=', id)]).name,
            'type': 'binary',
            'datas': base64.encodestring(content),
            'res_model': 'event.event',
            'res_id': self.env['event.event'].search([('id', '=', id)]).id,
            'mimetype': 'application/x-pdf'
        })
        attachmentss.append(event_infos.id)

        # if self.env['event.event'].search([('id', '=', id)]).attach_external_export.id != False:
        #     attachmentss.append(self.env['event.event'].search([('id', '=', id)]).attach_external_export.id)
        # if self.env['event.event'].search([('id', '=', id)]).attach_invitation_id.id != False:
        #     attachmentss.append(self.env['event.event'].search([('id', '=', id)]).attach_invitation_id.id)
        # if self.env['event.event'].search([('id', '=', id)]).attach_note_id.id != False:
        #     attachmentss.append(self.env['event.event'].search([('id', '=', id)]).attach_note_id.id)
        # if self.env['event.event'].search([('id', '=', id)]).attach_participants_id.id != False:
        #     attachmentss.append(self.env['event.event'].search([('id', '=', id)]).attach_participants_id.id)
        # if self.env['event.event'].search([('id', '=', id)]).message_main_attachment_id.id != False:
        #     attachmentss.append(self.env['event.event'].search([('id', '=', id)]).message_main_attachment_id.id)
        if users:
            for user in users:
                template_id.email_to = user.work_email
                template_id.reply_to = user.work_email
                template_id.email_from = email_from
                if user:
                    name = user.name + ' ' + user.prenom
                else:
                    name = ''
                template_context = {
                    'name': name,
                }
                if template != 'cps_icesco.mail_event_informations':
                    template_id.with_context(**template_context).send_mail(id, force_send=True)
                if template == 'cps_icesco.mail_event_informations':
                    template_id.with_context(**template_context).send_mail(id, force_send=True, email_values={
                        'attachment_ids': event_infos})
        else:
            template_id.email_to = email_to
            template_id.reply_to = email_to
            template_id.email_from = email_from
            name = ''
            template_context = {
                'name': name,
            }
            if template != 'cps_icesco.mail_event_informations':
                template_id.with_context(**template_context).send_mail(id, force_send=True)
            if template == 'cps_icesco.mail_event_informations':
                template_id.with_context(**template_context).send_mail(id, force_send=True, email_values={
                'attachment_ids': event_infos})
            # if template == 'cps_icesco.mail_event_informations':
                # template_id.attachment_ids = [(6,0, [event_infos.id])]
                # print(template_id.attachment_ids)

class CpsEventRoom(models.Model):

    _name = 'cps.event.room'

    name = fields.Char('Name')
    date_start = fields.Date(string='Date start')
    date_end = fields.Date(string='Date end')

class CpsEventMembers(models.Model):

    _name = 'cps.event.members'

    name = fields.Char('Name')

class CpsCountry(models.Model):

    _name = 'cps.country'

    name = fields.Char('Name')
