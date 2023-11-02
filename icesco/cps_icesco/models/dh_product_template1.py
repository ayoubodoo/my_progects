# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from itertools import groupby


class DHProductTemplate1(models.Model):
    _inherit = 'product.template'

    qty_minimal = fields.Boolean(compute="is_qty_minimal",string="is_qty_minimal",store=True)
    qty_restant = fields.Float('rest',compute='is_qty_minimal')

    @api.depends('qty_available', "reordering_min_qty")
    def is_qty_minimal(self):
        for rec in self:
            rec.qty_restant = False
            rec.qty_minimal = False
            rec.qty_restant = rec.qty_available - rec.reordering_min_qty
            if rec.qty_restant <= 0:
                rec.qty_minimal = True



    @api.model
    def create(self, vals):
        res = super().create(vals)
        if 'qty_available' in vals and 'reordering_min_qty' in vals:
            self.is_qty_minimal()
        return res


    def write(self, vals):
        res = super(DHProductTemplate1, self).write(vals)
        if 'qty_available' in vals and 'reordering_min_qty' in vals:
            self.is_qty_minimal()
        return res