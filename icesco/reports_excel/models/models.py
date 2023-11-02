import datetime as dt
import locale
import time
from datetime import timedelta, datetime
from odoo import models

class BordereauxVirementXlsx(models.AbstractModel):
    _name = 'report.reports_excel.bordereau_virement_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, datas):
        for rec in datas:
            locale.setlocale(locale.LC_ALL,
                             'fr_FR.UTF-8')  # sudo locale-gen fr_FR.UTF-8
            report_name = '%s' % (rec.name)
            worksheet = workbook.add_worksheet(report_name)
            format0 = workbook.add_format(
                {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
                 'font_color': 'black', 'bg_color': 'white'})
            format1 = workbook.add_format(
                {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
                 'font_color': '#495057', 'bg_color': 'white'})
            format2 = workbook.add_format(
                {'font_size': 13, 'align': 'center', 'valign': 'vcenter',
                 'font_color': '#495057', 'bold': True, 'bg_color': 'white',
                 'underline': True})
            format4 = workbook.add_format(
                {'font_size': 14, 'align': 'center', 'valign': 'vcenter',
                 'font_color': 'black', 'bg_color': '#F8F5F7',
                 'border': 1,'border_color': 'black'})
            format5 = workbook.add_format(
                {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
                 'font_color': 'black', 'bg_color': 'white',
                 'border': 1, 'border_color': 'black'})
            format6 = workbook.add_format(
                {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
                 'font_color': '#495057', 'bg_color': 'white',
                 'border': 1, 'border_color': 'black'})

            worksheet.merge_range('B1:C1', '', format1)
            worksheet.merge_range('B2:C2', '', format1)
            worksheet.merge_range('B3:C3', '', format1)
            worksheet.merge_range('B4:C4', '', format1)
            worksheet.merge_range('A5:D5', '', format1)
            worksheet.merge_range('B6:D6', '', format1)
            worksheet.merge_range('B7:D7', '', format1)

            worksheet.set_row(0, 25)
            worksheet.set_row(1, 25)
            worksheet.set_row(2, 25)
            worksheet.set_row(3, 25)
            worksheet.set_row(4, 25)
            worksheet.set_row(5, 25)
            worksheet.set_row(6, 25)
            worksheet.set_row(7, 25)
            worksheet.set_row(8, 25)
            worksheet.set_row(9, 25)

            worksheet.set_column('A:A', 40)
            worksheet.set_column('B:B', 20)
            worksheet.set_column('C:C', 50)
            worksheet.set_column('D:D', 35)

            worksheet.write('A1:A1','ICESCO',format0)
            worksheet.write('A2:B2','Avenue des F.A.R., Hay Ryad, B.P. 2275',format1)
            worksheet.write('A3:A3','Rabat 10104',format1)
            worksheet.write('A4:A4','Maroc',format1)


            worksheet.write('D1:D1', 'A Monsieur le directeur', format1)
            if rec.company_id.banque_virement_paie:
                worksheet.write('D2:D2', 'DE %s' % (rec.company_id.banque_virement_paie),
                                format1)
            else:
                worksheet.write('D2:D2', '', format1)
            if rec.company_id.agence_virement_paie:
                worksheet.write('D3:D3', 'Agence %s' % (rec.company_id.agence_virement_paie),
                                format1)
            else:
                worksheet.write('D3:D3','' ,format1)
            if rec.company_id.ville_agence_virement_paie:
                worksheet.write('D4:D4','%s' % (rec.company_id.ville_agence_virement_paie),
                                format1)
            else:
                worksheet.write('D4:D4', '', format1)


            worksheet.write('A6:B6', 'Objet: Virement du mois %s' % (
                rec.period_id.name),format2)

            worksheet.merge_range('A7:D7', '', format1)
            worksheet.write('A7:D7', 'Monsieur,' , format1)

            if rec.company_id.rib_virement_paie:
                worksheet.merge_range('A8:D8', '', format1)
                worksheet.write('A8:D8', 'Par la présente, nous vous prions de bien '
                                         'vouloir virer par le débit de notre compte N° %s '
                                         'le montant de :' % (rec.company_id.rib_virement_paie), format1)
            else:
                worksheet.merge_range('A8:D8', '', format1)
                worksheet.write('A8:D8', 'Par la présente, nous vous prions de bien '
                                         'vouloir virer par le débit de notre compte '
                                         'le montant de :', format1)

            worksheet.merge_range('A9:D9', '', format1)
            worksheet.write('A9:D9', '%s (%s DHS)' % (
                                rec.total_net_a_payer_vrt_text,
                                rec.total_net_a_payer_vrt), format0)

            worksheet.merge_range('A10:D10', '', format1)
            worksheet.write('A10:B10', 'détaillé comme suit :', format1)

            worksheet.set_row(11, 25)
            worksheet.write('A12:A12', 'Matricule', format4)
            worksheet.write('B12:B12', 'Nom', format4)
            worksheet.write('C12:C12', 'Banque', format4)
            worksheet.write('D12:D12', 'N° de Compte', format4)
            worksheet.write('E12:E12', 'Montant', format4)

            i = 12
            for line in rec.bulletin_line_ids.filtered(lambda m:
                                                     m.employee_id.mode_reglement ==
                                                     'virement').sorted(key=lambda r: r.employee_id.matricule):
                worksheet.set_row(i, 25)
                worksheet.write(i,0, '%s' %(line.employee_id.matricule), format6)
                worksheet.write(i,1, '%s %s' %(line.employee_id.name,
                                               line.employee_id.prenom), format6)
                worksheet.write(i, 2, '%s' % (line.employee_id.bank.name), format6)
                worksheet.write(i, 3, '%s' % (line.employee_id.compte), format6)
                worksheet.write(i, 4, '%s' % (line.salaire_net_a_payer), format6)
                i = i + 1

            worksheet.set_row(i, 25)
            worksheet.merge_range(i, 0 ,i , 2, '', format1)
            worksheet.write(i, 0, "Veuillez, Monsieur, agréer l'expression de nos "
                                  "salutations les meilleures.", format1)

            worksheet.merge_range(i+1, 0, i+1, 2, '', format1)
            worksheet.set_row(i+1, 25)
            worksheet.write(i+1, 3, "Casablanca, le %s" %(datetime.now().strftime(
                '%d-%m-%Y')), format1)

            worksheet.set_row(i+2, 25)
            worksheet.merge_range(i + 3, 0, i + 3, 1, '', format1)
            worksheet.write(i + 3, 0, "Téléphone: + 212 (0) 5 37 56 60 52 / 53",
                            format0)
            worksheet.write(i + 3, 2, "Email: contact@icesco.org",
                            format0)
            worksheet.write(i + 3, 3, "Site: http://www.icesco.org",
                            format0)
