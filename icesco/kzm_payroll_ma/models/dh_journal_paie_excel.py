import datetime as dt
import locale
import time
from datetime import timedelta, datetime
from odoo import models,fields
import base64
import io
from io import BytesIO

class DhJournalPaieXlsx(models.AbstractModel):
    _name = 'report.kzm_payroll_ma.dh_journal_paie_xlsx'
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

            worksheet.merge_range('A1:Y4', '', format1)
            worksheet.merge_range('A5:Y5', '', format1)
            worksheet.merge_range('A6:Y6', '', format1)
            worksheet.merge_range('A7:Y7', '', format1)

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

            worksheet.write('A6:Y6', 'Journal de Paie' , format1)
            worksheet.write('A7:Y7', 'Mois: %s' % (rec.period_id.name) , format2)


            worksheet.write('A8:A8', 'Matricules', format4)
            worksheet.write('B8:B8', 'Nom - Prénom', format4)
            worksheet.write('C8:C8', 'Date embauche', format4)
            worksheet.write('D8:D8', 'Date naissance', format4)
            worksheet.write('E8:E8', 'Fonction', format4)
            worksheet.write('F8:F8', 'Département', format4)
            worksheet.write('G8:G8', 'Catégorie Salariale', format4)
            worksheet.write('H8:H8', 'Salaire de base', format4)
            worksheet.write('I8:I8', 'Rappel de salaire', format4)
            worksheet.write('J8:J8', 'Indemnité de logement', format4)
            worksheet.write('K8:k8', 'Indemnité de transport', format4)
            worksheet.write('L8:L8', 'Allocations familiales', format4)
            worksheet.write('M8:M8', "Prime d'expatriation", format4)
            worksheet.write('N8:N8', 'Heures Supplémentaires', format4)
            worksheet.write('O8:O8', "Bons d'essence", format4)
            worksheet.write('P8:P8', 'Prime de représentation', format4)
            worksheet.write('Q8:Q8', 'Prime de supervision', format4)
            worksheet.write('R8:R8', '13 ème mois', format4)
            worksheet.write('S8:S8', 'Elements en plus', format4)
            worksheet.write('T8:T8', 'Salaire brut', format4)
            worksheet.write('U8:U8', 'Elements en moins', format4)
            worksheet.write('V8:V8', 'Retenu de prêt', format4)
            worksheet.write('W8:W8', 'Mutuelle', format4)
            worksheet.write('X8:X8', 'Caisse fin service', format4)
            worksheet.write('Y8:Y8', 'Salaire Net', format4)

            i = 9

            for b in rec.bulletin_line_ids.filtered(lambda re: re.employee_id.matricule).sorted(key=lambda r: r.employee_id.matricule):
                worksheet.set_row(i, 30)
                worksheet.write('A%s:A%s' % (i, i), '%s' % (b.employee_id.matricule), format5)
                worksheet.write('B%s:B%s' % (i, i), '%s %s' % (b.employee_id.prenom, b.employee_id.name), format5)
                worksheet.write('C%s:C%s' % (i, i), '%s' % (b.employee_id.date), format5)
                worksheet.write('D%s:D%s' % (i, i), '%s' % (b.employee_id.birthday), format5)
                worksheet.write('E%s:E%s' % (i, i), '%s' % (b.dh_job_id.name), format5)
                worksheet.write('F%s:F%s' % (i, i), '%s' % (b.dh_department_id.name), format5)
                worksheet.write('G%s:G%s' % (i, i), '%s' % (b.dh_category_id.name), format5)
                worksheet.write('H%s:H%s' % (i, i), '%s' % (b.salaire_base_mois), format5)
                worksheet.write('I%s:I%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Rappel sur salaire').mapped('subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Rappel sur salaire')) > 0 else 0), format5)
                worksheet.write('J%s:J%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de logement').mapped('subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de logement')) > 0 else 0), format5)
                worksheet.write('K%s:k%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de transport').mapped('subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de transport')) > 0 else 0), format5)
                worksheet.write('L%s:L%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Allocations familiales').mapped('subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Allocations familiales')) > 0 else 0), format5)
                worksheet.write('M%s:M%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == "Prime d'expatriation").mapped('subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == "Prime d'expatriation")) > 0 else 0), format5)
                worksheet.write('N%s:N%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: 'Heures Sup' in x.name).mapped('subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: 'Heures Sup' in x.name)) > 0 else 0), format5)
                worksheet.write('O%s:O%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == "Bons d'essence").mapped('subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == "Bons d'essence")) > 0 else 0), format5)
                worksheet.write('P%s:P%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de représentation').mapped('subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de représentation')) > 0 else 0), format5)
                worksheet.write('Q%s:Q%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Prime de supervision').mapped('subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Prime de supervision')) > 0 else 0), format5)
                worksheet.write('R%s:R%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == '13 ieme Mois').mapped('subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == '13 ieme Mois')) > 0 else 0), format5)
                worksheet.write('S%s:S%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_plus', '=', True)]).mapped('name')).mapped('subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_plus', '=', True)]).mapped('name'))) > 0 else 0), format5)
                worksheet.write('T%s:T%s' % (i, i), '%s' % (b.salaire_brute), format5)
                worksheet.write('U%s:U%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_moins', '=', True)]).mapped('name')).mapped('subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_moins', '=', True)]).mapped('name'))) > 0 else 0), format5)
                worksheet.write('V%s:V%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Retenu de Prêt').mapped('subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Retenu de Prêt')) > 0 else 0), format5)
                worksheet.write('W%s:W%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle']).mapped('subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle'])) > 0 else 0), format5)
                worksheet.write('X%s:X%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service']).mapped('subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service'])) > 0 else 0), format5)
                worksheet.write('Y%s:Y%s' % (i, i), '%s' % (b.salaire_net), format5)

                i=i+1

            for b in rec.bulletin_line_ids.filtered(lambda re: not re.employee_id.matricule).sorted(key=lambda r: r.employee_id.matricule):
                worksheet.set_row(i, 30)
                worksheet.write('A%s:A%s' % (i, i), '%s' % (b.employee_id.matricule), format5)
                worksheet.write('B%s:B%s' % (i, i), '%s %s' % (b.employee_id.prenom, b.employee_id.name), format5)
                worksheet.write('C%s:C%s' % (i, i), '%s' % (b.employee_id.date), format5)
                worksheet.write('D%s:D%s' % (i, i), '%s' % (b.employee_id.birthday), format5)
                worksheet.write('E%s:E%s' % (i, i), '%s' % (b.dh_job_id.name), format5)
                worksheet.write('F%s:F%s' % (i, i), '%s' % (b.dh_department_id.name), format5)
                worksheet.write('G%s:G%s' % (i, i), '%s' % (b.employee_id.category_id.name), format5)
                worksheet.write('H%s:H%s' % (i, i), '%s' % (b.salaire_base_mois), format5)
                worksheet.write('I%s:I%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Rappel sur salaire').mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Rappel sur salaire')) > 0 else 0), format5)
                worksheet.write('J%s:J%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de logement').mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de logement')) > 0 else 0), format5)
                worksheet.write('K%s:k%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de transport').mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de transport')) > 0 else 0), format5)
                worksheet.write('L%s:L%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Allocations familiales').mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Allocations familiales')) > 0 else 0), format5)
                worksheet.write('M%s:M%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == "Prime d'expatriation").mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == "Prime d'expatriation")) > 0 else 0), format5)
                worksheet.write('N%s:N%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: 'Heures Sup' in x.name).mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: 'Heures Sup' in x.name)) > 0 else 0), format5)
                worksheet.write('O%s:O%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == "Bons d'essence").mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == "Bons d'essence")) > 0 else 0), format5)
                worksheet.write('P%s:P%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de représentation').mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de représentation')) > 0 else 0),
                                format5)
                worksheet.write('Q%s:Q%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Prime de supervision').mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Prime de supervision')) > 0 else 0), format5)
                worksheet.write('R%s:R%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == '13 ieme Mois').mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == '13 ieme Mois')) > 0 else 0), format5)
                worksheet.write('S%s:S%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_plus', '=', True)]).mapped('name')).mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_plus', '=', True)]).mapped('name'))) > 0 else 0), format5)
                worksheet.write('T%s:T%s' % (i, i), '%s' % (b.salaire_brute), format5)
                worksheet.write('U%s:U%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_moins', '=', True)]).mapped('name')).mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_moins', '=', True)]).mapped('name'))) > 0 else 0), format5)
                worksheet.write('V%s:V%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Retenu de Prêt').mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Retenu de Prêt')) > 0 else 0), format5)
                worksheet.write('W%s:W%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle']).mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle'])) > 0 else 0),
                                format5)
                worksheet.write('X%s:X%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service']).mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service'])) > 0 else 0),
                                format5)
                worksheet.write('Y%s:Y%s' % (i, i), '%s' % (b.salaire_net), format5)

                i=i+1

class JournalPaieByDepartmentXlsx(models.AbstractModel):
    _name = 'report.kzm_payroll_ma.dh_journal_paie_by_department_xlsx'
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
                 'font_color': 'black', 'bg_color': '#E2F0D9',
                 'border': 1, 'border_color': 'black', 'bold': True})
            format41 = workbook.add_format(
                {'font_size': 15, 'align': 'center', 'valign': 'vcenter',
                 'font_color': 'black', 'bg_color': '#C5E0B4',
                 'border': 1, 'border_color': 'black', 'bold': True})
            format42 = workbook.add_format(
                {'font_size': 15, 'align': 'center', 'valign': 'vcenter',
                 'font_color': 'black', 'bg_color': '#F2F2F2',
                 'border': 1, 'border_color': 'black',})
            format5 = workbook.add_format(
                {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
                 'font_color': 'black', 'bg_color': 'white',
                 'border': 1, 'border_color': 'black'})
            format6 = workbook.add_format(
                {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
                 'font_color': '#495057', 'bg_color': 'white',
                 'border': 1, 'border_color': 'black'})

            worksheet.merge_range('A1:Y4', '', format1)
            worksheet.merge_range('A5:Y5', '', format1)
            worksheet.merge_range('A6:Y6', '', format1)
            worksheet.merge_range('A7:Y7', '', format1)
            worksheet.merge_range('A8:Y8', '', format41)

            worksheet.set_row(0, 30)
            worksheet.set_row(1, 30)
            worksheet.set_row(2, 30)
            worksheet.set_row(3, 30)
            worksheet.set_row(4, 30)
            worksheet.set_row(5, 30)
            worksheet.set_row(6, 30)
            worksheet.set_row(7, 30)
            worksheet.set_row(8, 30)
            worksheet.set_row(9, 30)

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

            worksheet.write('A6:Y6', 'Journal de Paie par département', format1)
            worksheet.write('A7:Y7', 'Mois: %s' % (rec.period_id.name), format2)

            worksheet.write('A8:Y8', 'Département', format41)
            worksheet.write('A9:A9', 'Matricules', format4)
            worksheet.write('B9:B9', 'Nom - Prénom', format4)
            worksheet.write('C9:C9', 'Date embauche', format4)
            worksheet.write('D9:D9', 'Date naissance', format4)
            worksheet.write('E9:E9', 'Fonction', format4)
            worksheet.write('F9:F9', 'Département', format4)
            worksheet.write('G9:G9', 'Catégorie Salariale', format4)
            worksheet.write('H9:H9', 'Salaire de base', format4)
            worksheet.write('I9:I9', 'Rappel de salaire', format4)
            worksheet.write('J9:J9', 'Indemnité de logement', format4)
            worksheet.write('K9:k9', 'Indemnité de transport', format4)
            worksheet.write('L9:L9', 'Allocations familiales', format4)
            worksheet.write('M9:M9', "Prime d'expatriation", format4)
            worksheet.write('N9:N9', 'Heures Supplémentaires', format4)
            worksheet.write('O9:O9', "Bons d'essence", format4)
            worksheet.write('P9:P9', 'Prime de représentation', format4)
            worksheet.write('Q9:Q9', 'Prime de supervision', format4)
            worksheet.write('R9:R9', '13 ème mois', format4)
            worksheet.write('S9:S9', 'Elements en plus', format4)
            worksheet.write('T9:T9', 'Salaire brut', format4)
            worksheet.write('U9:U9', 'Elements en moins', format4)
            worksheet.write('V9:V9', 'Retenu de prêt', format4)
            worksheet.write('W9:W9', 'Mutuelle', format4)
            worksheet.write('X9:X9', 'Caisse fin service', format4)
            worksheet.write('Y9:Y9', 'Salaire Net', format4)

            i = 10

            for department in rec.bulletin_line_ids.mapped('employee_id').mapped('department_id'):
                worksheet.set_row(i, 30)
                worksheet.merge_range('A%s:Y%s' % (i, i), '', format42)
                worksheet.write('A%s:Y%s' % (i, i), '%s' % (department.name), format42)
                i = i+1
                for b in rec.bulletin_line_ids.filtered(lambda re: re.employee_id.matricule and re.department_id.id == department.id).sorted(
                        key=lambda r: r.employee_id.matricule):
                    worksheet.set_row(i, 30)
                    worksheet.write('A%s:A%s' % (i, i), '%s' % (b.employee_id.matricule), format5)
                    worksheet.write('B%s:B%s' % (i, i), '%s %s' % (b.employee_id.prenom, b.employee_id.name), format5)
                    worksheet.write('C%s:C%s' % (i, i), '%s' % (b.employee_id.date), format5)
                    worksheet.write('D%s:D%s' % (i, i), '%s' % (b.employee_id.birthday), format5)
                    worksheet.write('E%s:E%s' % (i, i), '%s' % (b.dh_job_id.name), format5)
                    worksheet.write('F%s:F%s' % (i, i), '%s' % (b.dh_department_id.name), format5)
                    worksheet.write('G%s:G%s' % (i, i), '%s' % (b.employee_id.category_id.name), format5)
                    worksheet.write('H%s:H%s' % (i, i), '%s' % (b.salaire_base_mois), format5)
                    worksheet.write('I%s:I%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: x.name == 'Rappel sur salaire').mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: x.name == 'Rappel sur salaire')) > 0 else 0), format5)
                    worksheet.write('J%s:J%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de logement').mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de logement')) > 0 else 0), format5)
                    worksheet.write('K%s:k%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de transport').mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de transport')) > 0 else 0), format5)
                    worksheet.write('L%s:L%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: x.name == 'Allocations familiales').mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: x.name == 'Allocations familiales')) > 0 else 0), format5)
                    worksheet.write('M%s:M%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: x.name == "Prime d'expatriation").mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: x.name == "Prime d'expatriation")) > 0 else 0), format5)
                    worksheet.write('N%s:N%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: 'Heures Sup' in x.name).mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: 'Heures Sup' in x.name)) > 0 else 0), format5)
                    worksheet.write('O%s:O%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: x.name == "Bons d'essence").mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: x.name == "Bons d'essence")) > 0 else 0), format5)
                    worksheet.write('P%s:P%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de représentation').mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de représentation')) > 0 else 0),
                                    format5)
                    worksheet.write('Q%s:Q%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: x.name == 'Prime de supervision').mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: x.name == 'Prime de supervision')) > 0 else 0), format5)
                    worksheet.write('R%s:R%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: x.name == '13 ieme Mois').mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: x.name == '13 ieme Mois')) > 0 else 0), format5)
                    worksheet.write('S%s:S%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_plus', '=', True)]).mapped('name')).mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_plus', '=', True)]).mapped('name'))) > 0 else 0), format5)
                    worksheet.write('T%s:T%s' % (i, i), '%s' % (b.salaire_brute), format5)
                    worksheet.write('U%s:U%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_moins', '=', True)]).mapped('name')).mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_moins', '=', True)]).mapped('name'))) > 0 else 0), format5)
                    worksheet.write('V%s:V%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: x.name == 'Retenu de Prêt').mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: x.name == 'Retenu de Prêt')) > 0 else 0), format5)
                    worksheet.write('W%s:W%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle']).mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle'])) > 0 else 0),
                                    format5)
                    worksheet.write('X%s:X%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service']).mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service'])) > 0 else 0),
                                    format5)
                    worksheet.write('Y%s:Y%s' % (i, i), '%s' % (b.salaire_net), format5)

                    i = i + 1

                for b in rec.bulletin_line_ids.filtered(lambda re: not re.employee_id.matricule and re.department_id.id == department.id).sorted(
                        key=lambda r: r.employee_id.matricule):
                    worksheet.set_row(i, 30)
                    worksheet.write('A%s:A%s' % (i, i), '%s' % (b.employee_id.matricule), format5)
                    worksheet.write('B%s:B%s' % (i, i), '%s %s' % (b.employee_id.prenom, b.employee_id.name), format5)
                    worksheet.write('C%s:C%s' % (i, i), '%s' % (b.employee_id.date), format5)
                    worksheet.write('D%s:D%s' % (i, i), '%s' % (b.employee_id.birthday), format5)
                    worksheet.write('E%s:E%s' % (i, i), '%s' % (b.dh_job_id.name), format5)
                    worksheet.write('F%s:F%s' % (i, i), '%s' % (b.dh_department_id.name), format5)
                    worksheet.write('G%s:G%s' % (i, i), '%s' % (b.employee_id.category_id.name), format5)
                    worksheet.write('H%s:H%s' % (i, i), '%s' % (b.salaire_base_mois), format5)
                    worksheet.write('I%s:I%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: x.name == 'Rappel sur salaire').mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: x.name == 'Rappel sur salaire')) > 0 else 0), format5)
                    worksheet.write('J%s:J%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de logement').mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de logement')) > 0 else 0), format5)
                    worksheet.write('K%s:k%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de transport').mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de transport')) > 0 else 0), format5)
                    worksheet.write('L%s:L%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: x.name == 'Allocations familiales').mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: x.name == 'Allocations familiales')) > 0 else 0), format5)
                    worksheet.write('M%s:M%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: x.name == "Prime d'expatriation").mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: x.name == "Prime d'expatriation")) > 0 else 0), format5)
                    worksheet.write('N%s:N%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: 'Heures Sup' in x.name).mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: 'Heures Sup' in x.name)) > 0 else 0), format5)
                    worksheet.write('O%s:O%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: x.name == "Bons d'essence").mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: x.name == "Bons d'essence")) > 0 else 0), format5)
                    worksheet.write('P%s:P%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de représentation').mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de représentation')) > 0 else 0),
                                    format5)
                    worksheet.write('Q%s:Q%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: x.name == 'Prime de supervision').mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: x.name == 'Prime de supervision')) > 0 else 0), format5)
                    worksheet.write('R%s:R%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: x.name == '13 ieme Mois').mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: x.name == '13 ieme Mois')) > 0 else 0), format5)
                    worksheet.write('S%s:S%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_plus', '=', True)]).mapped('name')).mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_plus', '=', True)]).mapped('name'))) > 0 else 0), format5)
                    worksheet.write('T%s:T%s' % (i, i), '%s' % (b.salaire_brute), format5)
                    worksheet.write('U%s:U%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_moins', '=', True)]).mapped('name')).mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_moins', '=', True)]).mapped('name'))) > 0 else 0), format5)
                    worksheet.write('V%s:V%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: x.name == 'Retenu de Prêt').mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: x.name == 'Retenu de Prêt')) > 0 else 0), format5)
                    worksheet.write('W%s:W%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle']).mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle'])) > 0 else 0),
                                    format5)
                    worksheet.write('X%s:X%s' % (i, i), '%s' % (
                        sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service']).mapped(
                            'subtotal_employee')) if len(
                            b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service'])) > 0 else 0),
                                    format5)
                    worksheet.write('Y%s:Y%s' % (i, i), '%s' % (b.salaire_net), format5)

                    i = i + 1

class DhJournalPaieBulletinXlsx(models.AbstractModel):
    _name = 'report.kzm_payroll_ma.dh_journal_department_xlsx'
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

        worksheet.merge_range('A1:Y4', '', format1)
        worksheet.merge_range('A5:Y5', '', format1)
        worksheet.merge_range('A6:Y6', '', format1)
        worksheet.merge_range('A7:Y7', '', format1)

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

        worksheet.write('A6:Y6', 'Journal de Paie', format1)


        worksheet.write('A8:A8', 'Matricules', format4)
        worksheet.write('B8:B8', 'Nom - Prénom', format4)
        worksheet.write('C8:C8', 'Date embauche', format4)
        worksheet.write('D8:D8', 'Date naissance', format4)
        worksheet.write('E8:E8', 'Fonction', format4)
        worksheet.write('F8:F8', 'Département', format4)
        worksheet.write('G8:G8', 'Catégorie Salariale', format4)
        worksheet.write('H8:H8', 'Salaire de base', format4)
        worksheet.write('I8:I8', 'Rappel de salaire', format4)
        worksheet.write('J8:J8', 'Indemnité de logement', format4)
        worksheet.write('K8:k8', 'Indemnité de transport', format4)
        worksheet.write('L8:L8', 'Allocations familiales', format4)
        worksheet.write('M8:M8', "Prime d'expatriation", format4)
        worksheet.write('N8:N8', 'Heures Supplémentaires', format4)
        worksheet.write('O8:O8', "Bons d'essence", format4)
        worksheet.write('P8:P8', 'Prime de représentation', format4)
        worksheet.write('Q8:Q8', 'Prime de supervision', format4)
        worksheet.write('R8:R8', '13 ème mois', format4)
        worksheet.write('S8:S8', 'Elements en plus', format4)
        worksheet.write('T8:T8', 'Salaire brut', format4)
        worksheet.write('U8:U8', 'Elements en moins', format4)
        worksheet.write('V8:V8', 'Retenu de prêt', format4)
        worksheet.write('W8:W8', 'Mutuelle', format4)
        worksheet.write('X8:X8', 'Caisse fin service', format4)
        worksheet.write('Y8:Y8', 'Salaire Net', format4)

        i = 9

        for b in datas.filtered(lambda re: re.employee_id.matricule).sorted(key=lambda r: r.employee_id.matricule):
            worksheet.set_row(i, 30)
            worksheet.write('A%s:A%s' % (i, i), '%s' % (b.employee_id.matricule), format5)
            worksheet.write('B%s:B%s' % (i, i), '%s %s' % (b.employee_id.prenom, b.employee_id.name), format5)
            worksheet.write('C%s:C%s' % (i, i), '%s' % (b.employee_id.date), format5)
            worksheet.write('D%s:D%s' % (i, i), '%s' % (b.employee_id.birthday), format5)
            worksheet.write('E%s:E%s' % (i, i), '%s' % (b.employee_id.job_id.name), format5)
            worksheet.write('F%s:F%s' % (i, i), '%s' % (b.employee_id.department_id.name), format5)
            worksheet.write('G%s:G%s' % (i, i), '%s' % (b.employee_id.category_id.name), format5)
            worksheet.write('H%s:H%s' % (i, i), '%s' % (b.salaire_base_mois), format5)
            worksheet.write('I%s:I%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name == 'Rappel sur salaire').mapped('subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name == 'Rappel sur salaire')) > 0 else 0), format5)
            worksheet.write('J%s:J%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de logement').mapped('subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de logement')) > 0 else 0), format5)
            worksheet.write('K%s:k%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de transport').mapped('subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de transport')) > 0 else 0), format5)
            worksheet.write('L%s:L%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name == 'Allocations familiales').mapped('subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name == 'Allocations familiales')) > 0 else 0), format5)
            worksheet.write('M%s:M%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name == "Prime d'expatriation").mapped('subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name == "Prime d'expatriation")) > 0 else 0), format5)
            worksheet.write('N%s:N%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: 'Heures Sup' in x.name).mapped('subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: 'Heures Sup' in x.name)) > 0 else 0), format5)
            worksheet.write('O%s:O%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name == "Bons d'essence").mapped('subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name == "Bons d'essence")) > 0 else 0), format5)
            worksheet.write('P%s:P%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de représentation').mapped('subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de représentation')) > 0 else 0), format5)
            worksheet.write('Q%s:Q%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name == 'Prime de supervision').mapped('subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name == 'Prime de supervision')) > 0 else 0), format5)
            worksheet.write('R%s:R%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name == '13 ieme Mois').mapped('subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name == '13 ieme Mois')) > 0 else 0), format5)
            worksheet.write('S%s:S%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_plus', '=', True)]).mapped('name')).mapped('subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_plus', '=', True)]).mapped('name'))) > 0 else 0), format5)
            worksheet.write('T%s:T%s' % (i, i), '%s' % (b.salaire_brute), format5)
            worksheet.write('U%s:U%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_moins', '=', True)]).mapped('name')).mapped('subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_moins', '=', True)]).mapped('name'))) > 0 else 0), format5)
            worksheet.write('V%s:V%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name == 'Retenu de Prêt').mapped('subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name == 'Retenu de Prêt')) > 0 else 0), format5)
            worksheet.write('W%s:W%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle']).mapped('subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle'])) > 0 else 0), format5)
            worksheet.write('X%s:X%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service']).mapped('subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service'])) > 0 else 0), format5)
            worksheet.write('Y%s:Y%s' % (i, i), '%s' % (b.salaire_net), format5)

            i=i+1

        for b in datas.filtered(lambda re: not re.employee_id.matricule).sorted(key=lambda r: r.employee_id.matricule):
            worksheet.set_row(i, 30)
            worksheet.write('A%s:A%s' % (i, i), '%s' % (b.employee_id.matricule), format5)
            worksheet.write('B%s:B%s' % (i, i), '%s %s' % (b.employee_id.prenom, b.employee_id.name), format5)
            worksheet.write('C%s:C%s' % (i, i), '%s' % (b.employee_id.date), format5)
            worksheet.write('D%s:D%s' % (i, i), '%s' % (b.employee_id.birthday), format5)
            worksheet.write('E%s:E%s' % (i, i), '%s' % (b.employee_id.job_id.name), format5)
            worksheet.write('F%s:F%s' % (i, i), '%s' % (b.employee_id.department_id.name), format5)
            worksheet.write('G%s:G%s' % (i, i), '%s' % (b.employee_id.category_id.name), format5)
            worksheet.write('H%s:H%s' % (i, i), '%s' % (b.salaire_base_mois), format5)
            worksheet.write('I%s:I%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name == 'Rappel sur salaire').mapped(
                    'subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name == 'Rappel sur salaire')) > 0 else 0), format5)
            worksheet.write('J%s:J%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de logement').mapped(
                    'subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de logement')) > 0 else 0), format5)
            worksheet.write('K%s:k%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de transport').mapped(
                    'subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de transport')) > 0 else 0), format5)
            worksheet.write('L%s:L%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name == 'Allocations familiales').mapped(
                    'subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name == 'Allocations familiales')) > 0 else 0), format5)
            worksheet.write('M%s:M%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name == "Prime d'expatriation").mapped(
                    'subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name == "Prime d'expatriation")) > 0 else 0), format5)
            worksheet.write('N%s:N%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: 'Heures Sup' in x.name).mapped(
                    'subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: 'Heures Sup' in x.name)) > 0 else 0), format5)
            worksheet.write('O%s:O%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name == "Bons d'essence").mapped(
                    'subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name == "Bons d'essence")) > 0 else 0), format5)
            worksheet.write('P%s:P%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de représentation').mapped(
                    'subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de représentation')) > 0 else 0),
                            format5)
            worksheet.write('Q%s:Q%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name == 'Prime de supervision').mapped(
                    'subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name == 'Prime de supervision')) > 0 else 0), format5)
            worksheet.write('R%s:R%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name == '13 ieme Mois').mapped(
                    'subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name == '13 ieme Mois')) > 0 else 0), format5)
            worksheet.write('S%s:S%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_plus', '=', True)]).mapped('name')).mapped(
                    'subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_plus', '=', True)]).mapped('name'))) > 0 else 0), format5)
            worksheet.write('T%s:T%s' % (i, i), '%s' % (b.salaire_brute), format5)
            worksheet.write('U%s:U%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_moins', '=', True)]).mapped('name')).mapped(
                    'subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_moins', '=', True)]).mapped('name'))) > 0 else 0), format5)
            worksheet.write('V%s:V%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name == 'Retenu de Prêt').mapped(
                    'subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name == 'Retenu de Prêt')) > 0 else 0), format5)
            worksheet.write('W%s:W%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle']).mapped(
                    'subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle'])) > 0 else 0),
                            format5)
            worksheet.write('X%s:X%s' % (i, i), '%s' % (
                sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service']).mapped(
                    'subtotal_employee')) if len(
                    b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service'])) > 0 else 0),
                            format5)
            worksheet.write('Y%s:Y%s' % (i, i), '%s' % (b.salaire_net), format5)

            i=i+1

class JournalPaieBUlletinByDepartmentXlsx(models.AbstractModel):
    _name = 'report.kzm_payroll_ma.dh_journal_bulletin_department_xlsx'
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
            {'font_size': 22, 'align': 'center', 'valign': 'vcenter',
             'font_color': '#495057', 'bg_color': 'white', 'bold': True})
        format2 = workbook.add_format(
            {'font_size': 18, 'align': 'center', 'valign': 'vcenter',
             'font_color': '#495057', 'bold': True, 'bg_color': 'white',
             'underline': True})
        format4 = workbook.add_format(
            {'font_size': 15, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'black', 'bg_color': '#E2F0D9',
             'border': 1, 'border_color': 'black', 'bold': True})
        format41 = workbook.add_format(
            {'font_size': 15, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'black', 'bg_color': '#C5E0B4',
             'border': 1, 'border_color': 'black', 'bold': True})
        format42 = workbook.add_format(
            {'font_size': 15, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'black', 'bg_color': '#F2F2F2',
             'border': 1, 'border_color': 'black',})
        format5 = workbook.add_format(
            {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'black', 'bg_color': 'white',
             'border': 1, 'border_color': 'black'})
        format6 = workbook.add_format(
            {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
             'font_color': '#495057', 'bg_color': 'white',
             'border': 1, 'border_color': 'black'})

        worksheet.merge_range('A1:Y4', '', format1)
        worksheet.merge_range('A5:Y5', '', format1)
        worksheet.merge_range('A6:Y6', '', format1)
        worksheet.merge_range('A7:Y7', '', format1)
        worksheet.merge_range('A8:Y8', '', format41)

        worksheet.set_row(0, 30)
        worksheet.set_row(1, 30)
        worksheet.set_row(2, 30)
        worksheet.set_row(3, 30)
        worksheet.set_row(4, 30)
        worksheet.set_row(5, 30)
        worksheet.set_row(6, 30)
        worksheet.set_row(7, 30)
        worksheet.set_row(8, 30)
        worksheet.set_row(9, 30)

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

        worksheet.write('A6:Y6', 'Journal de Paie par département', format1)

        worksheet.write('A8:Y8', 'Département', format41)
        worksheet.write('A9:A9', 'Matricules', format4)
        worksheet.write('B9:B9', 'Nom - Prénom', format4)
        worksheet.write('C9:C9', 'Date embauche', format4)
        worksheet.write('D9:D9', 'Date naissance', format4)
        worksheet.write('E9:E9', 'Fonction', format4)
        worksheet.write('F9:F9', 'Département', format4)
        worksheet.write('G9:G9', 'Catégorie Salariale', format4)
        worksheet.write('H9:H9', 'Salaire de base', format4)
        worksheet.write('I9:I9', 'Rappel de salaire', format4)
        worksheet.write('J9:J9', 'Indemnité de logement', format4)
        worksheet.write('K9:k9', 'Indemnité de transport', format4)
        worksheet.write('L9:L9', 'Allocations familiales', format4)
        worksheet.write('M9:M9', "Prime d'expatriation", format4)
        worksheet.write('N9:N9', 'Heures Supplémentaires', format4)
        worksheet.write('O9:O9', "Bons d'essence", format4)
        worksheet.write('P9:P9', 'Prime de représentation', format4)
        worksheet.write('Q9:Q9', 'Prime de supervision', format4)
        worksheet.write('R9:R9', '13 ème mois', format4)
        worksheet.write('S9:S9', 'Elements en plus', format4)
        worksheet.write('T9:T9', 'Salaire brut', format4)
        worksheet.write('U9:U9', 'Elements en moins', format4)
        worksheet.write('V9:V9', 'Retenu de prêt', format4)
        worksheet.write('W9:W9', 'Mutuelle', format4)
        worksheet.write('X9:X9', 'Caisse fin service', format4)
        worksheet.write('Y9:Y9', 'Salaire Net', format4)

        i = 10

        for department in datas.mapped('employee_id').mapped('department_id'):
            worksheet.set_row(i, 30)
            worksheet.merge_range('A%s:Y%s' % (i, i), '', format42)
            worksheet.write('A%s:Y%s' % (i, i), '%s' % (department.name), format42)
            i = i+1
            for b in datas.filtered(lambda re: re.employee_id.matricule and re.department_id.id == department.id).sorted(
                    key=lambda r: r.employee_id.matricule):
                worksheet.set_row(i, 30)
                worksheet.write('A%s:A%s' % (i, i), '%s' % (b.employee_id.matricule), format5)
                worksheet.write('B%s:B%s' % (i, i), '%s %s' % (b.employee_id.prenom, b.employee_id.name), format5)
                worksheet.write('C%s:C%s' % (i, i), '%s' % (b.employee_id.date), format5)
                worksheet.write('D%s:D%s' % (i, i), '%s' % (b.employee_id.birthday), format5)
                worksheet.write('E%s:E%s' % (i, i), '%s' % (b.employee_id.job_id.name), format5)
                worksheet.write('F%s:F%s' % (i, i), '%s' % (b.employee_id.department_id.name), format5)
                worksheet.write('G%s:G%s' % (i, i), '%s' % (b.employee_id.category_id.name), format5)
                worksheet.write('H%s:H%s' % (i, i), '%s' % (b.salaire_base_mois), format5)
                worksheet.write('I%s:I%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Rappel sur salaire').mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Rappel sur salaire')) > 0 else 0), format5)
                worksheet.write('J%s:J%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de logement').mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de logement')) > 0 else 0), format5)
                worksheet.write('K%s:k%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de transport').mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de transport')) > 0 else 0), format5)
                worksheet.write('L%s:L%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Allocations familiales').mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Allocations familiales')) > 0 else 0), format5)
                worksheet.write('M%s:M%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == "Prime d'expatriation").mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == "Prime d'expatriation")) > 0 else 0), format5)
                worksheet.write('N%s:N%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: 'Heures Sup' in x.name).mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: 'Heures Sup' in x.name)) > 0 else 0), format5)
                worksheet.write('O%s:O%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == "Bons d'essence").mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == "Bons d'essence")) > 0 else 0), format5)
                worksheet.write('P%s:P%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de représentation').mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de représentation')) > 0 else 0),
                                format5)
                worksheet.write('Q%s:Q%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Prime de supervision').mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Prime de supervision')) > 0 else 0), format5)
                worksheet.write('R%s:R%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == '13 ieme Mois').mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == '13 ieme Mois')) > 0 else 0), format5)
                worksheet.write('S%s:S%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_plus', '=', True)]).mapped('name')).mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_plus', '=', True)]).mapped('name'))) > 0 else 0), format5)
                worksheet.write('T%s:T%s' % (i, i), '%s' % (b.salaire_brute), format5)
                worksheet.write('U%s:U%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_moins', '=', True)]).mapped('name')).mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_moins', '=', True)]).mapped('name'))) > 0 else 0), format5)
                worksheet.write('V%s:V%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Retenu de Prêt').mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Retenu de Prêt')) > 0 else 0), format5)
                worksheet.write('W%s:W%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle']).mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle'])) > 0 else 0),
                                format5)
                worksheet.write('X%s:X%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service']).mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service'])) > 0 else 0),
                                format5)
                worksheet.write('Y%s:Y%s' % (i, i), '%s' % (b.salaire_net), format5)

                i = i + 1

            for b in datas.filtered(lambda re: not re.employee_id.matricule and re.department_id.id == department.id).sorted(
                    key=lambda r: r.employee_id.matricule):
                worksheet.set_row(i, 30)
                worksheet.write('A%s:A%s' % (i, i), '%s' % (b.employee_id.matricule), format5)
                worksheet.write('B%s:B%s' % (i, i), '%s %s' % (b.employee_id.prenom, b.employee_id.name), format5)
                worksheet.write('C%s:C%s' % (i, i), '%s' % (b.employee_id.date), format5)
                worksheet.write('D%s:D%s' % (i, i), '%s' % (b.employee_id.birthday), format5)
                worksheet.write('E%s:E%s' % (i, i), '%s' % (b.employee_id.job_id.name), format5)
                worksheet.write('F%s:F%s' % (i, i), '%s' % (b.employee_id.department_id.name), format5)
                worksheet.write('G%s:G%s' % (i, i), '%s' % (b.employee_id.category_id.name), format5)
                worksheet.write('H%s:H%s' % (i, i), '%s' % (b.salaire_base_mois), format5)
                worksheet.write('I%s:I%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Rappel sur salaire').mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Rappel sur salaire')) > 0 else 0), format5)
                worksheet.write('J%s:J%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de logement').mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de logement')) > 0 else 0), format5)
                worksheet.write('K%s:k%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de transport').mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de transport')) > 0 else 0), format5)
                worksheet.write('L%s:L%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Allocations familiales').mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Allocations familiales')) > 0 else 0), format5)
                worksheet.write('M%s:M%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == "Prime d'expatriation").mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == "Prime d'expatriation")) > 0 else 0), format5)
                worksheet.write('N%s:N%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: 'Heures Sup' in x.name).mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: 'Heures Sup' in x.name)) > 0 else 0), format5)
                worksheet.write('O%s:O%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == "Bons d'essence").mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == "Bons d'essence")) > 0 else 0), format5)
                worksheet.write('P%s:P%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de représentation').mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Indemnité de représentation')) > 0 else 0),
                                format5)
                worksheet.write('Q%s:Q%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Prime de supervision').mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Prime de supervision')) > 0 else 0), format5)
                worksheet.write('R%s:R%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == '13 ieme Mois').mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == '13 ieme Mois')) > 0 else 0), format5)
                worksheet.write('S%s:S%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_plus', '=', True)]).mapped('name')).mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_plus', '=', True)]).mapped('name'))) > 0 else 0), format5)
                worksheet.write('T%s:T%s' % (i, i), '%s' % (b.salaire_brute), format5)
                worksheet.write('U%s:U%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_moins', '=', True)]).mapped('name')).mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name in self.env['hr.payroll_ma.rubrique'].search([('element_moins', '=', True)]).mapped('name'))) > 0 else 0), format5)
                worksheet.write('V%s:V%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name == 'Retenu de Prêt').mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name == 'Retenu de Prêt')) > 0 else 0), format5)
                worksheet.write('W%s:W%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle']).mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle'])) > 0 else 0),
                                format5)
                worksheet.write('X%s:X%s' % (i, i), '%s' % (
                    sum(b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service']).mapped(
                        'subtotal_employee')) if len(
                        b.salary_line_ids.filtered(lambda x: x.name in ['Indemnité Mutuelle/Fin service', 'Caisse fin service'])) > 0 else 0),
                                format5)
                worksheet.write('Y%s:Y%s' % (i, i), '%s' % (b.salaire_net), format5)

                i = i + 1
