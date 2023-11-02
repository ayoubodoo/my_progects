# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ProjectTaskBudgetGraph(models.Model):
    _name = 'project.task.budget.graph'

    name = fields.Char(translate=True, string='إسم')
    type = fields.Selection([('budget_out_icesco', 'Budget alloué hors ISESCO'), ('budget_initial', 'Budget initial')], string='Type')
    value = fields.Float(string='Percentage', compute='onchange_type', store=True)
    tasks_ids = fields.Many2many('project.task', string='Tasks', compute='compute_tasks')

    @api.depends('type')
    def onchange_type(self):
        for rec in self:
            if rec.type == 'budget_out_icesco':
                rec.value = sum(self.env['project.task'].search([]).mapped('budget_out_icesco'))
            if rec.type == 'budget_initial':
                rec.value = sum(self.env['project.task'].search([]).mapped('budget_initial'))

    @api.depends('type')
    def compute_tasks(self):
        for rec in self:
            rec.tasks_ids = [(4, task.id) for task in self.env['project.task'].search([])]

    def recalcule_button(self):
        for rec in self:
            rec.onchange_type()
            rec.compute_tasks()