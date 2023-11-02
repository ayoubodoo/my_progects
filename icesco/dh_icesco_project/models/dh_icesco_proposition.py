# -*- coding: utf-8 -*-
from odoo import models, fields, api


class DHIcescoProposition(models.Model):
    _name = 'dh.icesco.proposition'

    name = fields.Char(string='Name')
    location = fields.Char(string='Location')
    city = fields.Char(string='City')
    type = fields.Selection([('local', 'Local'),('regional', 'Regional'),('international', 'International')], string='Type')
    is_sponsorise = fields.Boolean(string='Sponsorise ?')
    proposition_sponsor = fields.Char(string='Proposition sponsor')
    participant_ids = fields.One2many('dh.icesco.proposition.lines', 'proposition_id', string='The most prominent personalities invited')
    number_participant_out_icesco = fields.Integer(string='Number of participants out')
    number_billets = fields.Integer(string='Number Billets')
    number_residences = fields.Integer(string='Number Residences')
    number_transferts = fields.Integer(string='Number Transfers')
    task_id = fields.Many2one('project.task', string='Task')

class DHIcescoProposition(models.Model):
    _name = 'dh.icesco.proposition.lines'

    proposition_id = fields.Many2one('dh.icesco.proposition', string='Proposition')
    name = fields.Char(string='Name')
    job_title = fields.Char(string='Job Title')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')