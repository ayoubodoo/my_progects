# -*- encoding: utf-8 -*-
##############################################################################
import xlwt
import datetime as dt
from odoo import models, fields, api


class interet(models.TransientModel):
    
    _name = "interet.report.erp"
    _description = "interet.report.erp"
    

    def generate_title(self,data,workbook):

        report_name =  'ETAT DES INTERETS DES EMPRUNTS CONTRACTES AUPRES DES ASSOCIES '
        report_name1='ET DES TIERS AUTRES QUE LES ORGANISMES DE BANQUE OU DE CREDIT'
        year_start = dt.datetime.strptime(str(data["from"]), "%Y-%m-%d")
        year_end = dt.datetime.strptime(str(data["clos"]), "%Y-%m-%d")
        workbook.formats[0].set_font_name("Arial")
        sheet = workbook.add_worksheet("T18 INTERET")
        sheet.set_column(0, 12, 15)


        sheet.write(2, 0, data["company"])
        sheet.write(3, 0, "IF : " + str(data["if"] or ''))
        report_name_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
        })
        sheet.write(3, 3, report_name, report_name_format)
        sheet.write(4, 3, report_name1, report_name_format)

        sheet.write(5, 0, "Tableau n° 18")
        sheet.write(5, 4, 'Exercice du: ' + year_start.strftime('%d/%m/%Y') + ' au ' + year_end.strftime('%d/%m/%Y'))

        header_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': 'yellow'})

        cell_format = workbook.add_format({
            'border': 1,
        })

        sheet.write(6, 0, "Nom,  prénomou  raison  sociale", header_format)
        sheet.write(6, 1, "Adresse", header_format)
        sheet.write(6, 2, 'N° C.I.N.  ou article  I.S.', header_format)
        sheet.write(6, 3, 'Montant du prêt', header_format)
        sheet.write(6, 4, 'Date du  prêt', header_format)
        sheet.write(6, 5, "Durée du prêt en mois", header_format)
        sheet.write(6, 6, "Taux d\'intérêt", header_format)
        sheet.write(6, 7, 'Charge financière globale', header_format)
        sheet.merge_range("I7:J7", 'Remboursement exercices antérieur', header_format)
        sheet.merge_range("K7:L7", 'Remboursement exercice actuel', header_format)
        sheet.write(6, 12, 'Observations', header_format)

        sheet.write(7, 0, "", cell_format)
        sheet.write(7, 1, "", cell_format)
        sheet.write(7, 2, '', cell_format)
        sheet.write(7, 3, '', cell_format)
        sheet.write(7, 4, '', cell_format)
        sheet.write(7, 5, "", cell_format)
        sheet.write(7, 6, "", cell_format)
        sheet.write(7, 7, '', cell_format)
        sheet.write(7, 8, 'Principal', cell_format)
        sheet.write(7, 9, 'Intérêt', cell_format)
        sheet.write(7, 10, 'Principal', cell_format)
        sheet.write(7, 11, 'Intérêt', cell_format)
        sheet.write(7, 12, '', cell_format)

        

        in_data = self.env['interets.erp']
        liasse_balance = self.env['liasse.balance.erp']
        liasse_balance_ids = liasse_balance.search([('id','=',data["id"])])
        liasse_balance_obj = liasse_balance_ids
        ina_data_ids = in_data.search([("type","=","0"),('balance_id','=',data["id"])])
        int_data_ids = in_data.search([("type","=","1"),('balance_id','=',data["id"])])
        ina_data_obj = ina_data_ids
        int_data_obj = int_data_ids


        sheet.write(8, 0, 'Associés', cell_format)

        i = 9
        if not ina_data_obj:
            nean_format = workbook.add_format({
                'bold': 3,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
            })
            sheet.merge_range("A10:M10", "NEANT", nean_format)
            i = i + 1

        for data in ina_data_obj:
            data1=data.name
            data2=data.adress
            data3=data.cin
            data4=data.mont_pretl
            data5=data.date_pret
            data6=data.duree_mois
            data7=data.taux_inter
            data8=data.charge_global
            data9=data.remb_princ
            data10=data.remb_inter
            data11=data.remb_actual_princ
            data12=data.remb_actual_inter
            data13=data.observation

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
            sheet.write(i, 10, data11, cell_format)
            sheet.write(i, 11, data12, cell_format)
            sheet.write(i, 12, data13, cell_format)


            i = i + 1

        sheet.write(i, 0, "Tiers", cell_format)
        i=i+1

        if not int_data_obj:
            nean_format = workbook.add_format({
                'bold': 3,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
            })
            sheet.merge_range("A"+str(i+1)+":M"+str(i+1), "NEANT", nean_format)
            i = i + 1

        for data in int_data_obj:
            data1=data.name
            data2=data.adress
            data3=data.cin
            data4=data.mont_pretl
            data5=data.date_pret
            data6=data.duree_mois
            data7=data.taux_inter
            data8=data.charge_global
            data9=data.remb_princ
            data10=data.remb_inter
            data11=data.remb_actual_princ
            data12=data.remb_actual_inter
            data13=data.observation

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
            sheet.write(i, 10, data11, cell_format)
            sheet.write(i, 11, data12, cell_format)
            sheet.write(i, 12, data13, cell_format)

            i = i + 1
            # modification des code EDI
            
        if liasse_balance_obj:
            if liasse_balance_obj.interets_associe or liasse_balance_obj.interets_tier:
                sheet.write(i, 0, "", cell_format)
                sheet.write(i, 1, "", cell_format)
                sheet.write(i, 2, "", cell_format)
                sheet.write(i, 3, "", cell_format)
                sheet.write(i, 4, "", cell_format)
                sheet.write(i, 5, "", cell_format)
                sheet.write(i, 6, "", cell_format)
                sheet.write(i, 7, liasse_balance_obj[0].in_charge_global, cell_format)
                sheet.write(i, 8, liasse_balance_obj[0].in_remb_princ, cell_format)
                sheet.write(i, 9, liasse_balance_obj[0].in_remb_inter, cell_format)
                sheet.write(i, 10, liasse_balance_obj[0].in_remb_actual_princ, cell_format)
                sheet.write(i, 11, liasse_balance_obj[0].in_remb_actual_inter, cell_format)



        return
    