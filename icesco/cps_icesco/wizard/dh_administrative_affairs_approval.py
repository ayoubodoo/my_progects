from odoo import models, fields, _, api
from odoo.exceptions import ValidationError
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta

class DhAdministrativeAffairsApprovalWizard(models.TransientModel):
    _name = "dh.approbation.administrative.affairs.wizard"


    signature_adm_affairs = fields.Binary(string='Signature Administrative Affairs Approval')

    def button_admin_affair_approval(self):

        task_id = self.env["project.task"].search([('id', '=', self.env.context.get("active_id"))])
        print("task_id",task_id)
        task_id.dh_state = 'admin_affair_approval'
        task_id.signature_adm_affairs = self.signature_adm_affairs
        task_id.date_adm_affairs = datetime.now().strftime('%Y-%m-%d')
        print("date_dg",task_id.date_dg)