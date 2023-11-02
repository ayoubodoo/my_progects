# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DhAgreementsInternationalGraph(models.Model):
    _name = 'dh.agreements.international.graph'

    name = fields.Char(translate=True, string='إسم')
    type = fields.Selection([('received_amount', 'Obtained budget'), ('received_amount_prevu', 'Expected budget')], string='Type')
    value = fields.Float(string='Percentage', compute='onchange_type', store=True)
    agreements_ids = fields.Many2many('dh.agreements.international', string='Agreements International', compute='compute_agreements')

    @api.depends('type')
    def onchange_type(self):
        for rec in self:
            if rec.type == 'received_amount':
                rec.value = sum(self.env['dh.agreements.international'].search([]).mapped('received_amount'))
            if rec.type == 'received_amount_prevu':
                rec.value = sum(self.env['dh.agreements.international'].search([]).mapped('received_amount_prevu'))

    @api.depends('type')
    def compute_agreements(self):
        for rec in self:
            rec.agreements_ids = [(4, agreement.id) for agreement in self.env['dh.agreements.international'].search([])]

    def recalcule_button(self):
        for rec in self:
            rec.onchange_type()
            rec.compute_agreements()