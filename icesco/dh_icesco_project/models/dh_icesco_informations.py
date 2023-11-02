# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DhIcescoInformations(models.Model):
    _name = 'dh.icesco.informations'
    _order = 'sequence'

    name = fields.Char(string='إسم')
    description = fields.Text(translate=True,string='التفاصيل')
    type = fields.Selection([('information', 'معلومة'), ('question', 'سؤال')], string='نوع')
    sequence = fields.Integer(string='متسلسل')

    @api.model
    def create(self, vals):
        vals['sequence'] = len(self.env['dh.icesco.office'].search([])) + 1
        return super(DhIcescoInformations, self).create(vals)