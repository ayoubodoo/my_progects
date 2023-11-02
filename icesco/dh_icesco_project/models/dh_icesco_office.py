# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DhIcescoOffice(models.Model):
    _name = 'dh.icesco.office'
    _order = 'sequence'

    name = fields.Char(string='إسم')
    description = fields.Text(translate=True,string='التفاصيل')
    type = fields.Selection([('delegate', 'مندوبية'), ('regional_office', 'مكتب اقليمي')], string='نوع')
    sequence = fields.Integer(string='متسلسل')

    @api.model
    def create(self, vals):
        vals['sequence'] = len(self.env['dh.icesco.office'].search([])) + 1
        return super(DhIcescoOffice, self).create(vals)