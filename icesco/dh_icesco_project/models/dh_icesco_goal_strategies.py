# -*- coding: utf-8 -*-
from odoo import models, fields, api
import requests

class DhIcescoGoalStrategies(models.Model):
    _name = 'dh.icesco.goal.strategies'
    _rec_name= 'strategie'

    strategie = fields.Many2one('dh.strategies', string='الخطط الإستراتيجية')
    date = fields.Date(string='تاريخ')
    goal_strategies_kanban_ids = fields.One2many('dh.icesco.goal.strategies.kanban', 'dh_icesco_goal_strategy_id', string='التفاصيل')


class DhIcescoGoalStrategiesKanban(models.Model):
    _name = 'dh.icesco.goal.strategies.kanban'
    _order = 'sequence'

    orientation_id = fields.Many2one('dh.orientations', string='الهدف')
    orientation_short_name = fields.Char(string='مختصر الهدف', related='orientation_id.short_name')
    dh_num_orientation = fields.Char(string='رقم الهدف', related='orientation_id.code')
    description = fields.Char(string='التفاصيل')
    percentage = fields.Integer(string='النسبة المئوية', related='orientation_id.percentage_of_done')
    sequence = fields.Integer(string='متسلسل')
    dh_icesco_goal_strategy_id = fields.Many2one('dh.icesco.goal.strategies', string='إستراتيجية التخطيط')
    dh_icesco_plan_strategy_id = fields.Many2one('dh.icesco.plan.strategies', string='إستراتيجية التخطيط')


    @api.model
    def create(self, vals):
        vals['sequence'] = len(self.env['dh.icesco.goal.strategies.kanban'].search([])) + 1
        return super(DhIcescoGoalStrategiesKanban, self).create(vals)

    def action_orientation_button(self):
        for rec in self:
            return {
                "name": "المؤشرات الإستراتيجية",
                "view_mode": "kanban,form",
                "res_model": "dh.icesco.operational.plan",
                "type": "ir.actions.act_window",
                # "context": context,
                'views': [(self.env.ref("dh_icesco_project.view_dh_icesco_operational_plan_kanban_2").id, 'kanban'), (self.env.ref("dh_icesco_project.dh_icesco_operational_plan_form_view").id, 'form')],
                "domain": [("orientation_id", "=", rec.orientation_id.id)],
            }

    # def action_project_project_button(self):
    #     for rec in self:
    #         for pilliar in rec.orientation_id.pilliar_ids:
    #             pilliar.compute_respect_time()
    #             pilliar.compute_target()
    #             pilliar.compute_actual()
    #             pilliar.compute_percentage_of_done()
    #
    #         return {
    #             "name": "المحاور",
    #             "view_mode": "tree,form",
    #             "res_model": "dh.pilliar",
    #             "type": "ir.actions.act_window",
    #             "context": "{'default_orientation_id': %s}" %(rec.orientation_id.id),
    #             'target': 'new',
    #             'views': [(self.env.ref("dh_icesco_project.dh_icesco_pilliar_wizard_tree").id, 'tree')],
    #             "domain": [("id", "in", rec.orientation_id.pilliar_ids.ids)],
    #         }

    def action_project_project_button(self):
        for rec in self:
            for pilliar in rec.orientation_id.pilliar_ids:
                pilliar.compute_respect_time()
                pilliar.compute_target()
                pilliar.compute_actual()
                pilliar.compute_percentage_of_done()

            return {
                "name": "المحاور",
                'view_type': 'form',
                'view_mode': 'form',
                "res_model": "dh.orientations",
                "type": "ir.actions.act_window",
                "context": "{'default_orientation_id': %s}" % (rec.orientation_id.id),
                'target': 'new',
                'views': [(self.env.ref("dh_icesco_project.dh_icesco_orientations_form_pilliars_view").id, 'form')],
                "res_id": rec.orientation_id.id,
            }

    # def action_project_button(self):
    #     for rec in self:
    #         for pilliar in rec.orientation_id.pilliar_ids:
    #             pilliar.compute_respect_time()
    #             pilliar.compute_target()
    #             pilliar.compute_actual()
    #             pilliar.compute_percentage_of_done()
    #         # return {
    #         #     "name": "المؤشرات الإستراتيجية",
    #         #     "view_mode": "kanban,form",
    #         #     "res_model": "dh.icesco.operational.plan",
    #         #     "type": "ir.actions.act_window",
    #         #     # "context": context,
    #         #     'views': [(self.env.ref("dh_icesco_project.view_dh_icesco_operational_plan_kanban").id, 'kanban')],
    #         #     "domain": [("id", "in", rec.orientation_id.pilliar_ids.mapped('strategic_indicator_ids').ids)],
    #         # }
    #         return {
    #         "name": "المؤشرات الإستراتيجية",
    #         "view_mode": "tree,form",
    #         "res_model": "dh.icesco.operational.plan",
    #         "type": "ir.actions.act_window",
    #         "context": "{'default_orientation_id': %s}" % (rec.orientation_id.id),
    #         'target': 'new',
    #         'views': [(self.env.ref("dh_icesco_project.dh_icesco_operational_plan_wizard_tree").id, 'tree')],
    #         "domain": [("id", "in", rec.orientation_id.mapped('strategic_indicator_ids').ids)],
    #         }

    def action_project_button(self):
        for rec in self:
            for pilliar in rec.orientation_id.pilliar_ids:
                pilliar.compute_respect_time()
                pilliar.compute_target()
                pilliar.compute_actual()
                pilliar.compute_percentage_of_done()
            # return {
            #     "name": "المؤشرات الإستراتيجية",
            #     "view_mode": "kanban,form",
            #     "res_model": "dh.icesco.operational.plan",
            #     "type": "ir.actions.act_window",
            #     # "context": context,
            #     'views': [(self.env.ref("dh_icesco_project.view_dh_icesco_operational_plan_kanban").id, 'kanban')],
            #     "domain": [("id", "in", rec.orientation_id.pilliar_ids.mapped('strategic_indicator_ids').ids)],
            # }
            return {
            "name": "المؤشرات الإستراتيجية",
            'view_type': 'form',
            'view_mode': 'form',
            "res_model": "dh.orientations",
            "type": "ir.actions.act_window",
            "context": "{'default_orientation_id': %s, 'create':False,'edit':False}" % (rec.orientation_id.id),
            'target': 'new',
            'views': [(self.env.ref("dh_icesco_project.dh_icesco_orientations_form_operational_plan_view").id, 'form')],
            "res_id": rec.orientation_id.id,

            }

    def view_group_by_orien(self):
        for rec in self:
            for pilliar in rec.orientation_id.pilliar_ids:
                pilliar.compute_respect_time()
                pilliar.compute_target()
                pilliar.compute_actual()
                pilliar.compute_percentage_of_done()
            return {
                'name': "نتائج المحاور",
                'res_model': 'dh.pilliar',
                'view_mode': 'kanban,form',
                'view_type': 'kanban',
                'views': [(self.env.ref("dh_icesco_project.view_dh_pilliar_kanban_3").id, 'kanban')],
                'type': 'ir.actions.act_window',
                "domain": [("orientation_id", "=", rec.orientation_id.id)],
                'context': "{'default_orientation_id': %s}" % rec.orientation_id.id
                # 'context': {
                #     'group_by': 'pillar_id.name',
                # },
            }




