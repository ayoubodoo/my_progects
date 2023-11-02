# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date

class CpsCpsAccountMove(models.Model):
    _name = 'cps.account.move'

    # first_date = fields.Date(string='Date Debut')
    last_date = fields.Date(string='Date Fin')
    asset_id = fields.Many2one('account.asset', string="Nom de l'immobilisation")
    account_asset_id_asset = fields.Many2one('account.account', string="Compte d'immobilisation",
                                             related='asset_id.account_asset_id',
                                             help="Account used to record the purchase of the asset at its original price.",
                                             store=True,
                                             states={'draft': [('readonly', False)], 'model': [('readonly', False)]},
                                             domain="[('company_id', '=', company_id)]")
    account_depreciation_id_asset = fields.Many2one('account.account', string='Depreciation Account',
                                                    related='asset_id.account_depreciation_id', readonly=True,
                                                    states={'draft': [('readonly', False)],
                                                            'model': [('readonly', False)]},
                                                    domain="[('internal_type', '=', 'other'), ('deprecated', '=', False), ('company_id', '=', company_id)]",
                                                    help="Account used in the depreciation entries, to decrease the asset value.")
    account_depreciation_expense_id_asset = fields.Many2one('account.account', string='Expense Account',
                                                            related='asset_id.account_depreciation_expense_id',
                                                            readonly=True, states={'draft': [('readonly', False)],
                                                                                   'model': [('readonly', False)]},
                                                            domain="[('internal_type', '=', 'other'), ('deprecated', '=', False), ('company_id', '=', company_id)]",
                                                            help="Account used in the periodical entries, to record a part of the asset as expense.")
    account_analytic_id_asset = fields.Many2one('account.analytic.account', string='Analytic Account',
                                                related='asset_id.account_analytic_id',
                                                domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    original_value_asset = fields.Monetary(string="Valeur d'origine", related='asset_id.original_value', store=True,
                                           readonly=True, states={'draft': [('readonly', False)]})
    acquisition_date_asset = fields.Date(readonly=True, string="Date d'acquisition", related='asset_id.acquisition_date',
                                         states={'draft': [('readonly', False)]}, store=True)
    book_value_asset = fields.Monetary(string='Valeur comptable', readonly=True, related='asset_id.book_value', store=True,
                                       help="Sum of the depreciable value, the salvage value and the book value of all value increase items")
    value_residual_asset = fields.Monetary(string='Valeur amortissable', related='asset_id.value_residual', digits=0,
                                           readonly="1")
    salvage_value_asset = fields.Monetary(string='Not Depreciable Value', related='asset_id.salvage_value', digits=0,
                                          readonly=True,
                                          states={'draft': [('readonly', False)]},
                                          help="It is the amount you plan to have that you cannot depreciate.")
    gross_increase_value_asset = fields.Monetary(string="Gross Increase Value", related='asset_id.gross_increase_value',
                                                 compute_sudo=True)
    journal_id_asset = fields.Many2one('account.journal', string='Journal', readonly=True,
                                       related='asset_id.journal_id',
                                       states={'draft': [('readonly', False)], 'model': [('readonly', False)]},
                                       domain="[('type', '=', 'general'), ('company_id', '=', company_id)]")
    code_asset = fields.Char(string="Code d'immobilisation", related='asset_id.code', store=True)
    employee_id_asset = fields.Many2one('hr.employee', string="Employée", related='asset_id.employee_id')
    name_asset = fields.Char(string="Asset Name", related='asset_id.name')
    num_serie_asset = fields.Char(string='Numéro de série', related='asset_id.num_serie')
    first_depreciation_date_asset = fields.Date(
        string='Premiére date de dépréciation',
        readonly=True, related='asset_id.first_depreciation_date', store=True
    )
    method_number_asset = fields.Integer(
        string="Nombre d'amortissements",
        readonly=False,
        related='asset_id.method_number', store=True
    )
    state_asset = fields.Selection(
        string="Statut",
        readonly=False,
        related='asset_id.state', store=True
    )
    move_asset_id = fields.Many2one('account.move', string='Piéce Comptable')
    name = fields.Char(string='Number', related='move_asset_id.name')
    date = fields.Date(string='Date', related='move_asset_id.date')
    ref = fields.Char(string='Reference', related='move_asset_id.ref')
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled')
    ], string='Statut', related='move_asset_id.state')
    type = fields.Selection(selection=[
        ('entry', 'Journal Entry'),
        ('out_invoice', 'Customer Invoice'),
        ('out_refund', 'Customer Credit Note'),
        ('in_invoice', 'Vendor Bill'),
        ('in_refund', 'Vendor Credit Note'),
        ('out_receipt', 'Sales Receipt'),
        ('in_receipt', 'Purchase Receipt'),
    ], string='Type', related='move_asset_id.type')
    amount_total = fields.Monetary(string='Total', store=True, related='move_asset_id.amount_total')
    asset_depreciated_value = fields.Monetary(string='Cumulative Depreciation', related='move_asset_id.asset_depreciated_value') # string='Cumulative Depreciation'
    asset_remaining_value = fields.Monetary(string='Valeur amortissable', related='move_asset_id.asset_remaining_value', store=True)
    currency_id = fields.Many2one('res.currency', related='asset_id.currency_id',
                                  string='Devise')
    company_id = fields.Many2one("res.company", string="Société", related='asset_id.company_id')

    dh_book_value_asset = fields.Monetary(string='Valeur comptable', readonly=True, compute='compute_dh_book_value', store=True,
                                       help="Sum of the depreciable value, the salvage value and the book value of all value increase items")

    dh_asset_remaining_value = fields.Monetary(string='Valeur amortissable', compute='compute_dh_asset_remaining_value', store=True)
    dh_asset_remaining_value_n_1 = fields.Monetary(string='Valeur amortissable initial', compute='compute_dh_asset_remaining_value', store=True)
    dh_amortissement_economiques = fields.Monetary(string='Amortissements économiques antérieurs', compute='compute_dh_asset_remaining_value', store=True)
    dh_dotation_exercice = fields.Monetary(string="Dotations de l'exercice", compute='compute_dh_asset_remaining_value', store=True)
    amortissement_cumule_exercice = fields.Monetary(string="Amortissements cumulés de l'exercice", compute='compute_dh_asset_remaining_value', store=True)
    nette_comptable = fields.Monetary(string="Valeur nette comptable", compute='compute_dh_asset_remaining_value', store=True)

    @api.depends('last_date', 'asset_id')
    def compute_dh_asset_remaining_value(self):
        for rec in self:
            rec.dh_asset_remaining_value = False
            rec.dh_asset_remaining_value_n_1 = False
            rec.dh_amortissement_economiques = False
            rec.dh_dotation_exercice = False
            rec.amortissement_cumule_exercice = False
            rec.nette_comptable = False
            if rec.asset_id:
                if rec.last_date:
                    rec.dh_asset_remaining_value = sum(rec.asset_id.depreciation_move_ids.filtered(lambda x: x.date <= rec.last_date and x.state == 'posted').mapped('amount_total'))
                    rec.dh_asset_remaining_value_n_1 = sum(
                        rec.asset_id.depreciation_move_ids.filtered(lambda x: rec.last_date > x.date and x.state == 'posted').mapped(
                            'amount_total'))
                    rec.dh_amortissement_economiques = rec.asset_id.salvage_value + sum(rec.asset_id.depreciation_move_ids.filtered(lambda x: date(rec.last_date.year - 1, 12, 31) >= x.date and x.state == 'posted').mapped('amount_total'))
                    rec.dh_dotation_exercice = sum(rec.asset_id.depreciation_move_ids.filtered(lambda x: date(rec.last_date.year, 1, 1) <= x.date <= rec.last_date and x.state == 'posted').mapped('amount_total'))
                    rec.amortissement_cumule_exercice = rec.asset_id.salvage_value + sum(
                        rec.asset_id.depreciation_move_ids.filtered(lambda x: x.date <= rec.last_date and x.state == 'posted').mapped(
                            'amount_total'))
                    rec.nette_comptable = rec.original_value_asset - rec.amortissement_cumule_exercice
                else:
                    rec.dh_asset_remaining_value = rec.asset_id.value_residual


    @api.depends('asset_remaining_value', 'asset_id.salvage_value')
    def compute_dh_book_value(self):
        for rec in self:
            rec.dh_book_value_asset = 0
            if rec.asset_remaining_value:
                rec.dh_book_value_asset = rec.asset_remaining_value + rec.asset_id.salvage_value
            else:
                rec.dh_book_value_asset = rec.asset_id.salvage_value