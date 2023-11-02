# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ActivityReference(models.Model):
    _name = 'activity.reference'
    _description = 'Activity Reference'

    name = fields.Char(translate=True,string="Name",required=True)