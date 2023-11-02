# -*- encoding: utf-8 -*-
##############################################################################
import xlwt
import datetime as dt

from odoo import models, fields, api
#from odoo.addons.report_xls.utils import rowcol_to_cell


class actif(models.TransientModel):
    
    _name = "passif.erp"
    _description = "passif.erp"
    

    def generate_passif_sheet(self, data, workbook):

        report_name = 'BILAN PASSIF'
        year_start = dt.datetime.strptime(str(data["from"]), "%Y-%m-%d")
        year_end = dt.datetime.strptime(str(data["clos"]), "%Y-%m-%d")
        workbook.formats[0].set_font_name("Arial")
        sheet = workbook.add_worksheet("T1 Passif")
        sheet.set_column(0, 0, 5)
        sheet.set_column(1, 1, 51)
        sheet.set_column(2, 5, 25)
        sheet.write(2, 1, data["company"])
        sheet.write(3, 1, "IF : " + str(data["if"] or ''))
        sheet.write(3, 2, report_name)
        sheet.write(4, 2, "(modèle normal)")
        sheet.write(5, 1, "Tableau n° 1")
        sheet.write(5, 3, 'Exercice du: ' + year_start.strftime('%d/%m/%Y') + ' au ' + year_end.strftime('%d/%m/%Y'))

        header_format = workbook.add_format({
            'font_name': "Arial",
            'bold': True,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True,
            # 'fg_color': 'yellow'
        })

        cell_format = workbook.add_format({
            'border': 1,
            'font_name': "Arial",
        })
        cell_color = workbook.add_format({
            'border': 1,
            'bold': True,
            'font_name': "Arial",
            'fg_color': '#FCF3A4'

        })
        cell_color_total = workbook.add_format({
            'border': 1,
            'bold': True,
            'font_name': "Arial",
            'fg_color': '#FCF3A4',
            'align': 'right',

        })

        sheet.write(6, 1, "PASSIF", header_format)
        sheet.write(6, 2, 'Exercice', header_format)
        sheet.write(6, 3, "Exercice précédent", header_format)

        bilan_passif = self.env['bilan.passif.fiscale.erp']
        bilan_passif_ids = bilan_passif.search([('balance_id','=',data['id'])],order='sequence')
        bilan_passif_obj = bilan_passif_ids

        style_text = None
        style_number = None
        i=7
        for code in bilan_passif_obj:
            if code.type in ['1']:
                style = cell_color

            elif code.type in ['2']:
                style = cell_color_total

            else:
                style = cell_format

            total1=code.code1
            total2=code.code2

            sheet.write(i, 1, code.lib, style)
            sheet.write(i, 2, total1, style)
            sheet.write(i, 3, total2, style)

            i = i + 1


        return
    