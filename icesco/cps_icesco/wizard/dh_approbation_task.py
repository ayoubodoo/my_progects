from odoo import models, fields, _, api
from odoo.exceptions import ValidationError
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta

class DhApprobationDGWizard(models.TransientModel):
    _name = "dh.approbation.dg.wizard"


    # date_dg = fields.Date("Date Approbation DG")
    signature_dg = fields.Binary(string='Signature DG')

    def button_dg_approval(self):

        task_id = self.env["project.task"].search([('id', '=', self.env.context.get("active_id"))])
        task_id.dh_state = 'dg_approval'
        task_id.signature_dg = self.signature_dg
        task_id.date_dg = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
