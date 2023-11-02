# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AppraisalAxis(models.Model):
    _name = 'appraisal.axis'
    _description = 'Appraisal Axis'

    name = fields.Char(string="Name",required=True)
    factor_ids = fields.One2many('appraisal.rating.factor','axe_id', string="Factors",)
    appraisal_line_id = fields.Many2one('appraisal.appraisal.line', string="Appraisal Lines",)