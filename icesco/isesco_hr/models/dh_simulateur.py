import datetime as dt
import locale
import time
from datetime import timedelta, datetime
from odoo import models,fields
import base64
import io
from io import BytesIO

class IrSimulateurXlsx(models.AbstractModel):
    _name = 'report.isesco_hr.report_ir_simulateur'
    _inherit = 'report.report_xlsx.abstract'
    def generate_xlsx_report(self, workbook, data, datas):
        locale.setlocale(locale.LC_ALL,
                         'fr_FR.UTF-8')
        i = 1
        s = 1
        for line in datas:
            report_name = "Simulateur ICESCO_ Payroll  %s" % (line.name)

            worksheet1 = workbook.add_worksheet(report_name)
            format0 = workbook.add_format(
                {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
                 'font_color': 'black', 'bg_color': '#E1F0DB'})

            format1 = workbook.add_format(
                {'font_size': 18, 'align': 'center', 'valign': 'vcenter',
                 'font_color': 'black', 'bg_color': 'white', 'bold': True, 'border': 2, 'border_color': 'black'})
            format11 = workbook.add_format(
                {'font_size': 18, 'align': 'left', 'valign': 'vcenter',
                 'font_color': '#495057', 'bg_color': 'white', 'bold': True})

            format4 = workbook.add_format(
                {'font_size': 13, 'align': 'center', 'valign': 'vcenter',
                 'font_color': 'black', 'bg_color': 'white',
                 'border': 2, 'border_color': 'black'})
            format2 = workbook.add_format(
                {'font_size': 14, 'align': 'left', 'valign': 'vcenter',
                 'font_color': 'white', 'bg_color': '#385724',
                  'border': 2, 'border_color': 'black'})
            format3 = workbook.add_format(
                {'font_size': 14, 'align': 'left', 'valign': 'vcenter',
                 'font_color': 'white', 'bg_color': '#00B050',
                  'border': 2, 'border_color': 'black'})
            format9 = workbook.add_format(
                {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
                 'font_color': 'black', 'bg_color': '#A6A6A6',
                 'border': 2, 'border_color': 'black'})

            format8 = workbook.add_format(
                {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
                 'font_color': '1E375E', 'bg_color': 'white','bold': True,
                 'border': 2, 'border_color': 'black'})
            format10 = workbook.add_format(
                {'font_size': 12, 'align': 'left', 'valign': 'vcenter',
                 'font_color': 'white', 'bg_color': '008484','bold': True,
                 'border': 2, 'border_color': 'black'})
            format5 = workbook.add_format(
                {'font_size': 14, 'align': 'L', 'valign': 'vcenter',
                 'font_color': '354F6D', 'bg_color': 'white',
                 'border': 2, 'border_color': 'black'})
            format6 = workbook.add_format(
                {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
                 'font_color': '#354F6D', 'bg_color': 'white',
                 'border': 2, 'border_color': 'black'})



            worksheet1.set_row(0, 40)
            worksheet1.set_row(1, 40)
            worksheet1.set_row(2, 40)
            worksheet1.set_row(3, 40)
            worksheet1.set_row(4, 40)
            worksheet1.set_row(5, 40)
            worksheet1.set_row(6, 40)
            worksheet1.set_row(7, 40)
            worksheet1.set_row(8, 40)
            worksheet1.set_row(9, 40)
            worksheet1.set_row(10, 40)
            worksheet1.set_row(11, 40)
            worksheet1.set_row(12, 40)
            worksheet1.set_row(13, 40)
            worksheet1.set_row(14, 40)

            worksheet1.set_column('A:A', 20)
            worksheet1.set_column('B:B', 20)
            worksheet1.set_column('C:C', 40)
            worksheet1.set_column('D:D', 30)
            worksheet1.set_column('E:E', 5)
            worksheet1.set_column('F:F', 20)
            worksheet1.set_column('G:G', 5)
            worksheet1.set_column('H:H', 20)
            worksheet1.set_column('I:I', 20)
            worksheet1.set_column('J:J', 20)
            worksheet1.set_column('K:K', 20)
            worksheet1.set_column('L:L', 20)
            worksheet1.set_column('M:M', 20)

            # , ['line_ids.category_id.id', '=', 'line.category_id.id']

            if line.nationality.name =='Morocco':
                trans_allowance = 0
            else:
                if len(self.env['hr.payroll_ma.rubrique'].search([('is_transport','=',True)]).mapped('line_ids').filtered(lambda x: x.category_id.id == line.category_contract_id.id)) > 0:
                    trans_allowance = self.env['hr.payroll_ma.rubrique'].search([('is_transport','=',True)]).mapped('line_ids').filtered(lambda x: x.category_id.id == line.category_contract_id.id)[0].amount
                else:
                    trans_allowance = 0
            # print("allowance",trans_allowance[0].amount)
            logo = self.env.company.logo
            if logo:
                imgdata = base64.b64decode(logo)
                image = io.BytesIO(imgdata)
                worksheet1.insert_image('A1:B4', 'logo.png',
                                        {'image_data': image, 'x_scale': 1.6, 'y_scale': 1})

            worksheet1.merge_range('C1:G2', '%s' % ("Simulateur ICESCO_ Payroll "), format1)
            # worksheet1.write('C3:C3', 'Nationalité', format4)
            # worksheet1.write('D3:D3', 'Marocain', format4)
            # if line.nationality == 'Morocoo':
            #     worksheet1.write('E3:E3', 'X', format4)
            # else:
            #     worksheet1.write('E3:E3', '', format4)


            # worksheet1.write('F3:F3', 'Expatrié', format4)

            # if line.nationality == 'Morocoo':
            #     worksheet1.write('G3:G3', '', format4)
            # else :
            #     worksheet1.write('G3:G3', 'X', format4)




            worksheet1.merge_range('C5:D5',  '%s' % (line.partner_name), format0)
            worksheet1.write('C6:C6', 'Rank', format2)
            worksheet1.write('C7:C7', 'Echelon/ Grade', format2)
            worksheet1.write('C8:C8', 'Salaire de Base/ Basic Salary ', format3)
            worksheet1.write('C9:C9', 'Transportation Allowance', format2)
            worksheet1.write('C10:C10', 'Family Allowances', format2)
            worksheet1.write('C11:C11', 'Housing Allowances', format2)
            worksheet1.write('C12:C12', 'Expartiation Allowances ', format2)
            worksheet1.write('C13:C13', 'Settlement allowance  ', format2)
            worksheet1.write('C14:C14', 'Supervisory Allowance', format2)


            worksheet1.write('D6:D6', '%s' % (line.code), format4)
            worksheet1.write('D7:D7', '%s' % (line.grade_id.code), format4)
            worksheet1.write('D8:D8', '%.2f' % (line.amount) , format9)
            worksheet1.write('D9:D9', '%.2f' % (trans_allowance), format4)
            worksheet1.write('D10:D10','%.2f' % (line.family_allowance), format4)
            worksheet1.write('D11:D11','%.2f' % (line.amount*0.2), format4)
            worksheet1.write('D12:D12', '%.2f' % (line.amount*0.25), format4)
            worksheet1.write('D13:D13', '%.2f' % (line.amount*0.5), format4)
            worksheet1.write('D14:D14', '%.2f' % (line.amount*0.25), format4)

            worksheet1.write('D16:D16',  '%.2f' % (line.amount+trans_allowance++line.family_allowance+line.amount*0.2+line.amount*0.5+line.amount*0.25+line.amount*0.25), format4)



            # worksheet1.write('E6:E6', '', format4)
            # worksheet1.write('E7:E7', '', format4)
            # worksheet1.write('E8:E8', ' ', format9)
            # worksheet1.write('E9:E9', '', format4)
            # worksheet1.write('E10:E10', '', format4)
            # worksheet1.write('E11:E11', '', format4)
            # worksheet1.write('E12:E12', ' ', format4)
            # worksheet1.write('E13:E13', '  ', format4)
            # worksheet1.write('E14:E14', '', format4)
            #
            # worksheet1.write('F6:F6', '', format4)
            # worksheet1.write('F7:F7', '', format4)
            # worksheet1.write('F8:F8', ' ', format9)
            # worksheet1.write('F9:F9', '', format4)
            # worksheet1.write('F10:F10', '', format4)
            # worksheet1.write('F11:F11', '', format4)
            # worksheet1.write('F12:F12', ' ', format4)
            # worksheet1.write('F13:F13', '  ', format4)
            # worksheet1.write('F14:F14', '', format4)
            #
            # worksheet1.write('G6:G6', '', format4)
            # worksheet1.write('G7:G7', '', format4)
            # worksheet1.write('G8:G8', ' ', format9)
            # worksheet1.write('G9:G9', '', format4)
            # worksheet1.write('G10:G10', '', format4)
            # worksheet1.write('G11:G11', '', format4)
            # worksheet1.write('G12:G12', ' ', format4)
            # worksheet1.write('G13:G13', '  ', format4)
            # worksheet1.write('G14:G14', '', format4)


            worksheet1.write('C16:C16', 'Global Salary ', format3)

            worksheet1.write('C18:C18', 'Mutuelle', format2)
            worksheet1.write('C19:C19', 'End of Service', format2)
            worksheet1.write('C20:C20', 'Net Salary ', format3)

            worksheet1.write('D18:D18','%.2f' % (line.amount*0.03), format4)
            worksheet1.write('D19:D19', '%.2f' % (line.amount*0.0025), format4)
            worksheet1.write('D20:D20','%.2f' % ((line.amount+trans_allowance++line.family_allowance+line.amount*0.2+line.amount*0.5+line.amount*0.25+line.amount*0.25)-(line.amount*0.03-line.amount*0.025)), format4)



            # worksheet1.write('E18:E18', '', format4)
            # worksheet1.write('E19:E19', '', format4)
            # worksheet1.write('E20:E20', '', format4)
            #
            # worksheet1.write('F18:F18', '', format4)
            # worksheet1.write('F19:F19', '', format4)
            # worksheet1.write('F20:F20', '', format4)
            #
            # worksheet1.write('G18:G18', '', format4)
            # worksheet1.write('G19:G19', '', format4)
            # worksheet1.write('G20:G20', '', format4)

            # worksheet1.write('E5:E5', "", format0)
            # worksheet1.write('F5:F5', 'Frequency', format0)
            # worksheet1.write('G5:G5', 'For', format0)
