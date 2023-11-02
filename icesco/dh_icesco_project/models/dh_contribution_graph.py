# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DhContributionGraph(models.Model):
    _name = 'dh.contribution.graph'

    name = fields.Char(translate=True, string='إسم')
    type = fields.Selection([('amount', 'Amount from contrubutions'), ('amount_not_paid', 'Inpaid Balance')], string='Type')
    value = fields.Float(string='Percentage', compute='onchange_type', store=True)
    contribution_ids = fields.Many2many('dh.contrubution', string='Contributions', compute='compute_agreements')

    @api.depends('type')
    def onchange_type(self):
        for rec in self:
            if rec.type == 'amount':
                rec.value = sum(self.env['dh.contrubution'].search([]).mapped('amount'))
            if rec.type == 'amount_not_paid':
                rec.value = sum(self.env['dh.contrubution'].search([]).mapped('amount_not_paid'))

    @api.depends('type')
    def compute_agreements(self):
        for rec in self:
            rec.contribution_ids = [(4, contribution.id) for contribution in self.env['dh.contrubution'].search([])]

    def recalcule_button(self):
        for rec in self:
            rec.onchange_type()
            rec.compute_agreements()