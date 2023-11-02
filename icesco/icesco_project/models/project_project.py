# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime



class ProjectProject(models.Model):
    _name = 'project.project'
    _inherit = ['project.project', 'mail.thread', 'mail.activity.mixin']

    state = fields.Selection(
        [('initial', 'Initial Stage'), ('in_progress', 'In progress'),
         ('executed', 'Executed')], string="State", default='initial', related='project_status.state')

    code = fields.Char(string='Project code',required=False)
    description = fields.Text(translate=True,string='Description')
    expert_id = fields.Many2one('hr.employee',string='Expert in charge')
    geographical_id = fields.Many2many('res.geographical',string='Geographical scope')
    zone_id = fields.Many2many('res.continent',string='Zone')
    country_id = fields.Many2many('res.country', relation="project_country_rel", string='Country')
    nature_ids = fields.One2many('project.nature','project_id',string='Nature of '
                                                                'intervention')
    category_ids = fields.Many2many('project.beneficiary.category',string='Beneficiary '
                                                                      'category')
    pays_cibles = fields.Many2one('dh.pays.cible',string="Pays cibles")

    number = fields.Integer('Number of beneficiaries')
    lieu = fields.Many2many('res.partner', string="Place of performance")
    date_start = fields.Date(string="Start date")
    date_end = fields.Date(string="End date")
    duration = fields.Float(string="Duration", compute='compute_duration')
    notes = fields.Text(translate=True,string="Notes")
    req_count = fields.Integer('Number of requests',compute='smart_count')
    expense_count = fields.Integer('Number of expenses',compute='smart_count')
    order_count = fields.Integer('Number of orders',compute='smart_count')
    expenseshifting_count = fields.Integer('Number of missions',compute='smart_count')
    event_count = fields.Integer('Number of events',compute='smart_count')
    intervention_type_ids = fields.Many2many('intervention.type', string="Intervention Type")
    stakeholder_ids = fields.One2many('res.stakeholder', 'project_id', string="Stakeholders")
    activity_reference_ids = fields.Many2many('activity.reference', string="Activity Reference")
    department_id = fields.Many2one('hr.department', string="Department")
    execution_country_ids = fields.Many2many('res.country', relation="project_execution_country_rel", string="Execution Country")
    city_ids = fields.Many2many('res.city', string="City")

    part = fields.Float(string="Icesco Part")
    is_late = fields.Boolean(string='Late', compute='compute_is_late', store=True)
  # budget
    budget = fields.Float(string="Initial Budget", compute='get_project_initial_budget', store=True)

    @api.depends('task_ids')
    def get_project_initial_budget(self):
        for rec in self:
            rec.budget = 0
            if rec.task_ids:
                for line in rec.task_ids:
                    if line.budget_initial:
                        rec.budget = rec.budget + line.budget_initial

    @api.depends('date_end')
    def compute_is_late(self):
        for rec in self:
            rec.is_late = False
            if rec.date_end:
                if rec.date_end < datetime.now().date():
                    rec.is_late = True

    @api.depends('date_start', 'date_end')
    def compute_duration(self):
        for r in self:
            r.duration = 0
            if r.date_end and r.date_start:
                r.duration = (r.date_end - r.date_start).days

    def smart_count(self):
        for rec in self:
            rec.req_count = len(
                self.env['purchase.request'].search([('project_id', '=', self.id)]))
            rec.expense_count = len(
                self.env['hr.expense'].search([('project_id', '=', self.id)]))
            rec.order_count = len(
                self.env['purchase.order'].search([('project_id', '=', self.id)]))
            rec.expenseshifting_count = len(
                self.env['hr.expense.shifting'].search([('project_id', '=', self.id)]))
            rec.event_count = len(
                self.env['event.event'].search([('project_id', '=', self.id)]))

    def purchase_request(self):
        self.ensure_one()
        domain = [
            ('project_id', '=', self.id),
        ]
        return {
            'name': _('Purchase requests'),
            'domain': domain,
            'res_model': 'purchase.request',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'limit': 80,
            'context': "{'default_project_id': %s}" % self.id
        }

    def expense(self):
        self.ensure_one()
        domain = [
            ('project_id', '=', self.id),
        ]
        return {
            'name': _('Expenses'),
            'domain': domain,
            'res_model': 'hr.expense',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'limit': 80,
            'context': "{'default_project_id': %s}" % self.id
        }

    def purchase_order(self):
        self.ensure_one()
        domain = [
            ('project_id', '=', self.id),
        ]
        return {
            'name': _('Purchase orders'),
            'domain': domain,
            'res_model': 'purchase.order',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'limit': 80,
            'context': "{'default_project_id': %s}" % self.id
        }

    def expense_shifting(self):
        self.ensure_one()
        domain = [
            ('project_id', '=', self.id),
        ]
        return {
            'name': _('Missions'),
            'domain': domain,
            'res_model': 'hr.expense.shifting',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'limit': 80,
            'context': "{'default_project_id': %s}" % self.id
        }

    def events(self):
        self.ensure_one()
        domain = [
            ('project_id', '=', self.id),
        ]
        return {
            'name': _('Events'),
            'domain': domain,
            'res_model': 'event.event',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'view_type': 'form',
            'limit': 80,
            'context': "{'default_project_id': %s}" % self.id
        }
