# -*- encoding: utf-8 -*-
##############################################################################
import xlwt

from odoo import models, fields, api
#from odoo.addons.report_xls.utils import rowcol_to_cell


class actif(models.TransientModel):
    
    _name = "caf.erp"
    _description = "caf.erp"
    

    def generate_title(self):
        c_specs_list = []
        cell_style = xlwt.easyxf(self.xls_styles['xls_title'] +self.xls_styles['borders_all']) 
        report_name =  'ETAT DES SOLDES DE GESTION (E.S.G)'
        c_specs = [
            ('1', 1, 0, 'text', None),('2', 1, 0, 'text', None),('report_name', 1, 0, 'text', report_name,None,cell_style),
        ]
        c_specs_list.append(c_specs)
        return c_specs_list
    
    def generate_header(self):
        c_specs_list = []
        c_specs = [
            ('0', 1, 0, 'text', None),
            ('1', 1, 0, 'text',None),
            ('3', 1, 0, 'text', None),
            ('4', 1, 0, 'text', 'LIBELLE', None, self.cell_style_header_tab),
            ('5', 1, 0, 'text', 'Exercice', None, self.cell_style_header_tab),
            ('6', 1, 0, 'text', 'Exercice pr�c�dent',None, self.cell_style_header_tab),
        ]
        c_specs_list.append(c_specs)
        return c_specs_list
    
    def generate_body(self, data):
        cell_style2 = xlwt.easyxf(self.xls_styles['xls_title2'] )
        bilan_actif = self.env['caf.fiscale.erp']
        bilan_actif_ids = bilan_actif.search([('balance_id','=',data['id'])],order='sequence')
        bilan_actif_obj = bilan_actif_ids
        report_name1= 'CAPACITE D\'AUTOFINANCEMENT (C.A.F.) - AUTOFINANCEMENT'
        c_specs = [
            ('report_name1', 4, 0, 'text', report_name1,None,cell_style2)
        ]
        c_sepcs_list = []
        c_sepcs_list.append(c_specs)

        for code in bilan_actif_obj:
            if code.type in ['1']:
                style_text = self.cell_style_header
                style_number = self.cell_style_number_header
            elif code.type in ['2']:
                style_text = self.cell_style_total
                style_number = self.cell_style_number_header
            else:
                style_text = self.cell_style_normal
                style_number = self.cell_style_number
            total1=code.code1
            total2=code.code2
                        
            c_specs = [
                           ('1', 1, 0, 'text',code.lettre, None,style_text),
                           ('2', 1, 0, 'text', code.num ,None,style_text),
                           ('0', 1, 0, 'text', code.op ,None,style_text),
                           ('5', 1, 0, 'text', code.lib ,None,style_text),
                           ('3', 1, 0, 'number', total1,None,style_number),
                           ('4', 1, 0, 'number', total2, None, style_number),
                           ]
            c_sepcs_list.append(c_specs)
        
                                
        return c_sepcs_list  
    