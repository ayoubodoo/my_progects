# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DHPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    project_id = fields.Many2one('project.project', string="Project")
