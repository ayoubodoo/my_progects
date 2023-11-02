# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from itertools import groupby

class AccountAssetWizard(models.Model):
    _name = 'account.asset.wizard'

    taux = fields.Float(string="Taux")
    remet_taux_zero = fields.Boolean(string='Remettre taux zero')

    def write_taux(self):
        for rec in self:
            rec.env['account.asset'].search([('id', '=', self.env.context.get("active_id"))]).write({'taux': rec.taux, 'remet_taux_zero': rec.remet_taux_zero})