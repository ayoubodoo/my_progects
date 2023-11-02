# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectNature(models.Model):
    _name = 'project.nature'
    _description = 'project_nature'

    name = fields.Char(string='name')
    project_id = fields.Many2one('project.project', string="Project")