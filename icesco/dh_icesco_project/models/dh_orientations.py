# -*- coding: utf-8 -*-
from odoo import models, fields, api


class DhOrientations(models.Model):
    _name = 'dh.orientations'

    code = fields.Char(string='Code')
    name = fields.Char(translate=True ,string='إسم')
    short_name = fields.Char(string='مختصر')
    # sector_id = fields.Many2one('dh.perf.sector', string='القطاع')
    pilliar_ids = fields.One2many('dh.pilliar', 'orientation_id', string='المحاور')
    percentage_of_done = fields.Integer(string='نسبة النتائج', compute='compute_percentage_of_done')
    percentage_of_done_stored = fields.Integer(string='نسبة النتائج', compute='compute_percentage_of_done', store=True)
    percentage_of_done_percent = fields.Char(string='نسبة النتائج', compute='compute_percentage_of_done', store=True)
    is_done = fields.Boolean(string='منجز', compute='compute_percentage_of_done')
    strategic_indicator_ids = fields.One2many('dh.icesco.operational.plan', 'orientation_id', string='المؤشرات الإستراتيجية')

    def name_get(self):
        result = []
        for rec in self:
            if rec.short_name:
                name = rec.short_name
                if rec.code:
                    name = " . ".join([rec.code, name])
                result.append((rec.id, name))
            else:
                name = rec.name
                result.append((rec.id, name))
        return result

    @api.depends('pilliar_ids.percentage_of_done')
    def compute_percentage_of_done(self):
        for rec in self:
            rec.is_done = False
            if len(rec.mapped('pilliar_ids')) > 0:
                rec.percentage_of_done = sum(rec.mapped('pilliar_ids').mapped('percentage_of_done')) / len(
                    rec.mapped('pilliar_ids'))
                if rec.percentage_of_done == 100:
                    rec.is_done = True
            else:
                rec.percentage_of_done = 0
            rec.percentage_of_done_stored = rec.percentage_of_done
            rec.percentage_of_done_percent = rec.percentage_of_done / 100

            for global_orientation in rec.env['dh.orientations.graph'].search([]):
                global_orientation.onchange_type() # comment juste pour change valeur presentation

    def view_show_pillars(self):
        for rec in self:
            return {
                'name': "Pillars",
                'res_model': 'dh.pilliar',
                'view_mode': 'kanban,tree',
                'view_type': 'kanban',
                'views': [(self.env.ref("dh_icesco_project.view_dh_pilliar_kanban_3").id, 'kanban')],
                'type': 'ir.actions.act_window',
                "domain": [("id", "in", self.pilliar_ids.ids)],
            }

    def view_form_orientation(self):
        for rec in self:
            return {
                'name': "التفاصيل",
                'res_model': 'dh.orientations',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': rec.id,
                'view_id': self.env.ref("dh_icesco_project.dh_icesco_orientations_form_view").id,
            }
