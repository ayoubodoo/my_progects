# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class DhContrubutions(models.Model):
    _name = 'dh.contrubution'

    date = fields.Char(string='Year')
    three_years = fields.Char(string='Three Years')
    pourcentage = fields.Float(string='Pourcentage', default=1)
    amount_contrubutions = fields.Float(string='Amount of contrubutions')
    amount = fields.Float(string='Amount from contrubutions')
    date_1 = fields.Date(string='Date')
    performance = fields.Float(string='Performance',compute="get_amount_not_paid", store=True)
    amount_not_paid = fields.Float(string='Inpaid Balance',compute="get_amount_not_paid", store=True)
    partner_id = fields.Many2one("res.partner")

    @api.depends("amount_contrubutions", "amount")
    def get_amount_not_paid(self):
        for rec in self:
            rec.amount_not_paid = False
            rec.performance = 0
            if rec.amount_contrubutions:
                rec.amount_not_paid = rec.amount_contrubutions - rec.amount
                rec.performance = rec.amount / rec.amount_contrubutions



