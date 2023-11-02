# # -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from odoo.tools import format_datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_round
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta


class CpsHrEmployeeDependent(models.Model):
    _inherit = 'hr.employee.dependent'

    def verify_age(self):
        for children in self.env['hr.employee.dependent'].search([('birthday', '!=', False)]).filtered(lambda x: relativedelta(fields.Date.today(),x.birthday).years >= self.env.company.age_limit and x.employee_id.active == True):
            if len(self.env['mail.activity'].search(
                    [('res_id', '=', children.employee_id.id),
                     ('summary', 'ilike', 'children age limit'),
                     ('note', 'ilike', "L'enfant %s du collaborateur suivant ne seront plus pris en charge" % (children.name))])) == 0:
                self.env['mail.activity'].create({
                            'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                            'user_id': self.env['res.users'].search([('login', '=', 'rh@icesco.org')]).id,
                            'summary': 'children age limit',
                            'note': "<p>L'enfant %s du collaborateur suivant ne seront plus pris en charge a partir du Date %s</p><p>Merci de regénérer <<rubriques dependents>> dans le contrat<p>" % (children.name, children.birthday+timedelta(days=self.env.company.age_limit*365)),
                            'res_model_id': self.env['ir.model']._get('hr.employee').id,
                            'res_id': children.employee_id.id
                        })

    def verify_age_limit_remboursement(self):
        for children in self.env['hr.employee.dependent'].search([('birthday', '!=', False)]).filtered(lambda x: relativedelta(fields.Date.today(),x.birthday).years >= self.env.company.age_limit_remboursement and x.employee_id.active == True):
            if len(self.env['mail.activity'].search(
                    [('res_id', '=', children.employee_id.id),
                     ('summary', 'ilike', 'children remboursement age limit'),
                     ('note', 'ilike', "<p>Votre enfant %s ne bénéficiera plus du Remboursement des Cotisations Salariales et Mutuelle" % (children.name))])) == 0:
                self.env['mail.activity'].create({
                            'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                            # 'user_id': children.employee_id.id,
                            'user_id': self.env['res.users'].search([('login', '=', 'rh@icesco.org')]).id,
                            'summary': 'children remboursement age limit',
                            'note': "<p>Votre enfant %s ne bénéficiera plus du Remboursement des Cotisations Salariales et Mutuelle à partir du Date %s</p><p>Merci de regénérer <<rubriques dependents>> dans le contrat<p>" % (children.name, children.birthday+timedelta(days=self.env.company.age_limit_remboursement*365)),
                            'res_model_id': self.env['ir.model']._get('hr.employee').id,
                            'res_id': children.employee_id.id
                        })
