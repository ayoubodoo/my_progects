# # -*- coding: utf-8 -*-
import base64
from odoo.tools.float_utils import float_compare
from odoo import models, fields, api, exceptions, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import date, datetime, timedelta
from odoo.exceptions import UserError, ValidationError
import json
from dateutil.relativedelta import relativedelta
from odoo.addons.resource.models.resource_mixin import timezone_datetime
from collections import defaultdict
from pytz import timezone, UTC


# class DhaccountPayement(models.Model):
#     _inherit = 'account.payment'
#
#
#
    # payment_type = fields.Selection([('outbound', 'Send Money'), ('inbound', 'Receive Money'), ('transfer', 'Internal Transfer'), ('virement_locaux', 'Virements locaux'), ('virement_locaux', 'Virements locaux'), ('virement_salaires', 'Virement des salaires'), ('virement_internationaux', 'Virements internationaux'), ('virements_compte_compte', 'Virements de compte à compte')], string='Payment Type', required=True, readonly=True, states={'draft': [('readonly', False)]})
    #
    # banque = fields.Many2one("res.bank",string="Banque")
    # banque_intermdiaire = fields.Many2one("res.bank",string="Banque intermédiaire")

class DhaccountPayement(models.Model):
    _inherit = 'account.payment'


    bank_intermidiaire = fields.Many2one("res.bank",string="Banque intermediaire")

    details = fields.Text('details')
    payment_type = fields.Selection([('outbound', 'Send Money'), ('inbound', 'Receive Money'), ('transfer', 'Internal Transfer'),  ('virement_locaux', 'Virements locaux'), ('virement_salaires', 'Virement des salaires'), ('virement_internationaux', 'Virements internationaux'), ('virements_compte_compte', 'Virements de compte à compte')], string='Payment Type', required=True, readonly=True, states={'draft': [('readonly', False)]})
    amount_to_text = fields.Char(string='Amount In Text', compute='convert')
    amount_to_text2 = fields.Char(string='Amount In Text', compute='convert2')
    mise_desposition = fields.Boolean(string='Mise à disposition')
    amount_mise_desposition = fields.Float(string='Montant à disposition')
    @api.depends("amount")
    def convert(self):
        for record in self:
            record.amount_to_text = False
            if record.amount:
                record.amount_to_text = record.currency_id.amount_to_text(record.amount)
    @api.depends("amount_mise_desposition")
    def convert2(self):
        for record in self:
            record.amount_to_text2 = False
            if record.amount_mise_desposition:
                record.amount_to_text2 = record.currency_id.amount_to_text(record.amount_mise_desposition)


    # def convert(self):
    #     for record in self:
    #         record.amount_to_text = record.currency_id.amount_to_text(record.invoice_totalttc)

    type = fields.Selection([('depense_caisse', 'Pièce Dépense Caisse'), ('depense_banque', 'Pièce Dépense Banque'),
                             ('virement_mad', 'Virement MAD'), ('virement_devise', 'Lettre Virement Devise'),
                             ('virement_salaire', 'virement des salaires avec mise à disposition'),
                             ('compte_compte', 'Lettre virement de compte à compte'),
                             ('alimentation_carte ', 'Lettre alimentation carte bancaire')],
                            string='Type')

    signature_supperviseur_affairs_financiere = fields.Binary(
        string='Signature  Superviseur des affairs financières')
    signature_controlleur_financiere = fields.Binary(string='Signature Contrôleur Financier ')
    signature_dg = fields.Binary(string='Signature Directeur général')
    signature_dg_adjoint = fields.Binary(string='Signature Directeur général Adjoint')
    signature_caissier = fields.Binary(string='Signature Caissier')
    signature_benefciaire = fields.Binary(string='Signature Bénéficiaire')
    signature_res_financier = fields.Binary(string='Signature Résponsable Financier')
    senario = fields.Selection([("s1","SAF/CF/DG"),("s2","SAF/CF/DGA"),("s3","SAF/CF"),("s4","SAF/DG"),("s5","CF/DGA"),("s6","SAF/DGA"),("s7","CF/DG")],string="Sénario  signatures")


    is_signature_supperviseur_affairs_financiere = fields.Boolean(string='Signature  Superviseur des affairs financières',
                                                                  compute='is_signature_set')
    is_signature_controlleur_financiere = fields.Boolean(string='Signature Contrôleur Financier ',
                                                         compute='is_signature_set')
    is_signature_dg = fields.Boolean(string='Signature Directeur général', compute='is_signature_set')
    is_signature_dg_adjoint = fields.Boolean(string='Signature Directeur général Adjoint', compute='is_signature_set')
    is_signature_caissier = fields.Boolean(string='Signature Caissier', compute='is_signature_set')
    is_signature_benefciaire = fields.Boolean(string='Signature Bénéficiaire', compute='is_signature_set')
    is_signature_res_financier = fields.Boolean(string='Signature Résponsable Financier', compute='is_signature_set')

    def is_signature_set(self):
        for rec in self:
            rec.is_signature_supperviseur_affairs_financiere = False
            rec.is_signature_dg_adjoint = False
            rec.is_signature_controlleur_financiere = False
            rec.is_signature_dg = False
            rec.is_signature_caissier = False
            rec.is_signature_res_financier = False
            rec.is_signature_benefciaire = False

            if rec.signature_supperviseur_affairs_financiere:
                rec.is_signature_supperviseur_affairs_financiere = True

            if rec.signature_controlleur_financiere:
                rec.is_signature_controlleur_financiere = True
            if rec.signature_dg_adjoint:

                rec.is_signature_dg_adjoint = True
            if rec.signature_dg:
                rec.is_signature_dg = True

            if rec.signature_caissier:
                rec.is_signature_caissier = True

            if rec.signature_res_financier :
                rec.is_signature_res_financier = True
            if rec.signature_benefciaire :
                rec.is_signature_benefciaire = True











