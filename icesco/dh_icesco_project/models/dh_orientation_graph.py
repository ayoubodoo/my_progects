# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DhOrientationGraph(models.Model):
    _name = 'dh.orientations.graph'

    name = fields.Char(translate=True, string='إسم')
    type = fields.Selection([('done', 'Done'), ('not_done', 'Not Done')], string='Type')
    value = fields.Float(string='Percentage', store=True, compute='onchange_type') #  : comment juste pour change valeur presentation
    orientation_ids = fields.Many2many('dh.orientations', string='Orientations', compute='compute_dh_orientations')

    # : comment juste pour change valeur presentation
    @api.depends('type')
    def onchange_type(self):
        for rec in self:
            if rec.type == 'done':
                rec.value = sum(self.env['dh.orientations'].search([]).mapped('percentage_of_done')) / len(self.env['dh.orientations'].search([]))
            if rec.type == 'not_done':
                rec.value = 100 - (sum(self.env['dh.orientations'].search([]).mapped('percentage_of_done')) / len(self.env['dh.orientations'].search([])))

    @api.depends('type')
    def compute_dh_orientations(self):
        for rec in self:
            rec.orientation_ids = [(4, orientation.id) for orientation in self.env['dh.orientations'].search([])]

    def recalcule_button(self):
        for rec in self:
            rec.onchange_type()
            rec.compute_dh_orientations() # : comment juste pour change valeur presentation