# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class DateTrimester(models.Model):
    _name = "date.trimester"

    name = fields.Char('Name')
    date_start = fields.Date(string='Date Start')
    date_end = fields.Date(string='Date end')
    periode_id = fields.Many2one('date.range', string='Periode')