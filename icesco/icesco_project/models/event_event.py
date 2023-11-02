# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EventEvent(models.Model):
    _inherit = 'event.event'

    project_id = fields.Many2one('project.project', string="Project",store=True)
    task_id = fields.Many2one('project.task', string='Task')