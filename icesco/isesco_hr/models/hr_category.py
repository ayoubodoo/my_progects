# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class HrCategory(models.Model):
    _name = 'hr.category'
    _description = 'HR Category'

    name = fields.Char(stranslate=True,tring="Name")
    category_id = fields.Many2one('hr.contract.category', string="Category")
    grade_id = fields.Many2one('hr.contract.grade', string="Grade")
    amount = fields.Float(string="Amount")
    code = fields.Char(string='code', compute='compute_code')

    @api.depends('name')
    def compute_code(self):
        for rec in self:
            if rec.name:
                rec.code = rec.name.split('-')[0]
            else:
                rec.code = ''

    @api.onchange('category_id')
    def onchange_category(self):
        self.ensure_one()
        domain = []
        self.grade_id = False
        if self.category_id:
            domain = [('id', 'in', self.category_id.grade_ids.ids)]
        return {'domain': {'grade_id': domain}}

    @api.onchange('grade_id','category_id')
    def onchange_category_grade(self):
        self.ensure_one()
        if self.grade_id and self.category_id:
            self.name = ' '.join([self.category_id.code, self.category_id.name, self.grade_id.name])
