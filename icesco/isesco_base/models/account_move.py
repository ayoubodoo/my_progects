# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from .amount_to_text_fr import amount_to_text_fr
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    can_reset = fields.Boolean("Can Reset", compute='_set_can_reset')
    campaign_id = fields.Many2one('utm.campaign', string='Campaign', required=False, readonly=False, index=False,
                                  ondelete='set null', store=True)
    deactivate_blockage = fields.Boolean(string='Déactivé Blockage', default=False)
    taux = fields.Float(string="Taux")
    remet_taux_zero = fields.Boolean(string="Remettre Taux A Zero", default=False)

    #assets fields
    account_asset_id_asset = fields.Many2one('account.account', string='Fixed Asset Account', related='asset_id.account_asset_id', help="Account used to record the purchase of the asset at its original price.", store=True, states={'draft': [('readonly', False)], 'model': [('readonly', False)]}, domain="[('company_id', '=', company_id)]")
    account_depreciation_id_asset = fields.Many2one('account.account', string='Depreciation Account', related='asset_id.account_depreciation_id', readonly=True, states={'draft': [('readonly', False)], 'model': [('readonly', False)]}, domain="[('internal_type', '=', 'other'), ('deprecated', '=', False), ('company_id', '=', company_id)]", help="Account used in the depreciation entries, to decrease the asset value.")
    account_depreciation_expense_id_asset = fields.Many2one('account.account', string='Expense Account', related='asset_id.account_depreciation_expense_id', readonly=True, states={'draft': [('readonly', False)], 'model': [('readonly', False)]}, domain="[('internal_type', '=', 'other'), ('deprecated', '=', False), ('company_id', '=', company_id)]", help="Account used in the periodical entries, to record a part of the asset as expense.")
    account_analytic_id_asset = fields.Many2one('account.analytic.account', string='Analytic Account', related='asset_id.account_analytic_id',
                                          domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    original_value_asset = fields.Monetary(string="Original Value", related='asset_id.original_value', store=True, readonly=True, states={'draft': [('readonly', False)]})
    acquisition_date_asset = fields.Date(readonly=True, related='asset_id.acquisition_date', states={'draft': [('readonly', False)]}, )
    book_value_asset = fields.Monetary(string='Book Value', readonly=True, related='asset_id.book_value', store=True,
                                 help="Sum of the depreciable value, the salvage value and the book value of all value increase items")
    value_residual_asset = fields.Monetary(string='Depreciable Value', related='asset_id.value_residual', digits=0, readonly="1")
    salvage_value_asset = fields.Monetary(string='Not Depreciable Value', related='asset_id.salvage_value', digits=0, readonly=True,
                                    states={'draft': [('readonly', False)]},
                                    help="It is the amount you plan to have that you cannot depreciate.")
    gross_increase_value_asset = fields.Monetary(string="Gross Increase Value", related='asset_id.gross_increase_value',
                                           compute_sudo=True)
    journal_id_asset = fields.Many2one('account.journal', string='Journal', readonly=True, related='asset_id.journal_id',
                                 states={'draft': [('readonly', False)], 'model': [('readonly', False)]},
                                 domain="[('type', '=', 'general'), ('company_id', '=', company_id)]")
    code_asset = fields.Char(string="Code",related='asset_id.code')
    employee_id_asset = fields.Many2one('hr.employee', string="Employée", related='asset_id.employee_id')
    name_asset = fields.Char(string="Asset Name", related='asset_id.name')
    num_serie_asset = fields.Char(string='Numéro de série', related='asset_id.num_serie')
    first_depreciation_date_asset = fields.Date(
        string='First Depreciation Date',
        readonly=True, related='asset_id.first_depreciation_date'
    )
    method_number_asset = fields.Integer(
        string="Nombre d'amortissements",
        readonly=False,
        related='asset_id.method_number'
    )
    state_asset = fields.Selection(
        string="Status Asset",
        readonly=False,
        related='asset_id.state'
    )

    def _set_can_reset(self):

        for rec in self:
            can = True
            if any([line.validation in ('validation1', 'validation2')
                    for line in rec.line_ids]):
                can = False
            if can:
                rec.can_reset = True
            else:
                if rec.env.user.has_group('isesco_base.icesco_validation_account_move_line_validate_1') or \
                        rec.env.user.has_group('isesco_base.icesco_validation_account_move_line_validate_2'):
                    rec.can_reset = True
                else:
                    rec.can_reset = False

    def _check_balanced(self):
        ''' Assert the move is fully balanced debit = credit.
        An error is raised if it's not the case.
        '''
        for rec in self:
            moves = rec.filtered(lambda move: move.line_ids)
            if not moves:
                return

            # /!\ As this method is called in create / write, we can't make the assumption the computed stored fields
            # are already done. Then, this query MUST NOT depend of computed stored fields (e.g. balance).
            # It happens as the ORM makes the create with the 'no_recompute' statement.
            self.env['account.move.line'].flush(['debit', 'credit', 'move_id'])
            self.env['account.move'].flush(['journal_id'])
            self._cr.execute('''
                SELECT line.move_id, ROUND(SUM(line.debit - line.credit), currency.decimal_places)
                FROM account_move_line line
                JOIN account_move move ON move.id = line.move_id
                JOIN account_journal journal ON journal.id = move.journal_id
                JOIN res_company company ON company.id = journal.company_id
                JOIN res_currency currency ON currency.id = company.currency_id
                WHERE line.move_id IN %s
                GROUP BY line.move_id, currency.decimal_places
                HAVING ROUND(SUM(line.debit - line.credit), currency.decimal_places) != 0.0;
            ''', [tuple(rec.ids)])

            query_res = self._cr.fetchall()
            if query_res:
                ids = [res[0] for res in query_res]
                sums = [res[1] for res in query_res]
                if rec.deactivate_blockage == False:
                    raise UserError(_("Cannot create unbalanced journal entry. Ids: %s\nDifferences debit - credit: %s") % (ids, sums))

    # @api.depends('taux')
    # def change_taux_account_move(self):
    #     for rec in self:
    #         if rec.taux != 0:
    #             for l in rec.move_id.line_ids:
    #                 l.taux = rec.taux