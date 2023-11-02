from odoo import api, fields, models


class DHProductCategory(models.Model):
    _inherit = "product.category"

    active = fields.Boolean('active', default=True)