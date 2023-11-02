# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DhIcescoPerformanceStrategies(models.Model):
    _name = 'dh.icesco.performance.strategies'
    _order = 'sequence'

    sequence = fields.Integer(string='متسلسل')
    strategie = fields.Many2one('dh.strategies', string='الخطة الإستراتيجية')
    name = fields.Char(string='إسم المؤشر', store=True)
    expert_id = fields.Many2many('res.partner', string='الخبير')
    type = fields.Selection([('project', 'مشروع'), ('service', 'خدمة'), ('processe', 'العملية')],  string='النوع')
    ability_id = fields.Many2one('dh.operational.plan.ability', string='القدرة')
    responsable_id = fields.Many2one('res.partner', string='المسؤول')
    measure_cycle = fields.Date(string='دورة القياس', store=True)
    target = fields.Integer(string='المستهدف')
    actual = fields.Integer(string='الفعلي')
    stereotypes = fields.Selection([('very_high', 'مرتفع جداً'), ('high', 'مرتفع'), ('average', 'متوسط'),  ('low', 'منخفض'), ('very_low', 'منخفض جداً')],
                                string='النمطية')
    performance_ratio = fields.Integer(string='نسبة الأداء')
    result_actual = fields.Integer(string='النتيجة الفعلية')
    source_result = fields.Integer(string='مصدر النتائج')
    document_ids = fields.Many2many('ir.attachment', string='الأدلة')

    @api.model
    def create(self, vals):
        vals['sequence'] = len(self.env['dh.icesco.performance.strategies'].search([])) + 1
        return super(DhIcescoPerformanceStrategies, self).create(vals)