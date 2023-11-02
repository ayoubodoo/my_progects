# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _

class MailActivity(models.Model):
    _inherit = 'mail.activity'

    model_add_notification_mail = fields.Boolean(string='Model Add to menu notifications', related='res_model_id.add_notification_mail')
    type_add_notification_mail = fields.Boolean(string='Type Add to menu notifications', related='activity_type_id.add_notification_mail')

    # @api.model
    # def create(self, values):
    #     activity = super(MailActivity, self).create(values)
    #     context = self._context
    #     current_uid = context.get('uid')
    #     user_id = self.env['res.users'].sudo().browse(current_uid)
    #     email_to = []
    #     # employee_email_to = False
    #
    #     if activity.res_model == 'hr.leave':
    #         if user_id:
    #             for create_user in activity.create_uid:
    #                 email_to.append(create_user.partner_id.id)
    #             for user in activity.user_id:
    #                 email_to.append(user.partner_id.id)
    #             for user in activity.multiple_users:
    #                 email_to.append(user.partner_id.id)
    #
    #             #employee de congé
    #             employee_email_to = self.env['hr.leave'].search([('id', '=', int(activity.res_id))], limit=1).employee_id.work_email
    #
    #             template_id = self.env['ir.model.data'].get_object_reference('cps_icesco',
    #                                                                          'email_template_create_notification')[1]
    #             email_template_obj = self.env['mail.template'].browse(template_id)
    #             if template_id:
    #                 if activity.id:
    #                     # to responsable
    #                     values = email_template_obj.generate_email(activity.id, fields=None)
    #                     values['email_from'] = user_id.partner_id.email
    #                     values['recipient_ids'] = [(4, pid) for pid in email_to]
    #                     values['author_id'] = user_id.partner_id.id
    #                     values['res_id'] = False # activity.res_id
    #                     values['model'] = False # activity.res_model
    #                     mail_mail_obj = self.env['mail.mail']
    #                     msg_id = mail_mail_obj.create(values)
    #                     if msg_id:
    #                         mail_mail_obj.send([msg_id])
    #                         msg_id.sudo().send()
    #
    #                     # to employee
    #                     values = email_template_obj.generate_email(activity.id, fields=None)
    #                     values['email_from'] = user_id.partner_id.email
    #                     values['email_to'] = employee_email_to
    #                     values['author_id'] = user_id.partner_id.id
    #                     values['res_id'] = False # activity.res_id
    #                     values['model'] = False # activity.res_model
    #                     mail_mail_obj = self.env['mail.mail']
    #                     msg_id = mail_mail_obj.create(values)
    #                     if msg_id:
    #                         mail_mail_obj.send([msg_id])
    #                         msg_id.sudo().send()
    #     return activity

    def dh_send_mail(self):
        for activity in self:
            context = self._context
            current_uid = context.get('uid')
            user_id = self.env['res.users'].sudo().browse(current_uid)
            email_to = []

            if user_id:
                for create_user in activity.create_uid:
                    email_to.append(create_user.partner_id.id)
                for user in activity.user_id:
                    email_to.append(user.partner_id.id)
                for user in activity.multiple_users:
                    email_to.append(user.partner_id.id)
                template_id = self.env['ir.model.data'].get_object_reference('cps_icesco',
                                                                             'email_template_create_notification')[1]
                email_template_obj = self.env['mail.template'].browse(template_id)
                if template_id:
                    if activity.id:
                        values = email_template_obj.generate_email(activity.id, fields=None)
                        values['email_from'] = user_id.partner_id.email
                        values['recipient_ids'] = [(4, pid) for pid in email_to]
                        values['author_id'] = user_id.partner_id.id
                        values['res_id'] = False
                        values['model'] = False
                        mail_mail_obj = self.env['mail.mail']
                        msg_id = mail_mail_obj.create(values)
                        if msg_id:
                            mail_mail_obj.send([msg_id])
                            msg_id.sudo().send()