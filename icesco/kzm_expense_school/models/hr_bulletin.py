# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class HrPayrollRubrique(models.Model):
    _inherit = 'hr.payroll_ma.rubrique'

    is_13th_month = fields.Boolean("13th Month")

    element_plus = fields.Boolean('Element plus')
    element_moins = fields.Boolean('Element moins')
