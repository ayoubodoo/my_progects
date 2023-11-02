# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DhAgreementsInternationalSectors(models.Model):
    _name = 'dh.agreements.international.sectors'

    agreement_id = fields.Many2one('dh.agreements.international', string='Agreement international')
    sector_id = fields.Many2one('dh.perf.sector', string='Sector')
    received_amount = fields.Float(string='Obtained budget')
    received_amount_prevu = fields.Float(string='Expected budget')
    facet_exchange = fields.Char(string='Facets of exchange')

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if 'received_amount' in vals and ('agreement_id' in vals or res.agreement_id != False):
            res.agreement_id.write({'received_amount': sum(self.env['dh.agreements.international.sectors'].search([('agreement_id', '=', res.agreement_id.id)]).mapped('received_amount'))})
        if 'received_amount_prevu' in vals and ('agreement_id' in vals or res.agreement_id != False):
            res.agreement_id.write({'received_amount_prevu': sum(self.env['dh.agreements.international.sectors'].search([('agreement_id', '=', res.agreement_id.id)]).mapped('received_amount_prevu'))})
        return res

    def write(self, vals):
        res = super().write(vals)
        if 'received_amount' in vals and ('agreement_id' in vals or self.agreement_id.id != False):
            self.agreement_id.write({'received_amount': sum(self.env['dh.agreements.international.sectors'].search(
                [('agreement_id', '=', self.agreement_id.id)]).mapped('received_amount'))})
        if 'received_amount_prevu' in vals and ('agreement_id' in vals or self.agreement_id.id != False):
            self.agreement_id.write({'received_amount_prevu': sum(self.env['dh.agreements.international.sectors'].search(
                [('agreement_id', '=', self.agreement_id.id)]).mapped('received_amount_prevu'))})
        return res