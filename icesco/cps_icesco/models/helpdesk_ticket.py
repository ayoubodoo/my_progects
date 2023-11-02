# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tests import Form
from odoo.exceptions import ValidationError

class HelpdeskTicket(models.Model):

    _inherit = 'helpdesk.ticket'

    event_id = fields.Char(string='Event name')
    partner_id = fields.Many2one('res.partner', domain=[('type', '=', 'contact'),('supplier', '=', False)], string='Event coordinator')
    partner_email = fields.Char(string='Coordinator email')

    # fields.Many2one('event.event', string='Event', required=True)
    deptartment_id = fields.Many2one('hr.department', string='Presented by', required=True)
    date_start = fields.Datetime(string='Date start')
    local_time = fields.Float(string='Local time')
    duration = fields.Integer(string='Duration (in hours)')
    room_id = fields.Many2one('cps.event.room', string='Event location')
    meeting_link = fields.Char(string='Meeting link')
    company = fields.Char(string='Company')

    data_uploading = fields.Boolean(string='Data uploading', default=False)
    meeting_zoom_link = fields.Boolean(string='Zoom meeting link', default=False)
    registration_link = fields.Boolean(string='Registration link', default=False)

    video_recording = fields.Boolean(string='Video recording', default=False)
    video_conference_management = fields.Boolean(string='Video conference', default=False)
    webinar_link = fields.Boolean(string='Webinar link', default=False)
    webinar_attendees = fields.Integer(string='Webinar attendees')
    website_edition = fields.Boolean(string='Website edition', default=False)
    waiting_room = fields.Boolean(string='Waiting Room', default=False)
    is_translation = fields.Boolean(string='Translation', default=False)
    is_translation_arabic = fields.Boolean(string='Translation Arabic', default=False)
    is_translation_english = fields.Boolean(string='Translation English', default=False)
    is_translation_french = fields.Boolean(string='Translation French', default=False)
    list_it_service = fields.Many2one('dh.service.department', string="List of Translation services",
                                      domain=[("type_department", "=", 'translation')])

    @api.model
    def create(self, vals):
        ticket = super(HelpdeskTicket, self).create(vals)

        self.mailmessage(ticket.id, 'cps_icesco.mail_Tickets_validation', 'it@icesco.org', '')

        return ticket

    def mailmessage(self, id, template, email_to, department):
        template_id = self.env.ref(template)  # xml id of your email template
        template_id.email_to = email_to
        template_id.reply_to = email_to
        template_id.email_from = self.env['res.users'].search([('id', '=', self.env.uid)]).login

        name = "Mohamed Helal"

        template_context = {
            'name': name,
        }
        template_id.with_context(**template_context).sudo().send_mail(id, force_send=True)