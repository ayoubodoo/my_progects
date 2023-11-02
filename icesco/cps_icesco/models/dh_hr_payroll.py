# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class DHHrPayroll_maRubrique(models.Model):
    _inherit = 'hr.payroll_ma.rubrique'


    is_transport = fields.Boolean(string='transportation allowanc')