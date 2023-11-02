# -*- encoding: utf-8 -*-
##############################################################################
import xlwt
import datetime as dt

from odoo import models, fields, api
#from odoo.addons.report_xls.utils import rowcol_to_cell


class immo(models.TransientModel):
    
    _name = "immo.erp"
    _description = "immo.erp"
    

    def generate_immo_sheet(self, data, workbook):

        report_name = 'TABLEAU DES IMMOBILISATIONS AUTRES QUE FINANCIERES'
        year_start = dt.datetime.strptime(str(data["from"]), "%Y-%m-%d")
        year_end = dt.datetime.strptime(str(data["clos"]), "%Y-%m-%d")
        workbook.formats[0].set_font_name("Arial")
        sheet = workbook.add_worksheet("T4 Immo")
        sheet.set_column(0, 0, 40)
        sheet.set_column(1, 1, 22)
        sheet.set_column(2, 8, 18)
        sheet.write(2, 0, data["company"])
        sheet.write(3, 0, "IF : " + str(data["if"] or ''))
        report_name_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'valign': 'vcenter',
        })
        sheet.write(3, 2, report_name,report_name_format)
        
        sheet.write(5, 0, "Tableau n° 4")
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

        sheet.write(6, 0, "Nature", header_format)
        sheet.write(6, 1, 'Montant brut début exercice', header_format)
        sheet.merge_range("C7:E7", "AUGMENTATION", header_format)
        sheet.merge_range("F7:H7", "DIMINUTION", header_format)
        sheet.write(6, 8, "Montant brut fin exercice", header_format)

        sheet.write(7, 0, "", header_format)
        sheet.write(7, 1, '', header_format)
        sheet.write(7, 2, "Acquisition", header_format)
        sheet.write(7, 3, "Production par l\'entreprise pour elle-même", header_format)
        sheet.write(7, 4, "Virement", header_format)
        sheet.write(7, 5, "Cession", header_format)
        sheet.write(7, 6, "Retrait", header_format)
        sheet.write(7, 7, "Virement", header_format)
        
        
    

        balance = self.env['liasse.balance.erp']
        balance_ids = balance.search( [('id','=',data["id"])])
        balance_obj = balance_ids

        if balance_obj:
            sheet.write(8, 0, "IMMOBILISATION EN NON-VALEURS", cell_color)
            sheet.write(8, 1,  balance_obj[0].immonv_mb, cell_color)
            sheet.write(8, 2, balance_obj[0].immonv_aug_acq, cell_color)
            sheet.write(8, 3, balance_obj[0].immonv_aug_pd, cell_color)
            sheet.write(8, 4, balance_obj[0].immonv_aug_vir, cell_color)
            sheet.write(8, 5, balance_obj[0].immonv_dim_cess, cell_color)
            sheet.write(8, 6, balance_obj[0].immonv_dim_ret, cell_color)
            sheet.write(8, 7, balance_obj[0].immonv_dim_vir, cell_color)
            sheet.write(8, 8, balance_obj[0].immonv_mbf, cell_color)

            sheet.write(9, 0, "*Frais préliminaires", cell_format)
            sheet.write(9, 1, balance_obj[0].fp_mb, cell_format)
            sheet.write(9, 2, balance_obj[0].fp_aug_acq, cell_format)
            sheet.write(9, 3, balance_obj[0].fp_aug_pd, cell_format)
            sheet.write(9, 4, balance_obj[0].fp_aug_vir, cell_format)
            sheet.write(9, 5, balance_obj[0].fp_dim_cess, cell_format)
            sheet.write(9, 6, balance_obj[0].fp_dim_ret, cell_format)
            sheet.write(9, 7, balance_obj[0].fp_dim_vir, cell_format)
            sheet.write(9, 8, balance_obj[0].fp_mbf, cell_format)

            sheet.write(10, 0, "*Charges à répartir sur plusieurs exercices", cell_format)
            sheet.write(10, 1, balance_obj[0].charge_mb, cell_format)
            sheet.write(10, 2, balance_obj[0].charge_aug_acq, cell_format)
            sheet.write(10, 3, balance_obj[0].charge_aug_pd, cell_format)
            sheet.write(10, 4, balance_obj[0].charge_aug_vir, cell_format)
            sheet.write(10, 5, balance_obj[0].charge_dim_cess, cell_format)
            sheet.write(10, 6, balance_obj[0].charge_dim_ret, cell_format)
            sheet.write(10, 7, balance_obj[0].charge_dim_vir, cell_format)
            sheet.write(10, 8, balance_obj[0].charge_mbf, cell_format)

            sheet.write(11, 0, "*Primes de remboursement obligations", cell_format)
            sheet.write(11, 1, balance_obj[0].prime_mb, cell_format)
            sheet.write(11, 2, balance_obj[0].prime_aug_acq, cell_format)
            sheet.write(11, 3, balance_obj[0].prime_aug_pd, cell_format)
            sheet.write(11, 4, balance_obj[0].prime_aug_vir, cell_format)
            sheet.write(11, 5, balance_obj[0].prime_dim_cess, cell_format)
            sheet.write(11, 6, balance_obj[0].prime_dim_ret, cell_format)
            sheet.write(11, 7, balance_obj[0].prime_dim_vir, cell_format)
            sheet.write(11, 8, balance_obj[0].prime_mbf, cell_format)

            sheet.write(12, 0, "*IMMOBILISATIONS INCORPORELLES", cell_color)
            sheet.write(12, 1, balance_obj[0].immoi_mb, cell_color)
            sheet.write(12, 2, balance_obj[0].immoi_aug_acq, cell_color)
            sheet.write(12, 3, balance_obj[0].immoi_aug_pd, cell_color)
            sheet.write(12, 4, balance_obj[0].immoi_aug_vir, cell_color)
            sheet.write(12, 5, balance_obj[0].immoi_dim_cess, cell_color)
            sheet.write(12, 6, balance_obj[0].immoi_dim_ret, cell_color)
            sheet.write(12, 7, balance_obj[0].immoi_dim_vir, cell_color)
            sheet.write(12, 8, balance_obj[0].immoi_mbf, cell_color)

            sheet.write(13, 0, "*Immobilisation en recherche et développement", cell_format)
            sheet.write(13, 1, balance_obj[0].immord_mb, cell_format)
            sheet.write(13, 2, balance_obj[0].immord_aug_acq, cell_format)
            sheet.write(13, 3, balance_obj[0].immord_aug_pd, cell_format)
            sheet.write(13, 4, balance_obj[0].immord_aug_vir, cell_format)
            sheet.write(13, 5, balance_obj[0].immord_dim_cess, cell_format)
            sheet.write(13, 6, balance_obj[0].immord_dim_ret, cell_format)
            sheet.write(13, 7, balance_obj[0].immord_dim_vir, cell_format)
            sheet.write(13, 8, balance_obj[0].immord_mbf, cell_format)

            sheet.write(14, 0, "Brevets, marques, droits et valeurs similaires", cell_format)
            sheet.write(14, 1, balance_obj[0].brevet_mb, cell_format)
            sheet.write(14, 2, balance_obj[0].brevet_aug_acq, cell_format)
            sheet.write(14, 3, balance_obj[0].brevet_aug_pd, cell_format)
            sheet.write(14, 4, balance_obj[0].brevet_aug_vir, cell_format)
            sheet.write(14, 5, balance_obj[0].brevet_dim_cess, cell_format)
            sheet.write(14, 6, balance_obj[0].brevet_dim_ret, cell_format)
            sheet.write(14, 7, balance_obj[0].brevet_dim_vir, cell_format)
            sheet.write(14, 8, balance_obj[0].brevet_mbf, cell_format)

            sheet.write(15, 0, "Fonds commercial", cell_format)
            sheet.write(15, 1, balance_obj[0].fond_mb, cell_format)
            sheet.write(15, 2, balance_obj[0].fond_aug_acq, cell_format)
            sheet.write(15, 3, balance_obj[0].fond_aug_pd, cell_format)
            sheet.write(15, 4, balance_obj[0].fond_aug_vir, cell_format)
            sheet.write(15, 5, balance_obj[0].fond_dim_cess, cell_format)
            sheet.write(15, 6, balance_obj[0].fond_dim_ret, cell_format)
            sheet.write(15, 7, balance_obj[0].fond_dim_vir, cell_format)
            sheet.write(15, 8, balance_obj[0].fond_mbf, cell_format)

            sheet.write(16, 0, "Autres immobilisations incorporelles", cell_format)
            sheet.write(16, 1, balance_obj[0].autre_incorp_mb, cell_format)
            sheet.write(16, 2, balance_obj[0].autre_incorp_aug_acq, cell_format)
            sheet.write(16, 3, balance_obj[0].autre_incorp_aug_pd, cell_format)
            sheet.write(16, 4, balance_obj[0].autre_incorp_aug_vir, cell_format)
            sheet.write(16, 5, balance_obj[0].autre_incorp_dim_cess, cell_format)
            sheet.write(16, 6, balance_obj[0].autre_incorp_dim_ret, cell_format)
            sheet.write(16, 7, balance_obj[0].autre_incorp_dim_vir, cell_format)
            sheet.write(16, 8, balance_obj[0].autre_incorp_mbf, cell_format)

            sheet.write(17, 0, "IMMOBILISATIONS CORPORELLES", cell_color)
            sheet.write(17, 1, balance_obj[0].immonc_mb, cell_color)
            sheet.write(17, 2, balance_obj[0].immonc_aug_acq, cell_color)
            sheet.write(17, 3, balance_obj[0].immonc_aug_pd, cell_color)
            sheet.write(17, 4, balance_obj[0].immonc_aug_vir, cell_color)
            sheet.write(17, 5, balance_obj[0].immonc_dim_cess, cell_color)
            sheet.write(17, 6, balance_obj[0].immonc_dim_ret, cell_color)
            sheet.write(17, 7, balance_obj[0].immonc_dim_vir, cell_color)
            sheet.write(17, 8, balance_obj[0].immonc_mbf, cell_color)

            sheet.write(18, 0, "Terrains", cell_format)
            sheet.write(18, 1, balance_obj[0].terrain_mb, cell_format)
            sheet.write(18, 2, balance_obj[0].terrain_aug_acq, cell_format)
            sheet.write(18, 3, balance_obj[0].terrain_aug_pd, cell_format)
            sheet.write(18, 4, balance_obj[0].terrain_aug_vir, cell_format)
            sheet.write(18, 5, balance_obj[0].terrain_dim_cess, cell_format)
            sheet.write(18, 6, balance_obj[0].terrain_dim_ret, cell_format)
            sheet.write(18, 7, balance_obj[0].terrain_dim_vir, cell_format)
            sheet.write(18, 8, balance_obj[0].terrain_mbf, cell_format)

            sheet.write(19, 0, "Constructions", cell_format)
            sheet.write(19, 1, balance_obj[0].constructions_mb, cell_format)
            sheet.write(19, 2, balance_obj[0].constructions_aug_acq, cell_format)
            sheet.write(19, 3, balance_obj[0].constructions_aug_pd, cell_format)
            sheet.write(19, 4, balance_obj[0].constructions_aug_vir, cell_format)
            sheet.write(19, 5, balance_obj[0].constructions_dim_cess, cell_format)
            sheet.write(19, 6, balance_obj[0].constructions_dim_ret, cell_format)
            sheet.write(19, 7, balance_obj[0].constructions_dim_vir, cell_format)
            sheet.write(19, 8, balance_obj[0].constructions_mbf, cell_format)
               
            


            sheet.write(20, 0,'Installat. techniques,materiel et outillage',cell_format)
            sheet.write(20, 1, balance_obj[0].inst_mb,cell_format)
            sheet.write(20, 2, balance_obj[0].inst_aug_acq,cell_format)
            sheet.write(20, 3, balance_obj[0].inst_aug_pd,cell_format)
            sheet.write(20, 4, balance_obj[0].inst_aug_vir,cell_format)
            sheet.write(20, 5, balance_obj[0].inst_dim_cess,cell_format)
            sheet.write(20, 6, balance_obj[0].inst_dim_ret,cell_format)
            sheet.write(20, 7, balance_obj[0].inst_dim_vir,cell_format)
            sheet.write(20, 8, balance_obj[0].inst_mbf,cell_format)

            sheet.write(21, 0,'Materiel de transport',cell_format)
            sheet.write(21, 1, balance_obj[0].mat_mb,cell_format)
            sheet.write(21, 2, balance_obj[0].mat_aug_acq,cell_format)
            sheet.write(21, 3, balance_obj[0].mat_aug_pd,cell_format)
            sheet.write(21, 4, balance_obj[0].mat_aug_vir,cell_format)
            sheet.write(21, 5, balance_obj[0].mat_dim_cess,cell_format)
            sheet.write(21, 6, balance_obj[0].mat_dim_ret,cell_format)
            sheet.write(21, 7, balance_obj[0].mat_dim_vir,cell_format)
            sheet.write(21, 8, balance_obj[0].mat_mbf,cell_format)

            sheet.write(22, 0,'Mobilier, materiel bureau et amenagements',cell_format)
            sheet.write(22, 1, balance_obj[0].mob_mb,cell_format)
            sheet.write(22, 2, balance_obj[0].mob_aug_acq,cell_format)
            sheet.write(22, 3, balance_obj[0].mob_aug_pd,cell_format)
            sheet.write(22, 4, balance_obj[0].mob_aug_vir,cell_format)
            sheet.write(22, 5, balance_obj[0].mob_dim_cess,cell_format)
            sheet.write(22, 6, balance_obj[0].mob_dim_ret,cell_format)
            sheet.write(22, 7, balance_obj[0].mob_dim_vir,cell_format)
            sheet.write(22, 8, balance_obj[0].mob_mbf,cell_format)

            sheet.write(23, 0,'Immobilisations corporelles diverses',cell_format)
            sheet.write(23, 1, balance_obj[0].autre_corp_mb,cell_format)
            sheet.write(23, 2, balance_obj[0].autre_corp_aug_acq,cell_format)
            sheet.write(23, 3, balance_obj[0].autre_corp_aug_pd,cell_format)
            sheet.write(23, 4, balance_obj[0].autre_corp_aug_vir,cell_format)
            sheet.write(23, 5, balance_obj[0].autre_corp_dim_cess,cell_format)
            sheet.write(23, 6, balance_obj[0].autre_corp_dim_ret,cell_format)
            sheet.write(23, 7, balance_obj[0].autre_corp_dim_vir,cell_format)
            sheet.write(23, 8, balance_obj[0].autre_corp_mbf,cell_format)


            sheet.write(24, 0,'Immobilisations corporelles en cours',cell_format)
            sheet.write(24, 1, balance_obj[0].immocc_mb,cell_format)
            sheet.write(24, 2, balance_obj[0].immocc_aug_acq,cell_format)
            sheet.write(24, 3, balance_obj[0].immocc_aug_pd,cell_format)
            sheet.write(24, 4, balance_obj[0].immocc_aug_vir,cell_format)
            sheet.write(24, 5, balance_obj[0].immocc_dim_cess,cell_format)
            sheet.write(24, 6, balance_obj[0].immocc_dim_ret,cell_format)
            sheet.write(24, 7, balance_obj[0].immocc_dim_vir,cell_format)
            sheet.write(24, 8, balance_obj[0].immocc_mbf,cell_format)

            sheet.write(25, 0,'Matériel informatique',cell_format)
            sheet.write(25, 1, balance_obj[0].mati_mb,cell_format)
            sheet.write(25, 2, balance_obj[0].mati_aug_acq,cell_format)
            sheet.write(25, 3, balance_obj[0].mati_aug_pd,cell_format)
            sheet.write(25, 4, balance_obj[0].mati_aug_vir,cell_format)
            sheet.write(25, 5, balance_obj[0].mati_dim_cess,cell_format)
            sheet.write(25, 6, balance_obj[0].mati_dim_ret,cell_format)
            sheet.write(25, 7, balance_obj[0].mati_dim_vir,cell_format)
            sheet.write(25, 8, balance_obj[0].mati_mbf,cell_format)


        return
    