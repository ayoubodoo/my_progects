# -*- encoding: utf-8 -*-
##############################################################################
import xlwt
import datetime as dt
from odoo import models, fields, api
#from odoo.addons.report_xls.utils import rowcol_to_cell


class actif(models.TransientModel):
    
    _name = "cpc.report.erp"
    _description = "cpc.report.erp"

    def generate_cpc_sheet(self,data, workbook):


        report_name = 'COMPTE DE PRODUITS ET CHARGES (hors taxes)'
        year_start = dt.datetime.strptime(str(data["from"]), "%Y-%m-%d")
        year_end = dt.datetime.strptime(str(data["clos"]), "%Y-%m-%d")
        workbook.formats[0].set_font_name("Arial")
        sheet = workbook.add_worksheet("T2 CPC")
        sheet.set_column(0, 0, 5)
        sheet.set_column(1, 1, 36)
        sheet.set_column(2, 5, 15)
        sheet.set_column(7, 40)
        sheet.write(2, 1, data["company"])
        sheet.write(3, 1, "IF : " + str(data["if"] or ''))
        sheet.write(3, 2, report_name)
        sheet.write(5, 1, "Tableau n° 2")
        sheet.write(5, 3, 'Exercice du: ' + year_start.strftime('%d/%m/%Y') + ' au ' + year_end.strftime('%d/%m/%Y'))

        header_format = workbook.add_format({
            'font_name': "Arial",
            'bold': True,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True,

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

        sheet.write(6, 1, "NATURE", header_format)
        sheet.merge_range('C7:D7', 'OPERATIONS', header_format)
        sheet.merge_range('E7:F7', '', header_format)

        sheet.write(7, 1, "", header_format)
        sheet.write(7, 2, "Propres à l\'exercice", header_format)
        sheet.write(7, 3, "Concernant les exercices précédent", header_format)
        sheet.write(7, 4, "TOTAUX DE L\'EXERCICE", header_format)
        sheet.write(7, 5, "TOTAUX DE L\'EXERCICE PRECEDENT", header_format)

        bilan_actif = self.env['cpc.fiscale.erp']
        bilan_actif_ids = bilan_actif.search([('balance_id','=',data['id'])],order='sequence')
        bilan_actif_obj = bilan_actif_ids

        i = 8
        for code in bilan_actif_obj:
            if code.type in ['1']:
                style = cell_color

            elif code.type in ['2']:
                style = cell_color_total

            else:
                style = cell_format

            total1=code.code1
            total2=code.code2
            total3=code.code3
            total4=code.code4

            sheet.write(i, 1, code.lib, style)
            sheet.write(i, 2, total1, style)
            sheet.write(i, 3, total2, style)
            sheet.write(i, 4, total3, style)
            sheet.write(i, 5, total4, style)
            i = i + 1


        return
    