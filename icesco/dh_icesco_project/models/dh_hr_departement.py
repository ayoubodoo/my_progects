# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError, UserError

class DhcpsExpense1(models.Model):
    _inherit = 'hr.department'

    _order = 'seq'
    seq = fields.Char(required=False, readonly=True, copy=False, default=lambda self: _('New'))
