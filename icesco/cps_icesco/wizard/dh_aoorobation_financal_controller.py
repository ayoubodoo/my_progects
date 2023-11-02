from odoo import models, fields, _, api
from odoo.exceptions import ValidationError
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta

class DhApprobationFinancalControllerWizard(models.TransientModel):
    _name = "dh.approbation.financal.controller.wizard"


    # date_dg = fields.Date("Date Approbation DG")
    signature_financal_controller = fields.Binary(string=' Financal Controller Signature')

    def button_financial_affair_approval(self):

        task_id = self.env["project.task"].search([('id', '=', self.env.context.get("active_id"))])
        print("task_id",task_id)
        task_id.dh_state = 'financial_affair_approval'
        task_id.signature_financal_controller = self.signature_financal_controller
        task_id.date_signature_financal_controller = datetime.now().strftime('%Y-%m-%d')
        if task_id.budget_compta == 0:
            raise ValidationError(
                _("Il n'est pas possible de valider l'activité si le montant reçu en comptabilité est nul.")
            )
        # task_id.dh_state = 'financial_affair_approval'
        task_id.date_validation = fields.Date.today()
        # notifications au cabdg
        for user in self.env['res.users'].search(
                [("groups_id", "=", self.env.ref("dh_icesco_project.group_cabdg").id)]):
            self.env['mail.activity'].create({
                'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                'user_id': user.id,
                'summary': 'Financial affair approved Activity',
                'note': 'The Activity %s has approved by the financial affair' % (task_id.name),
                'res_model_id': self.env['ir.model']._get('project.task').id,
                'res_id': task_id.id
            })

        # notifications aux differents support defini sur event
        if task_id.translation == True:
            for user in self.env['res.users'].search([('is_translation', '=', True)]):
                self.env['mail.activity'].create({
                    'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                    'user_id': user.id,
                    'summary': 'Financial affair approved Activity',
                    'note': 'The Activity %s has approved by the financial affair' % (task_id.name),
                    'res_model_id': self.env['ir.model']._get('project.task').id,
                    'res_id': task_id.id
                })
        if task_id.is_support_designing == True:
            for user in self.env['res.users'].search([('is_design', '=', True)]):
                self.env['mail.activity'].create({
                    'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                    'user_id': user.id,
                    'summary': 'Financial affair approved Activity',
                    'note': 'The Activity %s has approved by the financial affair' % (task_id.name),
                    'res_model_id': self.env['ir.model']._get('project.task').id,
                    'res_id': task_id.id
                })

        if task_id.is_support_legal == True:
            for user in self.env['res.users'].search([('is_legal', '=', True)]):
                self.env['mail.activity'].create({
                    'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                    'user_id': user.id,
                    'summary': 'Financial affair approved Activity',
                    'note': 'The Activity %s has approved by the financial affair' % (task_id.name),
                    'res_model_id': self.env['ir.model']._get('project.task').id,
                    'res_id': task_id.id
                })

        if task_id.is_support_logistics == True:
            for user in self.env['res.users'].search([('is_logistics', '=', True)]):
                self.env['mail.activity'].create({
                    'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                    'user_id': user.id,
                    'summary': 'Financial affair approved Activity',
                    'note': 'The Activity %s has approved by the financial affair' % (task_id.name),
                    'res_model_id': self.env['ir.model']._get('project.task').id,
                    'res_id': task_id.id
                })

        if task_id.is_support_protocol == True:
            for user in self.env['res.users'].search([('is_protocol', '=', True)]):
                self.env['mail.activity'].create({
                    'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                    'user_id': user.id,
                    'summary': 'Financial affair approved Activity',
                    'note': 'The Activity %s has approved by the financial affair' % (task_id.name),
                    'res_model_id': self.env['ir.model']._get('project.task').id,
                    'res_id': task_id.id
                })

        if task_id.is_support_finance == True:
            for user in self.env['res.users'].search([('is_finance', '=', True)]):
                self.env['mail.activity'].create({
                    'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                    'user_id': user.id,
                    'summary': 'Financial affair approved Activity',
                    'note': 'The Activity %s has approved by the financial affair' % (task_id.name),
                    'res_model_id': self.env['ir.model']._get('project.task').id,
                    'res_id': task_id.id
                })

        if task_id.is_support_it == True:
            for user in self.env['res.users'].search([('is_it', '=', True)]):
                self.env['mail.activity'].create({
                    'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                    'user_id': user.id,
                    'summary': 'Financial affair approved Activity',
                    'note': 'The Activity %s has approved by the financial affair' % (task_id.name),
                    'res_model_id': self.env['ir.model']._get('project.task').id,
                    'res_id': task_id.id
                })

        if task_id.is_support_admin == True:
            for user in self.env['res.users'].search([('is_admin', '=', True)]):
                self.env['mail.activity'].create({
                    'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                    'user_id': user.id,
                    'summary': 'Financial affair approved Activity',
                    'note': 'The Activity %s has approved by the financial affair' % (task_id.name),
                    'res_model_id': self.env['ir.model']._get('project.task').id,
                    'res_id': task_id.id
                })

        if task_id.is_support_media == True:
            for user in self.env['res.users'].search([('is_media', '=', True)]):
                self.env['mail.activity'].create({
                    'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                    'user_id': user.id,
                    'summary': 'Financial affair approved Activity',
                    'note': 'The Activity %s has approved by the financial affair' % (task_id.name),
                    'res_model_id': self.env['ir.model']._get('project.task').id,
                    'res_id': task_id.id
                })