import datetime as dt
import locale
import time
from datetime import timedelta, datetime, date
from odoo import models,fields
import base64
import io
from io import BytesIO
from dateutil.relativedelta import relativedelta

class PresenceXlsx(models.AbstractModel):
    _name = 'report.cps_icesco.report_presence_xlsx'
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
        month = datas.months
        year = datas.years
        # date_start = date(year=int(datas.years), month=int(datas.months), day=1)
        # date_end = date(year=int(datas.years), month=int(datas.months), day=(
        #                     date(year=int(datas.years), month=int(datas.months), day=1) + relativedelta(months=1) - timedelta(days=1)).day)
        date_start = datas.date_start
        date_end = datas.date_end

        locale.setlocale(locale.LC_ALL,
                         'fr_FR.UTF-8')  # sudo locale-gen fr_FR.UTF-8
        report_name = 'Attendances'
        worksheet = workbook.add_worksheet(report_name)
        format0 = workbook.add_format(
            {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'black', 'bg_color': 'white'})
        format1 = workbook.add_format(
            {'font_size': 18, 'align': 'center', 'valign': 'vcenter',
             'font_color': '#495057', 'bg_color': 'white', 'bold': True})
        format11 = workbook.add_format(
            {'font_size': 18, 'align': 'center', 'valign': 'vcenter',
             'font_color': '#495057', 'bg_color': 'white', 'bold': True, 'border': 1})
        format12 = workbook.add_format(
            {'font_size': 18, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'black', 'bg_color': '#9DC3E6', 'bold': True, 'border': 1})
        format13 = workbook.add_format(
            {'font_size': 18, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'black', 'bg_color': '#9DC3E6', 'bold': True, 'border': 1})
        format2 = workbook.add_format(
            {'font_size': 13, 'align': 'center', 'valign': 'vcenter',
             'font_color': '#495057', 'bold': True, 'bg_color': 'white',
             'underline': True})
        format4 = workbook.add_format(
            {'font_size': 15, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'black', 'bg_color': '#F8F5F7',
             'border': 1, 'border_color': 'black', 'bold': True})
        format5 = workbook.add_format(
            {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'black', 'bg_color': 'white',
             'border': 1, 'border_color': 'black'})
        format6 = workbook.add_format(
            {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'white', 'bg_color': '#44546A',
             'border': 1, 'border_color': 'black', })
        format60 = workbook.add_format(
            {'font_size': 14, 'align': 'left', 'valign': 'vleft',
             'font_color': 'black',
             'border': 1, 'border_color': 'black', })
        format61 = workbook.add_format(
            {'font_size': 14, 'align': 'left', 'valign': 'vleft',
             'font_color': 'black', 'bg_color': '#FFD966',
             'border': 1, 'border_color': 'black'})
        format15 = workbook.add_format(
            {'font_size': 12, 'align': 'left', 'valign': 'vcenter',
             'font_color': '#495057', 'bg_color': 'green', 'bold': True})
        format_retard = workbook.add_format(
            {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'white', 'bg_color': '#F89120',
             'border': 1, 'border_color': 'black', })
        format_conge_urgent = workbook.add_format(
            {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'white', 'bg_color': '#B0DD7F',
             'border': 1, 'border_color': 'black', })
        format_absence = workbook.add_format(
            {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'white', 'bg_color': '#ff4f4f',
             'border': 1, 'border_color': 'black', })
        format_maladie = workbook.add_format(
            {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'white', 'bg_color': '#00E668',
             'border': 1, 'border_color': 'black', })
        format_sortie_avant = workbook.add_format(
            {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'white', 'bg_color': '#843C0B',
             'border': 1, 'border_color': 'black', })
        format_auto_sortie = workbook.add_format(
            {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'white', 'bg_color': '#379430',
             'border': 1, 'border_color': 'black', })

        legend_format = workbook.add_format(
            {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'black', 'bg_color': '#379430',
             'border': 1, 'border_color': 'black', })

        format62 = workbook.add_format(
            {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
             'font_color': '#203864', 'bg_color': '#e7e6e6',
             'border': 1, 'border_color': 'black', })

        format63 = workbook.add_format(
            {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
             'font_color': '#203864', 'bg_color': '#70AD47',
             'border': 1, 'border_color': 'black', })

        format64 = workbook.add_format(
            {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
             'font_color': '#203864', 'bg_color': '#FFC000',
             'border': 1, 'border_color': 'black', })

        format65 = workbook.add_format(
            {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
             'font_color': '#203864', 'bg_color': '#FF0000',
             'border': 1, 'border_color': 'black', })

        worksheet.set_row(0, 30)
        worksheet.set_row(1, 30)
        worksheet.set_row(2, 30)
        worksheet.set_row(3, 30)
        worksheet.set_row(4, 30)
        worksheet.set_row(5, 30)
        worksheet.set_row(6, 30)


        worksheet.set_column('A:A', 70)
        worksheet.set_column('B:B', 10)
        worksheet.set_column('C:C', 10)
        worksheet.set_column('D:D', 10)
        worksheet.set_column('E:E', 10)
        worksheet.set_column('F:F', 10)
        worksheet.set_column('G:G', 10)
        worksheet.set_column('H:H', 10)
        worksheet.set_column('I:I', 10)
        worksheet.set_column('J:J', 10)
        worksheet.set_column('K:K', 10)
        worksheet.set_column('L:L', 10)
        worksheet.set_column('M:M', 10)
        worksheet.set_column('N:N', 10)
        worksheet.set_column('O:O', 10)
        worksheet.set_column('P:P', 10)
        worksheet.set_column('Q:Q', 10)
        worksheet.set_column('R:R', 10)
        worksheet.set_column('S:S', 10)
        worksheet.set_column('T:T', 10)
        worksheet.set_column('U:U', 10)
        worksheet.set_column('V:V', 10)
        worksheet.set_column('W:W', 10)
        worksheet.set_column('X:X', 10)
        worksheet.set_column('Y:Y', 10)
        worksheet.set_column('Z:Z', 10)
        worksheet.set_column('AA:AA', 10)
        worksheet.set_column('AB:AB', 10)
        worksheet.set_column('AC:AC', 20)

        # worksheet.merge_range('M1:P1', '', format1)
        worksheet.merge_range('A1:AB5', '', format1)

        presence_image = self.env.company.image_presence
        imgdata = base64.b64decode(presence_image)
        image = io.BytesIO(imgdata)
        worksheet.insert_image('A1:AB5', 'icesco_presence.png',
                           {'image_data': image, 'x_scale': 1.49, 'y_scale': 3})


        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

        worksheet.write('A6:A6', '%s %s' % (months[int(date_start.month)-1], date_start.year), format12)
        worksheet.write('A7:A7', 'Employee name', format13)

        start_date = date_start
        end_date = date_end

        delta = end_date - start_date

        i = 5
        j = 1
        WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        for day in range(delta.days + 1):
            if start_date.replace(day=day+ start_date.day).weekday() not in [5, 6]:
                if start_date.replace(day=day+ start_date.day).weekday() != 4:
                    worksheet.write(i, j, '%s' % (WEEKDAYS[start_date.replace(day=day+ start_date.day).weekday()])[:3], format5)
                    worksheet.write(i+1, j, '%s' % (day+ start_date.day), format6)
                    j = j + 1
                else:
                    worksheet.write(i, j, '%s' % (WEEKDAYS[start_date.replace(day=day+ start_date.day).weekday()])[:3], format5)
                    worksheet.write(i+1, j, '%s' % (day+ start_date.day), format6)
                    if self.check_if_last_day_of_week(start_date) == False:
                        worksheet.write(i, j+1, '', format15)
                        worksheet.write(i+1, j+1, '', format15)
                        j = j + 2
                    else:
                        j = j + 1

        worksheet.merge_range(i, j, i+1, j, '', format1)
        worksheet.write(i, j, 'Monthly Total', format6)

        i = 7
        j = 1

        for department in [*set(self.env['hr.attendance'].search([('check_out', '!=', False)]).filtered(lambda x:x.check_in.date() >= start_date and x.check_out.date() <= end_date).mapped('department_id') + self.env['hr.leave'].search([]).filtered(lambda x:x.date_from.date() >= start_date and x.date_to.date() <= end_date).mapped('department_id') + self.env['dh.autorisation.sortie'].search([('check_in', '!=', False)]).filtered(lambda x:x.check_out.date() >= start_date and x.check_in.date() <= end_date).mapped('department_id'))]:
            worksheet.set_row(i, 30)
            worksheet.write(i, 0, '%s' % (department.name), format61)
            i = i+1
            for employee in self.env['hr.employee'].search([('department_id', '=', department.id), ('active', '=', 'True'), ('sans_pointage', '=', False)]):
                j = 1
                worksheet.set_row(i, 30)
                worksheet.write(i, 0, '%s' % (employee.display_name), format60)
                total_monthly = 0

                for day in range(delta.days + 1):
                    if start_date.replace(day=day + start_date.day).weekday() not in [5, 6]:
                        retards = self.env['hr.attendance'].search([('horaire_id', '!=', False), ('employee_id', '=', employee.id), ('checkin_anomalie', '=', 'late')]).filtered(lambda x: x.check_in.date() == start_date.replace(day=day+ start_date.day))
                        time_retard = 0
                        for ret in retards:
                            time_retard += (datetime.strptime(ret.check_in.strftime('%H:%M:%S'),
                                                               '%H:%M:%S') - datetime.strptime(
                                ret.horaire_id.horaire_debut.strftime('%H:%M:%S'),
                                '%H:%M:%S')).total_seconds() / 60 if ret.horaire_id else 0

                        sortie_avant = self.env['hr.attendance'].search(
                            [('horaire_id', '!=', False), ('employee_id', '=', employee.id),
                             ('checkout_anomalie', '=', 'chekout_before_time')]).filtered(
                            lambda x: x.check_in.date() == start_date.replace(day=day + start_date.day))
                        time_sortie_avant = 0
                        for sor in sortie_avant:
                            time_sortie_avant += (datetime.strptime(
                                sor.horaire_id.horaire_fin.strftime('%H:%M:%S'),
                                '%H:%M:%S') - datetime.strptime(sor.check_out.strftime('%H:%M:%S'),
                                                                              '%H:%M:%S')).total_seconds() / 60 if sor.horaire_id else 0

                        presence = self.env['hr.attendance'].search([('employee_id', '=', employee.id)]).filtered(lambda x: x.check_in.date() == start_date.replace(day=day+ start_date.day))

                        conge = self.env['hr.leave'].search([('employee_id', '=', employee.id)]).filtered(lambda
                                                                                                      x: x.date_from.date() <= start_date.replace(day=day+ start_date.day) <= x.date_to.date())

                        conge_urgent = self.env['hr.leave'].search([('employee_id', '=', employee.id)]).filtered(lambda x:x.date_from.date() <= start_date.replace(day=day+ start_date.day) <= x.date_to.date() and x.holiday_status_id.is_urgent == True)

                        conge_maladie = self.env['hr.leave'].search([('employee_id', '=', employee.id)]).filtered(
                            lambda x: x.date_from.date() <= start_date.replace(day=day+ start_date.day) <= x.date_to.date() and x.holiday_status_id.is_maladie == True)

                        autorisation_sortie = self.env['dh.autorisation.sortie'].search(
                            [('check_in', '!=', False), ('employee_id', '=', employee.id)]).filtered(
                            lambda x: x.check_out.date() == start_date.replace(day=day + start_date.day))
                        time_auto_sortie = 0
                        for auto_sor in autorisation_sortie:
                            time_auto_sortie += (datetime.strptime(auto_sor.check_in.strftime('%H:%M:%S'),
                                                                '%H:%M:%S') - datetime.strptime(auto_sor.check_out.strftime('%H:%M:%S'),
                                                                '%H:%M:%S')).total_seconds() / 60

                        # total_monthly += (time_retard + time_sortie_avant + time_auto_sortie) / 60


                        if time_retard > 0:
                            worksheet.write(i, j, '%.2f' % (time_retard), format_retard)
                            total_monthly += time_retard / 60
                        elif len(conge_urgent) > 0:
                            worksheet.write(i, j, 'E', format_conge_urgent)
                        elif len(conge_maladie) > 0:
                            print('test')
                            worksheet.write(i, j, 'S', format_maladie)
                        elif len(conge) == 0 and len(presence) == 0:
                            worksheet.write(i, j, 'I', format_absence)
                        elif time_sortie_avant > 0:
                            worksheet.write(i, j, '%.2f' % (time_sortie_avant), format_sortie_avant)
                            total_monthly += time_sortie_avant / 60
                        elif len(presence) > 0 and ((sum(presence.mapped('worked_hours')) < 7 and (start_date.replace(day=day + start_date.day).weekday() in [0, 1, 2, 3])) or (sum(presence.mapped('worked_hours')) < 5 and (start_date.replace(day=day + start_date.day).weekday() in [4]))):
                            if start_date.replace(day=day + start_date.day).weekday() in [4]:
                                worksheet.write(i, j, '%.2f' % (5- sum(presence.mapped('worked_hours'))), format_sortie_avant)
                                total_monthly += (5- sum(presence.mapped('worked_hours'))) / 60
                            else:
                                worksheet.write(i, j, '%.2f' % (7 - sum(presence.mapped('worked_hours'))), format_sortie_avant)
                                total_monthly += (7 - sum(presence.mapped('worked_hours'))) / 60

                        elif time_auto_sortie > 0:
                            worksheet.write(i, j, '%.2f' % (time_auto_sortie), format_auto_sortie)
                            total_monthly += time_auto_sortie / 60
                        else:
                            worksheet.write(i, j, '', format60)

                        if start_date.replace(day=day + start_date.day).weekday() != 4:
                            j = j + 1
                        else:
                            if self.check_if_last_day_of_week(start_date) == False:
                                worksheet.write(i, j+1, '', format15)
                                j = j + 2
                            else:
                                j = j + 1

                if 0 < total_monthly < 2:
                    worksheet.write(i, j, '%.2f' % (total_monthly), format63)
                elif 2 < total_monthly < 5:
                    worksheet.write(i, j, '%.2f' % (total_monthly), format64)
                elif 5 < total_monthly:
                    worksheet.write(i, j, '%.2f' % (total_monthly), format65)
                else:
                    worksheet.write(i, j, '', format62)


                i = i+1

        i = i+1
        worksheet.set_row(i-1, 20)
        worksheet.set_row(i, 20)
        worksheet.set_row(i+1, 20)
        worksheet.set_row(i+2, 20)
        worksheet.set_row(i+3, 20)
        worksheet.set_row(i+4, 20)
        worksheet.set_row(i+5, 20)
        worksheet.set_row(i+6, 20)
        worksheet.write(i, 0, 'Legend', legend_format)
        worksheet.write(i+1, 0, 'D', format_retard)
        worksheet.write(i+2, 0, 'E', format_conge_urgent)
        worksheet.write(i+3, 0, 'S', format_maladie)
        worksheet.write(i+4, 0, 'I', format_absence)
        worksheet.write(i+5, 0, 'L', format_sortie_avant)
        worksheet.write(i+6, 0, 'P', format_auto_sortie)