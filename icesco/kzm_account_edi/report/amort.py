# -*- encoding: utf-8 -*-
##############################################################################
import xlwt
import datetime as dt

from odoo import models, fields, api
#from openerp.addons.report_xls.utils import rowcol_to_cell


class actif(models.TransientModel):
    
    _name = "amort.erp"
    _description = "amort.erp"

    column_sizes = [40,19,19,19,25]

    def generate_amort_sheet(self,data,workbook):
        report_name =  'TABLEAU DES AMORTISSEMENTS'


        year_start = dt.datetime.strptime(str(data["from"]), "%Y-%m-%d")
        year_end = dt.datetime.strptime(str(data["clos"]), "%Y-%m-%d")
        workbook.formats[0].set_font_name("Arial")
        sheet = workbook.add_worksheet("T8 AMT")
        sheet.set_column(0, 9, 12)
        sheet.set_column(10, 10, 15)

        sheet.write(2, 0, data["company"])
        sheet.write(3, 0, "IF : " + str(data["if"] or ''))
        report_name_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
        })
        sheet.write(3, 2, report_name, report_name_format)

        sheet.write(5, 0, "Tableau n° 8")
        sheet.write(5, 3, 'Exercice du: ' + year_start.strftime('%d/%m/%Y') + ' au ' + year_end.strftime('%d/%m/%Y'))

        header_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': 'yellow'})

        cell_format = workbook.add_format({
            'border': 1,
        })


        sheet.write(6, 0,'Nature',header_format)
        sheet.write(6, 1, 'Cumul début exercice \n',header_format)
        sheet.write(6, 2, 'Dotation de l\'exercice \n', header_format)
        sheet.write(6, 3, 'Amortissements sur immobilis-\nsorties \n', header_format)
        sheet.write(6, 4, 'Cumul d\'amor-\ntissement fin exercice \n', header_format)


        bilan_actif = self.env['amort.fiscale.erp']
        bilan_actif_ids = bilan_actif.search([('balance_id','=',data['id'])],order='sequence')
        bilan_actif_obj = bilan_actif_ids

        i = 7
        for code in bilan_actif_obj:

            total1=code.code1
            total2=code.code2
            total3=code.code3
            total4=code.code4

            sheet.write(i, 0, code.lib,cell_format)
            sheet.write(i, 1, total1,cell_format)
            sheet.write(i, 2, total2, cell_format)
            sheet.write(i, 3, total3, cell_format)
            sheet.write(i, 4, total4, cell_format)

            i = i+1
                                
        return
    