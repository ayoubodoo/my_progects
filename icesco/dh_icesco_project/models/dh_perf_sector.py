# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DhPerfSector(models.Model):
    _name = 'dh.perf.sector'

    name = fields.Char(translate=True , string='إسم')
    # goal_ids = fields.One2many('dh.orientations', 'sector_id', string='الأهداف')
    all_project_ids = fields.One2many('project.project', 'sector_id', string='المشاريع', store=True)
    project_ids = fields.Many2many('project.project', relation='rel_projects_sector', string='المشاريع', compute='compute_projects_sector', store=True)
    mission_ids = fields.One2many('project.task', 'sector_id', string='المهام', store=True, domain=[('is_mission', '=', True)])
    account_analytic_id = fields.Many2one("account.analytic.account", string="Analytic account", store=True)
    account_analytic_line_ids = fields.One2many('account.analytic.line', 'secteur_id', string='Account Analytic Lines')
    budget_icesco_reel = fields.Float(string='مصروفات المحققة', compute='_compute_budget_reel', store=True)
    budget_icesco_prevision = fields.Float(string='مصروفات المتوقعة', compute='_compute_budget_prevision', store=True)
    budget_hors_icesco_reel = fields.Float(string='المزانية الخارجية المحققة', compute='_compute_budget_hors_reel', store=True)
    budget_hors_icesco_prevision = fields.Float(string='المزانية الخارجية المتوقعة', compute='_compute_budget_hors_prevision', store=True)
    count_mission = fields.Integer(string='عدد المهام', compute='compute_count_mission', store=True)
    expense_mission = fields.Float(string='ميزانية المهام', compute='compute_expense_mission', store=True)
    email = fields.Char(string='Email')


    @api.depends('all_project_ids')
    def compute_projects_sector(self):
        for rec in self:
            rec.project_ids = False
            for project in rec.all_project_ids.filtered(lambda x:x.is_mission == False):
                rec.project_ids = [(4, project.id)]

    # @api.depends('all_project_ids.task_ids')
    # def compute_missions_sector(self):
    #     for rec in self:
    #         rec.mission_ids = False
    #         for task in rec.all_project_ids.mapped('task_ids').filtered(lambda x: x.is_mission == True):
    #             rec.mission_ids = [(4, task.id)]

    @api.depends('mission_ids')
    def compute_count_mission(self):
        for rec in self:
            rec.count_mission = len(rec.mission_ids)

    @api.depends('mission_ids')
    def compute_expense_mission(self):
        for rec in self:
            rec.expense_mission = sum(rec.mission_ids.mapped('expenses_ids').filtered(lambda x:x.state in ['approved', 'done']).mapped('total_amount'))

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if 'account_analytic_id' in vals:
            res.account_analytic_id.write({'secteur_id': res.id})
        return res

    def write(self, vals):
        res = super().write(vals)
        if 'account_analytic_id' in vals:
            self.account_analytic_id.write({'secteur_id': self.id})
        return res

    # masrofat icesco reel
    @api.depends('account_analytic_line_ids')
    def _compute_budget_reel(self):
        for rec in self:
            rec.budget_icesco_reel = abs(sum(rec.account_analytic_line_ids.filtered(lambda x:x.amount < 0).mapped('amount')))

    # masrofat icesco prevision
    @api.depends('project_ids')

    def _compute_budget_prevision(self):
        for rec in self:
            rec.budget_icesco_prevision = sum(rec.project_ids.task_ids.mapped('budget_icesco'))

    # mizania hors icesco réel
    @api.depends('account_analytic_line_ids')
    def _compute_budget_hors_reel(self):
        for rec in self:
            rec.budget_hors_icesco_reel = sum(rec.account_analytic_line_ids.filtered(lambda x:x.amount > 0).mapped('amount'))

    # mizania hors icesco prevision
    @api.depends('project_ids')
    def _compute_budget_hors_prevision(self):
        for rec in self:
            rec.budget_hors_icesco_prevision = sum(rec.project_ids.task_ids.mapped('budget_out_icesco'))

class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    secteur_id = fields.Many2one('dh.perf.sector', string='Secteur')

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    secteur_id = fields.Many2one('dh.perf.sector', string='Secteur', related='account_id.secteur_id')

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if 'amount' in vals:
            if res.secteur_id.id != False:
                res.secteur_id._compute_budget_reel()
                res.secteur_id._compute_budget_hors_reel()
        return res

    def write(self, vals):
        res = super().write(vals)
        if 'amount' in vals:
            if self.secteur_id.id != False:
                self.secteur_id._compute_budget_reel()
                self.secteur_id._compute_budget_hors_reel()
        return res
