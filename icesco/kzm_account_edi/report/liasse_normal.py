# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (c) 2013 Noviat nv/sa (www.noviat.com). All rights reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api


class PartnerXlsx(models.AbstractModel):
    _name = 'report.report_xlsx.report_xlsx'
    _description = 'report.report_xlsx.report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, liasse_balance):

        for obj in liasse_balance:

            self.env['actif.erp'].generate_actif_sheet(data,workbook)
            self.env['passif.erp'].generate_passif_sheet(data,workbook)
            self.env['cpc.report.erp'].generate_cpc_sheet(data,workbook)
            self.env['passage.report.erp'].generate_passage_sheet(data,workbook)
            self.env['tfr.erp'].generate_esg_sheet(data,workbook)
            self.env['affect.erp'].generate_affect_sheet(data,workbook)
            self.env['immo.erp'].generate_immo_sheet(data,workbook)
            self.env['credit.bail.report.erp'].generate_creditbail_sheet(data,workbook)
            self.env['det.cpc.erp'].generate_det_cpc_sheet(data,workbook)
            self.env['amort.erp'].generate_amort_sheet(data,workbook)
            self.env['prov.erp'].generate_prov_sheet(data,workbook)
            self.env['pm.value.report.erp'].generate_pm_value_sheet(data,workbook)
            self.env['titre.particip.report.erp'].generate_particip_sheet(data,workbook)
            self.env['tva.erp'].generate_tva_sheet(data,workbook)
            self.env['repart.cs.report.erp'].generate_repart_cs_sheet(data,workbook)
            self.env['encouragement.erp'].generate_title(data,workbook)
            self.env['dotation.report.erp'].generate_title(data,workbook)
            self.env['fusion.erp'].generate_title(data,workbook)
            self.env['interet.report.erp'].generate_title(data,workbook)
            self.env['beaux.report.erp'].generate_title(data,workbook)
            self.env['stock.erp'].generate_title(data,workbook)


