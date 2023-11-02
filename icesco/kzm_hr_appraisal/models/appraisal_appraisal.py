# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json
from lxml import etree
from itertools import groupby
import base64
from datetime import date
import datetime as dt

class AppraisalAppraisal(models.Model):
    _name = 'appraisal.appraisal'
    _description = 'Appraisal'

    def get_domain_employees(self):
        if self.env.user.has_group('kzm_hr_appraisal.appraisal_group_administrator'):
            return []
        else:
            return [('appraisal_manager_id', '=', self.env.user.id)]

    name = fields.Char(string="Reference", default='New')
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True,
                                  domain=get_domain_employees)
    department_id = fields.Many2one('hr.department', string="Department", compute='champs_employee', store=True, readonly=True)
    salary_category_id = fields.Many2one('hr.category', string="Salary Category", compute='champs_employee', store=True, readonly=True)
    recruitment_date = fields.Date(string="Recruitment Date", compute='champs_employee', store=True, readonly=True)

    @api.depends('employee_id')
    def champs_employee(self):
        for rec in self:
            if rec.employee_id.department_id.id != False:
                rec.department_id = rec.employee_id.department_id.id
            else:
                rec.department_id = False

            if rec.employee_id.category_id.id != False:
                rec.salary_category_id = rec.employee_id.category_id.id
            else:
                rec.salary_category_id = False

            if rec.employee_id.date != False:
                rec.recruitment_date = rec.employee_id.date
            else:
                rec.recruitment_date = False

    model_evaluation_id = fields.Many2one('appraisal.model', string='model')
    evaluator_id = fields.Many2one('res.users', string='Evaluator', domain=lambda self: [("groups_id", "=", self.env.ref("kzm_hr_appraisal.appraisal_group_evaluator").id)])
    evaluation_date = fields.Date("Evaluation date", default=fields.Date.today())
    state = fields.Selection([
        ('draft', 'Draft'),
        ('validation', 'Validation'),
        ('approved', 'Approved'),
        ('closed', 'Closed'),
    ], string="State", default='draft')
    maximal_note = fields.Integer(string="Maximal Note", default=100, readonly=1)
    appraisal_note = fields.Integer(string="Appraisal Note",
                                    compute='get_appraisal_note')

    # dh_appraisal_note = fields.Integer(string="Note")
    dh_remarque = fields.Char(string="Remarque")

    stored_appraisal_note = fields.Integer(string="Appraisal Note",
                                    compute='get_store_appraisal_note', store=True)

    appraisal_note_percent = fields.Float(string="Appraisal Note",
                                    compute='get_appraisal_note')

    appraisal_line_ids = fields.One2many('appraisal.appraisal.line', 'appraisal_id',
                                         string="Appraisal Lines")
    appraisal_axis_ids = fields.One2many('appraisal.axis.line', 'appraisal_id',
                                         string="Appraisal Axis ")
    appraisal_comment_ids = fields.One2many('appraisal.comment.line', 'appraisal_id',
                                            string="Appraisal Comments ")
    appraisal_id = fields.Many2one('appraisal.appraisal', string="Appraisal")
    appreciation = fields.Selection([
        ('weak', 'Weak'),
        ('good', 'Good'),
        ('very_good', 'Very good'),
        ('excellent', 'Excellent'),
        ('very_satisfied', 'Very satisfied'),
        ('somewhat_satisfied', 'Somewhat satisfied'),
        ('neither_satisfied', 'Neither satisfied nor dissatisfied'),
        ('somewhat_dissatisfied', 'Somewhat dissatisfied'),
        ('very_dissatisfied', 'Very dissatisfied'),
    ], string="Appreciation", compute='set_variables')
    recommended_action = fields.Text(string="Recommended Action",
                                     compute='set_variables')
    decision = fields.Text(translate=True,string="Decision")
    step_advancement = fields.Integer(string="Step Advancement",
                                      compute='set_variables')
    # employee_recontracted = fields.Selection([
    #     ('yes', 'Yes'),
    #     ('no', 'No')],
    #     string="Does the appraiser recommend the employee to be recontracted?")

    def set_variables(self):
        for rec in self:
            rec.appreciation = False
            rec.recommended_action = False
            rec.step_advancement = False
            for matrix in rec.model_evaluation_id.matrix_id.matrix_line_ids:
                if matrix.minimal_note <= rec.appraisal_note <= matrix.maximal_note:
                    rec.appreciation = matrix.appreciation
                    rec.recommended_action = matrix.impact
                    rec.step_advancement = matrix.step_advancement
                    break

    @api.model
    def create(self, vals):
        if self.env['hr.employee'].search([('id', '=', vals.get('employee_id'))]).is_member_state == True:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'dh.appraisal.appraisal') or 'New'
        else:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'appraisal.appraisal') or 'New'
        res = super(AppraisalAppraisal, self).create(vals)
        return res

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        res = super(AppraisalAppraisal, self).fields_view_get(view_id=view_id,
                                                              view_type=view_type,
                                                              toolbar=toolbar,
                                                              submenu=submenu)
        if view_type in ['form']:
            doc = etree.XML(res['arch'])
            for node in doc.xpath("//field"):
                modifiers = json.loads(node.get("modifiers"))
                modifiers['readonly'] = [('state', 'in', ['approved', 'closed'])]
                node.set("modifiers", json.dumps(modifiers))
            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res

    @api.onchange('employee_id')
    def set_managaer_appraisal_(self):
        self.evaluator_id = self.employee_id.appraisal_manager_id

    def action_validate(self):
        self.mailmessage()
        self.write({'state': 'validation'})

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_close(self):
        self.write({'state': 'closed'})

    def action_draft(self):
        self.write({'state': 'draft'})

    def func(self, arr, max_=None):
        if (max_ is None):
            max_ = arr.pop()
        current = arr.pop()
        if (current > max_):
            max_ = current
        if (arr):
            return self.func(arr, max_)
        return max_

    def get_appraisal_note(self):
        for rec in self:
            sum = 0
            max = 0
            for line in rec.appraisal_line_ids:
                sum += line.note_id.name
                max += self.func(line.factor_id.mapped('value_ids').mapped('name'))

            note = (sum / max) * 100
            rec.appraisal_note = note
            rec.appraisal_note_percent = note / 100
            rec.get_store_appraisal_note()

    @api.depends('appraisal_note')
    def get_store_appraisal_note(self):
        for rec in self:
            rec.stored_appraisal_note = rec.appraisal_note

    @api.onchange('model_evaluation_id')
    def set_appraisal_line_ids(self):
        self.appraisal_line_ids = False
        self.appraisal_comment_ids = False
        self.appraisal_axis_ids = False
        factors = []
        comm = []
        for factor in self.model_evaluation_id.factor_ids:
            factors.append((0, 0, {
                'number': factor.number,
                'factor_id': factor.id,
                'description': factor.description,
                'axe_id': factor.axe_id,
            }))
            if factor.axe_id not in comm:
                comm.append(factor.axe_id)

        self.appraisal_line_ids = sorted(factors, key=lambda tup: int(
            tup[2]['number'].split('.')[0]))

        axes = []
        for axe in self.model_evaluation_id.axe_evaluation__ids:
            axes.append((0, 0, {
                'evaluation_axe_id': axe.id,
            }))
        self.appraisal_comment_ids = axes

        comm = []
        for factor in self.model_evaluation_id.factor_ids:
            if factor.axe_id not in comm:
                comm.append(factor.axe_id)
        comments = []
        for id in comm:
            sum = 0
            for fa in self.appraisal_line_ids:
                if id == fa.axe_id:
                    sum += fa.note_id.name
            comments.append((0, 0, {
                'axe_id': id.id,
            }))

        self.appraisal_axis_ids = comments

    @api.onchange('appraisal_line_ids')
    def get_total_note(self):
        for rec in self:
            for axe in rec.appraisal_axis_ids:
                sum_note = 0
                lines = rec.appraisal_line_ids.filtered(lambda r: r.axe_id == axe.axe_id)
                for line in lines:
                    if line.note_id:
                        sum_note += line.note_id.name
                axe.total_note = sum_note

    def get_factors(self):
        """group by axe"""
        grouped_axes = groupby(
            sorted(self.appraisal_line_ids, key=lambda line: line.axe_id),
            key=lambda line: line.axe_id)
        t = []
        for i, h in grouped_axes:
            val = []
            cmpt = 0
            for n in h:
                cmpt += 1
                max_note = 0
                if n.factor_id.value_ids:
                    max_note = max(note.name for note in n.factor_id.value_ids)
                val.append([n, n.note_id, max_note])
            t.append([i, val, cmpt])
        return t

    def mailmessage(self):
        for rec in self.env['appraisal.appraisal'].browse(self._context.get('active_ids', [])):
            if rec.appreciation == 'good':
                template_id = self.env.ref('kzm_hr_appraisal.mail_evaluation_good')  # xml id of your email template
                attachmentss = []
                content, content_type = self.env.ref('kzm_hr_appraisal.annual_appraisal_menu_id').render_qweb_pdf(
                    rec.id)
                evaluation_infos = self.env['ir.attachment'].create({
                    'name': 'Evaluation %s.pdf' % rec.name,
                    'type': 'binary',
                    'datas': base64.encodestring(content),
                    'res_model': 'appraisal.appraisal',
                    'res_id': rec.id,
                    'mimetype': 'application/x-pdf'
                })
                # evaluation_infos = self.env['ir.attachment'].search([('name', '=', 'FEEDBACK ANNUAL APPRAISAL')])
                attachmentss.append(evaluation_infos.id)
            else:
                template_id = self.env.ref('kzm_hr_appraisal.mail_evaluation')  # xml id of your email template
                attachmentss = []
                content, content_type = self.env.ref('kzm_hr_appraisal.annual_appraisal_menu_id').render_qweb_pdf(
                    rec.id)
                evaluation_infos = self.env['ir.attachment'].create({
                    'name': 'Evaluation %s.pdf' % rec.name,
                    'type': 'binary',
                    'datas': base64.encodestring(content),
                    'res_model': 'appraisal.appraisal',
                    'res_id': rec.id,
                    'mimetype': 'application/x-pdf'
                })
                # evaluation_infos = self.env['ir.attachment'].search([('name', '=', 'FEEDBACK ANNUAL APPRAISAL')])
                attachmentss.append(evaluation_infos.id)

            # salarie
            for user in rec.employee_id:
                template_id.email_to = user.work_email
                template_id.reply_to = user.work_email
                template_id.email_from = self.env['res.users'].search([('id', '=', self.env.uid)]).login
                if user:
                    name = user.name + ' ' + user.prenom
                else:
                    name = ''
                template_context = {
                    'name': name,
                    'last_year': format(dt.date.today().replace(month=1, day=1) - dt.timedelta(days=1), '%Y'),
                    'this_year': str(date.today().year),
                }
                template_id.with_context(**template_context).send_mail(rec.id, force_send=True, email_values={
                    'attachment_ids': evaluation_infos})



        for manager in self.env['appraisal.appraisal'].search([('id', 'in', self._context.get('active_ids', []))]).mapped('employee_id.appraisal_manager_id'):
            manager_attachmentss = []
            for rec in self.env['appraisal.appraisal'].search([('id', 'in', self._context.get('active_ids', []))]).filtered(lambda x:x.employee_id.appraisal_manager_id.id == manager.id and x.appreciation == 'good'):
                template_id = self.env.ref('kzm_hr_appraisal.mail_evaluation_manager')  # xml id of your email template

                content, content_type = self.env.ref('kzm_hr_appraisal.annual_appraisal_menu_id').render_qweb_pdf(
                    rec.id)
                evaluation_infos = self.env['ir.attachment'].create({
                    'name': 'Evaluation %s.pdf' % rec.name,
                    'type': 'binary',
                    'datas': base64.encodestring(content),
                    'res_model': 'appraisal.appraisal',
                    'res_id': rec.id,
                    'mimetype': 'application/x-pdf'
                })
                manager_attachmentss.append(evaluation_infos.id)

            # manager
            if len(manager_attachmentss) > 0:
                template_id.email_to = manager.login
                template_id.reply_to = manager.login
                template_id.email_from = self.env['res.users'].search([('id', '=', self.env.uid)]).login
                name = manager.display_name
                template_context = {
                    'name': name,
                }
                template_id.with_context(**template_context).send_mail(rec.id, force_send=True, email_values={
                    'attachment_ids': manager_attachmentss})

class AppraisalAppraisalLine(models.Model):
    _name = 'appraisal.appraisal.line'
    _description = 'Appraisal Line'

    factor_id = fields.Many2one('appraisal.rating.factor', "Factor")
    number = fields.Char(string="Number")
    description = fields.Text(translate=False,string="Description")
    note_id = fields.Many2one('appraisal.rating.factor.value', "Note")
    level = fields.Selection([
        # ('weak', 'Weak'),
        # ('good', 'Good'),
        # ('very_good', 'Very good'),
        # ('excellent', 'Excellent'),
        ('very_satisfied', 'Very satisfied'),
        ('somewhat_satisfied', 'Somewhat satisfied'),
        ('neither_satisfied', 'Neither satisfied nor dissatisfied'),
        ('somewhat_dissatisfied', 'Somewhat dissatisfied'),
        ('very_dissatisfied', 'Very dissatisfied'),
    ], string="Level")
    appraisal_id = fields.Many2one('appraisal.appraisal', string="Appraisal")
    axe_id = fields.Many2one('appraisal.axis', string="Axe")
    is_very_satisfied = fields.Boolean(string='Very satisfied')
    is_somewhat_satisfied = fields.Boolean(string='Somewhat satisfied')
    is_neither_satisfied = fields.Boolean(string='Neither satisfied nor dissatisfied')
    is_somewhat_dissatisfied = fields.Boolean(string='Somewhat dissatisfied')
    is_very_dissatisfied = fields.Boolean(string='Very dissatisfied')

    @api.onchange('note_id')
    def set_level(self):
        self.level = self.note_id.level

    @api.onchange('level')
    def set_level(self):
        if len(self.factor_id.mapped('value_ids').filtered(lambda x: x.level == self.level)) > 0:
            self.note_id = self.factor_id.mapped('value_ids').filtered(lambda x: x.level == self.level)[0].name

    @api.onchange('is_very_satisfied')
    def onchange_rate_very_satisfied(self):
        for rec in self:
            if rec.is_very_satisfied == True:
                rec.level = 'very_satisfied'
                rec.is_somewhat_satisfied = False
                rec.is_neither_satisfied = False
                rec.is_somewhat_dissatisfied = False
                rec.is_very_dissatisfied = False
            else:
                if rec.level == 'very_satisfied':
                    rec.level = False
            rec.set_level()
    @api.onchange('is_somewhat_satisfied')
    def onchange_rate_somewhat_satisfied(self):
        for rec in self:
            if rec.is_somewhat_satisfied == True:
                rec.level = 'somewhat_satisfied'
                rec.is_very_satisfied = False
                rec.is_neither_satisfied = False
                rec.is_somewhat_dissatisfied = False
                rec.is_very_dissatisfied = False
            else:
                if rec.level == 'somewhat_satisfied':
                    rec.level = False
            rec.set_level()
    @api.onchange('is_neither_satisfied')
    def onchange_rate_neither_satisfied(self):
        for rec in self:
            if rec.is_neither_satisfied == True:
                rec.level = 'neither_satisfied'
                rec.is_very_satisfied = False
                rec.is_somewhat_satisfied = False
                rec.is_somewhat_dissatisfied = False
                rec.is_very_dissatisfied = False
            else:
                if rec.level == 'neither_satisfied':
                    rec.level = False
            rec.set_level()
    @api.onchange('is_somewhat_dissatisfied')
    def onchange_rate_somewhat_dissatisfied(self):
        for rec in self:
            if rec.is_somewhat_dissatisfied == True:
                rec.level = 'somewhat_dissatisfied'
                rec.is_very_satisfied = False
                rec.is_somewhat_satisfied = False
                rec.is_neither_satisfied = False
                rec.is_very_dissatisfied = False
            else:
                if rec.level == 'somewhat_dissatisfied':
                    rec.level = False
            rec.set_level()
    @api.onchange('is_very_dissatisfied')
    def onchange_rate_very_dissatisfied(self):
        for rec in self:
            if rec.is_very_dissatisfied == True:
                rec.level = 'very_dissatisfied'
                rec.is_very_satisfied = False
                rec.is_somewhat_satisfied = False
                rec.is_neither_satisfied = False
                rec.is_somewhat_dissatisfied = False
            else:
                if rec.level == 'very_dissatisfied':
                    rec.level = False
            rec.set_level()


class AppraisalAxisLine(models.Model):
    _name = 'appraisal.axis.line'
    _description = 'Appraisal Axis Line'

    axe_id = fields.Many2one('appraisal.axis', string="Axe")
    total_note = fields.Integer("Total Note")
    comment = fields.Text(translate=True,string="Comment")
    appraisal_id = fields.Many2one('appraisal.appraisal', string="Appraisal")


class AppraisalCommentLine(models.Model):
    _name = 'appraisal.comment.line'
    _description = 'Appraisal Comment Line'

    evaluation_axe_id = fields.Many2one('appraisal.axis.evaluation',
                                        string="Axe Evaluation")
    employee_comment = fields.Text(translate=True,string="Employee Comment")
    evaluator_comment = fields.Text(translate=True,string="Evaluator Comment")
    appraisal_id = fields.Many2one('appraisal.appraisal', string="Appraisal")
