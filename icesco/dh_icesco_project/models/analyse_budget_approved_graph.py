# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AnalyseBudgetApprovedGraph(models.Model):
    _name = 'analyse.budget.approved.graph'

    name = fields.Char(translate=True, string='إسم')
    type = fields.Selection([('budget_consommed', 'Budget Consommed'), ('budget_proposed', 'Budget Proposed')], string='Type')
    value = fields.Float(string='Percentage', compute='onchange_type', store=True)
    analyse_budget_ids = fields.Many2many('analyse.budget.approved', string='Budgets', compute='compute_analyse_budget')

    @api.depends('type')
    def onchange_type(self):
        for rec in self:
            if rec.type == 'budget_consommed':
                rec.value = sum(self.env['analyse.budget.approved'].search([]).mapped('budget_consommed'))
            if rec.type == 'budget_proposed':
                rec.value = sum(self.env['analyse.budget.approved'].search([]).mapped('budget_proposed'))

    @api.depends('type')
    def compute_analyse_budget(self):
        for rec in self:
            rec.analyse_budget_ids = [(4, budget.id) for budget in self.env['analyse.budget.approved'].search([])]

    def recalcule_button(self):
        for rec in self:
            rec.onchange_type()
            rec.compute_analyse_budget()