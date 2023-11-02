# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class DhStrategicObjectives(models.Model):
    _name = 'dh.strategic.objectives'
    _description = 'Strategic objectives'
    _rec_name = 'seq'
    _order = 'seq'
    seq = fields.Char(required=False, readonly=True, copy=False, default=lambda self: _('New'))

    # seq = fields.Char(required=False, string="sequence", readonly=True, copy=False, default=lambda self: _('New'))
    name = fields.Text(string="Name", translate=True)
    projects_ids = fields.One2many('project.project','strategic_id', string='projects')

    @api.model
    def create(self, vals):
        if vals.get('seq', _('New')) == _('New'):
            vals['seq'] = self.env['ir.sequence'].next_by_code(
                'sequence_cps_icesco.dh.strategic.objectives') or _(
                'New')
        return super(DhStrategicObjectives, self).create(vals)

    # commission_team_id = fields.Many2one('res.partner',string='National Commission Team')
































