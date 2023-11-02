# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DhTaskGraph(models.Model):
    _name = 'dh.task.graph'

    name = fields.Char(translate=True, string='إسم')
    type = fields.Selection([('done', 'Done'), ('not_done', 'Not Done')], string='Type')
    value_taux_livraison = fields.Float(string='Percentage taux livraison', compute='onchange_task_taux_livraison_type', store=True)
    value_taux_realisation = fields.Float(string='Percentage taux réalisation', compute='onchange_task_taux_realisation_type', store=True)
    task_ids = fields.Many2many('project.task', string='Activité', compute='compute_dh_tasks')

    @api.depends('type')
    def onchange_task_taux_livraison_type(self):
        for rec in self:
            if rec.type == 'done':
                rec.value_taux_livraison = sum(self.env['project.task'].search([('pencentage_report', '>', 0), ('is_mission', '=', True)]).mapped('pencentage_report')) / len(
                    self.env['project.task'].search([('is_mission', '=', True)]))
            if rec.type == 'not_done':
                rec.value_taux_livraison = 100 - (sum(self.env['project.task'].search([('pencentage_report', '>', 0), ('is_mission', '=', True)]).mapped('pencentage_report')) / len(
                    self.env['project.task'].search([('is_mission', '=', True)])))

    @api.depends('type')
    def onchange_task_taux_realisation_type(self):
        for rec in self:
            if rec.type == 'done':
                rec.value_taux_realisation = sum(
                    self.env['project.task'].search([('pencentage_done', '>', 0), ('is_mission', '=', True)]).mapped('pencentage_done')) / len(
                    self.env['project.task'].search([('is_mission', '=', True)]))
            if rec.type == 'not_done':
                rec.value_taux_realisation = 100 - (sum(
                    self.env['project.task'].search([('pencentage_done', '>', 0), ('is_mission', '=', True)]).mapped('pencentage_done')) / len(
                    self.env['project.task'].search([('is_mission', '=', True)])))

    @api.depends('type')
    def compute_dh_tasks(self):
        for rec in self:
            rec.task_ids = [(4, task.id) for task in self.env['project.task'].search([('is_mission', '=', True)])]

    def recalcule_button(self):
        for rec in self:
            rec.onchange_type()
            rec.compute_dh_orientations()