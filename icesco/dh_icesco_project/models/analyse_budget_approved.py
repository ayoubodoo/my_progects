# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AnalyseBudgetApproved(models.Model):
    _name = 'analyse.budget.approved'

    sequence = fields.Char(string='Sequence')
    type = fields.Char(string='Type')
    name = fields.Char(string='Name')
    budget_approved = fields.Float(string='Budget Approved')
    budget_consommed = fields.Float(string='Budget Consommed')
    percentage_budget_consommed = fields.Float(string='Percentage Budget Consommed', compute='compute_percentage_budget_residual')
    budget_residual = fields.Float(string='Budget Residual', compute='compute_percentage_budget_residual')
    percentage_budget_residual = fields.Float(string='Percentage Budget Residual', compute='compute_percentage_budget_residual')
    budget_initial = fields.Float(string='Budget Initial')
    percentage_budget_initial = fields.Float(string='Percentage Budget Initial', compute='compute_percentage_budget_initial')
    budget_proposed = fields.Float(string='Budget Proposed')
    percentage_budget_proposed = fields.Float(string='Percentage Budget Proposed', compute='compute_percentage_budget_proposed')
    difference_budget = fields.Float(string='Difference Budget', compute='compute_difference_budget')
    percentage_difference_budget = fields.Float(string='Percentage Difference Budget', compute='compute_difference_budget')
    project_icesco = fields.Many2many('project.project', relation='rel_project_icesco', string='Project Essentially funded icesco')
    project_out_icesco = fields.Many2many('project.project', relation='rel_project_out_icesco', string='Project fully funded out icesco')
    project_semi_icesco = fields.Many2many('project.project', relation='rel_project_semi_icesco', string='Project semi funded out icesco')
    remarques = fields.Text(string='Remarks')

    @api.depends('budget_approved', 'budget_consommed')
    def compute_percentage_budget_residual(self):
        for rec in self:
            if rec.budget_approved != 0:
                rec.percentage_budget_consommed = rec.budget_consommed / rec.budget_approved
            else:
                rec.percentage_budget_consommed = 0

            rec.budget_residual = rec.budget_approved - rec.budget_consommed

            if rec.budget_approved != 0:
                rec.percentage_budget_residual = rec.budget_residual / rec.budget_approved
            else:
                rec.percentage_budget_residual = 0

    @api.depends('budget_approved', 'budget_initial')
    def compute_percentage_budget_initial(self):
        for rec in self:
            if rec.budget_approved != 0:
                rec.percentage_budget_initial = rec.budget_initial / rec.budget_approved
            else:
                rec.percentage_budget_initial = 0

    @api.depends('budget_approved', 'budget_proposed')
    def compute_percentage_budget_proposed(self):
        for rec in self:
            if rec.budget_approved != 0:
                rec.percentage_budget_proposed = rec.budget_proposed / rec.budget_approved
            else:
                rec.percentage_budget_proposed = 0


    @api.depends('budget_residual', 'budget_proposed')
    def compute_difference_budget(self):
        for rec in self:
            rec.difference_budget = rec.percentage_budget_residual - rec.budget_proposed

            if rec.percentage_budget_residual != 0:
                rec.percentage_difference_budget = rec.difference_budget / rec.percentage_budget_residual
            else:
                rec.percentage_difference_budget = 0