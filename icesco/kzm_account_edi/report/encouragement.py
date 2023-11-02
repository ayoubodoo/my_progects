# -*- encoding: utf-8 -*-
##############################################################################
import xlwt
import datetime as dt

from odoo import models, fields, api
#from odoo.addons.report_xls.utils import rowcol_to_cell


class encouragement(models.TransientModel):
    
    _name = "encouragement.erp"
    _description = "encouragement.erp"
    

    def generate_title(self,data,workbook):

        report_name =  'ETAT POUR LE CALCUL DE L\'IMPOT DU PAR LES ENTREPRISES BENEFICIANTS DES MESURES D\'ENCOURAGEMENTS AUX INVESTISSEMENTS'

        year_start = dt.datetime.strptime(str(data["from"]), "%Y-%m-%d")
        year_end = dt.datetime.strptime(str(data["clos"]), "%Y-%m-%d")
        workbook.formats[0].set_font_name("Arial")
        sheet = workbook.add_worksheet("T15 ENCOURG")
        sheet.set_column(0, 0, 50)
        sheet.set_column(1, 3, 24)

        sheet.write(2, 0, data["company"])
        sheet.write(3, 0, "IF : " + str(data["if"] or ''))
        report_name_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
        })
        sheet.write(4, 0, report_name, report_name_format)

        sheet.write(5, 0, "Tableau n° 15")
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

        sheet.write(6, 0, "RUBRIQUES", header_format)
        sheet.write(6, 1, "Ensemble des produits", header_format)
        sheet.write(6, 2, 'Ensemble des produits correspondant à la base imposable', header_format)
        sheet.write(6, 3, 'Ensemble des produits correspondant au numérateur taxable', header_format)


        balance = self.env['liasse.balance.erp']
        balance_ids = balance.search([('id','=',data["id"])])
        balance_obj = balance_ids

        i = 7
        if balance_obj:
            sheet.write(i, 0, 'Vente', header_format)

            sheet.write(i+1, 0, 'Ventes imposables', cell_format)
            sheet.write(i+1, 1, balance_obj[0].vente_imp_ep, cell_format)
            sheet.write(i+1, 2, balance_obj[0].vente_imp_epi, cell_format)
            sheet.write(i+1, 3, balance_obj[0].vente_imp_ept, cell_format)

            sheet.write(i + 2, 0, 'Ventes exonérées à 100%', cell_format)
            sheet.write(i + 2, 1, balance_obj[0].vente_ex100_ep, cell_format)
            sheet.write(i + 2, 2, balance_obj[0].vente_ex100_epi, cell_format)
            sheet.write(i + 2, 3, balance_obj[0].vente_ex100_ept, cell_format)

            sheet.write(i + 3, 0, 'Ventes exonérées à 100%', cell_format)
            sheet.write(i + 3, 1, balance_obj[0].vente_ex50_ep, cell_format)
            sheet.write(i + 3, 2, balance_obj[0].vente_ex50_epi, cell_format)
            sheet.write(i + 3, 3, balance_obj[0].vente_ex50_ept, cell_format)

            sheet.write(i + 4, 0, "Lotissement et promotion immobilière", cell_format)

            sheet.write(i + 5, 0, 'Ventes et locations imposables', cell_format)
            sheet.write(i + 5, 1, balance_obj[0].vente_li_ep, cell_format)
            sheet.write(i + 5, 2, balance_obj[0].vente_li_epi, cell_format)
            sheet.write(i + 5, 3, balance_obj[0].vente_li_ept, cell_format)

            sheet.write(i + 6, 0, 'Ventes et locations exclus à 100%', cell_format)
            sheet.write(i + 6, 1, balance_obj[0].vente_lex100_ep, cell_format)
            sheet.write(i + 6, 2, balance_obj[0].vente_lex100_epi, cell_format)
            sheet.write(i + 6, 3, balance_obj[0].vente_lex100_ept, cell_format)

            sheet.write(i + 7, 0, 'Ventes et locations exclues à 50%', cell_format)
            sheet.write(i + 7, 1, balance_obj[0].vente_lex50_ep, cell_format)
            sheet.write(i + 7, 2, balance_obj[0].vente_lex50_epi, cell_format)
            sheet.write(i + 7, 3, balance_obj[0].vente_lex50_ept, cell_format)

            sheet.write(i + 8, 0, "Prestations de services", cell_format)

            sheet.write(i + 9, 0, 'Imposables', cell_format)
            sheet.write(i + 9, 1, balance_obj[0].pres_imp_ep, cell_format)
            sheet.write(i + 9, 2, balance_obj[0].pres_imp_epi, cell_format)
            sheet.write(i + 9, 3, balance_obj[0].pres_imp_ept, cell_format)

            sheet.write(i + 10, 0, 'Exonérées à 100%', cell_format)
            sheet.write(i + 10, 1, balance_obj[0].pres_ex100_ep, cell_format)
            sheet.write(i + 10, 2, balance_obj[0].pres_ex100_epi, cell_format)
            sheet.write(i + 10, 3, balance_obj[0].pres_ex100_ept, cell_format)

            sheet.write(i + 11, 0, 'Exonérées à 50%', cell_format)
            sheet.write(i + 11, 1, balance_obj[0].pres_ex50_ep, cell_format)
            sheet.write(i + 11, 2, balance_obj[0].pres_ex50_epi, cell_format)
            sheet.write(i + 11, 3, balance_obj[0].pres_ex50_ept, cell_format)

            sheet.write(i + 12, 0, "Produits et Subventions", cell_format)

            sheet.write(i + 13, 0, 'Produits accessoires. Produits financiers, dons et libéralités', cell_format)
            sheet.write(i + 13, 1, balance_obj[0].prod_acc_ep, cell_format)
            sheet.write(i + 13, 2, balance_obj[0].prod_acc_epi, cell_format)
            sheet.write(i + 13, 3, balance_obj[0].prod_acc_ept, cell_format)

            sheet.write(i + 14, 0, 'Subventions d\'équipement', cell_format)
            sheet.write(i + 14, 1, balance_obj[0].prod_sub_ep, cell_format)
            sheet.write(i + 14, 2, balance_obj[0].prod_sub_epi, cell_format)
            sheet.write(i + 14, 3, balance_obj[0].prod_sub_ept, cell_format)

            sheet.write(i + 15, 0, 'Subventions d\'équilibre', cell_format)

            sheet.write(i + 16, 0, 'Subventions d\'équilibre', cell_format)
            sheet.write(i + 16, 1, balance_obj[0].sub_eq_ep, cell_format)
            sheet.write(i + 16, 2, balance_obj[0].sub_eq_epi, cell_format)
            sheet.write(i + 16, 3, balance_obj[0].sub_eq_ept, cell_format)

            sheet.write(i + 17, 0, 'Imposables', cell_format)
            sheet.write(i + 17, 1, balance_obj[0].sub_imp_ep, cell_format)
            sheet.write(i + 17, 2, balance_obj[0].sub_imp_epi, cell_format)
            sheet.write(i + 17, 3, balance_obj[0].sub_imp_ept, cell_format)

            sheet.write(i + 18, 0, 'Exonérées à 100%', cell_format)
            sheet.write(i + 18, 1, balance_obj[0].sub_ex100_ep, cell_format)
            sheet.write(i + 18, 2, balance_obj[0].sub_ex100_epi, cell_format)
            sheet.write(i + 18, 3, balance_obj[0].sub_ex100_ept, cell_format)

            sheet.write(i + 19, 0, 'Exonérées à 50%', cell_format)
            sheet.write(i + 19, 1, balance_obj[0].sub_ex50_ep, cell_format)
            sheet.write(i + 19, 2, balance_obj[0].sub_ex50_epi, cell_format)
            sheet.write(i + 19, 3, balance_obj[0].sub_ex50_ept, cell_format)

            sheet.write(i + 20, 0, "Totaux partiels", cell_format)

            sheet.write(i + 21, 0, 'Totaux partiels', cell_format)
            sheet.write(i + 21, 1, balance_obj[0].taux_part_ep, cell_format)
            sheet.write(i + 21, 2, balance_obj[0].taux_part_epi, cell_format)
            sheet.write(i + 21, 3, balance_obj[0].taux_part_ept, cell_format)


            sheet.write(i + 22, 0, "Profits", cell_format)

            sheet.write(i + 23, 0, 'Profit net global des cessions après abattement pondéré', cell_format)
            sheet.write(i + 23, 1, balance_obj[0].profit_g_ep, cell_format)
            sheet.write(i + 23, 2, balance_obj[0].profit_g_epi, cell_format)
            sheet.write(i + 23, 3, balance_obj[0].profit_g_ept, cell_format)

            sheet.write(i + 24, 0, 'Autres profils exceptionnels', cell_format)
            sheet.write(i + 24, 1, balance_obj[0].profit_ex_ep, cell_format)
            sheet.write(i + 24, 2, balance_obj[0].profit_ex_epi, cell_format)
            sheet.write(i + 24, 3, balance_obj[0].profit_ex_ept, cell_format)

            sheet.write(i + 25, 0, "Total général", cell_format)

            sheet.write(i + 26, 0, 'Total général', cell_format)
            sheet.write(i + 26, 1, balance_obj[0].total_g_ep, cell_format)
            sheet.write(i + 26, 2, balance_obj[0].total_g_epi, cell_format)
            sheet.write(i + 26, 3, balance_obj[0].total_g_ept, cell_format)

        return
    