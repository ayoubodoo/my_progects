# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AppraisalMatrix(models.Model):
    _name = 'appraisal.matrix'
    _description = 'Appraisal Matrix'

    name = fields.Char(string="Name", required=True)
    matrix_line_ids = fields.One2many('appraisal.matrix.line', 'matrix_id', string="Matrix Lines")
    # model_id = fields.Many2one('appraisal.model', string="Matrix")


class AppraisalMatrixLine(models.Model):
    _name = 'appraisal.matrix.line'
    _description = 'Appraisal Matrix Line'

    minimal_note = fields.Integer(string="Minimal Note")
    maximal_note = fields.Integer(string="Maximal Note")
    appreciation = fields.Selection([
        ('weak', 'Weak'),
        ('good', 'Good'),
        ('very_good', 'Very good'),
        ('excellent', 'Excellent'),
        ('very_satisfied', 'Very satisfied'),
        ('somewhat_satisfied', 'Somewhat satisfied'),
        ('neither_satisfied', 'Neither satisfied nor dissatisfied'),
        ('somewhat_dissatisfied', 'Somewhat dissatisfied'),
        ('very_dissatisfied', 'Very dissatisfied'),
    ], string="Appreciation")
    step_advancement = fields.Integer(string="Step advancement")
    impact = fields.Text(translate=True,string="Impact")
    matrix_id = fields.Many2one('appraisal.matrix', string="Matrix")
