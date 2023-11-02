import datetime as dt
import locale
import time
from datetime import timedelta, datetime
from odoo import models,fields
import base64
import io
from io import BytesIO

class IrRecruitementScoringXlsx(models.AbstractModel):
    _name = 'report.isesco_hr.report_ir_recruitement_scoring_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    def generate_xlsx_report(self, workbook, data, datas):
        locale.setlocale(locale.LC_ALL,
                         'fr_FR.UTF-8')
        i = 1
        s = 1


        report_name = "Recruitement Committee Scoring"

        worksheet1 = workbook.add_worksheet(report_name)


        # for line in datas:
        format0 = workbook.add_format(
            {'font_size': 16, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'black', 'bg_color': '#1E375E'})

        format1 = workbook.add_format(
            {'font_size': 18, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'black', 'bg_color': 'white', 'bold': True, 'border': 2, 'border_color': '#0074BB'})
        format11 = workbook.add_format(
            {'font_size': 18, 'align': 'left', 'valign': 'vcenter',
             'font_color': '#495057', 'bg_color': 'white', 'bold': True})

        format4 = workbook.add_format(
            {'font_size': 13, 'align': 'center', 'valign': 'vcenter',
             'font_color': 'black', 'bg_color': 'white',
             'border': 2, 'border_color': '#0074BB'})
        format2 = workbook.add_format(
            {'font_size': 12, 'align': 'left', 'valign': 'vcenter',
             'font_color': '354F6D', 'bg_color': 'white',
              'border': 2, 'border_color': '#0074BB'})
        format9 = workbook.add_format(
            {'font_size': 12, 'align': 'left', 'valign': 'vcenter',
             'font_color': '354F6D', 'bg_color': 'white',
             'border': 2, 'border_color': '#0074BB'})

        format8 = workbook.add_format(
            {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
             'font_color': '1E375E', 'bg_color': 'white','bold': True,
             'border': 2, 'border_color': '#539FD5'})
        format10 = workbook.add_format(
            {'font_size': 12, 'align': 'left', 'valign': 'vcenter',
             'font_color': 'white', 'bg_color': '008484','bold': True,
             'border': 2, 'border_color': '#0074BB'})
        format5 = workbook.add_format(
            {'font_size': 14, 'align': 'L', 'valign': 'vcenter',
             'font_color': '354F6D', 'bg_color': 'white',
             'border': 2, 'border_color': '0074BB'})
        format6 = workbook.add_format(
            {'font_size': 12, 'align': 'center', 'valign': 'vcenter',
             'font_color': '#354F6D', 'bg_color': 'white',
             'border': 2, 'border_color': '0074BB'})



        worksheet1.set_row(0, 40)
        worksheet1.set_row(1, 40)
        worksheet1.set_row(2, 40)
        worksheet1.set_row(3, 40)
        worksheet1.set_row(4, 40)
        worksheet1.set_row(5, 40)
        worksheet1.set_row(6, 40)
        worksheet1.set_row(7, 40)
        worksheet1.set_row(8, 40)
        worksheet1.set_row(9, 40)
        worksheet1.set_row(10, 40)
        worksheet1.set_row(11, 40)
        worksheet1.set_row(12, 40)
        worksheet1.set_row(13, 40)
        worksheet1.set_row(14, 40)

        worksheet1.set_column('A:A', 20)
        worksheet1.set_column('B:B', 20)
        worksheet1.set_column('C:C', 20)
        worksheet1.set_column('D:D', 20)
        worksheet1.set_column('E:E', 20)
        worksheet1.set_column('F:F', 20)
        worksheet1.set_column('G:G', 20)
        worksheet1.set_column('H:H', 20)
        worksheet1.set_column('I:I', 20)
        worksheet1.set_column('J:J', 20)
        worksheet1.set_column('K:K', 20)
        worksheet1.set_column('L:L', 20)
        worksheet1.set_column('M:M', 20)







        worksheet1.merge_range('A1:J1', '%s' % ("Recruitement Committee Scoring Sheet"), format1)
        n = i
        i = 2



        for interviewr in self.env['hr.applicant'].search([('id', 'in', datas.ids)]).mapped('interview_ids').mapped('interview_lines').mapped('interviewr_id'):
            worksheet1.set_row(i, 40)
            worksheet1.set_row(i+1, 40)
            worksheet1.set_row(i+2, 40)
            worksheet1.set_row(i+3, 40)
            worksheet1.merge_range('E%s:J%s' % (i, i), '%s' % (interviewr.name if interviewr.name != False else ''),
                                   format10)

            worksheet1.merge_range('A%s:B%s' % (i, i+2), 'Candidate Name', format10)

            worksheet1.merge_range('C%s:C%s' % (i, i+2), 'Position', format10)
            worksheet1.merge_range('D%s:D%s' % (i, i+2), 'Date of interviews', format10)
            # worksheet1.merge_range('D%s:D%s' % (i, i), 'Date of interviews', format10)
            worksheet1.write('E%s:E%s' % (i+1, i+1), 'Knowledge of the field', format10)
            worksheet1.write('F%s:F%s' % (i+1, i+1), 'Leadership Quality', format10)
            worksheet1.write('G%s:G%s' % (i+1,i+1), 'EQ', format10)
            worksheet1.write('H%s:H%s' % (i+1, i+1), 'Experience', format10)
            worksheet1.write('I%s:I%s' % (i+1, i+1), 'Languages', format10)
            worksheet1.write('J%s:J%s' % (i+1, i+1), 'Total', format10)
            worksheet1.write('E%s:E%s' % (i+2, i+2), '/35', format10)
            worksheet1.write('F%s:F%s' % (i+2, i+2), '/20', format10)
            worksheet1.write('G%s:G%s' % (i+2, i), '/15', format10)
            worksheet1.write('H%s:H%s' % (i+2,i+2), '/15', format10)
            worksheet1.write('I%s:I%s' % (i+2, i+2), '/15', format10)
            worksheet1.write('J%s:J%s' % (i+2, i+2), '/100', format10)
            # i += len(self.env['hr.applicant'].search([('id', 'in', datas.ids)]).mapped('interview_ids').mapped('interview_lines').mapped('interviewr_id'))


            print('len',len(self.env['hr.applicant'].search([('id', 'in', datas.ids)]).mapped('interview_ids')) )

            i = i + 3

            # i += len(self.env['hr.applicant'].search([('id', 'in', datas.ids)]).mapped('interview_ids'))
            #
            s = 1
            for interview in self.env['hr.applicant'].search([('id', 'in', datas.ids)]).mapped('interview_ids'):
                print('interview',interview)


                score = self.env['hr.applicant'].search([('id', 'in', datas.ids)]).mapped('interview_ids').mapped('interview_lines').filtered(lambda a: a.interviewr_id.id == interviewr.id and a.interviews_id.id == interview.id )
                print('score', score)
            # for interview in interview.applicant_id.interview_ids:
            #     for l in interview.interview_lines:
            #         worksheet1.merge_range('E2:J2','%s' % (score.interviewr_id.name if score.interviewr_id.name != False else ''), format10)


                if len(score) > 0:
                    worksheet1.set_row(i, 40)
                    #
                    worksheet1.write('A%s:A%s' % (i, i),
                                     '%.f' % (s), format2)
                    worksheet1.write('B%s:B%s' % (i, i), '%s' % (interview.applicant_id.partner_name if interview.applicant_id.partner_name != False else ''), format2)
                    worksheet1.write('C%s:C%s' % (i, i), '%s' % (interview.applicant_id.job_id.display_name if interview.applicant_id.job_id.display_name != False else ''), format2)
                    worksheet1.write('D%s:D%s' % (i, i), '%s' % (interview.date_interview if interview.date_interview != False else ''), format2)
                    worksheet1.write('E%s:E%s' % (i, i), '%.2f' % (score.knowledge_field if score.knowledge_field != 0 else 0), format2),

                    worksheet1.write('F%s:F%s' % (i, i),'%.2f' % (score.leadership_quality if score.leadership_quality != 0 else 0), format2)
                    worksheet1.write('G%s:G%s' % (i, i),'%.2f' % (score.eq if score.eq != 0 else 0),format2)
                    worksheet1.write('H%s:H%s' % (i, i),'%.2f' % (score.experience if score.experience != 0 else 0), format2)
                    worksheet1.write('I%s:I%s' % (i, i),'%.2f' % (score.languages if score.languages != 0 else 0),format2)
                    worksheet1.write('J%s:J%s' % (i, i),'%.2f' % (score.total if score.total != 0 else 0),format2)

                    # i += len(self.env['hr.applicant'].search([('id', 'in', datas.ids)]).mapped('interview_ids'))
                    i += 1
                    n = i


                    s +=1
        i = n+1
        worksheet1.merge_range('A%s:B%s' % (i + 1, i + 2), 'Candidate Name', format10)

        worksheet1.merge_range('C%s:C%s' % (i + 1, i + 2), 'Position', format10)
        worksheet1.merge_range('D%s:D%s' % (i + 1, i + 2), 'Date of interviews', format10)
        worksheet1.write('E%s:E%s' % (i + 1, i + 1), 'Total Scores', format10)
        worksheet1.write('E%s:E%s' % (i + 2, i + 2), '/100', format10)

        worksheet1.merge_range('F%s:J%s' % (i + 1, i + 2), 'Comments ', format10)
        seq = 1
        for condidate in self.env['hr.applicant'].search([('id', 'in', datas.ids)]):
            print('condidate', condidate)

            score = self.env['hr.applicant'].search([('id', 'in', datas.ids)]).filtered(lambda x: x.partner_name == condidate.partner_name).mapped(
                'interview_ids')
            print('score', score)
            # for interview in interview.applicant_id.interview_ids:
            #     for l in interview.interview_lines:
            #         worksheet1.merge_range('E2:J2','%s' % (score.interviewr_id.name if score.interviewr_id.name != False else ''), format10)

            if len(score) > 0:


                worksheet1.set_row(i, 40)
                #
                worksheet1.write('A%s:A%s' % (i+3,i+3),
                                 '%.f' % (seq), format2)
                worksheet1.write('B%s:B%s' % (i+3,i+3), '%s' % (
                    condidate.partner_name if condidate.partner_name != False else ''),
                                 format2)
                worksheet1.write('C%s:C%s' % (i+3,i+3), '%s' % (
                    condidate.job_id.display_name if condidate.job_id.display_name != False else ''),
                                 format2)
                worksheet1.write('D%s:D%s' % (i+3,i+3), '%s' % (
                    score[-1].date_interview if score[-1].date_interview != False else ''), format2)
                worksheet1.write('E%s:E%s' % (i+3,i+3),
                                 '%.2f' % (score[-1].total if score[-1].total != 0 else 0),
                                 format2)
                worksheet1.merge_range('F%s:J%s' % (i+3,i+3),
                                 '%s' % (score[-1].comment if score[-1].comment != 0 else ''),
                                 format2)
                seq +=1



                    # i += len(self.env['hr.applicant'].search([('id', 'in', datas.ids)]).mapped('interview_ids'))
                i += 1



