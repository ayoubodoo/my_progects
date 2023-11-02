# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResStakeholder(models.Model):
    _name = 'res.stakeholder'
    _description = 'Stakeholder'
    _rec_name = "partner_id"

    project_id = fields.Many2one('project.project', string="Project")
    partner_id = fields.Many2one('res.partner', string="Stakeholder")
    stakeholder_type_ids = fields.Many2many('res.stakeholder.type', string="Stakeholder Type")
    intervention_type_ids = fields.Many2many('intervention.type', string="Intervention Type")
    budget = fields.Float(string="Allocated Budget")


class ResStakeholderType(models.Model):
    _name = 'res.stakeholder.type'
    _description = 'Stakeholder Type'

    name = fields.Char(string='name', required=True)