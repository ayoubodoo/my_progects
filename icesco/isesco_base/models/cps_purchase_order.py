# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tests import Form
from odoo.exceptions import ValidationError
from datetime import datetime

class CpsPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }
    partner_id = fields.Many2one('res.partner', string='Vendor', required=True, states=READONLY_STATES,
                                 change_default=True, tracking=True,
                                 domain="['&', ('supplier_rank', '>', 0), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
                                 help="You can find a vendor by its Name, TIN, Email or Internal Reference.")
    print_date = fields.Date(string="Print Date")

    def _print_date(self):
        for rec in self:
            rec.print_date = datetime.today()
