# -*- encoding: utf-8 -*-
##############################################################################
import xlwt
import datetime as dt
from odoo import models, fields, api
#from openerp.addons.report_xls.utils import rowcol_to_cell


class actif(models.TransientModel):
    
    _name = "tfr.erp"
    _description = "tfr.erp"
    

    def generate_esg_sheet(self,data,workbook):

        report_name = 'ETAT DES SOLDES DE GESTION (E.S.G)'
        year_start = dt.datetime.strptime(str(data["from"]), "%Y-%m-%d")
        year_end = dt.datetime.strptime(str(data["clos"]), "%Y-%m-%d")
        workbook.formats[0].set_font_name("Arial")
        sheet = workbook.add_worksheet("T5 ESG")
        sheet.set_column(0, 0, 5)
        sheet.set_column(1, 2, 4)
        sheet.set_column(3, 3, 37)
        sheet.set_column(3, 3, 17)
        sheet.write(2, 0, data["company"])
        sheet.write(3, 0, "IF : " + str(data["if"] or ''))
        report_name_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
        })
        sheet.merge_range("A5:C5", report_name, report_name_format)

        sheet.write(5, 0, "Tableau n° 5")
        sheet.write(6, 0, 'ETAT DES SOLDES DE GESTION (E.S.G)')
        sheet.write(6, 3, 'Exercice du: ' + year_start.strftime('%d/%m/%Y') + ' au ' + year_end.strftime('%d/%m/%Y'))

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

        sheet.write(7, 0, "", header_format)
        sheet.write(7, 1, '', header_format)
        sheet.write(7, 2, "", header_format)
        sheet.write(7, 3, "LIBELLE", header_format)
        sheet.write(7, 4, "Exercice", header_format)
        sheet.write(7, 5, "Exercice précédent", header_format)


        bilan_actif = self.env['tfr.fiscale.erp']
        bilan_actif_ids = bilan_actif.search([('balance_id','=',data['id'])],order='sequence')
        bilan_actif_obj = bilan_actif_ids


        i = 8
        for code in bilan_actif_obj:

            total1=code.code1
            total2=code.code2

            sheet.write(i, 0, code.lettre, cell_format)
            sheet.write(i, 1, code.num, cell_format)
            sheet.write(i, 2, code.op, cell_format)
            sheet.write(i, 3, code.lib, cell_format)
            sheet.write(i, 4, total1, cell_format)
            sheet.write(i, 5, total2, cell_format)

            i = i + 1


                                
        return
    