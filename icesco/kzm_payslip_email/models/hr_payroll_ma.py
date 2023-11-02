# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import base64


class HrPayroll_ma(models.Model):
    _inherit = 'hr.payroll_ma'

    def send_emails(self):
        for r in self:
            r.bulletin_line_ids.send_emails()


class HrPayroll_maBulletin(models.Model):
    _inherit = 'hr.payroll_ma.bulletin'

    def send_emails(self):
        template = self.env.ref('kzm_payslip_email.notif_hr_payroll_ma_bulletin', False)
        for bulletin in self:
            if bulletin.employee_id and bulletin.employee_id.work_email:

                content, content_type = self.env.ref('kzm_payroll_ma.bulletin_paie_id').render_qweb_pdf(
                    bulletin.id)
                bulletin_paie_att = self.env['ir.attachment'].create({
                    'name': 'Bulletin %s.pdf' %  bulletin.period_id.name,
                    'type': 'binary',
                    'datas': base64.encodestring(content),
                    'res_model': 'hr.payroll_ma.bulletin',
                    'res_id': bulletin.id,
                    'mimetype': 'application/x-pdf'
                })

                email_values = {
                    'email_to': bulletin.employee_id.work_email,
                    'attachment_ids':[(6, 0, [bulletin_paie_att.id])]
                }
                self.env['mail.template'].browse(template.id).send_mail(bulletin.id, email_values=email_values,
                                                                        force_send=False, raise_exception=True)

