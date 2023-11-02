import datetime as dt
import locale
import time
from datetime import timedelta, datetime, date
from odoo import models,fields
import base64
import io
from io import BytesIO
from dateutil.relativedelta import relativedelta

class ReportGlobalEvaluation(models.TransientModel):
    _name = 'report.global.evaluation'

    start_date = fields.Date("Start Date", default=fields.Date.from_string(
        str(fields.Date.today().year) + '-01-01'))
    end_date = fields.Date("End Date", default=fields.Date.from_string(
        str(fields.Date.today().year) + '-12-31'))

    # type = fields.Selection([('mensuel', 'Mensuel'), ('trimestriel', 'Trimestriel'), ('annuel', 'Annuel')], string='Type', required=True)

    def generate_excel(self):
        # data = {'month': self.months, 'year': self.years, 'date_start': date(year=int(self.years), month=int(self.months), day=1), 'date_end': date(year=int(self.years), month=int(self.months), day=(date(year=int(self.years), month=int(self.months), day=1) + relativedelta(months=1) - timedelta(days=1)).day)}
        data = {'date_start': self.start_date, 'date_end': self.end_date}
        # data = {}
        return self.env.ref('kzm_hr_appraisal.report_global_evaluation_xlsx').report_action(self, data=data)