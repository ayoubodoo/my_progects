# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DhIcescoOperationalPlan(models.Model):
    _name = 'dh.icesco.operational.plan'
    _rec_name = 'strategie'
    _order = 'sequence'

    sequence = fields.Integer(string='متسلسل')
    strategie = fields.Many2one('dh.strategies', string='إسم المؤشر الإستراتيجي')
    orientation_id = fields.Many2one('dh.orientations', string='الهدف') # related='pilliar_id.orientation_id'
    level_one_id = fields.Many2one('dh.operational.plan.level.one', string='المستوى الأول')
    ability_id = fields.Many2one('dh.operational.plan.ability', string='القدرة')
    type = fields.Selection([('project', 'مبادرة'), ('process', 'عملية')], string='النوع')
    type_2 = fields.Selection([('activity', 'نشاط'),('service', 'خدمة'), ('process', 'عملية')], string='النوع 2')
    responsable_id = fields.Many2one('res.partner', string='المسؤول')
    priority = fields.Selection([('very_high', 'مرتفع جداً'), ('high', 'مرتفع'), ('average', 'متوسط')], string='الأولوية')
    rate_ratio = fields.Integer(string='نسبة الإنجاز', compute='compute_rate_ratio', store=True)
    rate_non_ratio = fields.Integer(string='نسبة غير منجزة', compute='_compute_rate_non_ratio', store=True)
    pilliar_ids = fields.One2many('dh.pilliar', related='orientation_id.pilliar_ids', string='المحاور')

    @api.depends('actual', 'target')
    def compute_rate_ratio(self):
        for rec in self:
            if rec.target > 0:
                rec.rate_ratio = (rec.actual / rec.target) * 100
            else:
                rec.rate_ratio = 0

    @api.depends('rate_ratio')
    def _compute_rate_non_ratio(self):
        for rec in self:
            rec.rate_non_ratio = 100 - rec.rate_ratio

    date_start = fields.Date(string='تاريخ البدء')
    date_end = fields.Date(string='تاريخ الإنتهاء')
    type_operation = fields.Selection([('operational', 'تشغيلية'), ('capacity', 'القدرات')], string='نوع الادخال')
    standard_government_system_id = fields.Many2many('dh.government.system', string='معايير منظومة التميز الحكومي')
    strategic_indicator_id = fields.Many2one('dh.icesco.strategic.indicator', string='مؤشر استراتيجي')
    operational_indecator_ids = fields.One2many('dh.icesco.operational.indicators', 'operational_plan_id', string='المؤشرات التشغيلية')
    operational_indecator_id = fields.Char(string='المؤشرات التشغيلية')
    respect_time = fields.Integer(string='الالتزام بالوقت')
    respect_time_compute = fields.Integer(string='الالتزام بالوقت', compute='compute_respect_time')
    target = fields.Integer(string='المستهدف', compute='compute_target')
    actual = fields.Integer(string='الفعلي', compute='compute_actual')
    # project_id = fields.Many2one('project.project', string='المحور')
    # pilliar_id = fields.Many2one('dh.pilliar', string='المحور')
    operational_indecator_result_ids = fields.One2many('dh.icesco.operational.indicators.result', 'operational_plan_id',
                                                string='نتائج المؤشرات التشغيلية')
    percentage_of_done = fields.Integer(string='نسبة النتائج', compute='_compute_percentage_of_done')
    percentage_of_done_percent = fields.Char(string='نسبة النتائج', compute='_compute_percentage_of_done', store=True)

    @api.depends('operational_indecator_ids', 'operational_indecator_result_ids')
    def _compute_percentage_of_done(self):
        for rec in self:
            rec.percentage_of_done = 0
            rec.percentage_of_done_percent = 0
            if len(rec.operational_indecator_ids) > 0:
                rec.percentage_of_done = len(rec.operational_indecator_result_ids.filtered(lambda x: x.is_done == True).mapped('operational_indicator_id')) / len(rec.operational_indecator_ids) * 100
                rec.percentage_of_done_percent = rec.percentage_of_done / 100

    @api.depends('respect_time')
    def compute_respect_time(self):
        for rec in self:
            rec.respect_time_compute = rec.respect_time

    @api.depends('operational_indecator_ids.target')
    def compute_target(self):
        for rec in self:
            if len(rec.operational_indecator_ids) > 0:
                rec.target = sum(rec.operational_indecator_ids.mapped('target')) / len(rec.operational_indecator_ids)
            else:
                rec.target = 0

    @api.depends('operational_indecator_ids.actual')
    def compute_actual(self):
        for rec in self:
            if len(rec.operational_indecator_ids) > 0:
                rec.actual = sum(rec.operational_indecator_ids.mapped('actual')) / len(rec.operational_indecator_ids)
            else:
                rec.actual = 0

    @api.model
    def create(self, vals):
        vals['sequence'] = len(self.env['dh.icesco.operational.plan'].search([])) + 1
        return super(DhIcescoOperationalPlan, self).create(vals)

    def view_group_by_none(self):
        return {
            'name': ".",
            'res_model': 'dh.icesco.operational.plan',
            'view_mode': 'tree,form',
            'view_type': 'tree',
            'views': [(self.env.ref("dh_icesco_project.dh_icesco_operational_plan_tree").id, 'list'), (self.env.ref("dh_icesco_project.dh_icesco_operational_plan_form_view").id, 'form')],
            'type': 'ir.actions.act_window',
            'domain': [('type_operation', '=', 'operational')] + self.ids,
            'context': {
                'default_type_operation': 'operational',
            },
        }

    def view_group_by_goal(self):
        return {
            'name': ".",
            'res_model': 'dh.icesco.operational.plan',
            'view_mode': 'tree,form',
            'view_type': 'tree',
            'views': [(self.env.ref("dh_icesco_project.dh_icesco_operational_plan_tree").id, 'list'), (self.env.ref("dh_icesco_project.dh_icesco_operational_plan_form_view").id, 'form')],
            'type': 'ir.actions.act_window',
            'domain': [('type_operation', '=', 'operational')] + self.ids,
            'context': {
                'default_type_operation': 'operational',
                'group_by': 'orientation_id',
            },
        }

    def view_group_by_expert(self):
        return {
            'name': ".",
            'res_model': 'dh.icesco.operational.plan',
            'view_mode': 'tree,form',
            'view_type': 'tree',
            'views': [(self.env.ref("dh_icesco_project.dh_icesco_operational_plan_tree").id, 'list'), (self.env.ref("dh_icesco_project.dh_icesco_operational_plan_form_view").id, 'form')],
            'type': 'ir.actions.act_window',
            'domain': [('type_operation', '=', 'operational')] + self.ids,
            'context': {
                'default_type_operation': 'operational',
                'group_by': 'responsable_id',
            },
        }

    def view_group_by_sector(self):
        return {
            'name': ".",
            'res_model': 'dh.icesco.operational.plan',
            'view_mode': 'tree,form',
            'view_type': 'tree',
            'views': [(self.env.ref("dh_icesco_project.dh_icesco_operational_plan_tree").id, 'list'), (self.env.ref("dh_icesco_project.dh_icesco_operational_plan_form_view").id, 'form')],
            'type': 'ir.actions.act_window',
            'domain': [('type_operation', '=', 'operational')] + self.ids,
            'context': {
                'default_type_operation': 'operational',
                'group_by': 'type',
            },
        }