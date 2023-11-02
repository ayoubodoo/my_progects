# # -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from odoo.tools import format_datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_round
from datetime import date, datetime, timedelta


class CpsHrContract(models.Model):
    _inherit = 'hr.contract'

    def verify_periode_essaie(self):
        first_user = False
        remain_user_ids = []
        i = 0
        for user1 in self.env['res.users'].search(
                [("groups_id", "=", self.env.ref("hr.group_hr_manager").id)]):
            if user1.has_group('hr_contract.group_hr_contract_manager') and i == 0:
                first_user = user1[0]
                i = i + 1

        for user in self.env['res.users'].search(
                [("groups_id", "=", self.env.ref("hr.group_hr_manager").id)]):
            if user.has_group('hr_contract.group_hr_contract_manager'):
                if user.id != first_user.id:
                    remain_user_ids.append(user.id)

        for contract in self.env['hr.contract'].search([('active', '=', True), ('state', '=', 'open'), ('trial_date_end', '!=', False)]):
            # if contract.trial_date_end and first_user.id != False:
            if int(self.env["ir.config_parameter"].sudo().get_param("cps_icesco.notif_fin_periode_essai")) >= (contract.trial_date_end - fields.Date.today()).days >= 0:
                if len(self.env['mail.activity'].search(
                        [('user_id', '=', self.env['res.users'].search([('login', '=', 'rh@icesco.org')]).id), ('date_deadline', '=', contract.trial_date_end), ('summary', 'ilike', 'la période d’essai'), ('res_id', '=', contract.id)])) == 0:
                    self.env['mail.activity'].create({
                                'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                                'user_id': self.env['res.users'].search([('login', '=', 'rh@icesco.org')]).id,
                                # 'multiple_users': [(6, 0, remain_user_ids)],
                                'summary': 'la période d’essai',
                                'note': 'Le collaborateur suivant s’approche de la fin de la période d’essai : %s' % (contract.trial_date_end),
                                'date_deadline': contract.trial_date_end,
                                'res_model_id': self.env['ir.model']._get('hr.contract').id,
                                'res_id': contract.id
                            })

    def verify_end_contract(self):
        first_user = False
        remain_user_ids = []
        i = 0
        for user1 in self.env['res.users'].search(
                [("groups_id", "=", self.env.ref("hr.group_hr_manager").id)]):
            if user1.has_group('hr_contract.group_hr_contract_manager') and i == 0:
                first_user = user1[0]
                i = i + 1

        for user in self.env['res.users'].search(
                [("groups_id", "=", self.env.ref("hr.group_hr_manager").id)]):
            if user.has_group('hr_contract.group_hr_contract_manager'):
                if user.id != first_user.id:
                    remain_user_ids.append(user.id)

        for contract in self.env['hr.contract'].search([('active', '=', True), ('state', '=', 'open'), ('date_end', '!=', False)]):
            # if first_user.id != False:
            if int(self.env["ir.config_parameter"].sudo().get_param("cps_icesco.notif_fin_contrat")) >= (
                    contract.date_end - fields.Date.today()).days >= 0:
                if len(self.env['mail.activity'].search([('user_id', '=', self.env['res.users'].search([('login', '=', 'rh@icesco.org')]).id), ('date_deadline', '=', contract.date_end), ('summary', 'ilike', 'fin de contrat'), ('res_id', '=', contract.id)])) == 0:
                    self.env['mail.activity'].create({
                        'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                        'user_id': self.env['res.users'].search([('login', '=', 'rh@icesco.org')]).id,
                        # 'multiple_users': [(6, 0, remain_user_ids)],
                        'summary': 'fin de contrat',
                        'note': 'Le collaborateur suivant s’approche de la fin de contrat : %s' % (contract.date_end),
                        'date_deadline': contract.date_end,
                        'res_model_id': self.env['ir.model']._get('hr.contract').id,
                        'res_id': contract.id
                    })