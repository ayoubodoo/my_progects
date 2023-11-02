# -*- encoding: utf-8 -*-
##############################################################################
import xlwt
import datetime as dt
from odoo import models, fields, api
#from odoo.addons.report_xls.utils import rowcol_to_cell


class tva(models.TransientModel):
    
    _name = "tva.erp"
    _description = "tva.erp"
    

    def generate_tva_sheet(self,data,workbook):
        report_name =  'DETAIL DE LA TAXE SUR LA VALEUR AJOUTEE'
        year_start = dt.datetime.strptime(str(data["from"]), "%Y-%m-%d")
        year_end = dt.datetime.strptime(str(data["clos"]), "%Y-%m-%d")
        workbook.formats[0].set_font_name("Arial")
        sheet = workbook.add_worksheet("T12 TVA")
        sheet.set_column(0, 0, 38)
        sheet.set_column(1, 4, 19)

        sheet.write(2, 0, data["company"])
        sheet.write(3, 0, "IF : " + str(data["if"] or ''))
        report_name_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
        })
        sheet.write(3, 3, report_name, report_name_format)

        sheet.write(5, 0, "Tableau n° 12")
        sheet.write(5, 4, 'Exercice du: ' + year_start.strftime('%d/%m/%Y') + ' au ' + year_end.strftime('%d/%m/%Y'))

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

        sheet.write(6, 0, "NATURE", header_format)
        sheet.write(6, 1, "Solde au début de l\'exercice", header_format)
        sheet.write(6, 2, 'Opérations comptables de l\'exercice', header_format)
        sheet.write(6, 3, 'Declarations T.V.A de l\'exercice', header_format)
        sheet.write(6, 4, 'Solde fin d\'exercice', header_format)


        encour = self.env['liasse.tva.erp']
        encour_edi_ids = encour.search([],limit=1)
        encour_edi_obj = encour_edi_ids
        #liasse_conf = self.pool.get('liasse.configuration')
        code_conf = self.env['liasse.code.erp']
        balance = self.env['liasse.balance.erp']
        balance_ids = balance.search([('id','=',data["id"])])
        balance_obj  = balance_ids

        i = 7
        for code in encour_edi_obj:

            if balance_obj:
                sheet.write(i, 0, "A. T.V.A. Facturée", cell_format)
                sheet.write(i, 1, balance_obj[0].tva_facsd, cell_format)
                sheet.write(i, 2, balance_obj[0].tva_faco, cell_format)
                sheet.write(i, 3, balance_obj[0].tva_facd, cell_format)
                sheet.write(i, 4, balance_obj[0].tva_facsf, cell_format)

                i = i+1

                sheet.write(i, 0, "A. T.V.A. Récupérable", cell_format)
                sheet.write(i, 1, balance_obj[0].tva_recsd, cell_format)
                sheet.write(i, 2, balance_obj[0].tva_reco, cell_format)
                sheet.write(i, 3, balance_obj[0].tva_recd, cell_format)
                sheet.write(i, 4, balance_obj[0].tva_recsf, cell_format)

                i = i+1

                sheet.write(i, 0, "Sur charges", cell_format)
                sheet.write(i, 1, balance_obj[0].tva_charsd, cell_format)
                sheet.write(i, 2, balance_obj[0].tva_charo, cell_format)
                sheet.write(i, 3, balance_obj[0].tva_chard, cell_format)
                sheet.write(i, 4, balance_obj[0].tva_charsf, cell_format)

                i = i + 1

                sheet.write(i, 0, "Sur immobilisations", cell_format)
                sheet.write(i, 1, balance_obj[0].tva_immosd, cell_format)
                sheet.write(i, 2, balance_obj[0].tva_immoo, cell_format)
                sheet.write(i, 3, balance_obj[0].tva_immod, cell_format)
                sheet.write(i, 4, balance_obj[0].tva_immosf, cell_format)

                i = i + 1

                sheet.write(i, 0, "C. T.V.A. due ou crédit de T.V.A = (A - B )", cell_format)
                sheet.write(i, 1, balance_obj[0].tva_totalsd, cell_format)
                sheet.write(i, 2, balance_obj[0].tva_totalo, cell_format)
                sheet.write(i, 3, balance_obj[0].tva_totald, cell_format)
                sheet.write(i, 4, balance_obj[0].tva_totalsf, cell_format)

                

            # modification des code EDI
                code.tva_facsd.write({'valeur':balance_obj[0].tva_facsd})
                code.tva_faco.write({'valeur':balance_obj[0].tva_faco})
                code.tva_facd.write({'valeur':balance_obj[0].tva_facd})
                code.tva_facsf.write({'valeur':balance_obj[0].tva_facsf})
                code.tva_recsd.write({'valeur':balance_obj[0].tva_recsd})
                code.tva_reco.write({'valeur':balance_obj[0].tva_reco})
                code.tva_recd.write({'valeur':balance_obj[0].tva_recd})
                code.tva_recsf.write({'valeur':balance_obj[0].tva_recsf})
                code.tva_charsd.write({'valeur':balance_obj[0].tva_charsd})
                code.tva_charo.write({'valeur':balance_obj[0].tva_charo})
                code.tva_chard.write({'valeur':balance_obj[0].tva_chard})
                code.tva_charsf.write({'valeur':balance_obj[0].tva_charsf})
                code.tva_immosd.write({'valeur':balance_obj[0].tva_immosd})
                code.tva_immoo.write({'valeur':balance_obj[0].tva_immoo})
                code.tva_immod.write({'valeur':balance_obj[0].tva_immod})
                code.tva_immosf.write({'valeur':balance_obj[0].tva_immosf})
                code.tva_totalsd.write({'valeur':balance_obj[0].tva_totalsd})
                code.tva_totalo.write({'valeur':balance_obj[0].tva_totalo})
                code.tva_totald.write({'valeur':balance_obj[0].tva_totald})
                code.tva_totalsf.write({'valeur':balance_obj[0].tva_totalsf})
                
        return
    