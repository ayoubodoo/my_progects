import datetime as dt
import locale
import time
from datetime import timedelta, datetime
from odoo import models,fields
import base64
import io
from io import BytesIO

class JournalPaieXlsx(models.AbstractModel):
    _name = 'report.kzm_payroll_ma.journal_paie_xlsx'
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
                {'font_size': 18, 'align': 'center', 'valign': 'vcenter',
                 'font_color': '#495057', 'bg_color': 'white', 'bold': True})
            format2 = workbook.add_format(
                {'font_size': 13, 'align': 'center', 'valign': 'vcenter',
                 'font_color': '#495057', 'bold': True, 'bg_color': 'white',
                 'underline': True})
            format4 = workbook.add_format(
                {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
                 'font_color': 'black', 'bg_color': '#F8F5F7',
                 'border': 1,'border_color': 'black'})
            format5 = workbook.add_format(
                {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
                 'font_color': 'black', 'bg_color': 'white',
                 'border': 1, 'border_color': 'black'})
            format6 = workbook.add_format(
                {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
                 'font_color': '#495057', 'bg_color': 'white',
                 'border': 1, 'border_color': 'black'})


            worksheet.merge_range('A1:Q1', '', format1)
            worksheet.merge_range('A2:Q2', '', format1)

            worksheet.set_row(0, 50)
            worksheet.set_row(1, 50)
            worksheet.set_row(2, 25)
            worksheet.set_row(3, 25)


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

            worksheet.write('A1:Q1', 'Journal de Paie' , format1)
            worksheet.write('A2:Q2', 'Mois: %s' % (rec.period_id.name) , format2)

            worksheet.merge_range('A3:A4', '', format1)
            worksheet.write('A3:A4', 'Matr', format4)
            worksheet.write('B3:B3', 'Nom - Prénom', format4)
            worksheet.write('B4:B4', 'Primes imposables', format5)
            worksheet.write('C3:C3', 'Fonction', format4)
            worksheet.write('C4:C4', 'Rev brut global', format5)
            worksheet.write('D3:D3', 'Date embauche', format4)
            worksheet.write('D4:D4', 'Rev brut impos', format5)
            worksheet.write('E3:E3', 'Date naissance', format4)
            worksheet.write('E4:E4', 'CNSS', format5)
            worksheet.write('F3:F3', 'N°CNSS', format4)
            worksheet.write('F4:F4', 'CIMR/ASS/AMO', format5)
            worksheet.write('G3:G3', 'NE', format4)
            worksheet.write('H3:H3', 'NCF', format4)
            worksheet.write('I3:I3', 'Sal Base', format4)
            worksheet.merge_range('G4:I4', '', format1)
            worksheet.write('G4:I4', 'Rev net impos', format5)
            worksheet.write('J3:J3', 'Ancient', format4)
            worksheet.write('J4:J4', 'IGR', format5)
            worksheet.write('K3:k3', 'HSup 0%', format4)
            worksheet.write('K4:K4', 'Avances', format5)
            worksheet.write('L3:L3', 'HSup 25%', format4)
            worksheet.write('M3:M3', 'HSup 50%', format4)
            worksheet.merge_range('L4:M4', '', format1)
            worksheet.write('L4:M4', 'Prêt et Ret', format5)
            worksheet.write('N3:N3', 'HSup 100%', format4)
            worksheet.write('O3:O3', 'Jrs congés', format4)
            worksheet.merge_range('N4:O4', '', format1)
            worksheet.write('N4:O4', 'Primes non impos', format5)
            worksheet.write('P3:P3', 'Congés payés', format4)
            worksheet.write('P4:P4', 'Arrondi', format5)
            worksheet.merge_range('Q3:Q4', '', format1)
            worksheet.write('Q3:Q4', 'Net à payer', format4)

            i = 5
            for b in rec.bulletin_line_ids.filtered(lambda re: re.employee_id.matricule).sorted(key=lambda r: r.employee_id.matricule):
                worksheet.set_row(i, 30)
                worksheet.merge_range('A%s:A%s' % (i, i+1), '', format1)
                worksheet.write('A%s:A%s' % (i, i+1), '%s' % (b.employee_id.matricule), format4)
                worksheet.write('B%s:B%s' % (i, i), '%s %s' % (b.employee_id.prenom, b.employee_id.name), format4)
                worksheet.write('B%s:B%s' % (i+1, i+1), '%s' % (b.prime), format5)
                worksheet.write('C%s:C%s' % (i, i), '%s' % (b.dh_job_id.name), format4)
                worksheet.write('C%s:C%s' % (i+1, i+1), '%s' %(b.salaire_brute), format5)
                worksheet.write('D%s:D%s' % (i, i), '%s' % (b.employee_id.date), format4)
                worksheet.write('D%s:D%s' % (i+1, i+1), '%s' % (b.salaire_brute_imposable), format5)
                worksheet.write('E%s:E%s' % (i, i), '%s' % (b.employee_id.birthday), format4)
                worksheet.write('E%s:E%s' % (i+1, i+1), '%s' % (b.cnss), format5)
                worksheet.write('F%s:F%s' % (i, i), '%s' % (b.employee_id.ssnid if b.employee_id.ssnid else ''), format4)
                worksheet.write('F%s:F%s' % (i+1, i+1), '%s' % (b.cimr_assurance_amo), format5)
                worksheet.write('G%s:G%s' % (i, i), '%s' % (b.employee_id.children), format4)
                worksheet.write('H%s:H%s' % (i, i), '%s' % (b.employee_id.chargefam), format4)
                worksheet.write('I%s:I%s' % (i, i), '%s' % (b.salaire_base_mois), format4)
                worksheet.merge_range('G%s:I%s' % (i+1, i+1), '', format1)
                worksheet.write('G%s:I%s' % (i+1, i+1), '%s' % (b.salaire_net_imposable), format5)
                worksheet.write('J%s:J%s' % (i, i), '%s' % (b.prime_anciennete), format4)
                worksheet.write('J%s:J%s' % (i+1, i+1), '%s' % (b.igr), format5)
                worksheet.write('K%s:k%s' % (i, i), '', format4)
                worksheet.write('K%s:K%s' % (i+1, i+1), '', format5)
                worksheet.write('L%s:L%s' % (i, i), '%s' % (b.hsup_25), format4)
                worksheet.write('M%s:M%s' % (i, i), '%s' % (b.hsup_50), format4)
                worksheet.merge_range('L%s:M%s' % (i+1, i+1), '', format1)
                worksheet.write('L%s:M%s' % (i+1, i+1), '', format5)
                worksheet.write('N%s:N%s' % (i, i), '%s' % (b.hsup_100), format4)
                worksheet.write('O%s:O%s' % (i, i), '%s' % (b.jrs_conges), format4)
                worksheet.merge_range('N%s:O%s' % (i+1, i+1), '', format1)
                worksheet.write('N%s:O%s' % (i+1, i+1), '%s' % (b.exoneration), format5)
                worksheet.write('P%s:P%s' % (i, i), '%s' % (b.conges_payes), format4)
                worksheet.write('P%s:P%s' % (i+1, i+1), '%s' % (b.arrondi), format5)
                worksheet.merge_range('Q%s:Q%s' % (i, i+1), '', format1)
                worksheet.write('Q%s:Q%s' % (i, i+1), '%s' % (b.salaire_net_a_payer), format4)

                i=i+2

            for b in rec.bulletin_line_ids.filtered(lambda re: not re.employee_id.matricule).sorted(key=lambda r: r.employee_id.matricule):
                worksheet.set_row(i, 30)
                worksheet.merge_range('A%s:A%s' % (i, i+1), '', format1)
                worksheet.write('A%s:A%s' % (i, i+1), '%s' % (b.employee_id.matricule), format4)
                worksheet.write('B%s:B%s' % (i, i), '%s %s' % (b.employee_id.prenom, b.employee_id.name), format4)
                worksheet.write('B%s:B%s' % (i+1, i+1), '%s' % (b.prime), format5)
                worksheet.write('C%s:C%s' % (i, i), '%s' % (b.dh_job_id.name), format4)
                worksheet.write('C%s:C%s' % (i+1, i+1), '%s' %(b.salaire_brute), format5)
                worksheet.write('D%s:D%s' % (i, i), '%s' % (b.employee_id.date), format4)
                worksheet.write('D%s:D%s' % (i+1, i+1), '%s' % (b.salaire_brute_imposable), format5)
                worksheet.write('E%s:E%s' % (i, i), '%s' % (b.employee_id.birthday), format4)
                worksheet.write('E%s:E%s' % (i+1, i+1), '%s' % (b.cnss), format5)
                worksheet.write('F%s:F%s' % (i, i), '%s' % (b.employee_id.ssnid if b.employee_id.ssnid else ''), format4)
                worksheet.write('F%s:F%s' % (i+1, i+1), '%s' % (b.cimr_assurance_amo), format5)
                worksheet.write('G%s:G%s' % (i, i), '%s' % (b.employee_id.children), format4)
                worksheet.write('H%s:H%s' % (i, i), '%s' % (b.employee_id.chargefam), format4)
                worksheet.write('I%s:I%s' % (i, i), '%s' % (b.salaire_base_mois), format4)
                worksheet.merge_range('G%s:I%s' % (i+1, i+1), '', format1)
                worksheet.write('G%s:I%s' % (i+1, i+1), '%s' % (b.salaire_net_imposable), format5)
                worksheet.write('J%s:J%s' % (i, i), '%s' % (b.prime_anciennete), format4)
                worksheet.write('J%s:J%s' % (i+1, i+1), '%s' % (b.igr), format5)
                worksheet.write('K%s:k%s' % (i, i), '', format4)
                worksheet.write('K%s:K%s' % (i+1, i+1), '', format5)
                worksheet.write('L%s:L%s' % (i, i), '%s' % (b.hsup_25), format4)
                worksheet.write('M%s:M%s' % (i, i), '%s' % (b.hsup_50), format4)
                worksheet.merge_range('L%s:M%s' % (i+1, i+1), '', format1)
                worksheet.write('L%s:M%s' % (i+1, i+1), '', format5)
                worksheet.write('N%s:N%s' % (i, i), '%s' % (b.hsup_100), format4)
                worksheet.write('O%s:O%s' % (i, i), '%s' % (b.jrs_conges), format4)
                worksheet.merge_range('N%s:O%s' % (i+1, i+1), '', format1)
                worksheet.write('N%s:O%s' % (i+1, i+1), '%s' % (b.exoneration), format5)
                worksheet.write('P%s:P%s' % (i, i), '%s' % (b.conges_payes), format4)
                worksheet.write('P%s:P%s' % (i+1, i+1), '%s' % (b.arrondi), format5)
                worksheet.merge_range('Q%s:Q%s' % (i, i+1), '', format1)
                worksheet.write('Q%s:Q%s' % (i, i+1), '%s' % (b.salaire_net_a_payer), format4)

                i=i+2

            i=i+1

            worksheet.set_row(i, 30)
            worksheet.merge_range('A%s:A%s' % (i, i+1), '', format1)
            worksheet.write('A%s:A%s' % (i, i+1), '', format5)
            worksheet.write('B%s:B%s' % (i, i), 'TOTAL', format5)
            worksheet.write('B%s:B%s' % (i+1, i+1), '%.2f' % (sum(rec.bulletin_line_ids.mapped('prime'))), format4)
            worksheet.write('C%s:C%s' % (i, i), '', format5)
            worksheet.write('C%s:C%s' % (i+1, i+1), '%s' % (sum(rec.bulletin_line_ids.mapped('salaire_brute'))), format4)
            worksheet.write('D%s:D%s' % (i, i), '', format5)
            worksheet.write('D%s:D%s' % (i+1, i+1), '%s' % (sum(rec.bulletin_line_ids.mapped('salaire_brute_imposable'))), format4)
            worksheet.write('E%s:E%s' % (i, i), '', format5)
            worksheet.write('E%s:E%s' % (i+1, i+1), '%s' % (sum(rec.bulletin_line_ids.mapped('cnss'))), format4)
            worksheet.write('F%s:F%s' % (i, i), '', format5)
            worksheet.write('F%s:F%s' % (i+1, i+1), '%s' % (sum(rec.bulletin_line_ids.mapped('cimr_assurance_amo'))), format4)
            worksheet.write('G%s:G%s' % (i, i), '%s' % (sum(rec.bulletin_line_ids.mapped('employee_id').mapped('children'))), format5)
            worksheet.write('H%s:H%s' % (i, i), '%s' % (sum(rec.bulletin_line_ids.mapped('employee_id').mapped('chargefam'))), format5)
            worksheet.write('I%s:I%s' % (i, i), '', format5)
            worksheet.merge_range('G%s:I%s' % (i+1, i+1), '', format4)
            worksheet.write('G%s:I%s' % (i+1, i+1), '%s' % (sum(rec.bulletin_line_ids.mapped('salaire_net_imposable'))), format4)
            worksheet.write('J%s:J%s' % (i, i), 'total_3', format5)
            worksheet.write('J%s:J%s' % (i+1, i+1), '%s' % (sum(rec.bulletin_line_ids.mapped('igr'))), format4)
            worksheet.write('K%s:k%s' % (i, i), '%s' % (sum(rec.bulletin_line_ids.mapped('prime_anciennete'))), format5)
            worksheet.write('K%s:K%s' % (i+1, i+1), '', format4)
            worksheet.write('L%s:L%s' % (i, i), '%s' % (sum(rec.bulletin_line_ids.mapped('hsup_25'))), format5)
            worksheet.write('M%s:M%s' % (i, i), '%s' % (sum(rec.bulletin_line_ids.mapped('hsup_50'))), format5)
            worksheet.merge_range('L%s:M%s' % (i+1, i+1), '', format4)
            worksheet.write('L%s:M%s' % (i+1, i+1), '', format4)
            worksheet.write('N%s:N%s' % (i, i), '%s' % (sum(rec.bulletin_line_ids.mapped('hsup_100'))), format5)
            worksheet.write('O%s:O%s' % (i, i), '%s' % (sum(rec.bulletin_line_ids.mapped('jrs_conges'))), format5)
            worksheet.merge_range('N%s:O%s' % (i+1, i+1), '', format4)
            worksheet.write('N%s:O%s' % (i+1, i+1), '%.2f' % (sum(rec.bulletin_line_ids.mapped('exoneration'))), format4)
            worksheet.write('P%s:P%s' % (i, i), '%s' % (sum(rec.bulletin_line_ids.mapped('conges_payes'))), format5)
            worksheet.write('P%s:P%s' % (i+1, i+1), '%s' % (sum(rec.bulletin_line_ids.mapped('arrondi'))), format4)
            worksheet.write('Q%s:Q%s' % (i, i), '', format5)
            worksheet.write('Q%s:Q%s' % (i+1, i+1), '%.2f' % (sum(rec.bulletin_line_ids.mapped('salaire_net_a_payer'))), format4)

class JournalPaieByDepartmentXlsx(models.AbstractModel):
    _name = 'report.kzm_payroll_ma.journal_paie_by_department_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, datas):
        for rec in datas:
            locale.setlocale(locale.LC_ALL,
                             'fr_FR.UTF-8')  # sudo locale-gen fr_FR.UTF-8
            y = 0
            for department in rec.bulletin_line_ids.mapped('employee_id').mapped('department_id'):
                y = y + 1
                report_name = '%s) %s' % (y, department.name)
                worksheet = workbook.add_worksheet(report_name)
                format0 = workbook.add_format(
                    {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
                     'font_color': 'black', 'bg_color': 'white'})
                format1 = workbook.add_format(
                    {'font_size': 18, 'align': 'center', 'valign': 'vcenter',
                     'font_color': '#495057', 'bg_color': 'white', 'bold': True})
                format2 = workbook.add_format(
                    {'font_size': 13, 'align': 'center', 'valign': 'vcenter',
                     'font_color': '#495057', 'bold': True, 'bg_color': 'white',
                     'underline': True})
                format4 = workbook.add_format(
                    {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
                     'font_color': 'black', 'bg_color': '#F8F5F7',
                     'border': 1,'border_color': 'black'})
                format5 = workbook.add_format(
                    {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
                     'font_color': 'black', 'bg_color': 'white',
                     'border': 1, 'border_color': 'black'})
                format6 = workbook.add_format(
                    {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
                     'font_color': '#495057', 'bg_color': 'white',
                     'border': 1, 'border_color': 'black'})


                worksheet.merge_range('A1:Q1', '', format1)
                worksheet.merge_range('A2:Q2', '', format1)

                worksheet.set_row(0, 50)
                worksheet.set_row(1, 50)
                worksheet.set_row(2, 25)
                worksheet.set_row(3, 25)


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

                worksheet.write('A1:Q1', 'Journal de Paie' , format1)
                worksheet.write('A2:Q2', 'Department: %s' % (department.name), format2)
                worksheet.write('A2:Q2', 'Mois: %s' % (rec.period_id.name) , format2)

                worksheet.merge_range('A3:A4', '', format1)
                worksheet.write('A3:A4', 'Matr', format4)
                worksheet.write('B3:B3', 'Nom - Prénom', format4)
                worksheet.write('B4:B4', 'Primes imposables', format5)
                worksheet.write('C3:C3', 'Fonction', format4)
                worksheet.write('C4:C4', 'Rev brut global', format5)
                worksheet.write('D3:D3', 'Date embauche', format4)
                worksheet.write('D4:D4', 'Rev brut impos', format5)
                worksheet.write('E3:E3', 'Date naissance', format4)
                worksheet.write('E4:E4', 'CNSS', format5)
                worksheet.write('F3:F3', 'N°CNSS', format4)
                worksheet.write('F4:F4', 'CIMR/ASS/AMO', format5)
                worksheet.write('G3:G3', 'NE', format4)
                worksheet.write('H3:H3', 'NCF', format4)
                worksheet.write('I3:I3', 'Sal Base', format4)
                worksheet.merge_range('G4:I4', '', format1)
                worksheet.write('G4:I4', 'Rev net impos', format5)
                worksheet.write('J3:J3', 'Ancient', format4)
                worksheet.write('J4:J4', 'IGR', format5)
                worksheet.write('K3:k3', 'HSup 0%', format4)
                worksheet.write('K4:K4', 'Avances', format5)
                worksheet.write('L3:L3', 'HSup 25%', format4)
                worksheet.write('M3:M3', 'HSup 50%', format4)
                worksheet.merge_range('L4:M4', '', format1)
                worksheet.write('L4:M4', 'Prêt et Ret', format5)
                worksheet.write('N3:N3', 'HSup 100%', format4)
                worksheet.write('O3:O3', 'Jrs congés', format4)
                worksheet.merge_range('N4:O4', '', format1)
                worksheet.write('N4:O4', 'Primes non impos', format5)
                worksheet.write('P3:P3', 'Congés payés', format4)
                worksheet.write('P4:P4', 'Arrondi', format5)
                worksheet.merge_range('Q3:Q4', '', format1)
                worksheet.write('Q3:Q4', 'Net à payer', format4)

                i = 5
                for b in rec.bulletin_line_ids.filtered(lambda re: re.employee_id.matricule and re.department_id.id == department.id).sorted(key=lambda r: r.employee_id.matricule):
                    worksheet.set_row(i, 30)
                    worksheet.merge_range('A%s:A%s' % (i, i+1), '', format1)
                    worksheet.write('A%s:A%s' % (i, i+1), '%s' % (b.employee_id.matricule), format4)
                    worksheet.write('B%s:B%s' % (i, i), '%s %s' % (b.employee_id.prenom, b.employee_id.name), format4)
                    worksheet.write('B%s:B%s' % (i+1, i+1), '%s' % (b.prime), format5)
                    worksheet.write('C%s:C%s' % (i, i), '%s' % (b.employee_id.job_id.name), format4)
                    worksheet.write('C%s:C%s' % (i+1, i+1), '%s' %(b.salaire_brute), format5)
                    worksheet.write('D%s:D%s' % (i, i), '%s' % (b.employee_id.date), format4)
                    worksheet.write('D%s:D%s' % (i+1, i+1), '%s' % (b.salaire_brute_imposable), format5)
                    worksheet.write('E%s:E%s' % (i, i), '%s' % (b.employee_id.birthday), format4)
                    worksheet.write('E%s:E%s' % (i+1, i+1), '%s' % (b.cnss), format5)
                    worksheet.write('F%s:F%s' % (i, i), '%s' % (b.employee_id.ssnid if b.employee_id.ssnid else ''), format4)
                    worksheet.write('F%s:F%s' % (i+1, i+1), '%s' % (b.cimr_assurance_amo), format5)
                    worksheet.write('G%s:G%s' % (i, i), '%s' % (b.employee_id.children), format4)
                    worksheet.write('H%s:H%s' % (i, i), '%s' % (b.employee_id.chargefam), format4)
                    worksheet.write('I%s:I%s' % (i, i), '%s' % (b.salaire_base_mois), format4)
                    worksheet.merge_range('G%s:I%s' % (i+1, i+1), '', format1)
                    worksheet.write('G%s:I%s' % (i+1, i+1), '%s' % (b.salaire_net_imposable), format5)
                    worksheet.write('J%s:J%s' % (i, i), '%s' % (b.prime_anciennete), format4)
                    worksheet.write('J%s:J%s' % (i+1, i+1), '%s' % (b.igr), format5)
                    worksheet.write('K%s:k%s' % (i, i), '', format4)
                    worksheet.write('K%s:K%s' % (i+1, i+1), '', format5)
                    worksheet.write('L%s:L%s' % (i, i), '%s' % (b.hsup_25), format4)
                    worksheet.write('M%s:M%s' % (i, i), '%s' % (b.hsup_50), format4)
                    worksheet.merge_range('L%s:M%s' % (i+1, i+1), '', format1)
                    worksheet.write('L%s:M%s' % (i+1, i+1), '', format5)
                    worksheet.write('N%s:N%s' % (i, i), '%s' % (b.hsup_100), format4)
                    worksheet.write('O%s:O%s' % (i, i), '%s' % (b.jrs_conges), format4)
                    worksheet.merge_range('N%s:O%s' % (i+1, i+1), '', format1)
                    worksheet.write('N%s:O%s' % (i+1, i+1), '%s' % (b.exoneration), format5)
                    worksheet.write('P%s:P%s' % (i, i), '%s' % (b.conges_payes), format4)
                    worksheet.write('P%s:P%s' % (i+1, i+1), '%s' % (b.arrondi), format5)
                    worksheet.merge_range('Q%s:Q%s' % (i, i+1), '', format1)
                    worksheet.write('Q%s:Q%s' % (i, i+1), '%s' % (b.salaire_net_a_payer), format4)

                    i=i+2

                for b in rec.bulletin_line_ids.filtered(lambda re: not re.employee_id.matricule and re.department_id.id == department.id).sorted(key=lambda r: r.employee_id.matricule):
                    worksheet.set_row(i, 30)
                    worksheet.merge_range('A%s:A%s' % (i, i+1), '', format1)
                    worksheet.write('A%s:A%s' % (i, i+1), '%s' % (b.employee_id.matricule), format4)
                    worksheet.write('B%s:B%s' % (i, i), '%s %s' % (b.employee_id.prenom, b.employee_id.name), format4)
                    worksheet.write('B%s:B%s' % (i+1, i+1), '%s' % (b.prime), format5)
                    worksheet.write('C%s:C%s' % (i, i), '%s' % (b.employee_id.job_id.name), format4)
                    worksheet.write('C%s:C%s' % (i+1, i+1), '%s' %(b.salaire_brute), format5)
                    worksheet.write('D%s:D%s' % (i, i), '%s' % (b.employee_id.date), format4)
                    worksheet.write('D%s:D%s' % (i+1, i+1), '%s' % (b.salaire_brute_imposable), format5)
                    worksheet.write('E%s:E%s' % (i, i), '%s' % (b.employee_id.birthday), format4)
                    worksheet.write('E%s:E%s' % (i+1, i+1), '%s' % (b.cnss), format5)
                    worksheet.write('F%s:F%s' % (i, i), '%s' % (b.employee_id.ssnid if b.employee_id.ssnid else ''), format4)
                    worksheet.write('F%s:F%s' % (i+1, i+1), '%s' % (b.cimr_assurance_amo), format5)
                    worksheet.write('G%s:G%s' % (i, i), '%s' % (b.employee_id.children), format4)
                    worksheet.write('H%s:H%s' % (i, i), '%s' % (b.employee_id.chargefam), format4)
                    worksheet.write('I%s:I%s' % (i, i), '%s' % (b.salaire_base_mois), format4)
                    worksheet.merge_range('G%s:I%s' % (i+1, i+1), '', format1)
                    worksheet.write('G%s:I%s' % (i+1, i+1), '%s' % (b.salaire_net_imposable), format5)
                    worksheet.write('J%s:J%s' % (i, i), '%s' % (b.prime_anciennete), format4)
                    worksheet.write('J%s:J%s' % (i+1, i+1), '%s' % (b.igr), format5)
                    worksheet.write('K%s:k%s' % (i, i), '', format4)
                    worksheet.write('K%s:K%s' % (i+1, i+1), '', format5)
                    worksheet.write('L%s:L%s' % (i, i), '%s' % (b.hsup_25), format4)
                    worksheet.write('M%s:M%s' % (i, i), '%s' % (b.hsup_50), format4)
                    worksheet.merge_range('L%s:M%s' % (i+1, i+1), '', format1)
                    worksheet.write('L%s:M%s' % (i+1, i+1), '', format5)
                    worksheet.write('N%s:N%s' % (i, i), '%s' % (b.hsup_100), format4)
                    worksheet.write('O%s:O%s' % (i, i), '%s' % (b.jrs_conges), format4)
                    worksheet.merge_range('N%s:O%s' % (i+1, i+1), '', format1)
                    worksheet.write('N%s:O%s' % (i+1, i+1), '%s' % (b.exoneration), format5)
                    worksheet.write('P%s:P%s' % (i, i), '%s' % (b.conges_payes), format4)
                    worksheet.write('P%s:P%s' % (i+1, i+1), '%s' % (b.arrondi), format5)
                    worksheet.merge_range('Q%s:Q%s' % (i, i+1), '', format1)
                    worksheet.write('Q%s:Q%s' % (i, i+1), '%s' % (b.salaire_net_a_payer), format4)

                    i=i+2

                i=i+1

                worksheet.set_row(i, 30)
                worksheet.merge_range('A%s:A%s' % (i, i+1), '', format1)
                worksheet.write('A%s:A%s' % (i, i+1), '', format5)
                worksheet.write('B%s:B%s' % (i, i), 'TOTAL', format5)
                worksheet.write('B%s:B%s' % (i+1, i+1), '%.2f' % (sum(rec.bulletin_line_ids.filtered(lambda re:re.department_id.id == department.id).mapped('prime'))), format4)
                worksheet.write('C%s:C%s' % (i, i), '', format5)
                worksheet.write('C%s:C%s' % (i+1, i+1), '%s' % (sum(rec.bulletin_line_ids.filtered(lambda re:re.department_id.id == department.id).mapped('salaire_brute'))), format4)
                worksheet.write('D%s:D%s' % (i, i), '', format5)
                worksheet.write('D%s:D%s' % (i+1, i+1), '%s' % (sum(rec.bulletin_line_ids.filtered(lambda re:re.department_id.id == department.id).mapped('salaire_brute_imposable'))), format4)
                worksheet.write('E%s:E%s' % (i, i), '', format5)
                worksheet.write('E%s:E%s' % (i+1, i+1), '%s' % (sum(rec.bulletin_line_ids.filtered(lambda re:re.department_id.id == department.id).mapped('cnss'))), format4)
                worksheet.write('F%s:F%s' % (i, i), '', format5)
                worksheet.write('F%s:F%s' % (i+1, i+1), '%s' % (sum(rec.bulletin_line_ids.filtered(lambda re:re.department_id.id == department.id).mapped('cimr_assurance_amo'))), format4)
                worksheet.write('G%s:G%s' % (i, i), '%s' % (sum(rec.bulletin_line_ids.filtered(lambda re:re.department_id.id == department.id).mapped('employee_id').mapped('children'))), format5)
                worksheet.write('H%s:H%s' % (i, i), '%s' % (sum(rec.bulletin_line_ids.filtered(lambda re:re.department_id.id == department.id).mapped('employee_id').mapped('chargefam'))), format5)
                worksheet.write('I%s:I%s' % (i, i), '', format5)
                worksheet.merge_range('G%s:I%s' % (i+1, i+1), '', format4)
                worksheet.write('G%s:I%s' % (i+1, i+1), '%s' % (sum(rec.bulletin_line_ids.filtered(lambda re:re.department_id.id == department.id).mapped('salaire_net_imposable'))), format4)
                worksheet.write('J%s:J%s' % (i, i), 'total_3', format5)
                worksheet.write('J%s:J%s' % (i+1, i+1), '%s' % (sum(rec.bulletin_line_ids.filtered(lambda re:re.department_id.id == department.id).mapped('igr'))), format4)
                worksheet.write('K%s:k%s' % (i, i), '%s' % (sum(rec.bulletin_line_ids.filtered(lambda re:re.department_id.id == department.id).mapped('prime_anciennete'))), format5)
                worksheet.write('K%s:K%s' % (i+1, i+1), '', format4)
                worksheet.write('L%s:L%s' % (i, i), '%s' % (sum(rec.bulletin_line_ids.filtered(lambda re:re.department_id.id == department.id).mapped('hsup_25'))), format5)
                worksheet.write('M%s:M%s' % (i, i), '%s' % (sum(rec.bulletin_line_ids.filtered(lambda re:re.department_id.id == department.id).mapped('hsup_50'))), format5)
                worksheet.merge_range('L%s:M%s' % (i+1, i+1), '', format4)
                worksheet.write('L%s:M%s' % (i+1, i+1), '', format4)
                worksheet.write('N%s:N%s' % (i, i), '%s' % (sum(rec.bulletin_line_ids.filtered(lambda re:re.department_id.id == department.id).mapped('hsup_100'))), format5)
                worksheet.write('O%s:O%s' % (i, i), '%s' % (sum(rec.bulletin_line_ids.filtered(lambda re:re.department_id.id == department.id).mapped('jrs_conges'))), format5)
                worksheet.merge_range('N%s:O%s' % (i+1, i+1), '', format4)
                worksheet.write('N%s:O%s' % (i+1, i+1), '%.2f' % (sum(rec.bulletin_line_ids.filtered(lambda re:re.department_id.id == department.id).mapped('exoneration'))), format4)
                worksheet.write('P%s:P%s' % (i, i), '%s' % (sum(rec.bulletin_line_ids.filtered(lambda re:re.department_id.id == department.id).mapped('conges_payes'))), format5)
                worksheet.write('P%s:P%s' % (i+1, i+1), '%s' % (sum(rec.bulletin_line_ids.filtered(lambda re:re.department_id.id == department.id).mapped('arrondi'))), format4)
                worksheet.write('Q%s:Q%s' % (i, i), '', format5)
                worksheet.write('Q%s:Q%s' % (i+1, i+1), '%.2f' % (sum(rec.bulletin_line_ids.filtered(lambda re:re.department_id.id == department.id).mapped('salaire_net_a_payer'))), format4)

class JournalPaieBulletinXlsx(models.AbstractModel):
    _name = 'report.kzm_payroll_ma.journal_paie_bulletin_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, datas):
        # for rec in datas:
        locale.setlocale(locale.LC_ALL,
                         'fr_FR.UTF-8')  # sudo locale-gen fr_FR.UTF-8
        report_name = 'Journal de paie'
        worksheet = workbook.add_worksheet(report_name)
        format0 = workbook.add_format(
            {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'black', 'bg_color': 'white'})
        format1 = workbook.add_format(
            {'font_size': 18, 'align': 'center', 'valign': 'vcenter',
             'font_color': '#495057', 'bg_color': 'white', 'bold': True})
        format2 = workbook.add_format(
            {'font_size': 13, 'align': 'center', 'valign': 'vcenter',
             'font_color': '#495057', 'bold': True, 'bg_color': 'white',
             'underline': True})
        format4 = workbook.add_format(
            {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'black', 'bg_color': '#F8F5F7',
             'border': 1, 'border_color': 'black'})
        format5 = workbook.add_format(
            {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'black', 'bg_color': 'white',
             'border': 1, 'border_color': 'black'})
        format6 = workbook.add_format(
            {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
             'font_color': '#495057', 'bg_color': 'white',
             'border': 1, 'border_color': 'black'})

        worksheet.merge_range('A1:Q1', '', format1)
        worksheet.merge_range('A2:Q2', '', format1)

        worksheet.set_row(0, 50)
        worksheet.set_row(1, 50)
        worksheet.set_row(2, 25)
        worksheet.set_row(3, 25)

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

        worksheet.write('A1:Q1', 'Journal de Paie', format1)
        # worksheet.write('A2:Q2', 'Mois: %s' % (rec.period_id.name), format2)

        worksheet.merge_range('A3:A4', '', format1)
        worksheet.write('A3:A4', 'Matr', format4)
        worksheet.write('B3:B3', 'Nom - Prénom', format4)
        worksheet.write('B4:B4', 'Primes imposables', format5)
        worksheet.write('C3:C3', 'Fonction', format4)
        worksheet.write('C4:C4', 'Rev brut global', format5)
        worksheet.write('D3:D3', 'Date embauche', format4)
        worksheet.write('D4:D4', 'Rev brut impos', format5)
        worksheet.write('E3:E3', 'Date naissance', format4)
        worksheet.write('E4:E4', 'CNSS', format5)
        worksheet.write('F3:F3', 'N°CNSS', format4)
        worksheet.write('F4:F4', 'CIMR/ASS/AMO', format5)
        worksheet.write('G3:G3', 'NE', format4)
        worksheet.write('H3:H3', 'NCF', format4)
        worksheet.write('I3:I3', 'Sal Base', format4)
        worksheet.merge_range('G4:I4', '', format1)
        worksheet.write('G4:I4', 'Rev net impos', format5)
        worksheet.write('J3:J3', 'Ancient', format4)
        worksheet.write('J4:J4', 'IGR', format5)
        worksheet.write('K3:k3', 'HSup 0%', format4)
        worksheet.write('K4:K4', 'Avances', format5)
        worksheet.write('L3:L3', 'HSup 25%', format4)
        worksheet.write('M3:M3', 'HSup 50%', format4)
        worksheet.merge_range('L4:M4', '', format1)
        worksheet.write('L4:M4', 'Prêt et Ret', format5)
        worksheet.write('N3:N3', 'HSup 100%', format4)
        worksheet.write('O3:O3', 'Jrs congés', format4)
        worksheet.merge_range('N4:O4', '', format1)
        worksheet.write('N4:O4', 'Primes non impos', format5)
        worksheet.write('P3:P3', 'Congés payés', format4)
        worksheet.write('P4:P4', 'Arrondi', format5)
        worksheet.merge_range('Q3:Q4', '', format1)
        worksheet.write('Q3:Q4', 'Net à payer', format4)

        i = 5
        for b in datas.filtered(lambda re: re.employee_id.matricule).sorted(
                key=lambda r: r.employee_id.matricule):
            worksheet.set_row(i, 30)
            worksheet.merge_range('A%s:A%s' % (i, i + 1), '', format1)
            worksheet.write('A%s:A%s' % (i, i + 1), '%s' % (b.employee_id.matricule), format4)
            worksheet.write('B%s:B%s' % (i, i), '%s %s' % (b.employee_id.prenom, b.employee_id.name),
                            format4)
            worksheet.write('B%s:B%s' % (i + 1, i + 1), '%s' % (b.prime), format5)
            worksheet.write('C%s:C%s' % (i, i), '%s' % (b.employee_id.job_id.name), format4)
            worksheet.write('C%s:C%s' % (i + 1, i + 1), '%s' % (b.salaire_brute), format5)
            worksheet.write('D%s:D%s' % (i, i), '%s' % (b.employee_id.date), format4)
            worksheet.write('D%s:D%s' % (i + 1, i + 1), '%s' % (b.salaire_brute_imposable), format5)
            worksheet.write('E%s:E%s' % (i, i), '%s' % (b.employee_id.birthday), format4)
            worksheet.write('E%s:E%s' % (i + 1, i + 1), '%s' % (b.cnss), format5)
            worksheet.write('F%s:F%s' % (i, i), '%s' % (b.employee_id.ssnid if b.employee_id.ssnid else ''),
                            format4)
            worksheet.write('F%s:F%s' % (i + 1, i + 1), '%s' % (b.cimr_assurance_amo), format5)
            worksheet.write('G%s:G%s' % (i, i), '%s' % (b.employee_id.children), format4)
            worksheet.write('H%s:H%s' % (i, i), '%s' % (b.employee_id.chargefam), format4)
            worksheet.write('I%s:I%s' % (i, i), '%s' % (b.salaire_base_mois), format4)
            worksheet.merge_range('G%s:I%s' % (i + 1, i + 1), '', format1)
            worksheet.write('G%s:I%s' % (i + 1, i + 1), '%s' % (b.salaire_net_imposable), format5)
            worksheet.write('J%s:J%s' % (i, i), '%s' % (b.prime_anciennete), format4)
            worksheet.write('J%s:J%s' % (i + 1, i + 1), '%s' % (b.igr), format5)
            worksheet.write('K%s:k%s' % (i, i), '', format4)
            worksheet.write('K%s:K%s' % (i + 1, i + 1), '', format5)
            worksheet.write('L%s:L%s' % (i, i), '%s' % (b.hsup_25), format4)
            worksheet.write('M%s:M%s' % (i, i), '%s' % (b.hsup_50), format4)
            worksheet.merge_range('L%s:M%s' % (i + 1, i + 1), '', format1)
            worksheet.write('L%s:M%s' % (i + 1, i + 1), '', format5)
            worksheet.write('N%s:N%s' % (i, i), '%s' % (b.hsup_100), format4)
            worksheet.write('O%s:O%s' % (i, i), '%s' % (b.jrs_conges), format4)
            worksheet.merge_range('N%s:O%s' % (i + 1, i + 1), '', format1)
            worksheet.write('N%s:O%s' % (i + 1, i + 1), '%s' % (b.exoneration), format5)
            worksheet.write('P%s:P%s' % (i, i), '%s' % (b.conges_payes), format4)
            worksheet.write('P%s:P%s' % (i + 1, i + 1), '%s' % (b.arrondi), format5)
            worksheet.merge_range('Q%s:Q%s' % (i, i + 1), '', format1)
            worksheet.write('Q%s:Q%s' % (i, i + 1), '%s' % (b.salaire_net_a_payer), format4)

            i = i + 2

        for b in datas.filtered(lambda re: not re.employee_id.matricule).sorted(
                key=lambda r: r.employee_id.matricule):
            worksheet.set_row(i, 30)
            worksheet.merge_range('A%s:A%s' % (i, i + 1), '', format1)
            worksheet.write('A%s:A%s' % (i, i + 1), '%s' % (b.employee_id.matricule), format4)
            worksheet.write('B%s:B%s' % (i, i), '%s %s' % (b.employee_id.prenom, b.employee_id.name),
                            format4)
            worksheet.write('B%s:B%s' % (i + 1, i + 1), '%s' % (b.prime), format5)
            worksheet.write('C%s:C%s' % (i, i), '%s' % (b.employee_id.job_id.name), format4)
            worksheet.write('C%s:C%s' % (i + 1, i + 1), '%s' % (b.salaire_brute), format5)
            worksheet.write('D%s:D%s' % (i, i), '%s' % (b.employee_id.date), format4)
            worksheet.write('D%s:D%s' % (i + 1, i + 1), '%s' % (b.salaire_brute_imposable), format5)
            worksheet.write('E%s:E%s' % (i, i), '%s' % (b.employee_id.birthday), format4)
            worksheet.write('E%s:E%s' % (i + 1, i + 1), '%s' % (b.cnss), format5)
            worksheet.write('F%s:F%s' % (i, i), '%s' % (b.employee_id.ssnid if b.employee_id.ssnid else ''),
                            format4)
            worksheet.write('F%s:F%s' % (i + 1, i + 1), '%s' % (b.cimr_assurance_amo), format5)
            worksheet.write('G%s:G%s' % (i, i), '%s' % (b.employee_id.children), format4)
            worksheet.write('H%s:H%s' % (i, i), '%s' % (b.employee_id.chargefam), format4)
            worksheet.write('I%s:I%s' % (i, i), '%s' % (b.salaire_base_mois), format4)
            worksheet.merge_range('G%s:I%s' % (i + 1, i + 1), '', format1)
            worksheet.write('G%s:I%s' % (i + 1, i + 1), '%s' % (b.salaire_net_imposable), format5)
            worksheet.write('J%s:J%s' % (i, i), '%s' % (b.prime_anciennete), format4)
            worksheet.write('J%s:J%s' % (i + 1, i + 1), '%s' % (b.igr), format5)
            worksheet.write('K%s:k%s' % (i, i), '', format4)
            worksheet.write('K%s:K%s' % (i + 1, i + 1), '', format5)
            worksheet.write('L%s:L%s' % (i, i), '%s' % (b.hsup_25), format4)
            worksheet.write('M%s:M%s' % (i, i), '%s' % (b.hsup_50), format4)
            worksheet.merge_range('L%s:M%s' % (i + 1, i + 1), '', format1)
            worksheet.write('L%s:M%s' % (i + 1, i + 1), '', format5)
            worksheet.write('N%s:N%s' % (i, i), '%s' % (b.hsup_100), format4)
            worksheet.write('O%s:O%s' % (i, i), '%s' % (b.jrs_conges), format4)
            worksheet.merge_range('N%s:O%s' % (i + 1, i + 1), '', format1)
            worksheet.write('N%s:O%s' % (i + 1, i + 1), '%s' % (b.exoneration), format5)
            worksheet.write('P%s:P%s' % (i, i), '%s' % (b.conges_payes), format4)
            worksheet.write('P%s:P%s' % (i + 1, i + 1), '%s' % (b.arrondi), format5)
            worksheet.merge_range('Q%s:Q%s' % (i, i + 1), '', format1)
            worksheet.write('Q%s:Q%s' % (i, i + 1), '%s' % (b.salaire_net_a_payer), format4)

            i = i + 2

        i = i + 1

        worksheet.set_row(i, 30)
        worksheet.merge_range('A%s:A%s' % (i, i + 1), '', format1)
        worksheet.write('A%s:A%s' % (i, i + 1), '', format5)
        worksheet.write('B%s:B%s' % (i, i), 'TOTAL', format5)
        worksheet.write('B%s:B%s' % (i + 1, i + 1), '%.2f' % (sum(datas.mapped('prime'))),
                        format4)
        worksheet.write('C%s:C%s' % (i, i), '', format5)
        worksheet.write('C%s:C%s' % (i + 1, i + 1),
                        '%s' % (sum(datas.mapped('salaire_brute'))), format4)
        worksheet.write('D%s:D%s' % (i, i), '', format5)
        worksheet.write('D%s:D%s' % (i + 1, i + 1),
                        '%s' % (sum(datas.mapped('salaire_brute_imposable'))), format4)
        worksheet.write('E%s:E%s' % (i, i), '', format5)
        worksheet.write('E%s:E%s' % (i + 1, i + 1), '%s' % (sum(datas.mapped('cnss'))),
                        format4)
        worksheet.write('F%s:F%s' % (i, i), '', format5)
        worksheet.write('F%s:F%s' % (i + 1, i + 1),
                        '%s' % (sum(datas.mapped('cimr_assurance_amo'))), format4)
        worksheet.write('G%s:G%s' % (i, i),
                        '%s' % (sum(datas.mapped('employee_id').mapped('children'))),
                        format5)
        worksheet.write('H%s:H%s' % (i, i),
                        '%s' % (sum(datas.mapped('employee_id').mapped('chargefam'))),
                        format5)
        worksheet.write('I%s:I%s' % (i, i), '', format5)
        worksheet.merge_range('G%s:I%s' % (i + 1, i + 1), '', format4)
        worksheet.write('G%s:I%s' % (i + 1, i + 1),
                        '%s' % (sum(datas.mapped('salaire_net_imposable'))), format4)
        worksheet.write('J%s:J%s' % (i, i), 'total_3', format5)
        worksheet.write('J%s:J%s' % (i + 1, i + 1), '%s' % (sum(datas.mapped('igr'))),
                        format4)
        worksheet.write('K%s:k%s' % (i, i), '%s' % (sum(datas.mapped('prime_anciennete'))),
                        format5)
        worksheet.write('K%s:K%s' % (i + 1, i + 1), '', format4)
        worksheet.write('L%s:L%s' % (i, i), '%s' % (sum(datas.mapped('hsup_25'))), format5)
        worksheet.write('M%s:M%s' % (i, i), '%s' % (sum(datas.mapped('hsup_50'))), format5)
        worksheet.merge_range('L%s:M%s' % (i + 1, i + 1), '', format4)
        worksheet.write('L%s:M%s' % (i + 1, i + 1), '', format4)
        worksheet.write('N%s:N%s' % (i, i), '%s' % (sum(datas.mapped('hsup_100'))), format5)
        worksheet.write('O%s:O%s' % (i, i), '%s' % (sum(datas.mapped('jrs_conges'))),
                        format5)
        worksheet.merge_range('N%s:O%s' % (i + 1, i + 1), '', format4)
        worksheet.write('N%s:O%s' % (i + 1, i + 1),
                        '%.2f' % (sum(datas.mapped('exoneration'))), format4)
        worksheet.write('P%s:P%s' % (i, i), '%s' % (sum(datas.mapped('conges_payes'))),
                        format5)
        worksheet.write('P%s:P%s' % (i + 1, i + 1), '%s' % (sum(datas.mapped('arrondi'))),
                        format4)
        worksheet.write('Q%s:Q%s' % (i, i), '', format5)
        worksheet.write('Q%s:Q%s' % (i + 1, i + 1),
                        '%.2f' % (sum(datas.mapped('salaire_net_a_payer'))), format4)

class JournalPaieBulletinByDepartmentXlsx(models.AbstractModel):
    _name = 'report.kzm_payroll_ma.journal_paie_bulletin_by_department_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, datas):
        # for rec in datas:
        locale.setlocale(locale.LC_ALL,
                         'fr_FR.UTF-8')  # sudo locale-gen fr_FR.UTF-8
        y = 0
        for department in datas.mapped('employee_id').mapped('department_id'):
            y = y + 1
            report_name = '%s) %s' % (y, department.name)
            worksheet = workbook.add_worksheet(report_name)
            format0 = workbook.add_format(
                {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
                 'font_color': 'black', 'bg_color': 'white'})
            format1 = workbook.add_format(
                {'font_size': 18, 'align': 'center', 'valign': 'vcenter',
                 'font_color': '#495057', 'bg_color': 'white', 'bold': True})
            format2 = workbook.add_format(
                {'font_size': 13, 'align': 'center', 'valign': 'vcenter',
                 'font_color': '#495057', 'bold': True, 'bg_color': 'white',
                 'underline': True})
            format4 = workbook.add_format(
                {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
                 'font_color': 'black', 'bg_color': '#F8F5F7',
                 'border': 1, 'border_color': 'black'})
            format5 = workbook.add_format(
                {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
                 'font_color': 'black', 'bg_color': 'white',
                 'border': 1, 'border_color': 'black'})
            format6 = workbook.add_format(
                {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
                 'font_color': '#495057', 'bg_color': 'white',
                 'border': 1, 'border_color': 'black'})

            worksheet.merge_range('A1:Q1', '', format1)
            worksheet.merge_range('A2:Q2', '', format1)

            worksheet.set_row(0, 50)
            worksheet.set_row(1, 50)
            worksheet.set_row(2, 25)
            worksheet.set_row(3, 25)

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

            worksheet.write('A1:Q1', 'Journal de Paie', format1)
            worksheet.write('A2:Q2', 'Department: %s' % (department.name), format2)

            worksheet.merge_range('A3:A4', '', format1)
            worksheet.write('A3:A4', 'Matr', format4)
            worksheet.write('B3:B3', 'Nom - Prénom', format4)
            worksheet.write('B4:B4', 'Primes imposables', format5)
            worksheet.write('C3:C3', 'Fonction', format4)
            worksheet.write('C4:C4', 'Rev brut global', format5)
            worksheet.write('D3:D3', 'Date embauche', format4)
            worksheet.write('D4:D4', 'Rev brut impos', format5)
            worksheet.write('E3:E3', 'Date naissance', format4)
            worksheet.write('E4:E4', 'CNSS', format5)
            worksheet.write('F3:F3', 'N°CNSS', format4)
            worksheet.write('F4:F4', 'CIMR/ASS/AMO', format5)
            worksheet.write('G3:G3', 'NE', format4)
            worksheet.write('H3:H3', 'NCF', format4)
            worksheet.write('I3:I3', 'Sal Base', format4)
            worksheet.merge_range('G4:I4', '', format1)
            worksheet.write('G4:I4', 'Rev net impos', format5)
            worksheet.write('J3:J3', 'Ancient', format4)
            worksheet.write('J4:J4', 'IGR', format5)
            worksheet.write('K3:k3', 'HSup 0%', format4)
            worksheet.write('K4:K4', 'Avances', format5)
            worksheet.write('L3:L3', 'HSup 25%', format4)
            worksheet.write('M3:M3', 'HSup 50%', format4)
            worksheet.merge_range('L4:M4', '', format1)
            worksheet.write('L4:M4', 'Prêt et Ret', format5)
            worksheet.write('N3:N3', 'HSup 100%', format4)
            worksheet.write('O3:O3', 'Jrs congés', format4)
            worksheet.merge_range('N4:O4', '', format1)
            worksheet.write('N4:O4', 'Primes non impos', format5)
            worksheet.write('P3:P3', 'Congés payés', format4)
            worksheet.write('P4:P4', 'Arrondi', format5)
            worksheet.merge_range('Q3:Q4', '', format1)
            worksheet.write('Q3:Q4', 'Net à payer', format4)

            i = 5
            for b in datas.filtered(
                    lambda re: re.employee_id.matricule and re.department_id.id == department.id).sorted(
                    key=lambda r: r.employee_id.matricule):
                worksheet.set_row(i, 30)
                worksheet.merge_range('A%s:A%s' % (i, i + 1), '', format1)
                worksheet.write('A%s:A%s' % (i, i + 1), '%s' % (b.employee_id.matricule), format4)
                worksheet.write('B%s:B%s' % (i, i), '%s %s' % (b.employee_id.prenom, b.employee_id.name),
                                format4)
                worksheet.write('B%s:B%s' % (i + 1, i + 1), '%s' % (b.prime), format5)
                worksheet.write('C%s:C%s' % (i, i), '%s' % (b.employee_id.job_id.name), format4)
                worksheet.write('C%s:C%s' % (i + 1, i + 1), '%s' % (b.salaire_brute), format5)
                worksheet.write('D%s:D%s' % (i, i), '%s' % (b.employee_id.date), format4)
                worksheet.write('D%s:D%s' % (i + 1, i + 1), '%s' % (b.salaire_brute_imposable), format5)
                worksheet.write('E%s:E%s' % (i, i), '%s' % (b.employee_id.birthday), format4)
                worksheet.write('E%s:E%s' % (i + 1, i + 1), '%s' % (b.cnss), format5)
                worksheet.write('F%s:F%s' % (i, i),
                                '%s' % (b.employee_id.ssnid if b.employee_id.ssnid else ''), format4)
                worksheet.write('F%s:F%s' % (i + 1, i + 1), '%s' % (b.cimr_assurance_amo), format5)
                worksheet.write('G%s:G%s' % (i, i), '%s' % (b.employee_id.children), format4)
                worksheet.write('H%s:H%s' % (i, i), '%s' % (b.employee_id.chargefam), format4)
                worksheet.write('I%s:I%s' % (i, i), '%s' % (b.salaire_base_mois), format4)
                worksheet.merge_range('G%s:I%s' % (i + 1, i + 1), '', format1)
                worksheet.write('G%s:I%s' % (i + 1, i + 1), '%s' % (b.salaire_net_imposable), format5)
                worksheet.write('J%s:J%s' % (i, i), '%s' % (b.prime_anciennete), format4)
                worksheet.write('J%s:J%s' % (i + 1, i + 1), '%s' % (b.igr), format5)
                worksheet.write('K%s:k%s' % (i, i), '', format4)
                worksheet.write('K%s:K%s' % (i + 1, i + 1), '', format5)
                worksheet.write('L%s:L%s' % (i, i), '%s' % (b.hsup_25), format4)
                worksheet.write('M%s:M%s' % (i, i), '%s' % (b.hsup_50), format4)
                worksheet.merge_range('L%s:M%s' % (i + 1, i + 1), '', format1)
                worksheet.write('L%s:M%s' % (i + 1, i + 1), '', format5)
                worksheet.write('N%s:N%s' % (i, i), '%s' % (b.hsup_100), format4)
                worksheet.write('O%s:O%s' % (i, i), '%s' % (b.jrs_conges), format4)
                worksheet.merge_range('N%s:O%s' % (i + 1, i + 1), '', format1)
                worksheet.write('N%s:O%s' % (i + 1, i + 1), '%s' % (b.exoneration), format5)
                worksheet.write('P%s:P%s' % (i, i), '%s' % (b.conges_payes), format4)
                worksheet.write('P%s:P%s' % (i + 1, i + 1), '%s' % (b.arrondi), format5)
                worksheet.merge_range('Q%s:Q%s' % (i, i + 1), '', format1)
                worksheet.write('Q%s:Q%s' % (i, i + 1), '%s' % (b.salaire_net_a_payer), format4)

                i = i + 2

            for b in datas.filtered(
                    lambda re: not re.employee_id.matricule and re.department_id.id == department.id).sorted(
                    key=lambda r: r.employee_id.matricule):
                worksheet.set_row(i, 30)
                worksheet.merge_range('A%s:A%s' % (i, i + 1), '', format1)
                worksheet.write('A%s:A%s' % (i, i + 1), '%s' % (b.employee_id.matricule), format4)
                worksheet.write('B%s:B%s' % (i, i), '%s %s' % (b.employee_id.prenom, b.employee_id.name),
                                format4)
                worksheet.write('B%s:B%s' % (i + 1, i + 1), '%s' % (b.prime), format5)
                worksheet.write('C%s:C%s' % (i, i), '%s' % (b.employee_id.job_id.name), format4)
                worksheet.write('C%s:C%s' % (i + 1, i + 1), '%s' % (b.salaire_brute), format5)
                worksheet.write('D%s:D%s' % (i, i), '%s' % (b.employee_id.date), format4)
                worksheet.write('D%s:D%s' % (i + 1, i + 1), '%s' % (b.salaire_brute_imposable), format5)
                worksheet.write('E%s:E%s' % (i, i), '%s' % (b.employee_id.birthday), format4)
                worksheet.write('E%s:E%s' % (i + 1, i + 1), '%s' % (b.cnss), format5)
                worksheet.write('F%s:F%s' % (i, i),
                                '%s' % (b.employee_id.ssnid if b.employee_id.ssnid else ''), format4)
                worksheet.write('F%s:F%s' % (i + 1, i + 1), '%s' % (b.cimr_assurance_amo), format5)
                worksheet.write('G%s:G%s' % (i, i), '%s' % (b.employee_id.children), format4)
                worksheet.write('H%s:H%s' % (i, i), '%s' % (b.employee_id.chargefam), format4)
                worksheet.write('I%s:I%s' % (i, i), '%s' % (b.salaire_base_mois), format4)
                worksheet.merge_range('G%s:I%s' % (i + 1, i + 1), '', format1)
                worksheet.write('G%s:I%s' % (i + 1, i + 1), '%s' % (b.salaire_net_imposable), format5)
                worksheet.write('J%s:J%s' % (i, i), '%s' % (b.prime_anciennete), format4)
                worksheet.write('J%s:J%s' % (i + 1, i + 1), '%s' % (b.igr), format5)
                worksheet.write('K%s:k%s' % (i, i), '', format4)
                worksheet.write('K%s:K%s' % (i + 1, i + 1), '', format5)
                worksheet.write('L%s:L%s' % (i, i), '%s' % (b.hsup_25), format4)
                worksheet.write('M%s:M%s' % (i, i), '%s' % (b.hsup_50), format4)
                worksheet.merge_range('L%s:M%s' % (i + 1, i + 1), '', format1)
                worksheet.write('L%s:M%s' % (i + 1, i + 1), '', format5)
                worksheet.write('N%s:N%s' % (i, i), '%s' % (b.hsup_100), format4)
                worksheet.write('O%s:O%s' % (i, i), '%s' % (b.jrs_conges), format4)
                worksheet.merge_range('N%s:O%s' % (i + 1, i + 1), '', format1)
                worksheet.write('N%s:O%s' % (i + 1, i + 1), '%s' % (b.exoneration), format5)
                worksheet.write('P%s:P%s' % (i, i), '%s' % (b.conges_payes), format4)
                worksheet.write('P%s:P%s' % (i + 1, i + 1), '%s' % (b.arrondi), format5)
                worksheet.merge_range('Q%s:Q%s' % (i, i + 1), '', format1)
                worksheet.write('Q%s:Q%s' % (i, i + 1), '%s' % (b.salaire_net_a_payer), format4)

                i = i + 2

            i = i + 1

            worksheet.set_row(i, 30)
            worksheet.merge_range('A%s:A%s' % (i, i + 1), '', format1)
            worksheet.write('A%s:A%s' % (i, i + 1), '', format5)
            worksheet.write('B%s:B%s' % (i, i), 'TOTAL', format5)
            worksheet.write('B%s:B%s' % (i + 1, i + 1), '%.2f' % (
                sum(datas.filtered(lambda re: re.department_id.id == department.id).mapped(
                    'prime'))), format4)
            worksheet.write('C%s:C%s' % (i, i), '', format5)
            worksheet.write('C%s:C%s' % (i + 1, i + 1), '%s' % (
                sum(datas.filtered(lambda re: re.department_id.id == department.id).mapped(
                    'salaire_brute'))), format4)
            worksheet.write('D%s:D%s' % (i, i), '', format5)
            worksheet.write('D%s:D%s' % (i + 1, i + 1), '%s' % (
                sum(datas.filtered(lambda re: re.department_id.id == department.id).mapped(
                    'salaire_brute_imposable'))), format4)
            worksheet.write('E%s:E%s' % (i, i), '', format5)
            worksheet.write('E%s:E%s' % (i + 1, i + 1), '%s' % (
                sum(datas.filtered(lambda re: re.department_id.id == department.id).mapped(
                    'cnss'))), format4)
            worksheet.write('F%s:F%s' % (i, i), '', format5)
            worksheet.write('F%s:F%s' % (i + 1, i + 1), '%s' % (
                sum(datas.filtered(lambda re: re.department_id.id == department.id).mapped(
                    'cimr_assurance_amo'))), format4)
            worksheet.write('G%s:G%s' % (i, i), '%s' % (
                sum(datas.filtered(lambda re: re.department_id.id == department.id).mapped(
                    'employee_id').mapped('children'))), format5)
            worksheet.write('H%s:H%s' % (i, i), '%s' % (
                sum(datas.filtered(lambda re: re.department_id.id == department.id).mapped(
                    'employee_id').mapped('chargefam'))), format5)
            worksheet.write('I%s:I%s' % (i, i), '', format5)
            worksheet.merge_range('G%s:I%s' % (i + 1, i + 1), '', format4)
            worksheet.write('G%s:I%s' % (i + 1, i + 1), '%s' % (
                sum(datas.filtered(lambda re: re.department_id.id == department.id).mapped(
                    'salaire_net_imposable'))), format4)
            worksheet.write('J%s:J%s' % (i, i), 'total_3', format5)
            worksheet.write('J%s:J%s' % (i + 1, i + 1), '%s' % (
                sum(datas.filtered(lambda re: re.department_id.id == department.id).mapped(
                    'igr'))), format4)
            worksheet.write('K%s:k%s' % (i, i), '%s' % (
                sum(datas.filtered(lambda re: re.department_id.id == department.id).mapped(
                    'prime_anciennete'))), format5)
            worksheet.write('K%s:K%s' % (i + 1, i + 1), '', format4)
            worksheet.write('L%s:L%s' % (i, i), '%s' % (
                sum(datas.filtered(lambda re: re.department_id.id == department.id).mapped(
                    'hsup_25'))), format5)
            worksheet.write('M%s:M%s' % (i, i), '%s' % (
                sum(datas.filtered(lambda re: re.department_id.id == department.id).mapped(
                    'hsup_50'))), format5)
            worksheet.merge_range('L%s:M%s' % (i + 1, i + 1), '', format4)
            worksheet.write('L%s:M%s' % (i + 1, i + 1), '', format4)
            worksheet.write('N%s:N%s' % (i, i), '%s' % (
                sum(datas.filtered(lambda re: re.department_id.id == department.id).mapped(
                    'hsup_100'))), format5)
            worksheet.write('O%s:O%s' % (i, i), '%s' % (
                sum(datas.filtered(lambda re: re.department_id.id == department.id).mapped(
                    'jrs_conges'))), format5)
            worksheet.merge_range('N%s:O%s' % (i + 1, i + 1), '', format4)
            worksheet.write('N%s:O%s' % (i + 1, i + 1), '%.2f' % (
                sum(datas.filtered(lambda re: re.department_id.id == department.id).mapped(
                    'exoneration'))), format4)
            worksheet.write('P%s:P%s' % (i, i), '%s' % (
                sum(datas.filtered(lambda re: re.department_id.id == department.id).mapped(
                    'conges_payes'))), format5)
            worksheet.write('P%s:P%s' % (i + 1, i + 1), '%s' % (
                sum(datas.filtered(lambda re: re.department_id.id == department.id).mapped(
                    'arrondi'))), format4)
            worksheet.write('Q%s:Q%s' % (i, i), '', format5)
            worksheet.write('Q%s:Q%s' % (i + 1, i + 1), '%.2f' % (
                sum(datas.filtered(lambda re: re.department_id.id == department.id).mapped(
                    'salaire_net_a_payer'))), format4)

class JournalPaieBulletinByPeriodXlsx(models.AbstractModel):
    _name = 'report.kzm_payroll_ma.journal_paie_bulletin_by_period_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, datas):
        # for rec in datas:
        locale.setlocale(locale.LC_ALL,
                         'fr_FR.UTF-8')  # sudo locale-gen fr_FR.UTF-8
        y = 0
        for period in datas.mapped('period_id'):
            report_name = '%s) %s' % (y, period.name)
            worksheet = workbook.add_worksheet(report_name)
            format0 = workbook.add_format(
                {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
                 'font_color': 'black', 'bg_color': 'white'})
            format1 = workbook.add_format(
                {'font_size': 18, 'align': 'center', 'valign': 'vcenter',
                 'font_color': '#495057', 'bg_color': 'white', 'bold': True})
            format2 = workbook.add_format(
                {'font_size': 13, 'align': 'center', 'valign': 'vcenter',
                 'font_color': '#495057', 'bold': True, 'bg_color': 'white',
                 'underline': True})
            format4 = workbook.add_format(
                {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
                 'font_color': 'black', 'bg_color': '#F8F5F7',
                 'border': 1, 'border_color': 'black'})
            format5 = workbook.add_format(
                {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
                 'font_color': 'black', 'bg_color': 'white',
                 'border': 1, 'border_color': 'black'})
            format6 = workbook.add_format(
                {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
                 'font_color': '#495057', 'bg_color': 'white',
                 'border': 1, 'border_color': 'black'})

            worksheet.merge_range('A1:Q1', '', format1)
            worksheet.merge_range('A2:Q2', '', format1)

            worksheet.set_row(0, 50)
            worksheet.set_row(1, 50)
            worksheet.set_row(2, 25)
            worksheet.set_row(3, 25)

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

            worksheet.write('A1:Q1', 'Journal de Paie', format1)
            worksheet.write('A2:Q2', 'Mois: %s' % (period.name), format2)

            worksheet.merge_range('A3:A4', '', format1)
            worksheet.write('A3:A4', 'Matr', format4)
            worksheet.write('B3:B3', 'Nom - Prénom', format4)
            worksheet.write('B4:B4', 'Primes imposables', format5)
            worksheet.write('C3:C3', 'Fonction', format4)
            worksheet.write('C4:C4', 'Rev brut global', format5)
            worksheet.write('D3:D3', 'Date embauche', format4)
            worksheet.write('D4:D4', 'Rev brut impos', format5)
            worksheet.write('E3:E3', 'Date naissance', format4)
            worksheet.write('E4:E4', 'CNSS', format5)
            worksheet.write('F3:F3', 'N°CNSS', format4)
            worksheet.write('F4:F4', 'CIMR/ASS/AMO', format5)
            worksheet.write('G3:G3', 'NE', format4)
            worksheet.write('H3:H3', 'NCF', format4)
            worksheet.write('I3:I3', 'Sal Base', format4)
            worksheet.merge_range('G4:I4', '', format1)
            worksheet.write('G4:I4', 'Rev net impos', format5)
            worksheet.write('J3:J3', 'Ancient', format4)
            worksheet.write('J4:J4', 'IGR', format5)
            worksheet.write('K3:k3', 'HSup 0%', format4)
            worksheet.write('K4:K4', 'Avances', format5)
            worksheet.write('L3:L3', 'HSup 25%', format4)
            worksheet.write('M3:M3', 'HSup 50%', format4)
            worksheet.merge_range('L4:M4', '', format1)
            worksheet.write('L4:M4', 'Prêt et Ret', format5)
            worksheet.write('N3:N3', 'HSup 100%', format4)
            worksheet.write('O3:O3', 'Jrs congés', format4)
            worksheet.merge_range('N4:O4', '', format1)
            worksheet.write('N4:O4', 'Primes non impos', format5)
            worksheet.write('P3:P3', 'Congés payés', format4)
            worksheet.write('P4:P4', 'Arrondi', format5)
            worksheet.merge_range('Q3:Q4', '', format1)
            worksheet.write('Q3:Q4', 'Net à payer', format4)

            i = 5
            for b in datas.filtered(
                    lambda re: re.employee_id.matricule  and re.period_id.id == period.id).sorted(
                    key=lambda r: r.employee_id.matricule):
                worksheet.set_row(i, 30)
                worksheet.merge_range('A%s:A%s' % (i, i + 1), '', format1)
                worksheet.write('A%s:A%s' % (i, i + 1), '%s' % (b.employee_id.matricule), format4)
                worksheet.write('B%s:B%s' % (i, i), '%s %s' % (b.employee_id.prenom, b.employee_id.name),
                                format4)
                worksheet.write('B%s:B%s' % (i + 1, i + 1), '%s' % (b.prime), format5)
                worksheet.write('C%s:C%s' % (i, i), '%s' % (b.employee_id.job_id.name), format4)
                worksheet.write('C%s:C%s' % (i + 1, i + 1), '%s' % (b.salaire_brute), format5)
                worksheet.write('D%s:D%s' % (i, i), '%s' % (b.employee_id.date), format4)
                worksheet.write('D%s:D%s' % (i + 1, i + 1), '%s' % (b.salaire_brute_imposable), format5)
                worksheet.write('E%s:E%s' % (i, i), '%s' % (b.employee_id.birthday), format4)
                worksheet.write('E%s:E%s' % (i + 1, i + 1), '%s' % (b.cnss), format5)
                worksheet.write('F%s:F%s' % (i, i),
                                '%s' % (b.employee_id.ssnid if b.employee_id.ssnid else ''), format4)
                worksheet.write('F%s:F%s' % (i + 1, i + 1), '%s' % (b.cimr_assurance_amo), format5)
                worksheet.write('G%s:G%s' % (i, i), '%s' % (b.employee_id.children), format4)
                worksheet.write('H%s:H%s' % (i, i), '%s' % (b.employee_id.chargefam), format4)
                worksheet.write('I%s:I%s' % (i, i), '%s' % (b.salaire_base_mois), format4)
                worksheet.merge_range('G%s:I%s' % (i + 1, i + 1), '', format1)
                worksheet.write('G%s:I%s' % (i + 1, i + 1), '%s' % (b.salaire_net_imposable), format5)
                worksheet.write('J%s:J%s' % (i, i), '%s' % (b.prime_anciennete), format4)
                worksheet.write('J%s:J%s' % (i + 1, i + 1), '%s' % (b.igr), format5)
                worksheet.write('K%s:k%s' % (i, i), '', format4)
                worksheet.write('K%s:K%s' % (i + 1, i + 1), '', format5)
                worksheet.write('L%s:L%s' % (i, i), '%s' % (b.hsup_25), format4)
                worksheet.write('M%s:M%s' % (i, i), '%s' % (b.hsup_50), format4)
                worksheet.merge_range('L%s:M%s' % (i + 1, i + 1), '', format1)
                worksheet.write('L%s:M%s' % (i + 1, i + 1), '', format5)
                worksheet.write('N%s:N%s' % (i, i), '%s' % (b.hsup_100), format4)
                worksheet.write('O%s:O%s' % (i, i), '%s' % (b.jrs_conges), format4)
                worksheet.merge_range('N%s:O%s' % (i + 1, i + 1), '', format1)
                worksheet.write('N%s:O%s' % (i + 1, i + 1), '%s' % (b.exoneration), format5)
                worksheet.write('P%s:P%s' % (i, i), '%s' % (b.conges_payes), format4)
                worksheet.write('P%s:P%s' % (i + 1, i + 1), '%s' % (b.arrondi), format5)
                worksheet.merge_range('Q%s:Q%s' % (i, i + 1), '', format1)
                worksheet.write('Q%s:Q%s' % (i, i + 1), '%s' % (b.salaire_net_a_payer), format4)

                i = i + 2

            for b in datas.filtered(
                    lambda re: not re.employee_id.matricule and re.period_id.id == period.id).sorted(
                    key=lambda r: r.employee_id.matricule):
                worksheet.set_row(i, 30)
                worksheet.merge_range('A%s:A%s' % (i, i + 1), '', format1)
                worksheet.write('A%s:A%s' % (i, i + 1), '%s' % (b.employee_id.matricule), format4)
                worksheet.write('B%s:B%s' % (i, i), '%s %s' % (b.employee_id.prenom, b.employee_id.name),
                                format4)
                worksheet.write('B%s:B%s' % (i + 1, i + 1), '%s' % (b.prime), format5)
                worksheet.write('C%s:C%s' % (i, i), '%s' % (b.employee_id.job_id.name), format4)
                worksheet.write('C%s:C%s' % (i + 1, i + 1), '%s' % (b.salaire_brute), format5)
                worksheet.write('D%s:D%s' % (i, i), '%s' % (b.employee_id.date), format4)
                worksheet.write('D%s:D%s' % (i + 1, i + 1), '%s' % (b.salaire_brute_imposable), format5)
                worksheet.write('E%s:E%s' % (i, i), '%s' % (b.employee_id.birthday), format4)
                worksheet.write('E%s:E%s' % (i + 1, i + 1), '%s' % (b.cnss), format5)
                worksheet.write('F%s:F%s' % (i, i),
                                '%s' % (b.employee_id.ssnid if b.employee_id.ssnid else ''), format4)
                worksheet.write('F%s:F%s' % (i + 1, i + 1), '%s' % (b.cimr_assurance_amo), format5)
                worksheet.write('G%s:G%s' % (i, i), '%s' % (b.employee_id.children), format4)
                worksheet.write('H%s:H%s' % (i, i), '%s' % (b.employee_id.chargefam), format4)
                worksheet.write('I%s:I%s' % (i, i), '%s' % (b.salaire_base_mois), format4)
                worksheet.merge_range('G%s:I%s' % (i + 1, i + 1), '', format1)
                worksheet.write('G%s:I%s' % (i + 1, i + 1), '%s' % (b.salaire_net_imposable), format5)
                worksheet.write('J%s:J%s' % (i, i), '%s' % (b.prime_anciennete), format4)
                worksheet.write('J%s:J%s' % (i + 1, i + 1), '%s' % (b.igr), format5)
                worksheet.write('K%s:k%s' % (i, i), '', format4)
                worksheet.write('K%s:K%s' % (i + 1, i + 1), '', format5)
                worksheet.write('L%s:L%s' % (i, i), '%s' % (b.hsup_25), format4)
                worksheet.write('M%s:M%s' % (i, i), '%s' % (b.hsup_50), format4)
                worksheet.merge_range('L%s:M%s' % (i + 1, i + 1), '', format1)
                worksheet.write('L%s:M%s' % (i + 1, i + 1), '', format5)
                worksheet.write('N%s:N%s' % (i, i), '%s' % (b.hsup_100), format4)
                worksheet.write('O%s:O%s' % (i, i), '%s' % (b.jrs_conges), format4)
                worksheet.merge_range('N%s:O%s' % (i + 1, i + 1), '', format1)
                worksheet.write('N%s:O%s' % (i + 1, i + 1), '%s' % (b.exoneration), format5)
                worksheet.write('P%s:P%s' % (i, i), '%s' % (b.conges_payes), format4)
                worksheet.write('P%s:P%s' % (i + 1, i + 1), '%s' % (b.arrondi), format5)
                worksheet.merge_range('Q%s:Q%s' % (i, i + 1), '', format1)
                worksheet.write('Q%s:Q%s' % (i, i + 1), '%s' % (b.salaire_net_a_payer), format4)

                i = i + 2

            i = i + 1

            worksheet.set_row(i, 30)
            worksheet.merge_range('A%s:A%s' % (i, i + 1), '', format1)
            worksheet.write('A%s:A%s' % (i, i + 1), '', format5)
            worksheet.write('B%s:B%s' % (i, i), 'TOTAL', format5)
            worksheet.write('B%s:B%s' % (i + 1, i + 1), '%.2f' % (
                sum(datas.filtered(lambda re: re.period_id.id == period.id).mapped(
                    'prime'))), format4)
            worksheet.write('C%s:C%s' % (i, i), '', format5)
            worksheet.write('C%s:C%s' % (i + 1, i + 1), '%s' % (
                sum(datas.filtered(lambda re: re.period_id.id == period.id).mapped(
                    'salaire_brute'))), format4)
            worksheet.write('D%s:D%s' % (i, i), '', format5)
            worksheet.write('D%s:D%s' % (i + 1, i + 1), '%s' % (
                sum(datas.filtered(lambda re: re.period_id.id == period.id).mapped(
                    'salaire_brute_imposable'))), format4)
            worksheet.write('E%s:E%s' % (i, i), '', format5)
            worksheet.write('E%s:E%s' % (i + 1, i + 1), '%s' % (
                sum(datas.filtered(lambda re: re.period_id.id == period.id).mapped(
                    'cnss'))), format4)
            worksheet.write('F%s:F%s' % (i, i), '', format5)
            worksheet.write('F%s:F%s' % (i + 1, i + 1), '%s' % (
                sum(datas.filtered(lambda re: re.period_id.id == period.id).mapped(
                    'cimr_assurance_amo'))), format4)
            worksheet.write('G%s:G%s' % (i, i), '%s' % (
                sum(datas.filtered(lambda re: re.period_id.id == period.id).mapped(
                    'employee_id').mapped('children'))), format5)
            worksheet.write('H%s:H%s' % (i, i), '%s' % (
                sum(datas.filtered(lambda re: re.period_id.id == period.id).mapped(
                    'employee_id').mapped('chargefam'))), format5)
            worksheet.write('I%s:I%s' % (i, i), '', format5)
            worksheet.merge_range('G%s:I%s' % (i + 1, i + 1), '', format4)
            worksheet.write('G%s:I%s' % (i + 1, i + 1), '%s' % (
                sum(datas.filtered(lambda re: re.period_id.id == period.id).mapped(
                    'salaire_net_imposable'))), format4)
            worksheet.write('J%s:J%s' % (i, i), 'total_3', format5)
            worksheet.write('J%s:J%s' % (i + 1, i + 1), '%s' % (
                sum(datas.filtered(lambda re: re.period_id.id == period.id).mapped(
                    'igr'))), format4)
            worksheet.write('K%s:k%s' % (i, i), '%s' % (
                sum(datas.filtered(lambda re: re.period_id.id == period.id).mapped(
                    'prime_anciennete'))), format5)
            worksheet.write('K%s:K%s' % (i + 1, i + 1), '', format4)
            worksheet.write('L%s:L%s' % (i, i), '%s' % (
                sum(datas.filtered(lambda re: re.period_id.id == period.id).mapped(
                    'hsup_25'))), format5)
            worksheet.write('M%s:M%s' % (i, i), '%s' % (
                sum(datas.filtered(lambda re: re.period_id.id == period.id).mapped(
                    'hsup_50'))), format5)
            worksheet.merge_range('L%s:M%s' % (i + 1, i + 1), '', format4)
            worksheet.write('L%s:M%s' % (i + 1, i + 1), '', format4)
            worksheet.write('N%s:N%s' % (i, i), '%s' % (
                sum(datas.filtered(lambda re: re.period_id.id == period.id).mapped(
                    'hsup_100'))), format5)
            worksheet.write('O%s:O%s' % (i, i), '%s' % (
                sum(datas.filtered(lambda re: re.period_id.id == period.id).mapped(
                    'jrs_conges'))), format5)
            worksheet.merge_range('N%s:O%s' % (i + 1, i + 1), '', format4)
            worksheet.write('N%s:O%s' % (i + 1, i + 1), '%.2f' % (
                sum(datas.filtered(lambda re: re.period_id.id == period.id).mapped(
                    'exoneration'))), format4)
            worksheet.write('P%s:P%s' % (i, i), '%s' % (
                sum(datas.filtered(lambda re: re.period_id.id == period.id).mapped(
                    'conges_payes'))), format5)
            worksheet.write('P%s:P%s' % (i + 1, i + 1), '%s' % (
                sum(datas.filtered(lambda re: re.period_id.id == period.id).mapped(
                    'arrondi'))), format4)
            worksheet.write('Q%s:Q%s' % (i, i), '', format5)
            worksheet.write('Q%s:Q%s' % (i + 1, i + 1), '%.2f' % (
                sum(datas.filtered(lambda re: re.period_id.id == period.id).mapped(
                    'salaire_net_a_payer'))), format4)

class JournalPaieBulletinByPeriodDepartmentXlsx(models.AbstractModel):
    _name = 'report.kzm_payroll_ma.journal_paie_bull_by_per_depart_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, datas):
        # for rec in datas:
        locale.setlocale(locale.LC_ALL,
                         'fr_FR.UTF-8')  # sudo locale-gen fr_FR.UTF-8
        y = 0
        for period in datas.mapped('period_id'):
            for department in datas.mapped('employee_id').mapped('department_id'):
                y = y + 1
                report_name = '%s) %s_%s' % (y, department.name, period.name)
                worksheet = workbook.add_worksheet(report_name)
                format0 = workbook.add_format(
                    {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
                     'font_color': 'black', 'bg_color': 'white'})
                format1 = workbook.add_format(
                    {'font_size': 18, 'align': 'center', 'valign': 'vcenter',
                     'font_color': '#495057', 'bg_color': 'white', 'bold': True})
                format2 = workbook.add_format(
                    {'font_size': 13, 'align': 'center', 'valign': 'vcenter',
                     'font_color': '#495057', 'bold': True, 'bg_color': 'white',
                     'underline': True})
                format4 = workbook.add_format(
                    {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
                     'font_color': 'black', 'bg_color': '#F8F5F7',
                     'border': 1, 'border_color': 'black'})
                format5 = workbook.add_format(
                    {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
                     'font_color': 'black', 'bg_color': 'white',
                     'border': 1, 'border_color': 'black'})
                format6 = workbook.add_format(
                    {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
                     'font_color': '#495057', 'bg_color': 'white',
                     'border': 1, 'border_color': 'black'})

                worksheet.merge_range('A1:Q1', '', format1)
                worksheet.merge_range('A2:Q2', '', format1)

                worksheet.set_row(0, 50)
                worksheet.set_row(1, 50)
                worksheet.set_row(2, 25)
                worksheet.set_row(3, 25)

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

                worksheet.write('A1:Q1', 'Journal de Paie', format1)
                worksheet.write('A2:Q2', 'Department: %s' % (department.name), format2)
                worksheet.write('A2:Q2', 'Mois: %s' % (period.name), format2)

                worksheet.merge_range('A3:A4', '', format1)
                worksheet.write('A3:A4', 'Matr', format4)
                worksheet.write('B3:B3', 'Nom - Prénom', format4)
                worksheet.write('B4:B4', 'Primes imposables', format5)
                worksheet.write('C3:C3', 'Fonction', format4)
                worksheet.write('C4:C4', 'Rev brut global', format5)
                worksheet.write('D3:D3', 'Date embauche', format4)
                worksheet.write('D4:D4', 'Rev brut impos', format5)
                worksheet.write('E3:E3', 'Date naissance', format4)
                worksheet.write('E4:E4', 'CNSS', format5)
                worksheet.write('F3:F3', 'N°CNSS', format4)
                worksheet.write('F4:F4', 'CIMR/ASS/AMO', format5)
                worksheet.write('G3:G3', 'NE', format4)
                worksheet.write('H3:H3', 'NCF', format4)
                worksheet.write('I3:I3', 'Sal Base', format4)
                worksheet.merge_range('G4:I4', '', format1)
                worksheet.write('G4:I4', 'Rev net impos', format5)
                worksheet.write('J3:J3', 'Ancient', format4)
                worksheet.write('J4:J4', 'IGR', format5)
                worksheet.write('K3:k3', 'HSup 0%', format4)
                worksheet.write('K4:K4', 'Avances', format5)
                worksheet.write('L3:L3', 'HSup 25%', format4)
                worksheet.write('M3:M3', 'HSup 50%', format4)
                worksheet.merge_range('L4:M4', '', format1)
                worksheet.write('L4:M4', 'Prêt et Ret', format5)
                worksheet.write('N3:N3', 'HSup 100%', format4)
                worksheet.write('O3:O3', 'Jrs congés', format4)
                worksheet.merge_range('N4:O4', '', format1)
                worksheet.write('N4:O4', 'Primes non impos', format5)
                worksheet.write('P3:P3', 'Congés payés', format4)
                worksheet.write('P4:P4', 'Arrondi', format5)
                worksheet.merge_range('Q3:Q4', '', format1)
                worksheet.write('Q3:Q4', 'Net à payer', format4)

                i = 5
                for b in datas.filtered(
                        lambda re: re.employee_id.matricule and re.period_id.id == period.id and re.department_id.id == department.id).sorted(
                        key=lambda r: r.employee_id.matricule):
                    worksheet.set_row(i, 30)
                    worksheet.merge_range('A%s:A%s' % (i, i + 1), '', format1)
                    worksheet.write('A%s:A%s' % (i, i + 1), '%s' % (b.employee_id.matricule), format4)
                    worksheet.write('B%s:B%s' % (i, i), '%s %s' % (b.employee_id.prenom, b.employee_id.name),
                                    format4)
                    worksheet.write('B%s:B%s' % (i + 1, i + 1), '%s' % (b.prime), format5)
                    worksheet.write('C%s:C%s' % (i, i), '%s' % (b.employee_id.job_id.name), format4)
                    worksheet.write('C%s:C%s' % (i + 1, i + 1), '%s' % (b.salaire_brute), format5)
                    worksheet.write('D%s:D%s' % (i, i), '%s' % (b.employee_id.date), format4)
                    worksheet.write('D%s:D%s' % (i + 1, i + 1), '%s' % (b.salaire_brute_imposable), format5)
                    worksheet.write('E%s:E%s' % (i, i), '%s' % (b.employee_id.birthday), format4)
                    worksheet.write('E%s:E%s' % (i + 1, i + 1), '%s' % (b.cnss), format5)
                    worksheet.write('F%s:F%s' % (i, i),
                                    '%s' % (b.employee_id.ssnid if b.employee_id.ssnid else ''), format4)
                    worksheet.write('F%s:F%s' % (i + 1, i + 1), '%s' % (b.cimr_assurance_amo), format5)
                    worksheet.write('G%s:G%s' % (i, i), '%s' % (b.employee_id.children), format4)
                    worksheet.write('H%s:H%s' % (i, i), '%s' % (b.employee_id.chargefam), format4)
                    worksheet.write('I%s:I%s' % (i, i), '%s' % (b.salaire_base_mois), format4)
                    worksheet.merge_range('G%s:I%s' % (i + 1, i + 1), '', format1)
                    worksheet.write('G%s:I%s' % (i + 1, i + 1), '%s' % (b.salaire_net_imposable), format5)
                    worksheet.write('J%s:J%s' % (i, i), '%s' % (b.prime_anciennete), format4)
                    worksheet.write('J%s:J%s' % (i + 1, i + 1), '%s' % (b.igr), format5)
                    worksheet.write('K%s:k%s' % (i, i), '', format4)
                    worksheet.write('K%s:K%s' % (i + 1, i + 1), '', format5)
                    worksheet.write('L%s:L%s' % (i, i), '%s' % (b.hsup_25), format4)
                    worksheet.write('M%s:M%s' % (i, i), '%s' % (b.hsup_50), format4)
                    worksheet.merge_range('L%s:M%s' % (i + 1, i + 1), '', format1)
                    worksheet.write('L%s:M%s' % (i + 1, i + 1), '', format5)
                    worksheet.write('N%s:N%s' % (i, i), '%s' % (b.hsup_100), format4)
                    worksheet.write('O%s:O%s' % (i, i), '%s' % (b.jrs_conges), format4)
                    worksheet.merge_range('N%s:O%s' % (i + 1, i + 1), '', format1)
                    worksheet.write('N%s:O%s' % (i + 1, i + 1), '%s' % (b.exoneration), format5)
                    worksheet.write('P%s:P%s' % (i, i), '%s' % (b.conges_payes), format4)
                    worksheet.write('P%s:P%s' % (i + 1, i + 1), '%s' % (b.arrondi), format5)
                    worksheet.merge_range('Q%s:Q%s' % (i, i + 1), '', format1)
                    worksheet.write('Q%s:Q%s' % (i, i + 1), '%s' % (b.salaire_net_a_payer), format4)

                    i = i + 2

                for b in datas.filtered(
                        lambda re: not re.employee_id.matricule and re.period_id.id == period.id and re.department_id.id == department.id).sorted(
                        key=lambda r: r.employee_id.matricule):
                    worksheet.set_row(i, 30)
                    worksheet.merge_range('A%s:A%s' % (i, i + 1), '', format1)
                    worksheet.write('A%s:A%s' % (i, i + 1), '%s' % (b.employee_id.matricule), format4)
                    worksheet.write('B%s:B%s' % (i, i), '%s %s' % (b.employee_id.prenom, b.employee_id.name),
                                    format4)
                    worksheet.write('B%s:B%s' % (i + 1, i + 1), '%s' % (b.prime), format5)
                    worksheet.write('C%s:C%s' % (i, i), '%s' % (b.employee_id.job_id.name), format4)
                    worksheet.write('C%s:C%s' % (i + 1, i + 1), '%s' % (b.salaire_brute), format5)
                    worksheet.write('D%s:D%s' % (i, i), '%s' % (b.employee_id.date), format4)
                    worksheet.write('D%s:D%s' % (i + 1, i + 1), '%s' % (b.salaire_brute_imposable), format5)
                    worksheet.write('E%s:E%s' % (i, i), '%s' % (b.employee_id.birthday), format4)
                    worksheet.write('E%s:E%s' % (i + 1, i + 1), '%s' % (b.cnss), format5)
                    worksheet.write('F%s:F%s' % (i, i),
                                    '%s' % (b.employee_id.ssnid if b.employee_id.ssnid else ''), format4)
                    worksheet.write('F%s:F%s' % (i + 1, i + 1), '%s' % (b.cimr_assurance_amo), format5)
                    worksheet.write('G%s:G%s' % (i, i), '%s' % (b.employee_id.children), format4)
                    worksheet.write('H%s:H%s' % (i, i), '%s' % (b.employee_id.chargefam), format4)
                    worksheet.write('I%s:I%s' % (i, i), '%s' % (b.salaire_base_mois), format4)
                    worksheet.merge_range('G%s:I%s' % (i + 1, i + 1), '', format1)
                    worksheet.write('G%s:I%s' % (i + 1, i + 1), '%s' % (b.salaire_net_imposable), format5)
                    worksheet.write('J%s:J%s' % (i, i), '%s' % (b.prime_anciennete), format4)
                    worksheet.write('J%s:J%s' % (i + 1, i + 1), '%s' % (b.igr), format5)
                    worksheet.write('K%s:k%s' % (i, i), '', format4)
                    worksheet.write('K%s:K%s' % (i + 1, i + 1), '', format5)
                    worksheet.write('L%s:L%s' % (i, i), '%s' % (b.hsup_25), format4)
                    worksheet.write('M%s:M%s' % (i, i), '%s' % (b.hsup_50), format4)
                    worksheet.merge_range('L%s:M%s' % (i + 1, i + 1), '', format1)
                    worksheet.write('L%s:M%s' % (i + 1, i + 1), '', format5)
                    worksheet.write('N%s:N%s' % (i, i), '%s' % (b.hsup_100), format4)
                    worksheet.write('O%s:O%s' % (i, i), '%s' % (b.jrs_conges), format4)
                    worksheet.merge_range('N%s:O%s' % (i + 1, i + 1), '', format1)
                    worksheet.write('N%s:O%s' % (i + 1, i + 1), '%s' % (b.exoneration), format5)
                    worksheet.write('P%s:P%s' % (i, i), '%s' % (b.conges_payes), format4)
                    worksheet.write('P%s:P%s' % (i + 1, i + 1), '%s' % (b.arrondi), format5)
                    worksheet.merge_range('Q%s:Q%s' % (i, i + 1), '', format1)
                    worksheet.write('Q%s:Q%s' % (i, i + 1), '%s' % (b.salaire_net_a_payer), format4)

                    i = i + 2

                i = i + 1

                worksheet.set_row(i, 30)
                worksheet.merge_range('A%s:A%s' % (i, i + 1), '', format1)
                worksheet.write('A%s:A%s' % (i, i + 1), '', format5)
                worksheet.write('B%s:B%s' % (i, i), 'TOTAL', format5)
                worksheet.write('B%s:B%s' % (i + 1, i + 1), '%.2f' % (
                    sum(datas.filtered(lambda re: re.period_id.id == period.id and re.department_id.id == department.id).mapped(
                        'prime'))), format4)
                worksheet.write('C%s:C%s' % (i, i), '', format5)
                worksheet.write('C%s:C%s' % (i + 1, i + 1), '%s' % (
                    sum(datas.filtered(lambda re: re.period_id.id == period.id and re.department_id.id == department.id).mapped(
                        'salaire_brute'))), format4)
                worksheet.write('D%s:D%s' % (i, i), '', format5)
                worksheet.write('D%s:D%s' % (i + 1, i + 1), '%s' % (
                    sum(datas.filtered(lambda re: re.period_id.id == period.id and re.department_id.id == department.id).mapped(
                        'salaire_brute_imposable'))), format4)
                worksheet.write('E%s:E%s' % (i, i), '', format5)
                worksheet.write('E%s:E%s' % (i + 1, i + 1), '%s' % (
                    sum(datas.filtered(lambda re: re.period_id.id == period.id and re.department_id.id == department.id).mapped(
                        'cnss'))), format4)
                worksheet.write('F%s:F%s' % (i, i), '', format5)
                worksheet.write('F%s:F%s' % (i + 1, i + 1), '%s' % (
                    sum(datas.filtered(lambda re: re.period_id.id == period.id and re.department_id.id == department.id).mapped(
                        'cimr_assurance_amo'))), format4)
                worksheet.write('G%s:G%s' % (i, i), '%s' % (
                    sum(datas.filtered(lambda re: re.period_id.id == period.id and re.department_id.id == department.id).mapped(
                        'employee_id').mapped('children'))), format5)
                worksheet.write('H%s:H%s' % (i, i), '%s' % (
                    sum(datas.filtered(lambda re: re.period_id.id == period.id and re.department_id.id == department.id).mapped(
                        'employee_id').mapped('chargefam'))), format5)
                worksheet.write('I%s:I%s' % (i, i), '', format5)
                worksheet.merge_range('G%s:I%s' % (i + 1, i + 1), '', format4)
                worksheet.write('G%s:I%s' % (i + 1, i + 1), '%s' % (
                    sum(datas.filtered(lambda re: re.period_id.id == period.id and re.department_id.id == department.id).mapped(
                        'salaire_net_imposable'))), format4)
                worksheet.write('J%s:J%s' % (i, i), 'total_3', format5)
                worksheet.write('J%s:J%s' % (i + 1, i + 1), '%s' % (
                    sum(datas.filtered(lambda re: re.period_id.id == period.id and re.department_id.id == department.id).mapped(
                        'igr'))), format4)
                worksheet.write('K%s:k%s' % (i, i), '%s' % (
                    sum(datas.filtered(lambda re: re.period_id.id == period.id and re.department_id.id == department.id).mapped(
                        'prime_anciennete'))), format5)
                worksheet.write('K%s:K%s' % (i + 1, i + 1), '', format4)
                worksheet.write('L%s:L%s' % (i, i), '%s' % (
                    sum(datas.filtered(lambda re: re.period_id.id == period.id and re.department_id.id == department.id).mapped(
                        'hsup_25'))), format5)
                worksheet.write('M%s:M%s' % (i, i), '%s' % (
                    sum(datas.filtered(lambda re: re.period_id.id == period.id and re.department_id.id == department.id).mapped(
                        'hsup_50'))), format5)
                worksheet.merge_range('L%s:M%s' % (i + 1, i + 1), '', format4)
                worksheet.write('L%s:M%s' % (i + 1, i + 1), '', format4)
                worksheet.write('N%s:N%s' % (i, i), '%s' % (
                    sum(datas.filtered(lambda re: re.period_id.id == period.id and re.department_id.id == department.id).mapped(
                        'hsup_100'))), format5)
                worksheet.write('O%s:O%s' % (i, i), '%s' % (
                    sum(datas.filtered(lambda re: re.period_id.id == period.id and re.department_id.id == department.id).mapped(
                        'jrs_conges'))), format5)
                worksheet.merge_range('N%s:O%s' % (i + 1, i + 1), '', format4)
                worksheet.write('N%s:O%s' % (i + 1, i + 1), '%.2f' % (
                    sum(datas.filtered(lambda re: re.period_id.id == period.id and re.department_id.id == department.id).mapped(
                        'exoneration'))), format4)
                worksheet.write('P%s:P%s' % (i, i), '%s' % (
                    sum(datas.filtered(lambda re: re.period_id.id == period.id and re.department_id.id == department.id).mapped(
                        'conges_payes'))), format5)
                worksheet.write('P%s:P%s' % (i + 1, i + 1), '%s' % (
                    sum(datas.filtered(lambda re: re.period_id.id == period.id and re.department_id.id == department.id).mapped(
                        'arrondi'))), format4)
                worksheet.write('Q%s:Q%s' % (i, i), '', format5)
                worksheet.write('Q%s:Q%s' % (i + 1, i + 1), '%.2f' % (
                    sum(datas.filtered(lambda re: re.period_id.id == period.id and re.department_id.id == department.id).mapped(
                        'salaire_net_a_payer'))), format4)

class LivrePaieXlsx(models.AbstractModel):
    _name = 'report.kzm_payroll_ma.livre_paie_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, datas):
        for rec in datas:
            locale.setlocale(locale.LC_ALL,
                             'fr_FR.UTF-8')  # sudo locale-gen fr_FR.UTF-8
            report_name = '%s - %s' % (rec.name, rec.number)
            worksheet = workbook.add_worksheet(report_name)
            format0 = workbook.add_format(
                {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
                 'font_color': 'black', 'bg_color': 'white'})
            format1 = workbook.add_format(
                {'font_size': 18, 'align': 'center', 'valign': 'vcenter',
                 'font_color': '#495057', 'bg_color': 'white', 'bold': True})
            format2 = workbook.add_format(
                {'font_size': 13, 'align': 'center', 'valign': 'vcenter',
                 'font_color': '#495057', 'bold': True, 'bg_color': 'white',
                 'underline': True})
            format4 = workbook.add_format(
                {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
                 'font_color': 'black', 'bg_color': '#F8F5F7',
                 'border': 1,'border_color': 'black'})
            format5 = workbook.add_format(
                {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
                 'font_color': 'black', 'bg_color': 'white',
                 'border': 1, 'border_color': 'black'})
            format6 = workbook.add_format(
                {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
                 'font_color': '#495057', 'bg_color': 'white',
                 'border': 1, 'border_color': 'black'})

            worksheet.set_row(0, 30)
            worksheet.set_row(1, 30)
            worksheet.set_row(2, 30)
            worksheet.set_row(3, 30)
            worksheet.set_row(4, 30)
            worksheet.set_row(5, 30)
            worksheet.set_row(6, 30)
            worksheet.set_row(7, 30)
            worksheet.set_row(8, 30)
            worksheet.set_row(9, 40)


            worksheet.set_column('A:A', 20)
            worksheet.set_column('B:B', 20)
            worksheet.set_column('C:C', 30)
            worksheet.set_column('D:D', 30)
            worksheet.set_column('E:E', 50)
            worksheet.set_column('F:F', 40)
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

            worksheet.merge_range('M1:P1', '', format1)
            worksheet.merge_range('M2:P2', '', format1)
            worksheet.merge_range('C5:O5', '', format1)
            worksheet.write('M1:P1', 'Human Resources Department', format1)
            worksheet.write('M2:P2', 'Administrative Affairs Directorate', format1)
            worksheet.write('C5:O5', 'LIVRE DE PAIE', format1)

            worksheet.write('P7:P7', '%s' %(fields.Date.today().strftime('%d/%m/%Y')), format1)

            worksheet.merge_range('A1:B7', '', format1)
            icesco_image = self.env.company.logo
            imgdata = base64.b64decode(icesco_image)
            image = io.BytesIO(imgdata)
            worksheet.insert_image('A1:B7', 'icesco.png',
                               {'image_data': image, 'x_scale': 0.3, 'y_scale': 0.2})

            worksheet.write('A9:A9', 'N°', format4)
            worksheet.write('B9:B9', 'ID', format4)
            worksheet.write('C9:C9', "Nom de l'employé", format5)
            worksheet.write('D9:D9', 'Poste occupé', format4)
            worksheet.write('E9:E9', 'Secteur / Centre / Département', format5)
            worksheet.write('F9:F9', 'Catégorie', format4)
            worksheet.write('G9:G9', 'Grade', format5)
            worksheet.write('H9:H9', 'Echelon', format4)
            worksheet.write('I9:I9', 'Salaire de base', format5)
            worksheet.write('J9:J9', 'Allocations familiales', format4)
            worksheet.write('K9:K9', 'Indémnités de transport', format5)
            worksheet.write('L9:L9', 'Indémnités de logement', format4)
            worksheet.write('M9:M9', "Prime d'expatriation", format4)
            worksheet.write('N9:N9', 'Prime de supervision', format4)
            worksheet.write('O9:O9', 'Salaire brut imposable', format5)
            worksheet.write('P9:P9', 'Salaire net', format5)

            i = 10

            for b in rec.bulletin_line_ids.sorted(key=lambda r: r.employee_id.matricule):
                worksheet.set_row(i, 40)
                worksheet.write('A%s:A%s' % (i, i), '%s' % (b.name if b.name else ''), format4)
                worksheet.write('B%s:B%s' % (i, i), '%s' % (b.employee_id.matricule if b.employee_id.matricule else ''), format4)
                worksheet.write('C%s:C%s' % (i, i), '%s' % (b.employee_id.display_name if b.employee_id.id != False else ''), format4)
                worksheet.write('D%s:D%s' % (i, i), '%s' % (b.employee_id.job_title if b.employee_id.job_title else ''), format4)
                worksheet.write('E%s:E%s' % (i, i), '%s' % (b.employee_id.department_id.display_name if b.employee_id.department_id.id != False else ''), format4)
                worksheet.write('F%s:F%s' % (i, i), '%s' % (b.employee_id.category_id.category_id.display_name if b.employee_id.category_id.category_id.id != False else ''), format4)
                worksheet.write('G%s:G%s' % (i, i), '%s' % (b.employee_id.category_id.grade_id.display_name if b.employee_id.category_id.grade_id.id != False else ''), format4)
                worksheet.write('H%s:H%s' % (i, i), '', format4) # ??
                worksheet.write('I%s:I%s' % (i, i), '%s' % (b.salaire_base if b.salaire_base != False else ''),format4)
                worksheet.write('J%s:J%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Allocations familiales').mapped('subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Allocations familiales')) > 0 else 0), format4)
                worksheet.write('K%s:K%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de transport').mapped('subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de transport')) > 0 else 0), format4)
                worksheet.write('L%s:L%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de logement').mapped('subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de logement')) > 0 else 0), format4)
                worksheet.write('M%s:M%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == "Prime d'expatriation").mapped('subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == "Prime d'expatriation")) > 0 else 0), format4)
                worksheet.write('N%s:N%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == "Prime de supervision").mapped('subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == "Prime de supervision")) > 0 else 0), format4)
                worksheet.write('O%s:O%s' % (i, i), '%s' % (b.salaire_brute_imposable), format4)
                worksheet.write('P%s:P%s' % (i, i), '%s' % (b.salaire_net_a_payer), format4)

                i=i+1


class LivrePaieBulletinXlsx(models.AbstractModel):
    _name = 'report.kzm_payroll_ma.livre_paie_bulletin_xlsx'
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
                {'font_size': 18, 'align': 'center', 'valign': 'vcenter',
                 'font_color': '#495057', 'bg_color': 'white', 'bold': True})
            format2 = workbook.add_format(
                {'font_size': 13, 'align': 'center', 'valign': 'vcenter',
                 'font_color': '#495057', 'bold': True, 'bg_color': 'white',
                 'underline': True})
            format4 = workbook.add_format(
                {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
                 'font_color': 'black', 'bg_color': '#F8F5F7',
                 'border': 1,'border_color': 'black'})
            format5 = workbook.add_format(
                {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
                 'font_color': 'black', 'bg_color': 'white',
                 'border': 1, 'border_color': 'black'})
            format6 = workbook.add_format(
                {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
                 'font_color': '#495057', 'bg_color': 'white',
                 'border': 1, 'border_color': 'black'})

            worksheet.set_row(0, 30)
            worksheet.set_row(1, 30)
            worksheet.set_row(2, 30)
            worksheet.set_row(3, 30)
            worksheet.set_row(4, 30)
            worksheet.set_row(5, 30)
            worksheet.set_row(6, 30)
            worksheet.set_row(7, 30)
            worksheet.set_row(8, 30)
            worksheet.set_row(9, 40)


            worksheet.set_column('A:A', 20)
            worksheet.set_column('B:B', 20)
            worksheet.set_column('C:C', 30)
            worksheet.set_column('D:D', 30)
            worksheet.set_column('E:E', 50)
            worksheet.set_column('F:F', 40)
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

            worksheet.merge_range('M1:P1', '', format1)
            worksheet.merge_range('M2:P2', '', format1)
            worksheet.merge_range('C5:O5', '', format1)
            worksheet.write('M1:P1', 'Human Resources Department', format1)
            worksheet.write('M2:P2', 'Administrative Affairs Directorate', format1)
            worksheet.write('C5:O5', 'LIVRE DE PAIE', format1)

            worksheet.write('P7:P7', '%s' %(fields.Date.today().strftime('%d/%m/%Y')), format1)

            worksheet.merge_range('A1:B7', '', format1)
            icesco_image = self.env.company.logo
            imgdata = base64.b64decode(icesco_image)
            image = io.BytesIO(imgdata)
            worksheet.insert_image('A1:B7', 'icesco.png',
                               {'image_data': image, 'x_scale': 0.3, 'y_scale': 0.2})

            worksheet.write('A9:A9', 'N°', format4)
            worksheet.write('B9:B9', 'ID', format4)
            worksheet.write('C9:C9', "Nom de l'employé", format5)
            worksheet.write('D9:D9', 'Poste occupé', format4)
            worksheet.write('E9:E9', 'Secteur / Centre / Département', format5)
            worksheet.write('F9:F9', 'Catégorie', format4)
            worksheet.write('G9:G9', 'Grade', format5)
            worksheet.write('H9:H9', 'Echelon', format4)
            worksheet.write('I9:I9', 'Salaire de base', format5)
            worksheet.write('J9:J9', 'Allocations familiales', format4)
            worksheet.write('K9:K9', 'Indémnités de transport', format5)
            worksheet.write('L9:L9', 'Indémnités de logement', format4)
            worksheet.write('M9:M9', "Prime d'expatriation", format4)
            worksheet.write('N9:N9', 'Prime de supervision', format4)
            worksheet.write('O9:O9', 'Salaire brut imposable', format5)
            worksheet.write('P9:P9', 'Salaire net', format5)

            i = 10

            for b in rec.sorted(key=lambda r: r.employee_id.matricule):
                worksheet.set_row(i, 40)
                worksheet.write('A%s:A%s' % (i, i), '%s' % (b.name if b.name else ''), format4)
                worksheet.write('B%s:B%s' % (i, i), '%s' % (b.employee_id.matricule if b.employee_id.matricule else ''), format4)
                worksheet.write('C%s:C%s' % (i, i), '%s' % (b.employee_id.display_name if b.employee_id.id != False else ''), format4)
                worksheet.write('D%s:D%s' % (i, i), '%s' % (b.employee_id.job_title if b.employee_id.job_title else ''), format4)
                worksheet.write('E%s:E%s' % (i, i), '%s' % (b.employee_id.department_id.display_name if b.employee_id.department_id.id != False else ''), format4)
                worksheet.write('F%s:F%s' % (i, i), '%s' % (b.employee_id.category_id.category_id.display_name if b.employee_id.category_id.category_id.id != False else ''), format4)
                worksheet.write('G%s:G%s' % (i, i), '%s' % (b.employee_id.category_id.grade_id.display_name if b.employee_id.category_id.grade_id.id != False else ''), format4)
                worksheet.write('H%s:H%s' % (i, i), '', format4) # ??
                worksheet.write('I%s:I%s' % (i, i), '%s' % (b.salaire_base if b.salaire_base != False else ''),format4)
                worksheet.write('J%s:J%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Allocations familiales').mapped('subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Allocations familiales')) > 0 else 0), format4)
                worksheet.write('K%s:K%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de transport').mapped('subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de transport')) > 0 else 0), format4)
                worksheet.write('L%s:L%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de logement').mapped('subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de logement')) > 0 else 0), format4)
                worksheet.write('M%s:M%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == "Prime d'expatriation").mapped('subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == "Prime d'expatriation")) > 0 else 0), format4)
                worksheet.write('N%s:N%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == "Prime de supervision").mapped('subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == "Prime de supervision")) > 0 else 0), format4)
                worksheet.write('O%s:O%s' % (i, i), '%s' % (b.salaire_brute_imposable), format4)
                worksheet.write('P%s:P%s' % (i, i), '%s' % (b.salaire_net_a_payer), format4)

                i=i+1
