# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DhCrossoveredBudget(models.Model):
    _inherit = 'crossovered.budget'

    project_id = fields.Many2one("project.project", string="Project")
    analytic_account_id = fields.Many2one(
        "account.analytic.account", string="Default Analytic Account"
    )
    is_budget_icesco = fields.Boolean(string='Budget Icesco?')
    is_budget_extra_reel = fields.Boolean(string='Budget Extra reel?')
    is_budget_extra_indirect = fields.Boolean(string='Budget Extra indirect?')

class DhCrossoveredBudgetLines(models.Model):
    _inherit = 'crossovered.budget.lines'

    task_id = fields.Many2one('project.task')
    project_id = fields.Many2one("project.project", string="Project", related='crossovered_budget_id.project_id')
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account')
    is_budget_icesco = fields.Boolean(string='Budget Icesco?', related='crossovered_budget_id.is_budget_icesco')
    is_budget_extra_reel = fields.Boolean(string='Budget Extra reel?', related='crossovered_budget_id.is_budget_extra_reel')
    is_budget_extra_indirect = fields.Boolean(string='Budget Extra indirect?', related='crossovered_budget_id.is_budget_extra_indirect')