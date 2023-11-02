# -*- encoding: utf-8 -*-
##############################################################################
import xlwt
import datetime as dt
from odoo import models, fields, api
#from odoo.addons.report_xls.utils import rowcol_to_cell


class stock(models.TransientModel):
    
    _name = "stock.erp"
    _description = "stock.erp"

    def generate_title(self,data,workbook):

        report_name =  'ETAT DETAILLE DES STOCKS'

        year_start = dt.datetime.strptime(str(data["from"]), "%Y-%m-%d")
        year_end = dt.datetime.strptime(str(data["clos"]), "%Y-%m-%d")
        workbook.formats[0].set_font_name("Arial")
        sheet = workbook.add_worksheet("T20 STOCK")
        sheet.set_column(0, 0, 45)
        sheet.set_column(1, 6, 17)
        sheet.set_column(7, 7, 20)


        sheet.write(2, 0, data["company"])
        sheet.write(3, 0, "IF : " + str(data["if"] or ''))
        report_name_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
        })
        sheet.write(3, 3, report_name, report_name_format)

        sheet.write(5, 0, "Tableau n° 19")
        sheet.write(5, 4, 'Exercice du: ' + year_start.strftime('%d/%m/%Y') + ' au ' + year_end.strftime('%d/%m/%Y'))

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

        sheet.write(6, 0, "STOCK", header_format)
        sheet.merge_range("B7:D7", "STOCK FINAL", header_format)
        sheet.merge_range("E7:G7", 'STOCK INITIAL', header_format)
        sheet.write(6, 7, 'Variation de stock en valeur', header_format)

        sheet.write(7, 0, "", cell_format)
        sheet.write(7, 1, "Montant brut", cell_format)
        sheet.write(7, 2, 'Provision pour dépréciation', cell_format)
        sheet.write(7, 3, 'montant net', cell_format)
        sheet.write(7, 4, 'montant brut', cell_format)
        sheet.write(7, 5, 'Provision pour dépréciation', cell_format)
        sheet.write(7, 6, 'montant net', cell_format)
        sheet.write(7, 7, 'montant brut', cell_format)
        
        
    
    
        bilan_actif = self.env['stock.fiscale.erp']
        bilan_actif_ids = bilan_actif.search([('balance_id','=',data['id'])],order='sequence')
        bilan_actif_obj = bilan_actif_ids


        i=8
        for code in bilan_actif_obj:

            total1=code.code1
            total2=code.code2
            total3=code.code3
            total4=code.code4
            total5=code.code5
            total6=code.code6
            total7=code.code7

            sheet.write(i, 0, code.lib, cell_format)
            sheet.write(i, 1, total1, cell_format)
            sheet.write(i, 2, total2, cell_format)
            sheet.write(i, 3, total3, cell_format)
            sheet.write(i, 4, total4, cell_format)
            sheet.write(i, 5, total5, cell_format)
            sheet.write(i, 6, total6, cell_format)
            sheet.write(i, 7, total7, cell_format)

            i = i+1

                                
        return
    