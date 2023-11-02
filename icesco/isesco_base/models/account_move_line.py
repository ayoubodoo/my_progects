# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from .amount_to_text_fr import amount_to_text_fr
from datetime import timedelta
from dateutil.relativedelta import relativedelta

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    validation = fields.Selection([('none',"None"),('validation1', "Validation 1"),
                              ('validation2', "Validation 2")], default='none')
    # show_validation1 = fields.Boolean('Show Validation 1',default=True)
    # show_validation2 = fields.Boolean('Show Validation 2')
    taux = fields.Float(string="Taux", compute='compute_taux', inverse='uncompute_taux')
    currency_usd_id = fields.Many2one("res.currency", default=lambda self: self.env.ref('base.USD').id, string="Currency USD")
    total = fields.Monetary(compute='_compute_total', string='Montant USD', digits=(16, 2), store=True) # inverse='_inverse_total',
    parent_taux = fields.Float(string='Parent Taux', related='move_id.taux')
    remet_taux_zero = fields.Boolean(string='Remettre Taux A Zero', related='move_id.remet_taux_zero')
    move_asset_id = fields.Many2one('account.asset', related='move_id.asset_id')
    asset_taux = fields.Float(string='Asset Taux', related='move_asset_id.taux')
    asset_remet_taux_zero = fields.Boolean(string='Remettre Taux A Zero', related='move_asset_id.remet_taux_zero')

    def uncompute_taux(self):
        pass

    @api.depends('company_currency_id', 'type_convertion', 'parent_state', 'state', 'create_date', 'parent_taux', 'asset_taux', 'move_asset_id', 'move_asset_id.acquisition_date', 'remet_taux_zero')
    def compute_taux(self):
        for rec in self:
            total = 0
            if rec.debit == 0:
                total = rec.credit
            if rec.credit == 0:
                total = rec.debit
            if rec.move_asset_id.id == False:
                if rec.parent_taux != 0:
                    rec.taux = rec.parent_taux
                elif rec.parent_taux == 0 and rec.remet_taux_zero == True:
                    rec.taux = 0
                elif rec.type_convertion == 'jour':
                    if rec.date:
                        if rec.company_currency_id.with_context(date=rec.date).compute(total, self.env.ref('base.USD')) > 0:
                            rec.taux = total / rec.company_currency_id.with_context(date=rec.date).compute(
                            total, self.env.ref('base.USD'))
                        else:
                            rec.taux = 0
                    else:
                        rec.taux = 0
                # elif rec.type_convertion == 'historique':
                #     if rec.create_date:
                #         if rec.company_currency_id.with_context(date=rec.create_date).compute(total, self.env.ref('base.USD')) > 0:
                #             rec.taux = total / rec.company_currency_id.with_context(date=rec.create_date).compute(
                #             total, self.env.ref('base.USD'))
                #         else:
                #             rec.taux = 0
                #     else:
                #         rec.taux = 0
                elif rec.type_convertion == 'cloture':
                    if rec.create_date:
                        if (rec.create_date + timedelta(days=1)).month != rec.create_date.month:
                            if rec.company_currency_id.with_context(date=rec.create_date).compute(total, self.env.ref('base.USD')) > 0:
                                rec.taux = total / rec.company_currency_id.with_context(date=rec.create_date).compute(
                                total, self.env.ref('base.USD'))
                            else:
                                rec.taux = 0
                        else:
                            if rec.company_currency_id.with_context(date=(rec.create_date + relativedelta(day=1)) - timedelta(days=1)).compute(total, self.env.ref('base.USD')) > 0:
                                rec.taux = total / rec.company_currency_id.with_context(date=(rec.create_date + relativedelta(day=1)) - timedelta(days=1)).compute(
                                total, self.env.ref('base.USD'))
                            else:
                                rec.taux = 0
                    else:
                        rec.taux = 0
                else:
                    if rec.date:
                        if rec.company_currency_id.with_context(date=rec.date).compute(total, self.env.ref('base.USD')) > 0:
                            rec.taux = total / rec.company_currency_id.with_context(date=rec.date).compute(
                                total, self.env.ref('base.USD'))
                        else:
                            rec.taux = 0
                    else:
                        rec.taux = 0
            else:
                if rec.asset_taux != 0:
                    rec.taux = rec.asset_taux
                elif rec.asset_taux == 0 and rec.asset_remet_taux_zero == True:
                    rec.taux = 0
                elif rec.move_asset_id.acquisition_date:
                    if rec.company_currency_id.with_context(date=rec.move_asset_id.acquisition_date).compute(total,
                                                                                   self.env.ref('base.USD')) > 0:
                        rec.taux = total / rec.company_currency_id.with_context(date=rec.move_asset_id.acquisition_date).compute(
                            total, self.env.ref('base.USD'))
                    else:
                        rec.taux = 0
                else:
                    rec.taux = 0

    @api.depends('taux', 'debit', 'credit')
    def _compute_total(self):
        for r in self:
            r.total = 0
            if r.debit == 0 and r.taux > 0:
                r.total = round((-r.credit / r.taux), 2)
            if r.credit == 0 and r.taux > 0:
                r.total = round((r.debit / r.taux), 2)

    # @api.depends('total', 'debit', 'credit')
    # def _inverse_total(self):
    #     for r in self:
    #         r.taux = 1
    #         if r.debit == 0 and r.total:
    #             r.taux = abs(r.credit / r.total)
    #         if r.credit == 0 and r.total:
    #             r.taux = abs(r.debit / r.total)

    @api.onchange('taux')
    def change_taux_account_move(self):
        for rec in self:
            if rec.taux != 0:
                rec.move_id.taux = rec.taux

    @api.depends('parent_state')
    def validate1(self):
        for r in self:
            if r.parent_state == 'posted':
                r.validation = 'validation1'
                # r.show_validation2 = True

    @api.depends('parent_state')
    def validate2(self):
        for r in self:
            if r.parent_state == 'posted':
                r.validation = 'validation2'
                # r.show_validation2 = False
