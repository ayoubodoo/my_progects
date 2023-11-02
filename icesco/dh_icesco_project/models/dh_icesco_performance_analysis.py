# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DhIcescoPerformanceAnalysis(models.Model):
    _name = 'dh.icesco.performance.analysis'
    _rec_name = 'office_id'
    _order = 'sequence'

    sequence = fields.Integer(string='متسلسل')
    office_id = fields.Many2one('dh.icesco.office', string='الإدارة')
    analysis_cycle = fields.Selection([('year', 'سنوي'), ('month', 'شهري'), ('week', 'أسبوعي')], string='دورة التحليل')
    date = fields.Date(string='السنة')
    analysis_ids = fields.One2many('dh.icesco.analysis', 'performance_analysis_id', string='تحليل الأداء')
    document_ids = fields.Many2many('ir.attachment', string='الأدلة')

    @api.model
    def create(self, vals):
        vals['sequence'] = len(self.env['dh.icesco.performance.analysis'].search([])) + 1
        return super(DhIcescoPerformanceAnalysis, self).create(vals)

class DhIcescoAnalysis(models.Model):
    _name = 'dh.icesco.analysis'

    type = fields.Selection([('technical', 'الجانب الفني'), ('administrative', 'الجانب الإداري'), ('financial', 'الجانب المالي')], string='الجانب', required=True)
    analysis = fields.Char(string='تحليل', required=True)
    performance_analysis_id = fields.Many2one('dh.icesco.performance.analysis', string='تحليل الأداء')

    def name_get(self):
        res = []
        for p in self:
            name = ""
            if p.type is not False:
                name = name + dict(p._fields['type'].selection).get(p.type)
            if p.analysis is not False:
                name = name + " : " + p.analysis
            res.append((p.id, name))
        return res