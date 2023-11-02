# -*- encoding: utf-8 -*-
##############################################################################
import xlwt
import datetime as dt
from odoo import models, fields, api


class repart_cs(models.TransientModel):
    
    _name = "repart.cs.report.erp"
    _description = "repart.cs.report.erp"


    def generate_repart_cs_sheet(self,data,workbook):

        report_name =  'ETAT DE REPARTITION DU CAPITAL SOCIAL'
        year_start = dt.datetime.strptime(str(data["from"]), "%Y-%m-%d")
        year_end = dt.datetime.strptime(str(data["clos"]), "%Y-%m-%d")
        workbook.formats[0].set_font_name("Arial")

        sheet = workbook.add_worksheet("T13 REPART CS")
        sheet.set_column(0, 0, 25)
        sheet.set_column(1, 7, 15)
        sheet.set_column(8, 9, 18)

        sheet.write(2, 0, data["company"])
        sheet.write(3, 0, "IF : " + str(data["if"] or ''))
        report_name_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
        })
        sheet.write(3, 4, report_name, report_name_format)





        credit_bail_edi = self.env['liasse.repart.cs.erp']
        credit_bail_edi_ids = credit_bail_edi.search([],limit=1)
        credit_bail_edi_obj = credit_bail_edi_ids
        code_conf = self.env['liasse.code.erp']
        #montant
        montant = data["montant_cs"]
        #i = 6
        if credit_bail_edi_obj:
            sheet.write(5, 1, 'Montant du capital : '+str(montant))
            sheet.write(6, 0, "Tableau n° 13")
            sheet.write(6, 5,'Exercice du: ' + year_start.strftime('%d/%m/%Y') + ' au ' + year_end.strftime('%d/%m/%Y'))

            credit_bail_edi_obj.montant_capital.write({'valeur':str(data["montant_cs"])})

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

        sheet.write(7, 0, "Nom, prénom ou raison sociale des principaux associés", header_format)
        sheet.write(7, 1, "IF", header_format)
        sheet.write(7, 2, 'CIN', header_format)
        sheet.write(7, 3, 'Adreasse', header_format)
        sheet.merge_range("E8:F8", 'NOMBRE DE TITRES', header_format)
        sheet.write(7, 6, 'Valeur nominale de chaque action ou part sociale', header_format)
        sheet.merge_range("H8:J8", 'MONTANT DU CAPITAL', header_format)

        sheet.write(8, 0, "", cell_format)
        sheet.write(8, 1, "", cell_format)
        sheet.write(8, 2, '', cell_format)
        sheet.write(8, 3, '', cell_format)
        sheet.write(8, 4, 'Exercice précédent', cell_format)
        sheet.write(8, 5, 'Exercice actual', cell_format)
        sheet.write(8, 6, "", cell_format)
        sheet.write(8, 7, "Souscrit", cell_format)
        sheet.write(8, 8, "Appelé", cell_format)
        sheet.write(8, 9, "libéré", cell_format)


        credit_bail_data = self.env['repart.cs.erp']
        credit_bail_data_ids = credit_bail_data.search([('balance_id','=',data["id"])])
        credit_bail_data_obj = credit_bail_data_ids

        i = 9
        if not credit_bail_data_obj:
            nean_format = workbook.add_format({
                'bold': 3,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
            })
            sheet.merge_range("A10:J10", "NEANT", nean_format)
            i = i + 1

        for data in credit_bail_data_obj:
            data1=data.name
            data2=data.id_fisc
            data3=data.cin
            data4=data.adress
            data5=data.number_prec
            data6=data.number_actual
            data7=data.val_nom
            data8=data.val_sousc
            data9=data.val_appele
            data10=data.val_lib

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

        return
    