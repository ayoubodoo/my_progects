# -*- encoding: utf-8 -*-
##############################################################################
import xlwt
import datetime as dt
from odoo import models, fields, api


class interet(models.TransientModel):
    
    _name = "passage.report.erp"
    _description = "passage.report.erp"
    

    def generate_passage_sheet(self,data,workbook):


        report_name = 'PASSAGE DU RESULTAT NET COMPTABLE AU RESULTAT NET FISCAL'

        year_start = dt.datetime.strptime(str(data["from"]), "%Y-%m-%d")
        year_end = dt.datetime.strptime(str(data["clos"]), "%Y-%m-%d")
        workbook.formats[0].set_font_name("Arial")
        sheet = workbook.add_worksheet("T3 Passage")
        sheet.set_column(0, 0, 52)
        sheet.set_column(1, 1, 20)
        sheet.set_column(2, 2, 20)
        sheet.write(2, 0, data["company"])
        sheet.write(3, 0, "IF : " + str(data["if"] or ''))
        report_name_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
            })
        sheet.merge_range("A5:C5", report_name,report_name_format)

        sheet.write(5, 0, "Tableau n° 3")
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
            'fg_color': '#FCF3A4',
            'align': 'right',

        })

        sheet.write(6, 0, "INTITULE", header_format)
        sheet.write(6, 1, 'MONTANT', header_format)
        sheet.write(6, 2, "MONTANT", header_format)

        ps_data = self.env['passage.erp']
        liasse_balance = self.env['liasse.balance.erp']
        liasse_balance_ids = liasse_balance.search([('id','=',data["id"])])
        liasse_balance_obj = liasse_balance_ids
        psrfc_data_ids = ps_data.search([("type","=","0"),('balance_id','=',data["id"])])
        psrfnc_data_ids = ps_data.search([("type","=","1"),('balance_id','=',data["id"])])
        psdfc_data_ids = ps_data.search([("type","=","2"),('balance_id','=',data["id"])])
        psdfnc_data_ids = ps_data.search([("type","=","3"),('balance_id','=',data["id"])])
        psrfc_data_obj = psrfc_data_ids
        psrfnc_data_obj = psrfnc_data_ids
        psdfc_data_obj = psdfc_data_ids
        psdfnc_data_obj = psdfnc_data_ids



        i = 7

        if liasse_balance_obj:
            sheet.write(i, 0, "RESULTAT NET COMPTABLE", cell_color)
            sheet.write(i, 0, "", cell_color)
            sheet.write(i, 0, "", cell_color)

            sheet.write(i+1, 0, "Bénéfice net", cell_format)
            sheet.write(i+1, 1, liasse_balance_obj[0].p_benifice_p, cell_format)
            sheet.write(i+1, 2, liasse_balance_obj[0].p_benifice_m, cell_format)

            sheet.write(i+2, 0, "Perte nette ", cell_format)
            sheet.write(i+2, 1, liasse_balance_obj[0].p_perte_p, cell_format)
            sheet.write(i+2, 2, liasse_balance_obj[0].p_perte_m, cell_format)

            i = i+3

        if psrfc_data_obj:
            sheet.write(i, 0, "REINTEGRATIONS FISCALES COURANTES", cell_color)
            sheet.write(i, 0, "", cell_color)
            sheet.write(i, 0, "", cell_color)
            i = i+1

        for data in psrfc_data_obj:
            data1=data.name
            data2=data.montant1
            data3=data.montant2

            sheet.write(i, 0, data1, cell_format)
            sheet.write(i, 1, data2, cell_format)
            sheet.write(i, 2, data3, cell_format)
            i = i + 1


        if psrfnc_data_obj:
            sheet.write(i, 0, 'REINTEGRATIONS FISCALES NON COURANTES', cell_format)


            i=i+1
            for data in psrfnc_data_obj:
                data1=data.name
                data2=data.montant1
                data3=data.montant2

                sheet.write(i, 0, data1, cell_format)
                sheet.write(i, 1, data2, cell_format)
                sheet.write(i, 2, data3, cell_format)

                i = i + 1

        if psdfc_data_obj:
            sheet.write(i, 0, 'DEDUCTIONS FISCALES COURANTES', cell_format)
            i = i+1
            for data in psdfc_data_obj:
                data1=data.name
                data2=data.montant1
                data3=data.montant2

                sheet.write(i, 0, data1, cell_format)
                sheet.write(i, 1, data2, cell_format)
                sheet.write(i, 2, data3, cell_format)

                i = i + 1


        if psdfnc_data_obj:
            sheet.write(i, 0, 'DEDUCTIONS FISCALES NON COURANTES', cell_format)
            i = i + 1
            for data in psdfnc_data_obj:
                data1=data.name
                data2=data.montant1
                data3=data.montant2

                sheet.write(i, 0, data1, cell_format)
                sheet.write(i, 1, data2, cell_format)
                sheet.write(i, 2, data3, cell_format)
                i = i + 1

        if liasse_balance_obj:
            sheet.write(i, 0, 'Total', cell_color)
            sheet.write(i, 1, liasse_balance_obj[0].p_total_montantp, cell_color)
            sheet.write(i, 2, liasse_balance_obj[0].p_total_montantm, cell_color)


            sheet.write(i+1, 0, 'RESULTAT BRUT FISCAL', cell_color)

            sheet.write(i+2, 0, 'Bénéfice brut si T1> T2 (A)', cell_format)
            sheet.write(i+2, 1, liasse_balance_obj[0].p_benificebp, cell_format)
            sheet.write(i+2, 2, liasse_balance_obj[0].p_benificebm, cell_format)

            sheet.write(i + 3, 0, 'Déficit brut fiscal si T2> T1 (B)', cell_format)
            sheet.write(i + 3, 1, liasse_balance_obj[0].p_deficitfp, cell_format)
            sheet.write(i + 3, 2, liasse_balance_obj[0].p_deficitfm, cell_format)

            sheet.write(i + 4, 0, 'REPORTS DEFICITAIRES IMPUTES', cell_color)

            sheet.write(i + 5, 0, 'Exercice n-4', cell_format)
            sheet.write(i + 5, 1, liasse_balance_obj[0].p_exo4p, cell_format)
            sheet.write(i + 5, 2, '', cell_format)


            sheet.write(i + 6, 0, 'Exercice n-3', cell_format)
            sheet.write(i + 6, 1, liasse_balance_obj[0].p_exo3p, cell_format)
            sheet.write(i + 6, 2,'', cell_format)

            sheet.write(i + 7, 0, 'Exercice n-2', cell_format)
            sheet.write(i + 7, 1, liasse_balance_obj[0].p_exo2p, cell_format)
            sheet.write(i + 7, 2,'', cell_format)

            sheet.write(i + 8, 0, 'Exercice n-1', cell_format)
            sheet.write(i + 8, 1, liasse_balance_obj[0].p_exo1p, cell_format)
            sheet.write(i + 8, 2, '', cell_format)

            sheet.write(i + 9, 0, 'RESULTAT NET FISCAL', cell_color)

            sheet.write(i + 10, 0, 'Bénéfice net fiscal (A-C)', cell_format)
            sheet.write(i + 10, 1, liasse_balance_obj[0].p_benificenfp, cell_format)
            sheet.write(i + 10, 2, liasse_balance_obj[0].p_benificenfm, cell_format)

            sheet.write(i + 11, 0, 'ou déficit net fiscal (B)', cell_format)
            sheet.write(i + 11, 1, liasse_balance_obj[0].p_deficitnfp, cell_format)
            sheet.write(i + 11, 2, liasse_balance_obj[0].p_deficitnfm, cell_format)

            sheet.write(i + 12, 0, 'CUMUL DES AMORTISSEMENTS FISCALEMENT DIFFERES', cell_color)

            sheet.write(i + 13, 0, 'CUMUL DES AMORTISSEMENTS FISCALEMENT DIFFERES', cell_format)
            sheet.write(i + 13, 1, '', cell_format)
            sheet.write(i + 13, 2, liasse_balance_obj[0].p_cumulafdm, cell_format)

            sheet.write(i + 14, 0, 'CUMUL DES DEFICITS FISCAUX RESTANT A REPORTER', cell_color)

            sheet.write(i + 15, 0, 'Exercice n-4', cell_format)
            sheet.write(i + 15, 1, liasse_balance_obj[0].p_exo4cumulp, cell_format)
            sheet.write(i + 15, 2, '', cell_format)

            sheet.write(i + 16, 0, 'Exercice n-3', cell_format)
            sheet.write(i + 16, 1, liasse_balance_obj[0].p_exo3cumulp, cell_format)
            sheet.write(i + 16, 2, '', cell_format)

            sheet.write(i + 17, 0, 'Exercice n-2', cell_format)
            sheet.write(i + 17, 1, liasse_balance_obj[0].p_exo2cumulp, cell_format)
            sheet.write(i + 17, 2, '', cell_format)

            sheet.write(i + 18, 0, 'Exercice n-1', cell_format)
            sheet.write(i + 18, 1, liasse_balance_obj[0].p_exo1cumulp, cell_format)
            sheet.write(i + 18, 2, '', cell_format)


        return
    