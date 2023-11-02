# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DhIcescoPlanStrategies(models.Model):
    _name = 'dh.icesco.plan.strategies'
    _rec_name= 'strategie'

    strategie = fields.Many2one('dh.strategies', string='الخطط الإستراتيجية')
    date = fields.Date(string='تاريخ')
    plan_strategies_kanban_ids = fields.One2many('dh.icesco.plan.strategies.kanban', 'dh_icesco_plan_strategy_id', string='التفاصيل')
    goal_strategies_kanban_ids = fields.One2many('dh.icesco.goal.strategies.kanban', 'dh_icesco_plan_strategy_id',
                                                 string='التفاصيل 2')

class DhIcescoPlanStrategiesKanban(models.Model):
    _name = 'dh.icesco.plan.strategies.kanban'
    _order = 'sequence'

    name = fields.Char(string='إسم', readonly=False)
    description = fields.Text(translate=True,string='وصف', readonly=False)
    image = fields.Binary(string='الصورة', attachment=True, readonly=False)
    sequence = fields.Integer(string='متسلسل')
    dh_icesco_plan_strategy_id = fields.Many2one('dh.icesco.plan.strategies', string='إستراتيجية التخطيط')

    @api.model
    def create(self, vals):
        vals['sequence'] = len(self.env['dh.icesco.plan.strategies.kanban'].search([])) + 1
        return super(DhIcescoPlanStrategiesKanban, self).create(vals)

    def action_orientation_button(self):
        for rec in self:
            return {
                "name": "المؤشرات الإستراتيجية",
                "view_mode": "kanban,form",
                "res_model": "dh.icesco.operational.plan",
                "type": "ir.actions.act_window",
                # "context": context,
                'views': [(self.env.ref("dh_icesco_project.view_dh_icesco_operational_plan_kanban_2").id, 'kanban'), (self.env.ref("dh_icesco_project.dh_icesco_operational_plan_form_view").id, 'form')],
                "domain": [("orientation_id", "=", rec.env['dh.orientations'].search([('name', '=', rec.name)]).id)],
            }