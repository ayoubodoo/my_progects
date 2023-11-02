# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from itertools import groupby


class ProductProduct(models.Model):
    _inherit = 'product.product'

    articles_qty = fields.Integer(string="Quantity")


class OutOfStockWizard(models.TransientModel):
    _name = 'stock.picking.destination.wizard'
    _description = "Out of Stock Report wizard"

    start_date = fields.Date("Start date", required=1)
    end_date = fields.Date("End date", required=1)
    destination_id = fields.Many2one('res.partner', string="Destination", required=1)
    product_ids = fields.Many2many('product.product', string="Products", store=True)
    company_id = fields.Many2one('res.company')

    def print_report(self):
        if self.start_date and self.end_date and self.destination_id:
            self.company_id = self.env.company
            stock_picking_ids = self.env['stock.picking'].search(
                [('partner_id', '=', self.destination_id.id),
                 ('state', '=', 'done'),
                 ('scheduled_date', '>=', self.start_date),
                 ('scheduled_date', '<=', self.end_date)])
            move_lines = self.env['stock.move'].search(
                [('picking_id', 'in', stock_picking_ids.ids)])
            sous_list = move_lines.sorted(key=lambda x: x.product_id.id)
            list_prod = []
            for product_id, lines in groupby(sous_list, lambda l: l.product_id):
                lines = list(lines)
                qty = sum([l.product_uom_qty for l in lines])
                product_id.articles_qty = qty
                list_prod.append(product_id.id)
            self.product_ids = [(6, 0, list_prod)]
            return self.env.ref('isesco_base.out_of_stock_by_destination').report_action(self)
