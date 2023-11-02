# -*- encoding: utf-8 -*-
##############################################################################
import xlwt
import datetime as dt

from odoo import models, fields, api
#from odoo.addons.report_xls.utils import rowcol_to_cell


class actif(models.TransientModel):
    
    _name = "det.cpc.erp"
    _description = "det.cpc.erp"
    

    def generate_det_cpc_sheet(self, data,workbook):
        report_name =  'DETAIL DES POSTES DU C.P.C.'
        year_start = dt.datetime.strptime(str(data["from"]), "%Y-%m-%d")
        year_end = dt.datetime.strptime(str(data["clos"]), "%Y-%m-%d")
        workbook.formats[0].set_font_name("Arial")
        sheet = workbook.add_worksheet("T6 DET_CPC")
        sheet.set_column(0, 0, 10)
        sheet.set_column(1, 1, 51)
        sheet.set_column(2, 3, 25)
        sheet.write(2, 0, data["company"])
        sheet.write(3, 0, "IF : " + str(data["if"] or ''))
        report_name_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
        })
        sheet.write(3, 2, report_name, report_name_format)

        sheet.write(5, 0, "Tableau n° 4")
        sheet.write(5, 3, 'Exercice du: ' + year_start.strftime('%d/%m/%Y') + ' au ' + year_end.strftime('%d/%m/%Y'))


        code_conf = self.env['liasse.code.erp']
        extra_tab = self.env["liasse.extra.field.erp"]
        extra_tab_ids = extra_tab.search([],limit=1)
        extra_tab_obj = extra_tab_ids
        for extraline in extra_tab_obj:
            extraline.code0cpc.write({'valeur':data["clos"]})

        header_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': 'yellow'})

        cell_format = workbook.add_format({
            'border': 1,
        })

        sheet.write(6, 0, "Poste", header_format)
        sheet.write(6, 1, "LIBELLE", header_format)
        sheet.write(6, 2, "Exercice", header_format)
        sheet.write(6, 3, "Exercice précédent", header_format)


        bilan_actif = self.env['det.cpc.fiscale.erp']
        bilan_actif_ids = bilan_actif.search([('balance_id','=',data['id'])],order='sequence')
        bilan_actif_obj = bilan_actif_ids

        i = 7
        for code in bilan_actif_obj:

            total1=code.code1
            total2=code.code2


            sheet.write(i, 0, code.poste, cell_format)
            sheet.write(i, 1, code.lib, cell_format)
            sheet.write(i, 2, total1, cell_format)
            sheet.write(i, 3, total2, cell_format)

            i = i + 1

                                        
        return
    