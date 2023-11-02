# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DhPilliarGraph(models.Model):
    _name = 'dh.pilliar.graph'

    name = fields.Char(translate=True, string='إسم')
    type = fields.Selection([('done', 'Done'), ('not_done', 'Not Done')], string='Type')
    value = fields.Float(string='Percentage', compute='onchange_type', store=True)
    pilliar_ids = fields.Many2many('dh.pilliar', string='Orientations', compute='compute_dh_pilliars')

    @api.depends('type')
    def onchange_type(self):
        for rec in self:
            if rec.type == 'done':
                rec.value = sum(self.env['dh.pilliar'].search([('percentage_of_done', '>', 0)]).mapped('percentage_of_done')) / len(self.env['dh.pilliar'].search([]))
            if rec.type == 'not_done':
                rec.value = 100 - (sum(self.env['dh.pilliar'].search([('percentage_of_done', '>', 0)]).mapped('percentage_of_done')) / len(self.env['dh.pilliar'].search([])))

    @api.depends('type')
    def compute_dh_pilliars(self):
        for rec in self:
            rec.pilliar_ids = [(4, pilliar.id) for pilliar in self.env['dh.pilliar'].search([])]

    def recalcule_button(self):
        for rec in self:
            rec.onchange_type()
            rec.compute_dh_orientations()