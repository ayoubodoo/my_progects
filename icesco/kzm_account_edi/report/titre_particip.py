# -*- encoding: utf-8 -*-
##############################################################################
import xlwt
import datetime as dt
from odoo import models, fields, api


class titre_particip(models.TransientModel):
    
    _name = "titre.particip.report.erp"
    _description = "titre.particip.report.erp"
    

    def generate_particip_sheet(self,data,workbook):


        report_name =  'TABLEAU DES TITRES DE PARTICIPATION'



        year_start = dt.datetime.strptime(str(data["from"]), "%Y-%m-%d")
        year_end = dt.datetime.strptime(str(data["clos"]), "%Y-%m-%d")
        workbook.formats[0].set_font_name("Arial")
        sheet = workbook.add_worksheet("T11 PARTICIP")

        sheet.set_column(0, 9, 15)

        sheet.write(2, 0, data["company"])
        sheet.write(3, 0, "IF : " + str(data["if"] or ''))
        report_name_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
        })
        sheet.write(3, 2, report_name, report_name_format)

        sheet.write(5, 0, "Tableau n° 11")
        sheet.write(5, 5, 'Exercice du: ' + year_start.strftime('%d/%m/%Y') + ' au ' + year_end.strftime('%d/%m/%Y'))

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

        sheet.write(6, 0, "Raison sociale de la société émettrice", header_format)
        sheet.write(6, 1, "Secteur d\'activité", header_format)
        sheet.write(6, 2, 'Capital social', header_format)
        sheet.write(6, 3, 'Participation au capital en % ', header_format)
        sheet.write(6, 4, 'Prix  d\'acquisition global', header_format)
        sheet.write(6, 5, 'aleur comptable nette', header_format)
        sheet.merge_range("G7:I7", 'Extrait des derniers états de synthèse de la société émettrice', header_format)
        sheet.write(6, 9, "Produits inscrits au C.P.C. de l\'exercice", header_format)

        sheet.write(7, 0, "", cell_format)
        sheet.write(7, 1, "", cell_format)
        sheet.write(7, 2, '', cell_format)
        sheet.write(7, 3, '', cell_format)
        sheet.write(7, 4, '', cell_format)
        sheet.write(7, 5, '', cell_format)
        sheet.write(7, 6, 'Date de cloture', cell_format)
        sheet.write(7, 7, "Situation nette", cell_format)
        sheet.write(7, 8, "Résultat net", cell_format)
        sheet.write(7, 9, "", cell_format)


        tp_data = self.env['titre.particip.erp']
        liasse_balance = self.env['liasse.balance.erp']
        liasse_balance_ids = liasse_balance.search([("id","=",data["id"])])
        liasse_balance_obj = liasse_balance_ids
        tp_data_ids = tp_data.search([('balance_id','=',data["id"])])
        tp_data_obj = tp_data_ids

        i = 8
        if not tp_data_obj:
            nean_format = workbook.add_format({
                'bold': 3,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
            })
            sheet.merge_range("A9:J9", "NEANT", nean_format)
            i = i + 1
        for data in tp_data_obj:
            data1=data.raison_soc
            data2=data.sect_activity
            data3=data.capit_social
            data4=data.particip_cap
            data5=data.prix_global
            data6=data.val_compt
            data7=data.extr_date
            data8=data.extr_situation
            data9=data.extr_resultat
            data10=data.prod_inscrit

            sheet.write(i, 0, data1, cell_format)
            sheet.write(i, 1, data2, cell_format)
            sheet.write(i, 2, data3, cell_format)
            sheet.write(i, 3, data4, cell_format)
            sheet.write(i, 4, data5, cell_format)
            sheet.write(i, 5, data6, cell_format)
            sheet.write(i, 6, data7, cell_format)
            sheet.write(i, 7, data8, cell_format)
            sheet.write(i, 8, data9, cell_format)
            sheet.write(i, 9, data10, cell_format)

            i = i + 1

        if liasse_balance_obj:
            if liasse_balance_obj.titre_particip:

                sheet.write(i, 0, "Total", cell_format)
                sheet.write(i, 1, liasse_balance_obj[0].tp_sect_activity, cell_format)
                sheet.write(i, 2, liasse_balance_obj[0].tp_capit_social, cell_format)
                sheet.write(i, 3, liasse_balance_obj[0].tp_particip_cap, cell_format)
                sheet.write(i, 4, liasse_balance_obj[0].tp_prix_global, cell_format)
                sheet.write(i, 5, liasse_balance_obj[0].tp_val_compt, cell_format)
                sheet.write(i, 6, liasse_balance_obj[0].tp_extr_date, cell_format)
                sheet.write(i, 7, liasse_balance_obj[0].tp_extr_situation, cell_format)
                sheet.write(i, 8, liasse_balance_obj[0].tp_extr_resultat, cell_format)
                sheet.write(i, 9, liasse_balance_obj[0].tp_prod_inscrit, cell_format)

        return
