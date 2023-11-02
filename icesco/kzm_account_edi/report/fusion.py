# -*- encoding: utf-8 -*-
##############################################################################
import xlwt
import datetime as dt

from odoo import models, fields, api
#from odoo.addons.report_xls.utils import rowcol_to_cell


class fusion(models.TransientModel):
    
    _name = "fusion.erp"
    _description = "fusion.erp"
    

    def generate_title(self,data,workbook):
        
        report_name =  'ETAT DES PLUS-VALUES CONSTATEES EN CAS DE  FUSIONS'
        
        year_start = dt.datetime.strptime(str(data["from"]), "%Y-%m-%d")
        year_end = dt.datetime.strptime(str(data["clos"]), "%Y-%m-%d")
        workbook.formats[0].set_font_name("Arial")
        sheet = workbook.add_worksheet("T17 FUSION")
        sheet.set_column(0, 0, 30)
        sheet.set_column(1, 8, 18)

        sheet.write(2, 0, data["company"])
        sheet.write(3, 0, "IF : " + str(data["if"] or ''))
        report_name_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
        })
        sheet.write(3, 3, report_name, report_name_format)

        sheet.write(5, 0, "Tableau n° 17")
        sheet.write(5, 4, 'Exercice du: ' + year_start.strftime('%d/%m/%Y') + ' au ' + year_end.strftime('%d/%m/%Y'))

        code_conf = self.env['liasse.code.erp']
        extra_tab = self.env["liasse.extra.field.erp"]
        extra_tab_ids = extra_tab.search([], limit=1)
        extra_tab_obj = extra_tab_ids
        for extraline in extra_tab_obj:
            extraline.code2fusion.write({'valeur': data["clos"]})
        
        header_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': 'yellow'})

        cell_format = workbook.add_format({
            'border': 1,
        })

        sheet.write(6, 0, "Eléments", header_format)
        sheet.write(6, 1, "Valeur d\'apport", header_format)
        sheet.write(6, 2, 'Valeur nette comptable', header_format)
        sheet.write(6, 3, 'Plus-value constatée et différée', header_format)
        sheet.write(6, 4, 'Fraction de la plus-value rapportée aux l\'exercices antérieurs (cumul) en % (2)', header_format)
        sheet.write(6, 5, 'Fraction de la plus-value rapportée à l\'exercices actuel en %', header_format)
        sheet.write(6, 6, 'Cumul des plus-values rapportées', header_format)
        sheet.write(6, 7, 'Solde des plus-values non imputées', header_format)
        sheet.write(6, 8, 'Observations', header_format)

    
        bilan_actif = self.env['fusion.fiscale.erp']
        bilan_actif_ids = bilan_actif.search([('balance_id','=',data['id'])],order='sequence')
        bilan_actif_obj = bilan_actif_ids

        i = 7
        if not bilan_actif_obj:
            nean_format = workbook.add_format({
                'bold': 3,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
            })
            sheet.merge_range("A8:J8", "NEANT", nean_format)
            i = i + 1
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
            sheet.write(i, 8, code.code8, cell_format)

            i = i + 1
                                                            

        return
    