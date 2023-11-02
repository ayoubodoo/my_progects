import datetime as dt
import locale
import time
from datetime import timedelta, datetime
from odoo import models,fields
import base64
import io
from io import BytesIO

class DhReportIr(models.TransientModel):
    _name = 'report.ir.retrait'

    # date_start = fields.Date(string='Année', required=True)
    annee = fields.Selection(
        selection='years_selection',
        string="Année",
    )

    def years_selection(self):
        year_list = []
        for y in range(datetime.now().year - 20, datetime.now().year + 30):
            year_list.append((str(y), str(y)))
        return year_list


    # date_end = fields.Date(string='Vers', required=True)
    # type = fields.Selection([('mensuel', 'Mensuel'), ('trimestriel', 'Trimestriel'), ('annuel', 'Annuel')], string='Type', required=True)

    def generate_excel(self):
        data = {'annee': self.annee}
        # data = {}
        return self.env.ref('kzm_medical_insurance.report_ir_retrait_xlsx').report_action(self, data=data)
