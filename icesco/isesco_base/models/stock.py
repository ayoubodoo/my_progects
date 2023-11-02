# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _
from odoo.osv import expression
from pprint import pprint
from itertools import groupby
from datetime import date, datetime

class StockSituation(models.TransientModel):
    _name = 'stock.situation'
    _description = 'Stock situation'

    inventory_datetime_start = fields.Date('Inventory Start Date',
        help="Choose a date to get the inventory at that start date",
        default=fields.Datetime.now)

    inventory_datetime_end = fields.Date('Inventory End Date',
                                         help="Choose a date to get the inventory at that end date",
                                         default=fields.Datetime.now)

    stock_move_ids = fields.One2many('stock.move', 'product_id', help='Technical: used to compute quantities.')
    date = fields.Date(string="Date", default=date.today())
    total = fields.Float(string="Total")



    def get_situation(self):
        if self.inventory_datetime_start and self.inventory_datetime_end:
            self.ensure_one()
            [data] = self.read()
            domain_quant_loc, domain_move_in_loc, domain_move_out_loc = self.env['product.product']._get_domain_locations()
            picking_in_ids = self.env['stock.picking.type'].search([('code','=','incoming')])
            picking_out_ids = self.env['stock.picking.type'].search([('code','=','outgoing')])
            move_lines = self.env['stock.move'].search([('date','>=',self.inventory_datetime_start),('date','<=',self.inventory_datetime_end),
                                                                  ('state', '=', 'done')])
            # ('picking_type_id', 'in', picking_type_ids.ids)
            # move_lines = self.env['stock.move'].search([('picking_id', 'in', stock_picking_ids.ids)])
            list_lines = []
            list_prod = []
            product_ids = list(set([line.product_id for line in move_lines]))
            for product in product_ids:
                list_lines.append(move_lines.filtered(lambda x: x.product_id.id == product.id))
            # print(product)
            pprint(list_lines)
            print("/*/*/*/*/*/*/*/*/*/*/*/*/", picking_in_ids)
            for line in list_lines:
                product = line[0].product_id
                
                move_in_lines = self.env['stock.move'].search([('date','>=',self.inventory_datetime_start),('date','<=',self.inventory_datetime_end),
                                                                  ('state', '=', 'done'), ('product_id', '=', product.id)] + domain_move_in_loc)
                move_out_lines = self.env['stock.move'].search([('date','>=',self.inventory_datetime_start),('date','<=',self.inventory_datetime_end),
                                                                  ('state', '=', 'done'), ('product_id', '=', product.id)] + domain_move_out_loc)
                
                qty_in = sum([l.product_uom_qty for l in move_in_lines])
                qty_out = sum([l.product_uom_qty for l in move_out_lines])
                qty_available = self.env['product.product'].with_context(to_date=self.inventory_datetime_start).search(
                    [('id', '=', product.id)]
                    ).qty_available
                stock_final = qty_available + qty_in - qty_out
                price_cost = product.standard_price
                value_in = qty_in * price_cost
                value_out = qty_out * price_cost
                value = stock_final * price_cost
                slist = {
                    'product_id': product.name,
                    'product_code': product.default_code,
                    'quantity_in': qty_in,
                    'quantity_out': qty_out,
                    'qty_available': qty_available,
                    'stock_final': stock_final,
                    'price_cost': price_cost,
                    'value_in': value_in,
                    'value_out': value_out,
                    'value': value,
                }
                # res = product._compute_quantities_dict(False,False,False,self.inventory_datetime_start,self.inventory_datetime_end)

                # slist['quantity_in'] = res[product.id]['incoming_qty']
                # slist['quantity_out'] = res[product.id]['outgoing_qty']
                list_prod.append(slist)
            pprint(list_prod)
            return list_prod

        else:
            raise UserError(_("Choose a type of document before"))

    def print_report(self):
        return self.env.ref('isesco_base.stock_situation').report_action(self)

