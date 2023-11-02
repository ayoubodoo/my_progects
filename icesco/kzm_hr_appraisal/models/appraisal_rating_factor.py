# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AppraisalRatingFactor(models.Model):
    _name = 'appraisal.rating.factor'
    _description = 'appraisal rating factor'
    _order = 'number'

    name = fields.Char(string="Name")
    number = fields.Char(string="Number", required=1)
    description = fields.Text(translate=True,string="Description")
    axe_id = fields.Many2one('appraisal.axis', "Axe")
    value_ids = fields.Many2many('appraisal.rating.factor.value', string="Values")
