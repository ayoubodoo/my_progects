# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, _, api
from odoo.exceptions import ValidationError

class DhMeetingWizard(models.TransientModel):
    _name = "dh.meeting.invitation.wizard"


    meeting_link = fields.Char('Meeting Link ')
    applicant_id = fields.Many2one('hr.applicant')
    interview_id = fields.Many2one('dh.interviews')
    type = fields.Selection([('online','Online'),('offline','Face to Face')],string='Type')

    def interview_invitation_mail(self):

        self.applicant_id.meeting_link = self.meeting_link
        applicant_id = self.env["hr.applicant"].search([('id', '=', self.env.context.get("active_id"))])
        if self.type == 'online':

            if self.interview_id.date_interview and self.interview_id.time_interview and self.meeting_link :
                template_id = self.env.ref('isesco_hr.mail_interview_invitation_online')
                template_id.email_to = self.applicant_id.email_from
                template_id.reply_to = self.applicant_id.email_from
                template_id.email_from = 'icescoemployement@icesco.org'
                template_context = {
                    'applicant': self.applicant_id.partner_name,
                    'position': self.applicant_id.job_id.name,
                    'department': self.applicant_id.display_name,
                    'date': self.interview_id.date_interview ,
                    'time': '{0:02.0f}:{1:02.0f}'.format(*divmod(self.interview_id.time_interview * 60, 60)),

                    'link': self.applicant_id.meeting_link,

                }
                template_id.with_context(**template_context).send_mail(self.applicant_id.id, force_send=True)
            else:
                raise ValidationError(
                            _("You can not send this mail(meeting Link,Interview Date ,and Interview Time are obligatory)"))
        elif  self.type == 'offline':
            if self.interview_id.date_interview and self.interview_id.time_interview:
                template_id = self.env.ref('isesco_hr.mail_interview_invitation_face_to_face')
                template_id.email_to = self.applicant_id.email_from
                template_id.reply_to = self.applicant_id.email_from
                template_id.email_from = 'icescoemployement@icesco.org'
                template_context = {
                    'applicant': self.applicant_id.partner_name,
                    'position': self.applicant_id.job_id.name,
                    'department': self.applicant_id.display_name,
                    'date': self.interview_id.date_interview,
                    'time': '{0:02.0f}:{1:02.0f}'.format(*divmod(self.interview_id.time_interview * 60, 60)),

                    # 'link': self.applicant_id.meeting_link,

                }
                template_id.with_context(**template_context).send_mail(self.applicant_id.id, force_send=True)
            else:
                raise ValidationError(
                    _("You can not send this mail(Interview Date and Interview Time	are obligatory)"))

    def action_send_email(self):

        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = \
                ir_model_data.get_object_reference('isesco_hr', 'mail_interview_invitation_online')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'hr.applicant',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
        }
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
