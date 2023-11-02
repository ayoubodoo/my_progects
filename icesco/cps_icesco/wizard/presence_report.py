import datetime as dt
import locale
import time
from datetime import timedelta, datetime, date
from odoo import models,fields
import base64
import io
from io import BytesIO
from dateutil.relativedelta import relativedelta

class ReportPresence(models.TransientModel):
    _name = 'report.presence'

    months = fields.Selection([('1', 'Janvier'), ('2', 'Février'), ('3', 'Mars'), ('4', 'Avril'), ('5', 'Mai'), ('6', 'Juin'), ('7', 'Juillet'), ('8', 'Août'), ('9', 'Septembre'), ('10', 'Octobre'), ('11', 'Novembre'), ('12', 'Décembre')])
    years = fields.Selection(string='Year', selection='years_selection')

    def years_selection(self):
        year_list = []
        for y in range(datetime.now().year - 10, datetime.now().year + 10):
            year_list.append((str(y), str(y)))
        return year_list

    date_start = fields.Date(string='De', required=True) #
    date_end = fields.Date(string='Vers', required=True) #

    # type = fields.Selection([('mensuel', 'Mensuel'), ('trimestriel', 'Trimestriel'), ('annuel', 'Annuel')], string='Type', required=True)

    def generate_excel(self):
        # data = {'month': self.months, 'year': self.years, 'date_start': date(year=int(self.years), month=int(self.months), day=1), 'date_end': date(year=int(self.years), month=int(self.months), day=(date(year=int(self.years), month=int(self.months), day=1) + relativedelta(months=1) - timedelta(days=1)).day)}
        data = {'month': self.months, 'year': self.years, 'date_start': self.date_start, 'date_end': self.date_end}
        # data = {}
        return self.env.ref('cps_icesco.report_presences_xlsx').report_action(self, data=data)