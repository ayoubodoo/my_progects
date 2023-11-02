# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, _, api
from odoo.exceptions import ValidationError

class CpsAssetWizard(models.TransientModel):
    _name = "cps.asset.wizard"

    # first_date = fields.Date(string='Date Debut', required=True)
    last_date = fields.Date(string='Date Fin', required=True)
    first_code = fields.Many2one('account.asset', string='Premier Code', domain=[('asset_type', '=', 'purchase'), ('state', '!=', 'model'), ('parent_id', '=', False)])
    end_code = fields.Many2one('account.asset', string='Dernier Code', domain=[('asset_type', '=', 'purchase'), ('state', '!=', 'model'), ('parent_id', '=', False)])

    def generer_lines(self):
        for rec in self:
            self.env['cps.account.move'].search([]).unlink()
            for asset in self.env['account.asset'].search([('asset_type', '=', 'purchase'), ('state', '!=', 'model'), ('parent_id', '=', False)]):
                if rec.first_code and rec.end_code:
                    if int(rec.first_code.code) <= int(asset.code) <= int(rec.end_code.code):
                        if asset.depreciation_move_ids.filtered(lambda x:x.date <= rec.last_date and x.state == 'posted'): # and x.name != '/'
                            move = asset.depreciation_move_ids.filtered(lambda x:x.date <= rec.last_date and x.state == 'posted')[0] # and x.name != '/'
                            self.env['cps.account.move'].create({'last_date': rec.last_date, 'asset_id': asset.id, 'move_asset_id': move.id}) # 'first_date': rec.first_date,
                        else:
                            self.env['cps.account.move'].create({'last_date': rec.last_date, 'asset_id': asset.id, 'move_asset_id': False}) # 'first_date': rec.first_date,
                elif rec.first_code and rec.end_code == False:
                    if int(rec.first_code.code) <= int(asset.code):
                        if asset.depreciation_move_ids.filtered(lambda x:x.date <= rec.last_date and x.state == 'posted'): # and x.name != '/'
                            move = asset.depreciation_move_ids.filtered(lambda x:x.date <= rec.last_date and x.state == 'posted')[0] # and x.name != '/'
                            self.env['cps.account.move'].create({'last_date': rec.last_date, 'asset_id': asset.id, 'move_asset_id': move.id}) # 'first_date': rec.first_date,
                        else:
                            self.env['cps.account.move'].create({'last_date': rec.last_date, 'asset_id': asset.id, 'move_asset_id': False}) # 'first_date': rec.first_date,
                elif rec.first_code == False and rec.end_code:
                    if int(asset.code) <= int(rec.end_code.code):
                        if asset.depreciation_move_ids.filtered(lambda x:x.date <= rec.last_date and x.state == 'posted'): # and x.name != '/'
                            move = asset.depreciation_move_ids.filtered(lambda x:x.date <= rec.last_date and x.state == 'posted')[0] # and x.name != '/'
                            self.env['cps.account.move'].create({'last_date': rec.last_date, 'asset_id': asset.id, 'move_asset_id': move.id}) # 'first_date': rec.first_date,
                        else:
                            self.env['cps.account.move'].create({'last_date': rec.last_date, 'asset_id': asset.id, 'move_asset_id': False}) # 'first_date': rec.first_date,
                else:
                    if asset.depreciation_move_ids.filtered(lambda x:x.date <= rec.last_date and x.state == 'posted'): # and x.name != '/'
                        move = asset.depreciation_move_ids.filtered(lambda x:x.date <= rec.last_date and x.state == 'posted')[0] # and x.name != '/'
                        self.env['cps.account.move'].create({'last_date': rec.last_date, 'asset_id': asset.id, 'move_asset_id': move.id}) # 'first_date': rec.first_date,
                    else:
                        self.env['cps.account.move'].create({'last_date': rec.last_date, 'asset_id': asset.id, 'move_asset_id': False}) # 'first_date': rec.first_date,
            return {
                'name': 'Actifs Par Date',
                'res_model': 'cps.account.move',
                'type': 'ir.actions.act_window',
                'context': {},
                'view_mode': 'list',
                'view_type': 'tree',
                'domain': [],
                'view_id': self.env.ref("cps_icesco.cps_cps_account_move_tree_view").id,
                'target': 'target'
            }
