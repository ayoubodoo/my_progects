# -*- coding: utf-8 -*-
import base64

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError



class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    resume_cv = fields.Boolean()
    lettre_motivation = fields.Boolean()
    # meeting_link = fields.Char('Meeting Link ')
    # date_interview = fields.Date('Interview Date ')
    # time_interview = fields.Float('Interview Time ')
    interview_ids = fields.One2many('dh.interviews','applicant_id')
    meeting_link = fields.Char('Meeting Link ')
    text = fields.Text('Text',translate=True)
    category_id = fields.Many2one('hr.category',string="Category")
    category_contract_id = fields.Many2one(related='category_id.category_id',string="Category")
    amount = fields.Float(related='category_id.amount',string="Base Salary")
    family_allowance = fields.Float(string="Family Allowances")
    trans_allowance = fields.Float(string="Transportation Allowance",compute="_get_trans_allowance")
    gross_salary = fields.Float(string="Gross Salary",compute="_get_gross_salary")
    net_salary = fields.Float(string="Net Salary",compute="_get_net_salary")
    grade_id = fields.Many2one(related='category_id.grade_id',string="Grade")
    code = fields.Char(related='category_id.code',string="Code")
    nationality = fields.Many2one('res.country',string='Nationality')

    @api.depends('trans_allowance','family_allowance','amount')
    def _get_gross_salary(self):
        for rec in self:
            rec.gross_salary = False
            if rec.trans_allowance or rec.amount or rec.family_allowance:
                rec.gross_salary = rec.trans_allowance+ rec.family_allowance + rec.amount + rec.amount*0.2+ rec.amount*0.25
    @api.depends('gross_salary')
    def _get_net_salary(self):
        for rec in self:
            rec.net_salary = False
            if rec.gross_salary :
                rec.net_salary = rec.gross_salary - rec.amount*0.0025- rec.amount*0.03



    @api.depends('nationality')
    def _get_trans_allowance(self):
        for rec in self :
            rec.trans_allowance = False
            if rec.nationality.code == 'MA':
                rec.trans_allowance = 0
            else :
                if len(self.env['hr.payroll_ma.rubrique'].search([('is_transport','=',True)]).mapped('line_ids').filtered(lambda x: x.category_id.id == rec.category_contract_id.id)) > 0:
                    rec.trans_allowance = self.env['hr.payroll_ma.rubrique'].search([('is_transport','=',True)]).mapped('line_ids').filtered(lambda x: x.category_id.id == rec.category_contract_id.id)[0].amount
                else:
                    rec.trans_allowance = 0



    def applicant_auto_rejection(self):
        for rec in self.env["hr.applicant"].browse(self._context.get('active_ids', [])):

            template_id = self.env.ref('isesco_hr.mail_applicant_auto_rejection')
            template_id.email_to = rec.email_from
            template_id.reply_to = rec.email_from
            template_id.email_from = 'icescoemployement@icesco.org'
            template_context = {

            }
            template_id.with_context(**template_context).send_mail(rec.id, force_send=True)
    def applicant_rejection(self):
        for rec in self.env["hr.applicant"].browse(self._context.get('active_ids', [])):

            template_id = self.env.ref('isesco_hr.mail_applicant_rejection')
            template_id.email_to = rec.email_from
            template_id.reply_to = rec.email_from
            template_id.email_from = 'icescoemployement@icesco.org'
            template_context = {
                'applicant': rec.partner_name,
                'position': rec.job_id.name,

            }
            template_id.with_context(**template_context).send_mail(rec.id, force_send=True)

    def send_job_offer_mail(self):
        for rec in self.env["hr.applicant"].browse(self._context.get('active_ids', [])):

            content, content_type = self.env.ref('isesco_hr.dh_offer_letter_repport1').render_qweb_pdf(
                self.env['hr.applicant'].search([('id', '=', rec.id)]).id)
            job_offer = self.env['ir.attachment'].create({
                'name': 'Rapport %s.pdf' % self.env['hr.applicant'].search([('id', '=', rec.id)]).name,
                'type': 'binary',
                'datas': base64.encodestring(content),
                'res_model': 'hr.applicant',
                'res_id': self.env['hr.applicant'].search([('id', '=', rec.id)]).id,
                'mimetype': 'application/x-pdf'
            })

            template_id = self.env.ref('isesco_hr.job_offer_mail')
            template_id.email_to = rec.email_from
            template_id.reply_to = rec.email_from
            template_id.email_from = 'icescoemployement@icesco.org'
            template_context = {
                'applicant': rec.partner_name,
                'position': rec.job_id.name,

            }
            template_id.with_context(**template_context).send_mail(rec.id, force_send=True, email_values={
                    'attachment_ids': job_offer})

    def action_send_email1(self):
        content, content_type = self.env.ref('isesco_hr.dh_offer_letter_repport1').render_qweb_pdf(
            self.env['hr.applicant'].search([('id', '=', self.id)]).id)
        job_offer = self.env['ir.attachment'].create({
            'name': 'Rapport %s.pdf' % self.env['hr.applicant'].search([('id', '=', self.id)]).name,
            'type': 'binary',
            'datas': base64.encodestring(content),
            'res_model': 'hr.applicant',
            'res_id': self.env['hr.applicant'].search([('id', '=', self.id)]).id,
            'mimetype': 'application/x-pdf'
        })

        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = \
                ir_model_data.get_object_reference('isesco_hr', 'job_offer_mail')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'hr.applicant',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'attachment_ids': job_offer,
        }
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,

        }

    date_birth = fields.Date(string='Date Naissance')
    adresse = fields.Date(string='Adresse')
    nationality = fields.Many2one('res.country', string='Nationalité')
    country_residince = fields.Many2one('res.country', string='Pays résidence')
    city = fields.Many2one('res.city', string='Ville')
    state = fields.Many2one('res.country.state', string='État')
    zip = fields.Char(string='Code postal')

    bachelor = fields.Char(translate=True,string='Bachelier')
    master = fields.Char(translate=True,string='Master')
    phd = fields.Char(translate=True,string='Doctorat')

    nbr_years_experience = fields.Integer(string='Nbr years experience')
    current_latest_job_title = fields.Char(translate=True,string='Titre poste actuel/dernier')
    societe_job = fields.Char(string='Société poste actuel/dernier')
    had_experience_international_organization = fields.Boolean(string='Avoir expérience dans organisation internationale')
    name_international_organization = fields.Char(translate=True,string='Nom organisation internationale')

    language_1 = fields.Char(translate=True,string='Langue 1')
    language_2 = fields.Char(translate=True,string='Langue 2')
    language_3 = fields.Char(translate=True,string='Langue 3')
    language_4 = fields.Char(translate=True,string='Langue 4')
    language_5 = fields.Char(translate=True,string='Langue 5')

    linkedin_profil = fields.Char('LinkedIn Profile')

    def create_employee_from_applicant(self):
        """ Create an hr.employee from the hr.applicants """
        employee = False
        for applicant in self:
            contact_name = False
            if applicant.partner_id:
                address_id = applicant.partner_id.address_get(['contact'])['contact']
                contact_name = applicant.partner_id.display_name
            else:
                if not applicant.partner_name:
                    raise UserError(_('You must define a Contact Name for this applicant.'))
                new_partner_id = self.env['res.partner'].create({
                    'is_company': False,
                    'type': 'private',
                    'name': applicant.partner_name,
                    'email': applicant.email_from,
                    'phone': applicant.partner_phone,
                    'mobile': applicant.partner_mobile
                })
                address_id = new_partner_id.address_get(['contact'])['contact']
            if applicant.partner_name or contact_name:
                employee = self.env['hr.employee'].create({
                    'name': applicant.partner_name or contact_name,
                    'job_id': applicant.job_id.id or False,
                    'job_title': applicant.job_id.name,
                    'address_home_id': address_id,
                    'department_id': applicant.department_id.id or False,
                    'address_id': applicant.company_id and applicant.company_id.partner_id
                            and applicant.company_id.partner_id.id or False,
                    'work_email': applicant.department_id and applicant.department_id.company_id
                            and applicant.department_id.company_id.email or False,
                    'work_phone': applicant.department_id and applicant.department_id.company_id
                            and applicant.department_id.company_id.phone or False,
                    'date_birth': applicant.date_birth,
                    'adresse': applicant.adresse,
                    'nationality': applicant.nationality.id,
                    'country_residince': applicant.country_residince.id,
                    'city': applicant.city.id,
                    'state': applicant.state.id,
                    'zip': applicant.zip,
                    'bachelor': applicant.bachelor,
                    'master': applicant.master,
                    'phd': applicant.phd,
                    'nbr_years_experience': applicant.nbr_years_experience,
                    'current_latest_job_title': applicant.current_latest_job_title,
                    'societe_job': applicant.societe_job,
                    'had_experience_international_organization': applicant.had_experience_international_organization,
                    'name_international_organization': applicant.name_international_organization,
                    'language_1': applicant.language_1,
                    'language_2': applicant.language_2,
                    'language_3': applicant.language_3,
                    'language_4': applicant.language_4,
                    'language_5': applicant.language_5,
                    'linkedin_profil': applicant.linkedin_profil,
                    'country_id.id': applicant.nationality.id,
                    # 'category_id.id': applicant.category_id.id,
                    # 'category_id.id': applicant.category_id.id,
                    # 'contract_id.wage': applicant.gross_salary,
                    # 'contract_id.grade_id.id': applicant.grade_id.id,
                    # 'contract_id.amount': applicant.amount,
                    # 'wage': applicant.gross_salary,

                # family_allowance = fields.Float(string="Family Allowances")
                # trans_allowance = fields.Float(string="Transportation Allowance", compute="_get_trans_allowance")
                # net_salary = fields.Float(string="Net Salary", compute="_get_net_salary")

                })
                contrat = self.env['hr.contract'].create({
                    'employee_id': rec.id,
                    # 'location_id': rec.type_operation.default_location_src_id.id,
                    # 'location_dest_id': rec.type_operation.default_location_dest_id.id,
                    # # 'partner_id': self.test_partner.id,
                    # 'structure_id': self.entite_demandeur.id,
                    # 'type_demandeur': self.type_demandeur,
                    # 'demande_id': rec.id,
                    # # 'picking_type_id': self.env.ref('stock.picking_type_in').id,
                    # 'is_demande': True
                })


                applicant.write({'emp_id': employee.id})
                if applicant.job_id:
                    applicant.job_id.write({'no_of_hired_employee': applicant.job_id.no_of_hired_employee + 1})
                    applicant.job_id.message_post(
                        body=_('New Employee %s Hired') % applicant.partner_name if applicant.partner_name else applicant.name,
                        subtype="hr_recruitment.mt_job_applicant_hired")
                applicant.message_post_with_view(
                    'hr_recruitment.applicant_hired_template',
                    values={'applicant': applicant},
                    subtype_id=self.env.ref("hr_recruitment.mt_applicant_hired").id)

        employee_action = self.env.ref('hr.open_view_employee_list')
        dict_act_window = employee_action.read([])[0]
        dict_act_window['context'] = {'form_view_initial_mode': 'edit'}
        dict_act_window['res_id'] = employee.id
        return dict_act_window

class DHHrInterviews(models.Model):
    _name = 'dh.interviews'

    applicant_id = fields.Many2one('hr.applicant')

    def open_one2many_line(self, context=None):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Open Line',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': self._name,
            'res_id': self.id,
            'target': 'new',
        }


    meeting_link = fields.Char('Meeting Link ')
    date_interview = fields.Date('Interview Date ')
    time_interview = fields.Float('Interview Time ')
    knowledge_field = fields.Float('Knowledge of the field')
    leadership_quality = fields.Float('Leadership Quality')
    eq = fields.Float('EQ')
    experience = fields.Float('Experience')
    languages = fields.Float('Languages')
    total = fields.Float('Total',compute='_get_total')
    interview_lines = fields.One2many('dh.interviews.lines', 'interviews_id')
    comment = fields.Text('Comment')



    @api.depends('interview_lines')
    def _get_total(self):
        for rec in self:
            rec.total = 0
            if len(rec.interview_lines) > 0:
                rec.total = sum(rec.interview_lines.mapped("total")) / len(rec.interview_lines)

    @api.constrains('knowledge_field', 'leadership_quality', 'eq','experience','languages')
    def check_conge_urgent(self):
        for rec in self:
            if rec.knowledge_field >35:
                raise UserError(_('the value of knowledge field cannot be greater than 35'))
            if rec.leadership_quality >20:
                raise UserError(_('the value of leadrship quality  cannot be greater than 20'))
            if rec.eq >15 :
                raise UserError(_('the value of EQ cannot be greater than 15.'))
            if rec.experience >15 :
                raise UserError(_('the value of Experience cannot be greater than 15.'))
            if rec.languages >15:
                raise UserError(_('the value of languages  cannot be greater than 15.'))


    # def interview_invitation_face_to_face(self):
    #     for rec in self.env["hr.applicant"].browse(self._context.get('active_ids', [])):
    #
    #         if  rec.date_interview and rec.time_interview:
    #             template_id = self.env.ref('isesco_hr.mail_interview_invitation_face_to_face')
    #             template_id.email_to = rec.email_from
    #             template_id.reply_to = rec.email_from
    #             template_id.email_from = 'icescoemployement@icesco.org'
    #             template_context = {
    #                 'applicant': rec.partner_name,
    #                 'position': rec.job_id.name,
    #                 'department': rec.department_id.display_name,
    #                 'date': rec.date_interview,
    #                 'time': '{0:02.0f}:{1:02.0f}'.format(*divmod(rec.time_interview * 60, 60)),
    #
    #                 'link': rec.meeting_link,
    #
    #             }
    #             template_id.with_context(**template_context).send_mail(rec.id, force_send=True)
    #         else:
    #             raise ValidationError(_("You can not send this mail(meeting Link,Interview Date ,and Interview Time	are missing)"))
    #
    # def interview_invitation_online(self):
    #     for rec in self.env["hr.applicant"].browse(self._context.get('active_ids', [])):
    #
    #         if rec.meeting_link and rec.date_interview and rec.time_interview:
    #             template_id = self.env.ref('isesco_hr.mail_interview_invitation_online')
    #             template_id.email_to = rec.email_from
    #             template_id.reply_to = rec.email_from
    #             template_id.email_from = 'icescoemployement@icesco.org'
    #             template_context = {
    #                 'applicant': rec.partner_name,
    #                 'position': rec.job_id.name,
    #                 'department': rec.department_id.display_name,
    #                 'date': rec.date_interview,
    #                 'time': '{0:02.0f}:{1:02.0f}'.format(*divmod(rec.time_interview * 60, 60)),
    #
    #                 'link': rec.meeting_link,
    #
    #             }
    #             template_id.with_context(**template_context).send_mail(rec.id, force_send=True)
    #         else:
    #             raise ValidationError(_("You can not send this mail(meeting Link,Interview Date ,and Interview Time	are missing)"))
    #

    class DHHrInterviewsLines(models.Model):
        _name = 'dh.interviews.lines'

        interviews_id = fields.Many2one('dh.interviews')
        interviewr_id = fields.Many2one('hr.employee')



        knowledge_field = fields.Float('Knowledge of the field')
        leadership_quality = fields.Float('Leadership Quality')
        eq = fields.Float('EQ')
        experience = fields.Float('Experience')
        languages = fields.Float('Languages')
        total = fields.Float('Total', compute='_get_total')

        def generate_excel(self):
            # data = {'month': self.months, 'year': self.years, 'date_start': date(year=int(self.years), month=int(self.months), day=1), 'date_end': date(year=int(self.years), month=int(self.months), day=(date(year=int(self.years), month=int(self.months), day=1) + relativedelta(months=1) - timedelta(days=1)).day)}
            data = {}
            # data = {}
            return self.env.ref('isesco_hr.report_ir_recruitement_scoring_xlsx').report_action(self, data=data)

        def open_one2many_line(self, context=None):
            return {
                'type': 'ir.actions.act_window',
                'name': 'Open Line',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': self._name,
                'res_id': context.get('default_active_id'),
                'target': 'new',
            }

        @api.constrains('knowledge_field', 'leadership_quality', 'eq', 'experience', 'languages')
        def check_conge_urgent(self):
            for rec in self:
                if rec.knowledge_field > 35:
                    raise UserError(_('the value of knowledge field cannot be greater than 35'))
                if rec.leadership_quality > 20:
                    raise UserError(_('the value of leadrship quality  cannot be greater than 20'))
                if rec.eq > 15:
                    raise UserError(_('the value of EQ cannot be greater than 15.'))
                if rec.experience > 15:
                    raise UserError(_('the value of Experience cannot be greater than 15.'))
                if rec.languages > 15:
                    raise UserError(_('the value of languages  cannot be greater than 15.'))

        @api.depends('knowledge_field', 'leadership_quality', 'eq', 'experience', 'languages')
        def _get_total(self):
            for rec in self:
                rec.total = rec.knowledge_field + rec.leadership_quality + rec.eq + rec.experience + rec.languages





