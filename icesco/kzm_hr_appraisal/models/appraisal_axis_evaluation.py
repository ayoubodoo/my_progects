# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AppraisalAxisEvaluation(models.Model):
    _name = 'appraisal.axis.evaluation'
    _description = 'Appraisal Axis Evaluation'

    name = fields.Char(string="Name", required=True)
    is_training_action = fields.Boolean('Is training action ?')
