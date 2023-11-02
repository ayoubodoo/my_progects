# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AppraisalModel(models.Model):
    _name = 'appraisal.model'
    _description = 'Appraisal Model'

    name = fields.Char(string="Name", required=True, translate=True)
    matrix_id = fields.Many2one('appraisal.matrix', string="Matrix")
    concern = fields.Char(string='Concern')
    evaluation_pays_member = fields.Boolean(string='Pays Member Evaluation')
    factor_ids = fields.Many2many('appraisal.rating.factor', string="Factors")
    axe_evaluation__ids = fields.Many2many('appraisal.axis.evaluation', string="Evaluations")

    axe_evaluation_report_ids = fields.Many2many('appraisal.axis.evaluation', relation='rel_axe_evaluation_appraisal', string="Evaluations", compute='compute_axe_evaluation_appraisal')


    @api.depends('axe_evaluation__ids')
    def compute_axe_evaluation_appraisal(self):
        for rec in self:
            rec.axe_evaluation_report_ids = False
            for line in rec.axe_evaluation__ids:
                rec.axe_evaluation_report_ids = [(4, line.id)]