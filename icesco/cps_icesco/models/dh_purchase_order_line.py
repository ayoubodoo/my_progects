# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError



class DHStockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def create(self, vals):
        res = super(DHStockPicking, self).create(vals)
        if res.picking_type_id:
            if res.picking_type_id.code == "outgoing":
                for line in self.move_ids_without_package:
                    if line.product_id.qty_available == 0 or line.product_id.qty_available - line.product_qty <= 0:
                        raise ValidationError(_('The product  %s is not available ') % (line.product_id.name))

        return res

    def write(self, vals):
        res = super(DHStockPicking, self).create(vals)
        if res.picking_type_id:
            if res.picking_type_id.code == "outgoing":
                if 'move_ids_without_package' in vals :
                    for line in self.move_ids_without_package:
                        if line.product_id.qty_available == 0 or line.product_id.qty_available - line.product_qty <= 0:
                            raise ValidationError(_('The product  %s is not available ') % (line.product_id.name))

        return res


class DHPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'


    dimension = fields.Char("Dimension")

    # @api.model
    # def create(self, vals):
    #     res = super().create(vals)
    #     if res.product_id.qty_available == 0 or res.product_id.qty_available - res.product_qty <= 0 :
    #         raise ValidationError(_('The product  %s is not available ')% (res.product_id.name))
    #
    #     return res
    #
    # def write(self, vals):
    #     res = super().write(vals)
    #     if 'product_qty' in vals or 'product_id' in vals:
    #         if self.product_id.qty_available == 0 or self.product_id.qty_available - self.product_qty <= 0:
    #             raise ValidationError(_('The product  %s is not available ') % (self.product_id.name))
    #
    #     return res