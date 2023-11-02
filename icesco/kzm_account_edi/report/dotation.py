# -*- encoding: utf-8 -*-
##############################################################################
import xlwt
import datetime as dt

from odoo import models, fields, api


class dotation(models.TransientModel):
    
    _name = "dotation.report.erp"
    _description = "dotation.report.erp"
    

    def generate_title(self,data,workbook):

        report_name =  'ETAT DES DOTATIONS AUX AMORTISSEMENTS RELATIFS AUX IMMOBILISATIONS'



        year_start = dt.datetime.strptime(str(data["from"]), "%Y-%m-%d")
        year_end = dt.datetime.strptime(str(data["clos"]), "%Y-%m-%d")
        workbook.formats[0].set_font_name("Arial")
        sheet = workbook.add_worksheet("T16 Dotation")
        sheet.set_column(0, 0, 40)
        sheet.set_column(1, 2, 14)
        sheet.set_column(3, 4, 16)
        sheet.set_column(5, 9, 14)

        sheet.write(2, 0, data["company"])
        sheet.write(3, 0, "IF : " + str(data["if"] or ''))
        report_name_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
        })
        sheet.write(3, 3, report_name, report_name_format)
        sheet.write(4, 2, "Montant")
        sheet.write(4, 3, data["montant_dot"])
        sheet.write(5, 0, "Tableau n° 16")
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

        sheet.write(6, 0, "Immobilisations concernées", header_format)
        sheet.write(6, 1, "Date d\'entrée", header_format)
        sheet.write(6, 2, 'Valeur à amortir (Prix d\'acquisition)', header_format)
        sheet.write(6, 3, 'Valeur à amortir - Valeur comptable après réévaluation', header_format)
        sheet.write(6, 4, 'Amortissements antérieurs', header_format)
        sheet.write(6, 5, 'Amortissements déduits du Bénéfice brut de l\'exercice (Taux)', header_format)
        sheet.write(6, 6, 'Amortissements déduits du Bénéfice brut de l\'exercice Durée ', header_format)
        sheet.write(6, 7, 'Amortissements déduits du Bénéfice brut de l\'exercice Amortissements normaux ou accélérés de l\'exercice', header_format)
        sheet.write(6, 8, 'Total des amortissements à la fin de l\'exercice ', header_format)
        sheet.write(6, 9, 'Observations', header_format)


    

        pm_value_data = self.env['dotation.amort.erp']
        pm_value_edi = self.env['liasse.dotation.erp']
        liasse_balance = self.env['liasse.balance.erp']
        liasse_balance_ids = liasse_balance.search([("id","=",data["id"])])
        liasse_balance_obj = liasse_balance_ids
        pm_value_data_ids = pm_value_data.search([('balance_id','=',data["id"])])
        pm_value_edi_ids = pm_value_edi.search([],limit=1)
        pm_value_data_obj = pm_value_data_ids
        pm_value_edi_obj = pm_value_edi_ids

        if pm_value_edi_obj:
            if pm_value_edi_obj.dotation_line_ids:
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(pm_value_edi_obj.dotation_line_ids[0].code0.id))
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(pm_value_edi_obj.dotation_line_ids[0].code1.id))
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(pm_value_edi_obj.dotation_line_ids[0].code2.id))
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(pm_value_edi_obj.dotation_line_ids[0].code3.id))
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(pm_value_edi_obj.dotation_line_ids[0].code4.id))
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(pm_value_edi_obj.dotation_line_ids[0].code5.id))
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(pm_value_edi_obj.dotation_line_ids[0].code6.id))
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(pm_value_edi_obj.dotation_line_ids[0].code7.id))
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(pm_value_edi_obj.dotation_line_ids[0].code8.id))
                self.env.cr.execute('delete from liasse_code_line_erp where code_id='+str(pm_value_edi_obj.dotation_line_ids[0].code9.id))
        i = 7
        if not pm_value_data_obj:
            nean_format = workbook.add_format({
                'bold': 3,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter',
            })
            sheet.merge_range("A8:J8", "NEANT", nean_format)
            i = i + 1
        for data in pm_value_data_obj:
            data1=data.code0
            data2=data.code1
            data3=data.code2
            data4=data.code3
            data5=data.code4
            data6=data.code5
            data7=data.code6
            data8=data.code7
            data9=data.code8
            data10=data.code9

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
            if liasse_balance_obj.dotation_amort:
                sheet.write(i, 0, "Total", cell_format)
                sheet.write(i, 1, "", cell_format)
                sheet.write(i, 2, liasse_balance_obj[0].val_acq, cell_format)
                sheet.write(i, 3, liasse_balance_obj[0].val_compt, cell_format)
                sheet.write(i, 4, liasse_balance_obj[0].amort_ant, cell_format)
                sheet.write(i, 5, liasse_balance_obj[0].amort_ded_et, cell_format)
                sheet.write(i, 6, "", cell_format)
                sheet.write(i, 7, liasse_balance_obj[0].amort_ded_e, cell_format)
                sheet.write(i, 8, liasse_balance_obj[0].amort_fe, cell_format)


                i = i + 1

                                
        return
    