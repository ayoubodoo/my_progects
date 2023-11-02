import datetime as dt
import locale
import time
from datetime import timedelta, datetime, date
from odoo import models,fields
import base64
import io
from io import BytesIO
from dateutil.relativedelta import relativedelta

class GlobalEvaluationXlsx(models.AbstractModel):
    _name = 'report.kzm_hr_appraisal.report_global_evaluation_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def check_if_last_day_of_week(self, date):
        import datetime
        import calendar
        #  calendar.monthrange return a tuple (weekday of first day of the
        #  month, number
        #  of days in month)
        last_day_of_month = calendar.monthrange(date.year, date.month)[1]
        # here i check if date is last day of month
        if date == datetime.date(date.year, date.month, last_day_of_month):
            return True
        return False

    def generate_xlsx_report(self, workbook, data, datas):
        # for rec in datas:

        date_start = datas.start_date
        date_end = datas.end_date

        locale.setlocale(locale.LC_ALL,
                         'fr_FR.UTF-8')  # sudo locale-gen fr_FR.UTF-8
        report_name = 'Appraisal'
        worksheet = workbook.add_worksheet(report_name)
        format11 = workbook.add_format(
            {'font_size': 14,
             'font_color': 'black',})
        format12 = workbook.add_format(
            {'font_size': 18,
             'font_color': 'black', 'bold': True,})
        format13 = workbook.add_format(
            {'font_size': 22, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'black', 'bold': True,})
        format59 = workbook.add_format(
            {'font_size': 14, 'align': 'left', 'valign': 'vleft',
             'font_color': 'black', 'bg_color': '#A6A6A6',
             'border': 1, 'border_color': 'black', 'bold': True,})
        format60 = workbook.add_format(
            {'font_size': 14, 'align': 'left', 'valign': 'vleft',
             'font_color': 'black',
             'border': 1, 'border_color': 'black', })
        format61 = workbook.add_format(
            {'font_size': 14, 'align': 'left', 'valign': 'vleft',
             'font_color': 'black', 'bg_color': '#4F6228',
             'border': 1, 'border_color': 'black'})
        format62 = workbook.add_format(
            {'font_size': 14, 'align': 'left', 'valign': 'vleft',
             'font_color': 'black', 'bg_color': '#ebf1de',
             'border': 1, 'border_color': 'black', })
        format63 = workbook.add_format(
            {'font_size': 14, 'align': 'left', 'valign': 'vleft',
             'font_color': 'black', 'bg_color': '#ebf1de',
             'border': 1, 'border_color': 'black', })
        format64 = workbook.add_format(
            {'font_size': 14, 'align': 'left', 'valign': 'vleft',
             'font_color': 'black', 'bg_color': '#c3d69b',
             'border': 1, 'border_color': 'black', })
        format65 = workbook.add_format(
            {'font_size': 14, 'align': 'left', 'valign': 'vleft',
             'font_color': 'black', 'bg_color': '#77933C',
             'border': 1, 'border_color': 'black', })

        worksheet.set_row(0, 40)
        worksheet.set_row(1, 40)
        worksheet.set_row(2, 40)
        worksheet.set_row(3, 40)
        worksheet.set_row(4, 40)
        worksheet.set_row(5, 40)
        worksheet.set_row(6, 40)
        worksheet.set_row(7, 40)
        worksheet.set_row(8, 40)


        worksheet.set_column('A:A', 8)
        worksheet.set_column('B:B', 30)
        worksheet.set_column('C:C', 30)
        worksheet.set_column('D:D', 30)
        worksheet.set_column('E:E', 30)
        worksheet.set_column('F:F', 30)
        worksheet.set_column('G:G', 30)
        worksheet.set_column('H:H', 30)
        worksheet.set_column('I:I', 30)

        # worksheet.merge_range('M1:P1', '', format1)
        worksheet.merge_range('A1:B5', '', format11)
        worksheet.merge_range('E5:F5', '', format11)
        worksheet.merge_range('G1:H1', '', format11)
        worksheet.merge_range('G2:H2', '', format11)

        logo = self.env.company.logo
        imgdata = base64.b64decode(logo)
        image = io.BytesIO(imgdata)
        worksheet.insert_image('A1:B5', 'logo.png',
                           {'image_data': image, 'x_scale': 1.5, 'y_scale': 1})


        worksheet.write('E5:F5', 'ANNUAL APPRAISAL REPORT', format13)
        worksheet.write('G1:H1', 'Human Resources Department', format12)
        worksheet.write('G2:H2', 'Administrative Affairs Directorate', format12)
        worksheet.write('H3:H3', 'Date', format11)
        worksheet.write('I3:I3', '%s' % (date.today().strftime('%d/%m/%Y')), format11)

        start_date = date_start
        end_date = date_end

        delta = end_date - start_date

        worksheet.write(8, 0, '', format61)
        worksheet.write(8, 1, 'Référence', format61)
        worksheet.write(8, 2, 'Employé', format61)
        worksheet.write(8, 3, 'Département', format61)
        worksheet.write(8, 4, 'Catégorie de salaire', format61)
        worksheet.write(8, 5, 'Date de recrutement', format61)
        worksheet.write(8, 6, "Date d'évaluation", format61)
        worksheet.write(8, 7, "Note d'évaluation", format61)
        worksheet.write(8, 8, 'Appréciation', format61)

        i = 9
        n = 1

        excellent = 0
        very_good = 0
        good = 0
        weak = 0

        for evaluation in self.env['appraisal.appraisal'].search([('evaluation_date', '!=', False)]).filtered(lambda x: x.evaluation_date >= start_date and x.evaluation_date <= end_date):
            worksheet.set_row(i, 40)

            worksheet.write(i, 0, '%s' % (n), format59)
            worksheet.write(i, 1, '%s' % (evaluation.name), format60)
            worksheet.write(i, 2, '%s' % (evaluation.employee_id.display_name), format60)
            worksheet.write(i, 3, '%s' % (evaluation.department_id.display_name), format60)
            worksheet.write(i, 4, '%s' % (evaluation.salary_category_id.display_name), format60)
            worksheet.write(i, 5, '%s' % (evaluation.recruitment_date), format60)
            worksheet.write(i, 6, '%s' % (evaluation.evaluation_date), format60)
            worksheet.write(i, 7, '%s' % (evaluation.appraisal_note), format60)

            if evaluation.appreciation == 'weak':
                weak += 1
                worksheet.write(i, 8, '%s' % (
                    dict(evaluation._fields['appreciation'].selection).get(evaluation.appreciation)), format62)
            elif evaluation.appreciation == 'good':
                good += 1
                worksheet.write(i, 8, '%s' % (
                    dict(evaluation._fields['appreciation'].selection).get(evaluation.appreciation)), format63)
            elif evaluation.appreciation == 'very_good':
                very_good += 1
                worksheet.write(i, 8, '%s' % (
                    dict(evaluation._fields['appreciation'].selection).get(evaluation.appreciation)), format64)
            elif evaluation.appreciation == 'excellent':
                excellent += 1
                worksheet.write(i, 8, '%s' % (
                    dict(evaluation._fields['appreciation'].selection).get(evaluation.appreciation)), format65)
            else:
                worksheet.write(i, 8, '', format60)

            n = n + 1
            i = i + 1

        i = i + 2

        worksheet.set_row(i, 40)
        worksheet.set_row(i+1, 40)
        worksheet.set_row(i+2, 40)
        worksheet.set_row(i+3, 40)
        worksheet.set_row(i+4, 40)

        worksheet.write(i, 2, 'Excellent', format65)
        worksheet.write(i, 3, '%s' % (excellent), format60)
        worksheet.write(i+1, 2, 'Very good', format64)
        worksheet.write(i+1, 3, '%s' % (very_good), format60)
        worksheet.write(i+2, 2, 'Good', format63)
        worksheet.write(i+2, 3, '%s' % (good), format60)
        worksheet.write(i+3, 2, 'Weak', format62)
        worksheet.write(i+3, 3, '%s' % (weak), format60)
        worksheet.write(i+4, 3, '%s' % (excellent+very_good+good+weak), format62)