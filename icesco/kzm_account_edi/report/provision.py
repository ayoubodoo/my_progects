# -*- encoding: utf-8 -*-
##############################################################################
import xlwt
import datetime as dt
from odoo import models, fields, api
#from odoo.addons.report_xls.utils import rowcol_to_cell


class actif(models.TransientModel):
    
    _name = "prov.erp"
    _description = "prov.erp"
    

    def generate_prov_sheet(self,data,workbook):

        report_name =  'TABLEAU DES PROVISIONS'

        year_start = dt.datetime.strptime(str(data["from"]), "%Y-%m-%d")
        year_end = dt.datetime.strptime(str(data["clos"]), "%Y-%m-%d")
        workbook.formats[0].set_font_name("Arial")
        sheet = workbook.add_worksheet("T9 PROV")
        sheet.set_column(0, 0, 33)
        sheet.set_column(1, 8, 15)

        sheet.write(2, 1, data["company"])
        sheet.write(3, 1, "IF : " + str(data["if"] or ''))
        report_name_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
        })
        sheet.write(3, 4, report_name, report_name_format)

        sheet.write(5, 1, "Tableau n° 9")
        sheet.write(5, 5, 'Exercice du: ' + year_start.strftime('%d/%m/%Y') + ' au ' + year_end.strftime('%d/%m/%Y'))



        code_conf = self.env['liasse.code.erp']
        extra_tab = self.env["liasse.extra.field.erp"]
        extra_tab_ids = extra_tab.search([],limit=1)
        extra_tab_obj = extra_tab_ids
        for extraline in extra_tab_obj:
            extraline.code1prov.write({'valeur':data["clos"]})

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
        sheet.write(6, 0, "NATURE", header_format)
        sheet.write(6, 1, "Montant début exercice", header_format)
        sheet.merge_range('C7:E7', 'DOTATIONS', header_format)
        sheet.merge_range('F7:H7', 'REPRISES', header_format)
        sheet.write(6, 8, "Montant fin exercice", header_format)

        sheet.write(7, 0, "", header_format)
        sheet.write(7, 1, "", header_format)
        sheet.write(7, 2, 'D\'exploitation', header_format)
        sheet.write(7, 3, "financières", header_format)
        sheet.write(7, 4, 'Non courantes', header_format)
        sheet.write(7, 5, 'D\'exploitation', header_format)
        sheet.write(7, 6, 'financières', header_format)
        sheet.write(7, 7, 'Non courantes', header_format)

        bilan_actif = self.env['provision.fiscale.erp']
        bilan_actif_ids = bilan_actif.search([('balance_id','=',data['id'])],order='sequence')
        bilan_actif_obj = bilan_actif_ids
        c_sepcs_list = []
        style_text = None
        style_number = None
        i = 8
        for code in bilan_actif_obj:
            # if code.type in ['1']:
            #     style_text = self.cell_style_header
            #     style_number = self.cell_style_number_header
            # elif code.type in ['2']:
            #     style_text = self.cell_style_total
            #     style_number = self.cell_style_number_header
            # else:
            #     style_text = self.cell_style_normal
            #     style_number = self.cell_style_number
            total1=code.code1
            total2=code.code2
            total3=code.code3
            total4=code.code4
            total5=code.code5
            total6=code.code6
            total7=code.code7
            total8=code.code8

            sheet.write(i, 0, code.lib, cell_format)
            sheet.write(i, 1, total1, cell_format)
            sheet.write(i, 2, total2, cell_format)
            sheet.write(i, 3, total3, cell_format)
            sheet.write(i, 4, total4, cell_format)
            sheet.write(i, 5, total5, cell_format)
            sheet.write(i, 6, total6, cell_format)
            sheet.write(i, 7, total7, cell_format)
            sheet.write(i, 8, total8, cell_format)
            i = i + 1

        return
    