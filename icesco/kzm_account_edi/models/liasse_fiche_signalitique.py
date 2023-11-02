# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api, exceptions, _
from odoo.exceptions import ValidationError

class liasse_fiche_signalitique(models.Model):
    _name = 'liasse.fiche.signalitique.erp'
    _rec_name = 'company_id'
    _description = 'Fiche signalitique'

    def default_company_id(self):
        return self.env.user.company_id

    company_id = fields.Many2one(comodel_name="res.company", ondelete='cascade',
                                 string=_("Ferme"), required=True,
                                 default= default_company_id
                                 )
    tp = fields.Char(related='company_id.patente')
    id_fiscal = fields.Char(related='company_id.vat')

