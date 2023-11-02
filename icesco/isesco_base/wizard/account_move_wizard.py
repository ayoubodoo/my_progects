# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from itertools import groupby

class AccountMoveWizard(models.Model):
    _name = 'account.move.wizard'

    taux = fields.Float(string="Taux")
    remet_taux_zero = fields.Boolean(string='Remettre taux zero')

    def write_taux(self):
        for rec in self:
            if rec.env['account.move'].search([('id', '=', self.env.context.get("active_id"))]).asset_id.id == False:
                rec.env['account.move'].search([('id', '=', self.env.context.get("active_id"))]).write({'taux': rec.taux, 'remet_taux_zero': rec.remet_taux_zero})
            else:
                raise ValidationError("Merci de modifier le taux depuis l'actif de cette piéce comptable")