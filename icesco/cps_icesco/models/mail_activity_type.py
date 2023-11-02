# -*- coding: utf-8 -*-
from odoo import models, fields, api

class MailActivityType(models.Model):
    _inherit = 'mail.activity.type'

    add_notification_mail = fields.Boolean(string='Add to menu notifications')