# -*- encoding: utf-8 -*-
##############################################################################
import xlwt
import datetime as dt

from odoo import models, fields, api
#from openerp.addons.report_xls.utils import rowcol_to_cell


class affect(models.TransientModel):
    
    _name = "affect.erp"
    _description = "affect.erp"
    

    column_sizes = [44,15,44,15]

    def generate_affect_sheet(self,data,workbook):

        report_name = 'TABLEAU D\'AFFECTATION DES RESULTATS INTERVENUE AU COURS DE L\'EXERCICE'
        year_start = dt.datetime.strptime(str(data["from"]), "%Y-%m-%d")
        year_end = dt.datetime.strptime(str(data["clos"]), "%Y-%m-%d")
        workbook.formats[0].set_font_name("Arial")
        sheet = workbook.add_worksheet("T14 AFFECT")
        sheet.set_column(0, 0, 44)
        sheet.set_column(1, 1, 15)
        sheet.set_column(2, 2, 44)
        sheet.set_column(3, 3, 15)
        sheet.write(2, 0, data["company"])
        sheet.write(3, 0, "IF : " + str(data["if"] or ''))
        report_name_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
            })
        sheet.merge_range("A5:C5", report_name,report_name_format)

        sheet.write(5, 0, "Tableau n° 14")
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
            'align': 'right',

        })

        sheet.write(6, 0,'A. ORIGINE DES RESULTATS A AFFECTER',header_format)
        sheet.write(6, 1, 'MONTANT', header_format)
        sheet.write(6, 2, 'B. AFFECTATION DES RESULTATS', header_format)
        sheet.write(6, 3, 'MONTANT', header_format)


        affect = self.env['liasse.affect.erp']
        affect_edi_ids = affect.search([],limit=1)
        affect_edi_obj = affect_edi_ids
        balance = self.env['liasse.balance.erp']
        balance_ids = balance.search([('id','=',data["id"])])
        balance_obj = balance_ids

        for code in affect_edi_obj:
            if balance_obj:
                sheet.write(7, 0, 'Report à nouveau ', cell_format)
                sheet.write(7, 1, balance_obj[0].aff_rep_n, cell_format)
                sheet.write(7, 2, 'Réserve légale', cell_format)
                sheet.write(7, 3, balance_obj[0].aff_rl, cell_format)

                sheet.write(8, 0, 'Résultats nets en instance d\'affectation ', cell_format)
                sheet.write(8, 1, balance_obj[0].aff_res_n_in, cell_format)
                sheet.write(8, 2, 'Autres réserves', cell_format)
                sheet.write(8, 3, balance_obj[0].aff_autre_r, cell_format)

                sheet.write(9, 0, 'Résultat net de l\'exercice ', cell_format)
                sheet.write(9, 1, balance_obj[0].aff_res_n_ex, cell_format)
                sheet.write(9, 2, 'Autres réserves', cell_format)
                sheet.write(9, 3, balance_obj[0].aff_tant, cell_format)

                sheet.write(10, 0, 'Prélèvements sur les réserves ', cell_format)
                sheet.write(10, 1, balance_obj[0].aff_prev, cell_format)
                sheet.write(10, 2, 'Dividendes', cell_format)
                sheet.write(10, 3, balance_obj[0].aff_div, cell_format)

                sheet.write(11, 0, 'Autres prélèvements ', cell_format)
                sheet.write(11, 1, balance_obj[0].aff_autre_prev, cell_format)
                sheet.write(11, 2, 'Autres affectations', cell_format)
                sheet.write(11, 3, balance_obj[0].aff_autre_aff, cell_format)

                sheet.write(12, 0, ' ', cell_format)
                sheet.write(12, 1,'' , cell_format)
                sheet.write(12, 2, 'Report à nouveau', cell_format)
                sheet.write(12, 3, balance_obj[0].aff_rep_n2, cell_format)

                sheet.write(13, 0, 'TOTAL A', cell_color_total)
                sheet.write(13, 1,balance_obj[0].aff_totala, cell_color_total)
                sheet.write(13, 2, 'TOTAL B', cell_color_total)
                sheet.write(13, 3, balance_obj[0].aff_totalb, cell_color_total)

        return
