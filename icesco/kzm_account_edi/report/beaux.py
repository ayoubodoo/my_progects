# -*- encoding: utf-8 -*-
##############################################################################
import xlwt
import datetime as dt

from odoo import models, fields, api


class beaux(models.TransientModel):
    
    _name = "beaux.report.erp"
    _description = "beaux.report.erp"
    


    def generate_title(self,data,workbook):
        report_name =  'TABLEAU DES LOCATIONS ET BAUX AUTRES QUE LE CREDIT-BAIL'

        year_start = dt.datetime.strptime(str(data["from"]), "%Y-%m-%d")
        year_end = dt.datetime.strptime(str(data["clos"]), "%Y-%m-%d")
        workbook.formats[0].set_font_name("Arial")
        sheet = workbook.add_worksheet("T19 BEAUX")
        sheet.set_column(0, 0, 14)
        sheet.set_column(1, 1, 35)
        sheet.set_column(2, 2, 28)
        sheet.set_column(3, 3, 14)
        sheet.set_column(4, 4, 16)
        sheet.set_column(5, 5, 18)
        sheet.set_column(6, 7, 11)

        sheet.write(2, 0, data["company"])
        sheet.write(3, 0, "IF : " + str(data["if"] or ''))
        report_name_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
        })
        sheet.write(3, 3, report_name, report_name_format)


        sheet.write(5, 0, "Tableau n° 19")
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

        sheet.write(6, 0, "Nature du bien loué", header_format)
        sheet.write(6, 1, "Lieu de situation", header_format)
        sheet.write(6, 2, 'Nom et prénoms ou Raison sociale et adresse du propriétaire', header_format)
        sheet.write(6, 3, 'Date de conclusion de l\'acte de location', header_format)
        sheet.write(6, 4, 'Montant annuel de location', header_format)
        sheet.write(6, 5, "Montant du loyer compris dans les charges de l\'exercice", header_format)
        sheet.merge_range("G7:H7", 'Nature du contrat', header_format)



        sheet.write(7, 0, "", cell_format)
        sheet.write(7, 1, "", cell_format)
        sheet.write(7, 2, '', cell_format)
        sheet.write(7, 3, '', cell_format)
        sheet.write(7, 4, '', cell_format)
        sheet.write(7, 5, "", cell_format)
        sheet.write(7, 6, "Bail-ordinaire", cell_format)
        sheet.write(7, 7, '(Nème période)', cell_format)



        beaux_data = self.env['beaux.erp']
        beaux_edi = self.env['liasse.beaux.erp']
        liasse_balance = self.env['liasse.balance.erp']
        liasse_balance_ids = liasse_balance.search([('id','=',data["id"])])
        liasse_balance_obj = liasse_balance_ids
        beaux_data_ids = beaux_data.search([('balance_id','=',data["id"])])
        beaux_edi_ids = beaux_edi.search([],limit=1)
        beaux_data_obj = beaux_data_ids
        beaux_edi_obj = beaux_edi_ids

        if beaux_edi_obj:
            if beaux_edi_obj.beaux_ids:
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(beaux_edi_obj.beaux_ids[0].code0.id))
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(beaux_edi_obj.beaux_ids[0].code1.id))
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(beaux_edi_obj.beaux_ids[0].code2.id))
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(beaux_edi_obj.beaux_ids[0].code3.id))
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(beaux_edi_obj.beaux_ids[0].code4.id))
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(beaux_edi_obj.beaux_ids[0].code5.id))
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(beaux_edi_obj.beaux_ids[0].code6.id))
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(beaux_edi_obj.beaux_ids[0].code7.id))
                

        i = 8
        if not beaux_data_obj:
            nean_format = workbook.add_format({
                'bold': 3,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
            })
            sheet.merge_range("A9:H9", "NEANT", nean_format)
            i = i + 1
            
        
        for data in beaux_data_obj:
            data1=data.nature
            data2=data.lieu
            data3=data.name
            data4=data.date_loc
            data5=data.mont_annuel
            data6=data.mont_loyer
            data7=data.nature_bail
            data8=data.nature_periode

            sheet.write(i, 0, data1, cell_format)
            sheet.write(i, 1, data2, cell_format)
            sheet.write(i, 2, data3, cell_format)
            sheet.write(i, 3, data4, cell_format)
            sheet.write(i, 4, data5, cell_format)
            sheet.write(i, 5, data6, cell_format)
            sheet.write(i, 6, data7, cell_format)
            sheet.write(i, 7, data8, cell_format)

        if liasse_balance_obj:
            if liasse_balance_obj.beaux:
                sheet.write(i, 0, "Total", cell_format)
                sheet.write(i, 1, "", cell_format)
                sheet.write(i, 2, "", cell_format)
                sheet.write(i, 3, liasse_balance_obj[0].bx_mont_pretl, cell_format)
                sheet.write(i, 4, liasse_balance_obj[0].bx_charge_global, cell_format)

                                
        return
    