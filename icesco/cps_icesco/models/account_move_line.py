# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.misc import formatLang

class CpsAccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    _description = 'Account Move Line'

    type_convertion = fields.Selection(related='account_id.type_convertion', string="Type Convertion")

class CpsAccountMove(models.Model):
    _inherit = 'account.move'

    remise_total = fields.Float(string='Remise Total')

    @api.depends('line_ids.price_subtotal', 'line_ids.tax_base_amount', 'line_ids.tax_line_id', 'partner_id',
                 'currency_id', 'remise_total')
    def _compute_invoice_taxes_by_group(self):
        ''' Helper to get the taxes grouped according their account.tax.group.
        This method is only used when printing the invoice.
        '''
        for move in self:
            lang_env = move.with_context(lang=move.partner_id.lang).env
            tax_lines = move.line_ids.filtered(lambda line: line.tax_line_id)
            tax_balance_multiplicator = -1 if move.is_inbound(True) else 1
            res = {}
            # There are as many tax line as there are repartition lines
            done_taxes = set()

            for line in tax_lines:
                if sum(move.invoice_line_ids.mapped('price_subtotal')) != 0:
                    tax = line.balance / sum(move.invoice_line_ids.mapped('price_subtotal'))
                else:
                    tax = 0
                res.setdefault(line.tax_line_id.tax_group_id, {'base': 0.0, 'amount': 0.0})
                res[line.tax_line_id.tax_group_id]['amount'] += tax_balance_multiplicator * (
                    line.amount_currency - move.remise_total * tax if line.currency_id else line.balance - move.remise_total * tax)
                tax_key_add_base = tuple(move._get_tax_key_for_group_add_base(line))
                if tax_key_add_base not in done_taxes:
                    if line.currency_id and line.company_currency_id and line.currency_id != line.company_currency_id:
                        amount = line.company_currency_id._convert(line.tax_base_amount - move.remise_total, line.currency_id,
                                                                   line.company_id, line.date or fields.Date.today())
                    else:
                        amount = line.tax_base_amount - move.remise_total
                    res[line.tax_line_id.tax_group_id]['base'] += amount
                    # The base should be added ONCE
                    done_taxes.add(tax_key_add_base)

            # At this point we only want to keep the taxes with a zero amount since they do not
            # generate a tax line.
            zero_taxes = set()
            for line in move.line_ids:
                for tax in line.tax_ids.flatten_taxes_hierarchy():
                    if tax.tax_group_id not in res or tax.id in zero_taxes:
                        res.setdefault(tax.tax_group_id, {'base': 0.0, 'amount': 0.0})
                        res[tax.tax_group_id]['base'] += tax_balance_multiplicator * (
                            line.amount_currency if line.currency_id else line.balance)
                        zero_taxes.add(tax.id)

            res = sorted(res.items(), key=lambda l: l[0].sequence)
            move.amount_by_group = [(
                group.name, amounts['amount'],
                amounts['base'],
                formatLang(lang_env, amounts['amount'], currency_obj=move.currency_id),
                formatLang(lang_env, amounts['base'], currency_obj=move.currency_id),
                len(res),
                group.id
            ) for group, amounts in res]

    @api.depends(
        'line_ids.debit',
        'line_ids.credit',
        'line_ids.currency_id',
        'line_ids.amount_currency',
        'line_ids.amount_residual',
        'line_ids.amount_residual_currency',
        'line_ids.payment_id.state', 'remise_total')
    def _compute_amount(self):
        invoice_ids = [move.id for move in self if move.id and move.is_invoice(include_receipts=True)]
        self.env['account.payment'].flush(['state'])
        if invoice_ids:
            self._cr.execute(
                '''
                    SELECT move.id
                    FROM account_move move
                    JOIN account_move_line line ON line.move_id = move.id
                    JOIN account_partial_reconcile part ON part.debit_move_id = line.id OR part.credit_move_id = line.id
                    JOIN account_move_line rec_line ON
                        (rec_line.id = part.debit_move_id AND line.id = part.credit_move_id)
                    JOIN account_payment payment ON payment.id = rec_line.payment_id
                    JOIN account_journal journal ON journal.id = rec_line.journal_id
                    WHERE payment.state IN ('posted', 'sent')
                    AND journal.post_at = 'bank_rec'
                    AND move.id IN %s
                UNION
                    SELECT move.id
                    FROM account_move move
                    JOIN account_move_line line ON line.move_id = move.id
                    JOIN account_partial_reconcile part ON part.debit_move_id = line.id OR part.credit_move_id = line.id
                    JOIN account_move_line rec_line ON
                        (rec_line.id = part.credit_move_id AND line.id = part.debit_move_id)
                    JOIN account_payment payment ON payment.id = rec_line.payment_id
                    JOIN account_journal journal ON journal.id = rec_line.journal_id
                    WHERE payment.state IN ('posted', 'sent')
                    AND journal.post_at = 'bank_rec'
                    AND move.id IN %s
                ''', [tuple(invoice_ids), tuple(invoice_ids)]
            )
            in_payment_set = set(res[0] for res in self._cr.fetchall())
        else:
            in_payment_set = {}

        for move in self:
            total_untaxed = 0.0
            total_untaxed_currency = 0.0
            total_tax = 0.0
            total_tax_currency = 0.0
            total_residual = 0.0
            total_residual_currency = 0.0
            total = 0.0
            total_currency = 0.0
            currencies = set()

            for line in move.line_ids:
                if line.currency_id:
                    currencies.add(line.currency_id)

                if move.is_invoice(include_receipts=True):
                    # === Invoices ===

                    if not line.exclude_from_invoice_tab:
                        # Untaxed amount.
                        total_untaxed += line.balance
                        total_untaxed_currency += line.amount_currency
                        total += line.balance
                        total_currency += line.amount_currency
                    elif line.tax_line_id:
                        # Tax amount.
                        total_tax += line.balance
                        total_tax_currency += line.amount_currency
                        total += line.balance
                        total_currency += line.amount_currency
                    elif line.account_id.user_type_id.type in ('receivable', 'payable'):
                        # Residual amount.
                        total_residual += line.amount_residual
                        total_residual_currency += line.amount_residual_currency
                else:
                    # === Miscellaneous journal entry ===
                    if line.debit:
                        total += line.balance
                        total_currency += line.amount_currency

            if move.type == 'entry' or move.is_outbound():
                sign = 1
            else:
                sign = -1

            if total_untaxed != 0:
                taxe = total_tax / total_untaxed
            else:
                taxe = 0

            total = total - move.remise_total * taxe
            total_residual = total_residual + move.remise_total * taxe

            move.amount_untaxed = sign * (total_untaxed_currency - move.remise_total if len(currencies) == 1 else total_untaxed - move.remise_total)
            move.amount_tax = sign * (total_tax_currency - move.remise_total * taxe if len(currencies) == 1 else total_tax - move.remise_total * taxe)
            move.amount_total = sign * (total_currency - move.remise_total if len(currencies) == 1 else total - move.remise_total)
            move.amount_residual = -sign * (total_residual_currency + move.remise_total if len(currencies) == 1 else total_residual + move.remise_total)
            move.amount_untaxed_signed = -total_untaxed + move.remise_total
            move.amount_tax_signed = -total_tax + move.remise_total * taxe
            move.amount_total_signed = abs(total - move.remise_total) if move.type == 'entry' else -total + move.remise_total
            move.amount_residual_signed = total_residual + move.remise_total

            currency = len(currencies) == 1 and currencies.pop() or move.company_id.currency_id
            is_paid = currency and currency.is_zero(move.amount_residual) or not move.amount_residual

            # Compute 'invoice_payment_state'.
            if move.type == 'entry':
                move.invoice_payment_state = False
            elif move.state == 'posted' and is_paid:
                if move.id in in_payment_set:
                    move.invoice_payment_state = 'in_payment'
                else:
                    move.invoice_payment_state = 'paid'
            else:
                move.invoice_payment_state = 'not_paid'

    @api.model
    def _autopost_draft_entries(self):
        ''' This method is called from a cron job.
        It is used to post entries such as those created by the module
        account_asset.
        '''
        records = self.search([
            ('state', '=', 'draft'),
            ('date', '<=', fields.Date.today()),
            ('auto_post', '=', True),
        ]).filtered(lambda x:x.asset_id.id == False or x.asset_id.state != 'close')

        for ids in self._cr.split_for_in_conditions(records.ids, size=1000):
            self.browse(ids).post()
            if not self.env.registry.in_test_mode():
                self._cr.commit()

    def _depreciate(self):
        for move in self.filtered(lambda m: m.asset_id):
            asset = move.asset_id
            if asset.state in ('open', 'paused'):
                asset.value_residual -= abs(
                    sum(move.line_ids.filtered(lambda l: l.account_id == asset.account_depreciation_id).mapped(
                        'balance')))
            elif asset.state == 'close':
                asset.value_residual -= abs(
                    sum(move.line_ids.filtered(lambda l: l.account_id != asset.account_depreciation_id).mapped(
                        'balance')))
            else:
                pass
                # raise UserError(_('You cannot post a depreciation on an asset in this state: %s') %
                #                 dict(self.env['account.asset']._fields['state'].selection)[asset.state])