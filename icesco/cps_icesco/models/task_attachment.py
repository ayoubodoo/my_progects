# -*- coding: utf-8 -*-
from odoo import models, fields, api,  _
from ast import literal_eval


class TaskAttachment(models.Model):
    _name = 'task.attachment'
    _rec_name = 'description'

    task_id = fields.Many2one('project.task', string='Task')
    description = fields.Many2one('type.attachment', string='Description')
    file = fields.Many2many("ir.attachment", string="Piece jointe")
