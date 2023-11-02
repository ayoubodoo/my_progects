# -*- coding: utf-8 -*-
from odoo import models, fields,_


class ResPartner(models.Model):
    _inherit = 'res.partner'

    i_siret= fields.Char(string="SIRET")
