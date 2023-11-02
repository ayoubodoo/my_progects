# -*- coding: utf-8 -*-
from odoo import models, fields, api

class IrModel(models.Model):
    _inherit = 'ir.model'

    add_notification_mail = fields.Boolean(string='Add to menu notifications')