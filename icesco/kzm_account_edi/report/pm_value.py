# -*- encoding: utf-8 -*-
##############################################################################
import xlwt
import datetime as dt
from odoo import models, fields, api


class pm_value(models.TransientModel):
    
    _name = "pm.value.report.erp"
    _description = "pm.value.report.erp"
    

    def generate_pm_value_sheet(self,data,workbook):
        report_name =  'TABLEAU DES PLUS OU MOINS VALUES SUR CESSIONS OU RETRAITS'

        year_start = dt.datetime.strptime(str(data["from"]), "%Y-%m-%d")
        year_end = dt.datetime.strptime(str(data["clos"]), "%Y-%m-%d")
        workbook.formats[0].set_font_name("Arial")
        sheet = workbook.add_worksheet("T10 PM VALUE")
        sheet.set_column(0, 2, 14)
        sheet.set_column(3, 4, 16)
        sheet.set_column(5, 7, 14)

        sheet.write(2, 0, data["company"])
        sheet.write(3, 0, "IF : " + str(data["if"] or ''))
        report_name_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
        })
        sheet.write(3, 4, report_name, report_name_format)

        sheet.write(5, 0, "Tableau n° 10")
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

        sheet.write(6, 0, "Date de cession ou de retrait", header_format)
        sheet.write(6, 1, "Compte principal", header_format)
        sheet.write(6, 2, 'Montant brut', header_format)
        sheet.write(6, 3, 'Amortissements cumulés', header_format)
        sheet.write(6, 4, 'Valeur nette d\'amortissements', header_format)
        sheet.write(6, 5, 'Produit de cession', header_format)
        sheet.write(6, 6, 'Plus values', header_format)
        sheet.write(6, 7, "Moins values", header_format)


        pm_value_data = self.env['pm.value.erp']
        liasse_balance = self.env['liasse.balance.erp']
        liasse_balance_ids = liasse_balance.search([("id","=",data["id"])])
        liasse_balance_obj = liasse_balance_ids
        pm_value_data_ids = pm_value_data.search([('balance_id','=',data["id"])])
        pm_value_data_obj = pm_value_data_ids

        i=7
        if not pm_value_data_obj:
            nean_format = workbook.add_format({
                'bold': 3,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
            })
            sheet.merge_range("A8:H8", "NEANT", nean_format)
            i = i + 1


        for data in pm_value_data_obj:
            data1=data.date_cession
            data2=data.compte_princ
            data3=data.montant_brut
            data4=data.amort_cumul
            data5=data.val_net_amort
            data6=data.prod_cess
            data7=data.plus_value
            data8=data.moins_value

            sheet.write(i, 0, data1, cell_format)
            sheet.write(i, 1, data2, cell_format)
            sheet.write(i, 2, data3, cell_format)
            sheet.write(i, 3, data4, cell_format)
            sheet.write(i, 4, data5, cell_format)
            sheet.write(i, 5, data6, cell_format)
            sheet.write(i, 6, data7, cell_format)
            sheet.write(i, 7, data8, cell_format)

            i = i + 1


        if liasse_balance_obj:
            if liasse_balance_obj.pm_value:
                sheet.write(i, 0, "Total", cell_format)
                sheet.write(i, 1, liasse_balance_obj[0].pm_compte_princ, cell_format)
                sheet.write(i, 2, liasse_balance_obj[0].pm_montant_brut, cell_format)
                sheet.write(i, 3, liasse_balance_obj[0].pm_amort_cumul, cell_format)
                sheet.write(i, 4, liasse_balance_obj[0].pm_val_net_amort, cell_format)
                sheet.write(i, 5, liasse_balance_obj[0].pm_prod_cess, cell_format)
                sheet.write(i, 6, liasse_balance_obj[0].pm_plus_value, cell_format)
                sheet.write(i, 7, liasse_balance_obj[0].pm_moins_value, cell_format)

                                
        return
    