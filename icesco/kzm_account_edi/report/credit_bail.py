# -*- encoding: utf-8 -*-
##############################################################################
import xlwt
import datetime as dt

from odoo import models, fields, api
#from odoo.addons.report_xls.utils import rowcol_to_cell


class credit_bail(models.TransientModel):
    
    _name = "credit.bail.report.erp"
    _description = "credit.bail.report.erp"
    

    def generate_creditbail_sheet(self,data,workbook):
        report_name =  'TABLEAU DES BIENS EN CREDIT-BAIL'

        year_start = dt.datetime.strptime(str(data["from"]), "%Y-%m-%d")
        year_end = dt.datetime.strptime(str(data["clos"]), "%Y-%m-%d")
        workbook.formats[0].set_font_name("Arial")
        sheet = workbook.add_worksheet("T7 CREDITBAI")
        sheet.set_column(0, 9, 12)
        sheet.set_column(10, 10, 15)

        sheet.write(2, 0, data["company"])
        sheet.write(3, 0, "IF : " + str(data["if"] or ''))
        report_name_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
        })
        sheet.write(3, 2, report_name, report_name_format)

        sheet.write(5, 0, "Tableau n° 7")
        sheet.write(5, 3, 'Exercice du: ' + year_start.strftime('%d/%m/%Y') + ' au ' + year_end.strftime('%d/%m/%Y'))

        header_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': 'yellow'})

        cell_format = workbook.add_format({
            'border': 1,
        })

        sheet.write(6, 0, "Rubriques", header_format)
        sheet.write(6, 1, "Date de la 1ère échéance", header_format)
        sheet.write(6, 2, "Durée du contrat en mois", header_format)
        sheet.write(6, 3, "Valeur estimée du bien en date du contrat", header_format)
        sheet.write(6, 4, "Durée théorique d\'amortissement du bien", header_format)
        sheet.write(6, 5, "Cumul des exercices précédents des redevances", header_format)
        sheet.write(6, 6, "Montant de l\'exercice des redevances", header_format)
        sheet.merge_range("H7:I7", "Redevances restant à payer", header_format)
        sheet.write(6, 9, "Prix d\'achats résiduel en fin de contrat", header_format)
        sheet.write(6, 10, "Observations\11", header_format)

        sheet.write(7, 0, "", cell_format)
        sheet.write(7, 1, "", cell_format)
        sheet.write(7, 2, "", cell_format)
        sheet.write(7, 3, "", cell_format)
        sheet.write(7, 4, "", cell_format)
        sheet.write(7, 5, "", cell_format)
        sheet.write(7, 6, "", cell_format)
        sheet.write(7, 7, "A moins d\'un an", cell_format)
        sheet.write(7, 8, "A plus d\'un an", cell_format)
        sheet.write(7, 9, "", cell_format)
        sheet.write(7, 10, "", cell_format)


    

        credit_bail_data = self.env['credi.bail.erp']
        credit_bail_edi = self.env['liasse.credit.bail.erp']
        credit_bail_data_ids = credit_bail_data.search([('balance_id','=',data["id"])])
        credit_bail_edi_ids = credit_bail_edi.search([],limit=1)
        credit_bail_data_obj = credit_bail_data_ids
        credit_bail_edi_obj = credit_bail_edi_ids

        if credit_bail_edi_obj:
            if credit_bail_edi_obj.credit_bail_ids:
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(credit_bail_edi_obj.credit_bail_ids[0].code0.id))
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(credit_bail_edi_obj.credit_bail_ids[0].code1.id))
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(credit_bail_edi_obj.credit_bail_ids[0].code2.id))
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(credit_bail_edi_obj.credit_bail_ids[0].code3.id))
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(credit_bail_edi_obj.credit_bail_ids[0].code4.id))
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(credit_bail_edi_obj.credit_bail_ids[0].code5.id))
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(credit_bail_edi_obj.credit_bail_ids[0].code6.id))
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(credit_bail_edi_obj.credit_bail_ids[0].code7.id))
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(credit_bail_edi_obj.credit_bail_ids[0].code8.id))
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(credit_bail_edi_obj.credit_bail_ids[0].code9.id))
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(credit_bail_edi_obj.credit_bail_ids[0].code10.id))

        i = 8
        if not credit_bail_data_obj:

            nean_format = workbook.add_format({
                'bold': 3,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
            })
            sheet.merge_range("A9:K9", "NEANT", nean_format)
            i = i+1
        for data in credit_bail_data_obj:
            data1=data.rubrique
            data2=data.date_first_ech
            data3=data.duree_contrat
            data4=data.val_estime
            data5=data.duree_theo
            data6=data.cumul_prec
            data7=data.montant_rev
            data8=data.rev_moins
            data9=data.rev_plus
            data10=data.prix_achat
            data11=data.observation

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

            i= i+1

        return
    