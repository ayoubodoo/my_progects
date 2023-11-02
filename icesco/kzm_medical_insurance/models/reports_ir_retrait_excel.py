import datetime as dt
import locale
import time
from datetime import timedelta, datetime
from odoo import models,fields
import base64
import io
from io import BytesIO



class IrRetraitXlsx(models.AbstractModel):
    _name = 'report.kzm_medical_insurance.report_ir_retrait_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, datas):
        locale.setlocale(locale.LC_ALL,
                         'fr_FR.UTF-8')
        report_name_retraite = 'RETRAITE'
        worksheet1 = workbook.add_worksheet(report_name_retraite)
        format0 = workbook.add_format(
            {'font_size': 8, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'black', 'bg_color': '#E6E0Ec',})
        format10 = workbook.add_format(
            {'font_size': 7.5, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'black', 'bg_color': '#E6E0Ec', 'bold': True})
        format1 = workbook.add_format(
            {'font_size': 32, 'align': 'center', 'valign': 'vcenter',
             'font_color': '#495057', 'bg_color': 'white', 'bold': True})
        format11 = workbook.add_format(
            {'font_size': 18, 'align': 'left', 'valign': 'vcenter',
             'font_color': '#495057', 'bg_color': 'white', 'bold': True})
        format2 = workbook.add_format(
            {'font_size': 13, 'align': 'center', 'valign': 'vcenter',
             'font_color': '#495057', 'bold': True, 'bg_color': 'white',
             'underline': True})
        format4 = workbook.add_format(
            {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'black', 'bg_color': '#E6E0Ec',
             'border': 1, 'border_color': 'black', 'bold': True})
        format5 = workbook.add_format(
            {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'black', 'bg_color': 'white',
             'border': 1, 'border_color': 'black'})
        format6 = workbook.add_format(
            {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
             'font_color': '#495057', 'bg_color': 'white',
             'border': 1, 'border_color': 'black'})

        worksheet1.set_row(0, 30)
        worksheet1.set_row(1, 30)
        worksheet1.set_row(2, 30)
        worksheet1.set_row(3, 30)
        worksheet1.set_row(4, 30)
        worksheet1.set_row(5, 30)
        worksheet1.set_row(6, 30)
        worksheet1.set_row(7, 30)
        worksheet1.set_row(8, 30)
        worksheet1.set_row(9, 30)
        worksheet1.set_row(10, 30)

        worksheet1.set_column('A:A', 40)
        worksheet1.set_column('B:B', 20)
        worksheet1.set_column('C:C', 20)
        worksheet1.set_column('D:D', 20)
        worksheet1.set_column('E:E', 20)
        worksheet1.set_column('F:F', 20)
        worksheet1.set_column('G:G', 20)
        worksheet1.set_column('H:H', 20)
        worksheet1.set_column('I:I', 20)
        worksheet1.set_column('J:J', 20)
        worksheet1.set_column('K:K', 20)
        worksheet1.set_column('L:L', 20)
        worksheet1.set_column('M:M', 20)
        worksheet1.set_column('N:N', 20)
        worksheet1.set_column('O:O', 20)
        worksheet1.set_column('P:P', 20)
        worksheet1.set_column('Q:Q', 20)
        worksheet1.set_column('R:R', 20)
        worksheet1.set_column('S:S', 20)
        worksheet1.set_column('T:T', 20)
        worksheet1.set_column('U:U', 20)
        worksheet1.set_column('V:V', 20)
        worksheet1.set_column('W:W', 20)
        worksheet1.set_column('X:X', 20)
        worksheet1.set_column('Y:Y', 20)
        worksheet1.set_column('Z:Z', 20)
        worksheet1.set_column('AA:AA', 20)
        worksheet1.set_column('AB:AB', 20)
        worksheet1.set_column('AC:AC', 20)
        worksheet1.set_column('AD:AD', 20)
        worksheet1.set_column('AE:AE', 20)
        worksheet1.set_column('AF:AF', 20)
        worksheet1.set_column('AG:AG', 20)
        worksheet1.set_column('AH:AH', 20)
        worksheet1.set_column('AI:AI', 20)
        worksheet1.set_column('AJ:AJ', 20)
        worksheet1.set_column('AK:AK', 20)
        worksheet1.set_column('AL:AL', 20)
        worksheet1.set_column('AM:AM', 20)


        worksheet1.merge_range('A2:AK8', '', format1)
        worksheet1.write('A2:AK8', " Cotisations des employés de l'ICESCO à la caisse mutuelle (%s)" % (datas.annee), format1)




        worksheet1.write('A9:A9', "", format1)
        worksheet1.write('A10:A10', "Nom de l'employée", format4)
        worksheet1.merge_range('B9:D9', "Janvier", format4)
        worksheet1.write('B10:B10', "COT Salariale", format0)
        worksheet1.write('C10:C10', "COT patronale", format0)
        worksheet1.write('D10:D10', "COT(S+P)", format0)
        worksheet1.merge_range('E9:G9', 'FEVRIER', format4)
        worksheet1.write('E10:E10', "COT Salariale", format0)
        worksheet1.write('F10:F10', "COT patronale", format0)
        worksheet1.write('G10:G10', "COT(S+P)", format0)


        worksheet1.merge_range('H9:J9', "MARS", format4)
        worksheet1.write('H10:H10', "COT Salariale", format0)
        worksheet1.write('I10:I10', "COT patronale", format0)
        worksheet1.write('J10:J10', "COT(S+P)", format0)
        worksheet1.merge_range('K9:M9', 'AVRIL', format4)
        worksheet1.write('K10:K10', "COT Salariale", format0)
        worksheet1.write('L10:L10', "COT patronale", format0)
        worksheet1.write('M10:M10', "COT(S+P)", format0)
        worksheet1.merge_range('N9:P9', 'MAI', format4)
        worksheet1.write('N10:N10', "COT Salariale", format0)
        worksheet1.write('O10:O10', "COT patronale", format0)
        worksheet1.write('P10:P10', "COT(S+P)", format0)
        worksheet1.merge_range('Q9:S9', 'JUIN', format4)
        worksheet1.write('Q10:Q10', "COT Salariale", format0)
        worksheet1.write('R10:R10', "COT patronale", format0)
        worksheet1.write('S10:S10', "COT(S+P)", format0)
        worksheet1.merge_range('T9:V9', 'JUIELLET', format4)
        worksheet1.write('T10:T10', "COT Salariale", format0)
        worksheet1.write('U10:U10', "COT patronale", format0)
        worksheet1.write('V10:V10', "COT(S+P)", format0)
        worksheet1.merge_range('W9:Y9', 'AOUT', format4)
        worksheet1.write('W10:W10', "COT Salariale", format0)
        worksheet1.write('X10:X10', "COT patronale", format0)
        worksheet1.write('Y10:Y10', "COT(S+P)", format0)
        worksheet1.merge_range('Z9:AB9', 'SEPTEMBRE', format4)
        worksheet1.write('Z10:Z10', "COT Salariale", format0)
        worksheet1.write('AA10:AA10', "COT patronale", format0)
        worksheet1.write('AB10:AB10', "COT(S+P)", format0)
        worksheet1.merge_range('AC9:AE9', 'OCTOBRE', format4)
        worksheet1.write('AC10:AC10', "COT Salariale", format0)
        worksheet1.write('AD10:AD10', "COT patronale", format0)
        worksheet1.write('AE10:AE10', "COT(S+P)", format0)
        worksheet1.merge_range('AF9:AH9', 'NOVEMBRE', format4)
        worksheet1.write('AF10:AF10', "COT Salariale", format0)
        worksheet1.write('AG10:AG10', "COT patronale", format0)
        worksheet1.write('AH10:AH10', "COT(S+P)", format0)
        worksheet1.merge_range('AI9:AK9', 'DECEMBRE', format4)
        worksheet1.write('AI10:AI10', "COT Salariale", format0)
        worksheet1.write('AJ10:AJ10', "COT patronale", format0)
        worksheet1.write('AK10:AK10', "COT(S+P)", format0)
        worksheet1.write('AL10:AL10', "Total général COT(S+P)", format10)
        worksheet1.write('AM10:AM10', "Montant de remboursement (Annuel)", format10)

        list_month  = ['01','02','03','04','05','06','07','08','09','10','11','12']
        list_employee  = []

        # for month in list_month:
        #     for b in self.env['hr.payroll_ma.bulletin'].search([]):



        i = 11

        for employee in self.env['hr.payroll_ma.bulletin'].search([]).filtered(
                lambda x: x.period_id.date_start.strftime('%Y') == datas.annee and x.period_id.date_end.strftime('%Y') ==  datas.annee).mapped('employee_id'):
            # list_employee.append(b.employee_id)

            worksheet1.set_row(i, 30)
            worksheet1.write('A%s:A%s' % (i, i),
                             '%s' % (employee.display_name if employee.display_name else ''),
                             format5)
            i = i + 1

        worksheet1.set_row(i, 30)
        worksheet1.write('A%s:A%s' % (i, i),
                         'TOTAL',
                         format4)

        i = 10
        j = 1

        for month in list_month:
            sum_cotisation_month = 0
            i = 10
            period_id = self.env['date.range'].search([]).filtered(lambda x:x.date_start.strftime('%m') == month and x.date_start.strftime('%Y') == datas.annee and x.type_id.fiscal_period == True)
            if len(period_id) > 0:
                for employee in self.env['hr.payroll_ma.bulletin'].search([]).filtered(
                        lambda x: x.period_id.date_start.strftime(
                            '%Y') == datas.annee and x.period_id.date_end.strftime('%Y') == datas.annee).mapped(
                    'employee_id'):
                    b = self.env['hr.payroll_ma.bulletin'].search([('employee_id', '=', employee.id), ('period_id', '=', period_id.id)])
                    cot_employee = sum(b.salary_line_ids.filtered(
                            lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle']).mapped(
                            'subtotal_employee'))
                    cot_employeur = sum(b.salary_line_ids.filtered(
                            lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle']).mapped(
                            'subtotal_employer'))
                    worksheet1.write(i, j, '%.2f' % (cot_employee if cot_employee > 0 else 0),
                                    format5)
                    worksheet1.write(i, j+1, '%.2f' % (cot_employeur if cot_employeur > 0 else 0),
                                    format5)

                    worksheet1.write(i, j + 2, '%.2f' % (cot_employee+cot_employeur),
                                     format5)

                    i = i + 1

                    sum_cotisation_month += cot_employee+cot_employeur

                worksheet1.merge_range(i, j, i, j + 2, '', format1)
                worksheet1.write(i, j, '%.2f' % (sum_cotisation_month),
                                 format5)

            j = j + 3

        i = 10
        sum_cotisation_general = 0
        for employee in self.env['hr.payroll_ma.bulletin'].search([]).filtered(
                lambda x: x.period_id.date_start.strftime(
                    '%Y') == datas.annee and x.period_id.date_end.strftime('%Y') == datas.annee).mapped('employee_id'):

            b = self.env['hr.payroll_ma.bulletin'].search(
                [('employee_id', '=', employee.id)]).filtered(
                lambda x: x.period_id.date_start.strftime(
                    '%Y') == datas.annee and x.period_id.date_end.strftime('%Y') == datas.annee)
            cot_employee = sum(b.mapped('salary_line_ids').filtered(
                lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle']).mapped(
                'subtotal_employee'))
            cot_employeur = sum(b.mapped('salary_line_ids').filtered(
                lambda x: x.name in ['Indemnité Mutuelle/Fin contrat', 'Mutuelle']).mapped(
                'subtotal_employer'))

            worksheet1.write(i, j, '%.2f' % (cot_employee + cot_employeur),
                             format5)

            i = i + 1

            sum_cotisation_general += cot_employee + cot_employeur

        worksheet1.write(i, j, '%.2f' % (sum_cotisation_general),
                         format5)

        j = j + 1
        i = 10
        remb_general = 0
        for employee in self.env['hr.payroll_ma.bulletin'].search([]).filtered(
                lambda x: x.period_id.date_start.strftime(
                    '%Y') == datas.annee and x.period_id.date_end.strftime('%Y') == datas.annee).mapped('employee_id'):

            r = self.env['medical.refund.request'].search(
                [('employee_id', '=', employee.id)]).filtered(
                lambda x: x.date.strftime(
                    '%Y') == datas.annee)
            remb = sum(r.mapped('total_to_refund'))

            worksheet1.write(i, j, '%.2f' % (remb),
                             format5)

            i = i + 1

            remb_general += remb

        worksheet1.write(i, j, '%.2f' % (remb_general),
                         format5)


        # for employee in list_employee:
        #     worksheet1.set_row(i, 40)
        #     worksheet1.write('A%s:A%s' % (i, i),
        #                          '%.2f' % (employee.display_name if employee.display_name else ''),
        #                          format5)
        #     i = i + 1





        #     print( 'lambda5',b.line_ids.filtered(lambda x: x.code == 'AMOE '))
        #     worksheet1.set_row(i, 40)
        #     worksheet1.write('A%s:A%s' % (i, i),
        #                      '%.2f' % (b.employee_id.n_inscription if b.employee_id.n_inscription else ''),
        #                      format5)
        #     worksheet1.write('B%s:B%s' % (i, i),
        #                      '%.2f' % (b.employee_id.x_studio_matricule if b.employee_id.x_studio_matricule != False else ''), format5)
        #     worksheet1.write('C%s:C%s' % (i, i), '%.2f' % (b.employee_id.department_id.name if b.employee_id.department_id.name  else ''),
        #                      format5)
        #     worksheet1.write('D%s:D%s' % (i, i),
        #                      '%.2f' % (b.employee_id.display_name if b.employee_id.id != False else ''), format5)
        #     worksheet1.write('E%s:E%s' % (i, i),
        #                      '%.2f' % (''), format5)
        #     worksheet1.write('F%s:F%s' % (i, i), '%.2f' % (
        #         sum(b.line_ids.filtered(lambda x: x.code == 'BRUT').mapped('total')) if len(
        #             b.line_ids.filtered(lambda x: x.code == 'BRUT')) > 0 else 0), format5)
        #     worksheet1.write('G%s:G%s' % (i, i), '%.2f' % (
        #         sum(b.line_ids.filtered(lambda x: x.code == 'AMOE ').mapped('total')) if len(
        #             b.line_ids.filtered(lambda x: x.code == 'AMOE ')) > 0 else 0), format5)
        #     worksheet1.write('H%s:H%s' % (i, i), '%.2f' % (
        #         sum(b.line_ids.filtered(lambda x: x.code == 'CNSSP').mapped('total')) if len(
        #             b.line_ids.filtered(lambda x: x.code == 'CNSSP')) > 0 else 0), format5)
        #
        #     i = i + 1