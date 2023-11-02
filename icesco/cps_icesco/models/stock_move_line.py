# Copyright 2017 ForgeFlow, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import _, api, models, fields


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    picking_id = fields.Many2one(
        'stock.picking', 'Transfert', auto_join=True,
        check_company=True,
        index=True,
        help='The stock operation where the packing has been made')