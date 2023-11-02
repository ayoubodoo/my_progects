# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DhIcescoPilliar(models.Model):
    _name = 'dh.icesco.pilliar'

    name = fields.Char(translate=True,string='محور')

class DhPilliar(models.Model):
    _name = 'dh.pilliar'
    _order = 'code'

    code = fields.Char(string='Code')
    name = fields.Many2one('dh.icesco.pilliar', required=True,string='محور',translate=True)
    name_name = fields.Char(string='محور',translate=True, related='name.name')
    orientation_id = fields.Many2one('dh.orientations', store=True, string='الهدف')
    project_ids = fields.One2many('project.project', 'pilliar_id', string='المشاريع', store=True)
    respect_time = fields.Integer(string='الالتزام بالوقت', compute='compute_respect_time')
    target = fields.Integer(string='المستهدف', compute='compute_target')
    actual = fields.Integer(string='الفعلي', compute='compute_actual')
    percentage_of_done = fields.Integer(string='نسبة النتائج', compute='compute_percentage_of_done')
    percentage_of_done_stored = fields.Integer(string='نسبة النتائج', compute='compute_percentage_of_done', store=True)
    percentage_of_done_percent = fields.Char(string='نسبة النتائج', compute='compute_percentage_of_done', store=True)
    is_done = fields.Boolean(string='منجز', compute='compute_percentage_of_done')

    def name_get(self):
        result = []
        for rec in self:

            name = rec.name.name
            if rec.code:
                name = " . ".join([rec.code, name])
            result.append((rec.id, name))
        return result

    def count_my_projects(self):
        for rec in self:
            return len(rec.project_ids) # .filtered(lambda x:x.create_uid.id == self.env.uid)

    @api.depends('project_ids.percentage_of_done')
    def compute_percentage_of_done(self):
        for rec in self:
            if len(rec.mapped('project_ids')) > 0:
                rec.percentage_of_done = sum(rec.mapped('project_ids').mapped('percentage_of_done')) / len(
                    rec.mapped('project_ids'))
                if rec.percentage_of_done == 100:
                    rec.is_done = True
            else:
                rec.percentage_of_done = 0
            rec.percentage_of_done_stored = rec.percentage_of_done
            rec.percentage_of_done_percent = rec.percentage_of_done / 100

            for global_pilliar in rec.env['dh.pilliar.graph'].search([]):
                global_pilliar.onchange_type()

    @api.depends('project_ids.respect_time')
    def compute_respect_time(self):
        for rec in self:
            if len(rec.mapped('project_ids')) > 0:
                rec.respect_time = sum(rec.mapped('project_ids').mapped('respect_time')) / len(
                    rec.mapped('project_ids'))
            else:
                rec.respect_time = 0

    @api.depends('project_ids.target')
    def compute_target(self):
        for rec in self:
            if len(rec.mapped('project_ids')) > 0:
                rec.target = sum(rec.mapped('project_ids').mapped('target')) / len(rec.mapped('project_ids'))
            else:
                rec.target = 0

    @api.depends('project_ids.actual')
    def compute_actual(self):
        for rec in self:
            if len(rec.mapped('project_ids')) > 0:
                rec.actual = sum(rec.mapped('project_ids').mapped('actual')) / len(rec.mapped('project_ids'))
            else:
                rec.actual = 0

    def view_show_projects(self):
        for rec in self:
            return {
                'name': "المشاريع",
                'res_model': 'project.project',
                'view_mode': 'kanban,form',
                'view_type': 'kanban',
                'views': [(self.env.ref("dh_icesco_project.view_dh_project_project_kanban_2").id, 'kanban')],
                'type': 'ir.actions.act_window',
                "domain": [("pilliar_id", "=", rec.id)],
                'context': "{'default_pilliar_id': %s}" % rec.id
            }

    def view_form_pilliar(self):
        for rec in self:
            return {
                'name': "التفاصيل",
                'res_model': 'dh.pilliar',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': rec.id,
                'view_id': self.env.ref("dh_icesco_project.dh_icesco_pilliar_form_view").id,
            }

    @api.model
    def pillars_possible_search_read(self, **args):
        res = self.env['dh.pilliar'].sudo().search_read(domain=[(
            'orientation_id', '=', args['goal'])], offset=args['offset'], limit=args['limit'], fields=args['fields'])
        return res