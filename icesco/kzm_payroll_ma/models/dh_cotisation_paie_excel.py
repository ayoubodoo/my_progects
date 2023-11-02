import datetime as dt
import locale
import time
from datetime import timedelta, datetime
from odoo import models,fields
import base64
import io
from io import BytesIO

class DhCotisationsXlsx(models.AbstractModel):
    _name = 'report.kzm_payroll_ma.dh_cotisation_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, datas):
        for rec in datas:
            locale.setlocale(locale.LC_ALL,
                             'fr_FR.UTF-8')  # sudo locale-gen fr_FR.UTF-8
            report_name = '%s' % (rec.name)
            worksheet = workbook.add_worksheet(report_name)
            format0 = workbook.add_format(
                {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
                 'font_color': 'black', 'bg_color': 'white'})
            format1 = workbook.add_format(
                {'font_size': 22, 'align': 'center', 'valign': 'vcenter',
                 'font_color': '#495057', 'bg_color': 'white', 'bold': True})
            format2 = workbook.add_format(
                {'font_size': 18, 'align': 'center', 'valign': 'vcenter',
                 'font_color': '#495057', 'bold': True, 'bg_color': 'white',
                 'underline': True})
            format4 = workbook.add_format(
                {'font_size': 15, 'align': 'center', 'valign': 'vcenter',
                 'font_color': 'black', 'bg_color': '#C5E0B4',
                 'border': 1,'border_color': 'black', 'bold': True})
            format5 = workbook.add_format(
                {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
                 'font_color': 'black', 'bg_color': 'white',
                 'border': 1, 'border_color': 'black'})
            format6 = workbook.add_format(
                {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
                 'font_color': '#495057', 'bg_color': 'white',
                 'border': 1, 'border_color': 'black'})

            worksheet.merge_range('A1:J4', '', format1)
            worksheet.merge_range('A5:J5', '', format1)
            worksheet.merge_range('A6:J6', '', format1)
            worksheet.merge_range('A7:J7', '', format1)

            worksheet.set_row(0, 30)
            worksheet.set_row(1, 30)
            worksheet.set_row(2, 30)
            worksheet.set_row(3, 30)
            worksheet.set_row(4, 30)
            worksheet.set_row(5, 30)
            worksheet.set_row(6, 30)
            worksheet.set_row(7, 30)
            worksheet.set_row(8, 30)


            worksheet.set_column('A:A', 20)
            worksheet.set_column('B:B', 20)
            worksheet.set_column('C:C', 20)
            worksheet.set_column('D:D', 20)
            worksheet.set_column('E:E', 20)
            worksheet.set_column('F:F', 20)
            worksheet.set_column('G:G', 20)
            worksheet.set_column('H:H', 20)
            worksheet.set_column('I:I', 20)
            worksheet.set_column('J:J', 20)
            worksheet.set_column('K:K', 20)
            worksheet.set_column('L:L', 20)
            worksheet.set_column('M:M', 20)
            worksheet.set_column('N:N', 20)
            worksheet.set_column('O:O', 20)
            worksheet.set_column('P:P', 20)
            worksheet.set_column('Q:Q', 20)
            worksheet.set_column('R:R', 20)
            worksheet.set_column('S:S', 20)
            worksheet.set_column('T:T', 20)
            worksheet.set_column('U:U', 20)
            worksheet.set_column('V:V', 20)
            worksheet.set_column('W:W', 20)
            worksheet.set_column('X:X', 20)
            worksheet.set_column('Y:Y', 20)
            worksheet.set_column('Z:Z', 20)

            logo = self.env.company.logo
            imgdata = base64.b64decode(logo)
            image = io.BytesIO(imgdata)
            worksheet.insert_image('M1:M4', 'logo.png',
                                   {'image_data': image, 'x_scale': 1.5, 'y_scale': 1})

            worksheet.write('A6:Y6', 'Cotisation de Paie' , format1)
            worksheet.write('A7:Y7', 'Mois: %s' % (rec.period_id.name) , format2)


            worksheet.write('A8:A8', 'Matricules', format4)
            worksheet.write('B8:B8', 'Nom - Prénom', format4)
            worksheet.write('C8:C8', 'Date embauche', format4)
            worksheet.write('D8:D8', 'Date naissance', format4)
            worksheet.write('E8:E8', 'Fonction', format4)
            worksheet.write('F8:F8', 'Département', format4)
            worksheet.write('G8:G8', 'Mutuelle(Montant employé)', format4)
            worksheet.write('H8:H8', 'Mutuelle(Montant employeur)', format4)
            worksheet.write('I8:I8', 'Caisse fin service(Montant employé)', format4)
            worksheet.write('J8:J8', 'Caisse fin service(Montant employeur)', format4)

            i = 9

            for b in rec.bulletin_line_ids.filtered(lambda re: re.employee_id.matricule).sorted(key=lambda r: r.employee_id.matricule):
                worksheet.set_row(i, 30)
                worksheet.write('A%s:A%s' % (i, i), '%s' % (b.employee_id.matricule), format5)
                worksheet.write('B%s:B%s' % (i, i), '%s %s' % (b.employee_id.prenom, b.employee_id.name), format5)
                worksheet.write('C%s:C%s' % (i, i), '%s' % (b.employee_id.date), format5)
                worksheet.write('D%s:D%s' % (i, i), '%s' % (b.employee_id.birthday), format5)
                worksheet.write('E%s:E%s' % (i, i), '%s' % (b.dh_job_id.name), format5)
                worksheet.write('F%s:F%s' % (i, i), '%s' % (b.employee_id.department_id.name), format5)
                worksheet.write('G%s:G%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle']).mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle'])) > 0 else 0),
                                format5)
                worksheet.write('H%s:H%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle']).mapped(
                        'subtotal_employer')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle'])) > 0 else 0),
                                format5)
                worksheet.write('I%s:I%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service']).mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service'])) > 0 else 0),
                                format5)
                worksheet.write('J%s:J%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service']).mapped(
                        'subtotal_employer')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service'])) > 0 else 0),
                                format5)

                i=i+1

            for b in rec.bulletin_line_ids.filtered(lambda re: not re.employee_id.matricule).sorted(key=lambda r: r.employee_id.matricule):
                worksheet.set_row(i, 30)
                worksheet.write('A%s:A%s' % (i, i), '%s' % (b.employee_id.matricule), format5)
                worksheet.write('B%s:B%s' % (i, i), '%s %s' % (b.employee_id.prenom, b.employee_id.name), format5)
                worksheet.write('C%s:C%s' % (i, i), '%s' % (b.employee_id.date), format5)
                worksheet.write('D%s:D%s' % (i, i), '%s' % (b.employee_id.birthday), format5)
                worksheet.write('E%s:E%s' % (i, i), '%s' % (b.employee_id.job_id.name), format5)
                worksheet.write('F%s:F%s' % (i, i), '%s' % (b.employee_id.department_id.name), format5)
                worksheet.write('G%s:G%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle']).mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle'])) > 0 else 0),
                                format5)
                worksheet.write('H%s:H%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle']).mapped(
                        'subtotal_employer')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle'])) > 0 else 0),
                                format5)
                worksheet.write('I%s:I%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service']).mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service'])) > 0 else 0),
                                format5)
                worksheet.write('J%s:J%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service']).mapped(
                        'subtotal_employer')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service'])) > 0 else 0),
                                format5)

                i = i + 1

class DhCotisationsBulletinXlsx(models.AbstractModel):
    _name = 'report.kzm_payroll_ma.dh_cotisation_bulletin_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, datas):
        # for rec in datas:
        locale.setlocale(locale.LC_ALL,
                         'fr_FR.UTF-8')  # sudo locale-gen fr_FR.UTF-8
        report_name = 'Cotisations'
        worksheet = workbook.add_worksheet(report_name)
        format0 = workbook.add_format(
            {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'black', 'bg_color': 'white'})
        format1 = workbook.add_format(
            {'font_size': 22, 'align': 'center', 'valign': 'vcenter',
             'font_color': '#495057', 'bg_color': 'white', 'bold': True})
        format2 = workbook.add_format(
            {'font_size': 18, 'align': 'center', 'valign': 'vcenter',
             'font_color': '#495057', 'bold': True, 'bg_color': 'white',
             'underline': True})
        format4 = workbook.add_format(
            {'font_size': 15, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'black', 'bg_color': '#C5E0B4',
             'border': 1,'border_color': 'black', 'bold': True})
        format5 = workbook.add_format(
            {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'black', 'bg_color': 'white',
             'border': 1, 'border_color': 'black'})
        format6 = workbook.add_format(
            {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
             'font_color': '#495057', 'bg_color': 'white',
             'border': 1, 'border_color': 'black'})

        worksheet.merge_range('A1:J4', '', format1)
        worksheet.merge_range('A5:J5', '', format1)
        worksheet.merge_range('A6:J6', '', format1)
        worksheet.merge_range('A7:J7', '', format1)

        worksheet.set_row(0, 30)
        worksheet.set_row(1, 30)
        worksheet.set_row(2, 30)
        worksheet.set_row(3, 30)
        worksheet.set_row(4, 30)
        worksheet.set_row(5, 30)
        worksheet.set_row(6, 30)
        worksheet.set_row(7, 30)
        worksheet.set_row(8, 30)


        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 20)
        worksheet.set_column('F:F', 20)
        worksheet.set_column('G:G', 20)
        worksheet.set_column('H:H', 20)
        worksheet.set_column('I:I', 20)
        worksheet.set_column('J:J', 20)
        worksheet.set_column('K:K', 20)
        worksheet.set_column('L:L', 20)
        worksheet.set_column('M:M', 20)
        worksheet.set_column('N:N', 20)
        worksheet.set_column('O:O', 20)
        worksheet.set_column('P:P', 20)
        worksheet.set_column('Q:Q', 20)
        worksheet.set_column('R:R', 20)
        worksheet.set_column('S:S', 20)
        worksheet.set_column('T:T', 20)
        worksheet.set_column('U:U', 20)
        worksheet.set_column('V:V', 20)
        worksheet.set_column('W:W', 20)
        worksheet.set_column('X:X', 20)
        worksheet.set_column('Y:Y', 20)
        worksheet.set_column('Z:Z', 20)

        logo = self.env.company.logo
        imgdata = base64.b64decode(logo)
        image = io.BytesIO(imgdata)
        worksheet.insert_image('M1:M4', 'logo.png',
                               {'image_data': image, 'x_scale': 1.5, 'y_scale': 1})

        worksheet.write('A6:Y6', 'Cotisation de Paie' , format1)
        # worksheet.write('A7:Y7', 'Mois: %s' % (rec.period_id.name) , format2)


        worksheet.write('A8:A8', 'Matricules', format4)
        worksheet.write('B8:B8', 'Nom - Prénom', format4)
        worksheet.write('C8:C8', 'Date embauche', format4)
        worksheet.write('D8:D8', 'Date naissance', format4)
        worksheet.write('E8:E8', 'Fonction', format4)
        worksheet.write('F8:F8', 'Département', format4)
        worksheet.write('G8:G8', 'Mutuelle(Montant employé)', format4)
        worksheet.write('H8:H8', 'Mutuelle(Montant employeur)', format4)
        worksheet.write('I8:I8', 'Caisse fin service(Montant employé)', format4)
        worksheet.write('J8:J8', 'Caisse fin service(Montant employeur)', format4)

        i = 9

        for b in datas.filtered(lambda re: re.employee_id.matricule).sorted(key=lambda r: r.employee_id.matricule):
            worksheet.set_row(i, 30)
            worksheet.write('A%s:A%s' % (i, i), '%s' % (b.employee_id.matricule), format5)
            worksheet.write('B%s:B%s' % (i, i), '%s %s' % (b.employee_id.prenom, b.employee_id.name), format5)
            worksheet.write('C%s:C%s' % (i, i), '%s' % (b.employee_id.date), format5)
            worksheet.write('D%s:D%s' % (i, i), '%s' % (b.employee_id.birthday), format5)
            worksheet.write('E%s:E%s' % (i, i), '%s' % (b.employee_id.job_id.name), format5)
            worksheet.write('F%s:F%s' % (i, i), '%s' % (b.employee_id.department_id.name), format5)
            worksheet.write('G%s:G%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle']).mapped(
                    'subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle'])) > 0 else 0),
                            format5)
            worksheet.write('H%s:H%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle']).mapped(
                    'subtotal_employer')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle'])) > 0 else 0),
                            format5)
            worksheet.write('I%s:I%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service']).mapped(
                    'subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service'])) > 0 else 0),
                            format5)
            worksheet.write('J%s:J%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service']).mapped(
                    'subtotal_employer')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service'])) > 0 else 0),
                            format5)

            i=i+1

        for b in datas.filtered(lambda re: not re.employee_id.matricule).sorted(key=lambda r: r.employee_id.matricule):
            worksheet.set_row(i, 30)
            worksheet.write('A%s:A%s' % (i, i), '%s' % (b.employee_id.matricule), format5)
            worksheet.write('B%s:B%s' % (i, i), '%s %s' % (b.employee_id.prenom, b.employee_id.name), format5)
            worksheet.write('C%s:C%s' % (i, i), '%s' % (b.employee_id.date), format5)
            worksheet.write('D%s:D%s' % (i, i), '%s' % (b.employee_id.birthday), format5)
            worksheet.write('E%s:E%s' % (i, i), '%s' % (b.employee_id.job_id.name), format5)
            worksheet.write('F%s:F%s' % (i, i), '%s' % (b.employee_id.department_id.name), format5)
            worksheet.write('G%s:G%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle']).mapped(
                    'subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle'])) > 0 else 0),
                            format5)
            worksheet.write('H%s:H%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle']).mapped(
                    'subtotal_employer')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle'])) > 0 else 0),
                            format5)
            worksheet.write('I%s:I%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service']).mapped(
                    'subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service'])) > 0 else 0),
                            format5)
            worksheet.write('J%s:J%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service']).mapped(
                    'subtotal_employer')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service'])) > 0 else 0),
                            format5)

            i = i + 1