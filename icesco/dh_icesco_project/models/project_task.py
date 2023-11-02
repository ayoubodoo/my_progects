# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import ValidationError, UserError

class DhcpsExpense1(models.Model):
    _inherit = 'hr.expense'

    _order = 'seq'
    seq = fields.Char(required=False, readonly=True, copy=False)

    signature_dg = fields.Binary(string='DG Singature')
    signature_directorate_financial_affairs = fields.Binary(string='Directorate of Financial Affairs')
    signature_financal_controller = fields.Binary(string='Financal controller')
    date_signature_financal_controller = fields.Date("Financal Controller  Approval Date")
    date_adm_affairs = fields.Date(" Approbation Administrative Affairs Approval Date")
    date_dg = fields.Date("Approval DG Date")
    task_id = fields.Many2one('project.task', string="Task")
    other_info = fields.Html('Other informations')
    cooperating_party = fields.Char('Cooperating party')
    implementation_party = fields.Char('Implementation party')

    venue_implementation = fields.Char('Venue of implementation')
    date_implementation = fields.Char('Date of implementation')

    form_numero = fields.Char(compute="get_form_numero")
    achievement_budget = fields.Float(string="Achievement budget" , compute="get_achievement_budget")

    # sub_task_id = fields.Many2one('project.task', string="Mission")
    @api.depends('task_id')
    def get_achievement_budget(self):
        for rec in self :
            rec.achievement_budget = 0
            if rec.task_id.budget_icesco and rec.task_id.budget_out_icesco:
                rec.achievement_budget = rec.task_id.budget_icesco + rec.task_id.budget_out_icesco

    @api.depends('task_id')
    def get_form_numero(self):
        for rec in self:
            rec.form_numero = ""
            if rec.task_id.department_id :
                rec.form_numero = str( rec.task_id.department_id.seq) + "." + str(rec.task_id.sequence) + "." + str(rec.seq)
    @api.model
    def create(self, vals):
        if vals.get('seq', _('New')) == _('New'):
            vals['seq'] = self.env['ir.sequence'].next_by_code(
                'sequence_hr_expense.hr.expense') or _(
                'New')
        return super(DhcpsExpense1, self).create(vals)


    # @api.model
    # def create(self, vals):
    #     res = super(DhcpsExpense1, self).create(vals)
    #     if res.signature_dg:
    #         res.date_dg = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     if res.signature_directorate_financial_affairs:
    #         res.date_adm_affairs = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     if res.signature_financal_controller:
    #         res.date_signature_financal_controller = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #
    # def write(self, vals):
    #     res = super().write(vals)
    #     if res.signature_dg:
    #         res.date_dg = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     if res.signature_directorate_financial_affairs:
    #         res.date_adm_affairs = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     if res.signature_financal_controller:
    #         res.date_signature_financal_controller = datetime.now().strftime('%Y-%m-%d %H:%M:%S'

    @api.model
    def create(self, vals):
        res = super(DhcpsExpense1, self).create(vals)
        # if res.task_id:
        if res.signature_dg:
            res.date_dg = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if res.signature_directorate_financial_affairs:
            res.date_adm_affairs = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if res.signature_financal_controller:
            res.date_signature_financal_controller = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if res.task_id:
            res.task_id.get_consumed_budget()


        if self.env['project.task'].search([('id','=',res.task_id.id)]).budget_remaining < 0 :
            template_id = self.env.ref('dh_icesco_project.mail_budget_remaining')
            template_id.email_to = self.env['project.task'].search([('id','=',res.task_id.id)]).user_id.email
            template_id.reply_to = self.env['project.task'].search([('id','=',res.task_id.id)]).user_id.email
            template_id.email_from = 'icescoemployement@icesco.org'
            template_context = {
                'task': res.env['project.task'].search([('id', '=', res.task_id.id)]).name,
                'project': res.env['project.task'].search([('id', '=', res.task_id.id)]).project_id.name,
                'remaining_budget': res.env['project.task'].search([('id', '=', res.task_id.id)]).budget_remaining,

            }
            template_id.with_context(**template_context).send_mail(res.id, force_send=True)
            print('usersss',self.env.ref('cps_icesco.icesco_financial_controller').users)
            if len(self.env.ref('cps_icesco.icesco_financial_controller').users.ids) != 0:
                for user in  self.env.ref('cps_icesco.icesco_financial_controller').users :
                    template_id = self.env.ref('dh_icesco_project.mail_budget_remaining')
                    template_id.email_to = user.login
                    template_id.reply_to = user.login
                    template_id.email_from = 'icescoemployement@icesco.org'
                    template_context = {
                        'task': res.env['project.task'].search([('id', '=', res.task_id.id)]).name,
                'project': res.env['project.task'].search([('id', '=', res.task_id.id)]).project_id.name,
                'remaining_budget': res.env['project.task'].search([('id', '=', res.task_id.id)]).budget_remaining,

                    }
                    template_id.with_context(**template_context).send_mail(res.id, force_send=True)


        return res

    def write(self, vals):
        res = super(DhcpsExpense1, self).write(vals)
        # if res.get('task_id'):
        if "signature_dg" in vals:
            if vals['signature_dg'] != False :
              self.date_dg = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if "signature_directorate_financial_affairs" in vals:
            if  vals['signature_directorate_financial_affairs'] != False :
                self.date_adm_affairs = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if "signature_financal_controller" in vals:
            if vals['signature_financal_controller'] != False :
                self.date_signature_financal_controller = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if self.task_id:
            self.task_id.get_consumed_budget()

        if self.env['project.task'].search([('id','=',self.task_id.id)]).budget_remaining < 0 :
            template_id = self.env.ref('dh_icesco_project.mail_budget_remaining')
            template_id.email_to = self.env['project.task'].search([('id','=',self.task_id.id)]).user_id.email
            template_id.reply_to = self.env['project.task'].search([('id','=',self.task_id.id)]).user_id.email
            template_id.email_from = 'icescoemployement@icesco.org'
            template_context = {
                  'task': self.env['project.task'].search([('id', '=', self.task_id.id)]).name,
                'project': self.env['project.task'].search([('id', '=', self.task_id.id)]).project_id.name,
                'remaining_budget': self.env['project.task'].search([('id', '=', self.task_id.id)]).budget_remaining,

            }
            template_id.with_context(**template_context).send_mail(self.id, force_send=True)
            if len(self.env.ref('cps_icesco.icesco_financial_controller').users) != 0:
                for user in self.env.ref('cps_icesco.icesco_financial_controller').users:
                    template_id = self.env.ref('dh_icesco_project.mail_budget_remaining')
                    template_id.email_to = user.login
                    template_id.reply_to = user.login
                    template_id.email_from = 'icescoemployement@icesco.org'
                    template_context = {
                        'task': self.env['project.task'].search([('id', '=', self.task_id.id)]).name,
                        'project': self.env['project.task'].search([('id', '=', self.task_id.id)]).project_id.name,
                        'remaining_budget': self.env['project.task'].search(
                            [('id', '=', self.task_id.id)]).budget_remaining,

                    }
                    template_id.with_context(**template_context).send_mail(self.id, force_send=True)

        return res

class DhPurchaseRequest(models.Model):
    _inherit = 'purchase.request'

    project_id = fields.Many2one('project.project', string="Project")
    task_id = fields.Many2one('project.task', string="Task")

class DHPurchaseOrder22(models.Model):
    _inherit = 'purchase.order'

    project_id = fields.Many2one('project.project', string="Project")
    task_id = fields.Many2one('project.task', string="Task")

    @api.model
    def create(self, vals):
        res = super(DHPurchaseOrder22, self).create(vals)
        if res.task_id:
            res.task_id.get_consumed_budget()

        if self.env['project.task'].search([('id', '=', res.task_id.id)]).budget_remaining < 0:

            template_id = self.env.ref('dh_icesco_project.mail_budget_remaining1')
            template_id.email_to = self.env['project.task'].search([('id', '=', res.task_id.id)]).user_id.email
            template_id.reply_to = self.env['project.task'].search([('id', '=', res.task_id.id)]).user_id.email
            template_id.email_from = 'icescoemployement@icesco.org'
            template_context = {
                'task': res.env['project.task'].search([('id', '=', res.task_id.id)]).name,
                'project': res.env['project.task'].search([('id', '=', res.task_id.id)]).project_id.name,
                'remaining_budget': res.env['project.task'].search([('id', '=', res.task_id.id)]).budget_remaining,

            }
            template_id.with_context(**template_context).send_mail(res.id, force_send=True)
            if len(self.env.ref('cps_icesco.icesco_financial_controller').users) != 0:
                for user in self.env.ref('cps_icesco.icesco_financial_controller').users:
                    template_id = self.env.ref('dh_icesco_project.mail_budget_remaining1')
                    template_id.email_to = user.login
                    template_id.reply_to = user.login
                    template_id.email_from = 'icescoemployement@icesco.org'
                    template_context = {
                        'task': res.env['project.task'].search([('id', '=', res.task_id.id)]).name,
                        'project': res.env['project.task'].search([('id', '=', res.task_id.id)]).project_id.name,
                        'remaining_budget': res.env['project.task'].search(
                            [('id', '=', res.task_id.id)]).budget_remaining,

                    }
                    template_id.with_context(**template_context).send_mail(res.id, force_send=True)




        return res

    def write(self, vals):
        res = super(DHPurchaseOrder22, self).write(vals)

        if self.task_id:
            self.task_id.get_consumed_budget()


        if self.env['project.task'].search([('id', '=', self.task_id.id)]).budget_remaining < 0:
            template_id = self.env.ref('dh_icesco_project.mail_budget_remaining1')
            template_id.email_to = self.env['project.task'].search([('id', '=', self.task_id.id)]).user_id.email
            template_id.reply_to = self.env['project.task'].search([('id', '=', self.task_id.id)]).user_id.email
            template_id.email_from = 'icescoemployement@icesco.org'
            template_context = {
                'task': self.env['project.task'].search([('id', '=', self.task_id.id)]).name,
                'project': self.env['project.task'].search([('id', '=', self.task_id.id)]).project_id.name,
                'remaining_budget': self.env['project.task'].search([('id', '=', self.task_id.id)]).budget_remaining,

            }
            template_id.with_context(**template_context).send_mail(self.id, force_send=True)
            if len(self.env.ref('cps_icesco.icesco_financial_controller').users) != 0:
                for user in self.env.ref('cps_icesco.icesco_financial_controller').users:
                    template_id = self.env.ref('dh_icesco_project.mail_budget_remaining1')
                    template_id.email_to = user.login
                    template_id.reply_to = user.login
                    template_id.email_from = 'icescoemployement@icesco.org'
                    template_context = {
                        'task': self.env['project.task'].search([('id', '=', self.task_id.id)]).name,
                        'project': self.env['project.task'].search([('id', '=', self.task_id.id)]).project_id.name,
                        'remaining_budget': self.env['project.task'].search(
                            [('id', '=', self.task_id.id)]).budget_remaining,

                    }
                    template_id.with_context(**template_context).send_mail(res.id, force_send=True)

        return res

class DhTask(models.Model):
    _inherit = 'project.task'

    proposition_id = fields.Many2one('dh.icesco.proposition', string='Proposition')
    sector_dpt_id = fields.Many2one("dh.sector.dpt")
    participation_exxcellency_director = fields.Char(string='Participation of His Excellency the Director General')
    count_number = fields.Integer(string='Count Number', store=True, default=1)
    name = fields.Char(string='Title', tracking=True, required=True, index=True,translate=True)

    # numerotation

    code_pillar = fields.Char(related="pilliar_id.code",string='Pillar Code')
    code_projet = fields.Char(related="project_id.code",string='Project Code')
    code_goal = fields.Char(related="orientation_id.code",string='Goal Code')

    etape_done = fields.Many2one("dh.etapes.done",'Implementation stage')

    date_signature_financal_controller = fields.Date("Financal Controller  Approval Date")
    date_adm_affairs = fields.Date(" Approbation Administrative Affairs Approval Date")
    date_dg = fields.Date("Approval DG Date")
    signature_dg = fields.Binary(string='DG Signature')
    signature_adm_affairs = fields.Binary(string='Administrative Affairs Approval Signature')
    signature_financal_controller = fields.Binary(string='Controller Financial Affairs Approval Signature')

    partenaire_inernal = fields.Many2many("dh.sector" ,string="Internal Partner")



    # Missions Infos
    country_id = fields.Many2one("res.partner" ,string="Country", domain=[('is_member_state', '=', True)])
    beneficiary = fields.Many2one("res.partner" ,string="Beneficiary")
    part_action_plan = fields.Boolean(string="Part of Action plan?")
    is_member_state = fields.Boolean(related="country_id.is_member_state",string="Is member state ?")
    funded_by_icesco = fields.Boolean(string="Partially or Fully funded by ICESCO? ?")
    destination = fields.Char("Destination")
    per_diem = fields.Float("Per diem ($)")
    tickets = fields.Float("Tickets ($)")
    accommodation = fields.Float("Accommodation")
    transportation = fields.Float("Transportation")
    registration_fee = fields.Float("Registration fee")
    extra_weight = fields.Float("Extra Weight")
    medical_expense = fields.Float("Medical expenses (Vaccination...)")
    total_cost = fields.Float("Total Cost",compute="get_total_cost")
    mission_form_ab = fields.Binary("Mission Form A & B")
    mission_repport = fields.Binary("Mission report")
    comments = fields.Html("Mission report")


    def get_total_cost(self):
        for rec in self :
            rec.total_cost = 0
            if rec.per_diem or rec.tickets or  rec.accommodation or rec.transportation or rec.registration_fee or rec.extra_weight or rec.medical_expense :
                rec.total_cost = rec.per_diem + rec.tickets +  rec.accommodation + rec.transportation + rec.registration_fee + rec.extra_weight + rec.medical_expense

    # non_sector_programmes_id  = fields.Many2many('non.sector.programmes',string='Non sector programmes')
    non_sector_programmes_id  = fields.Many2one('non.sector.programmes',string='Non sector programmes', store=True)
    code_activity = fields.Char(string='Code Task', copy=False)
    manner_convening = fields.Char(string='Convening Method')
    code_project = fields.Char(related="project_id.code",string='Code Project', readonly=True, copy=False)
    # billeterie_ids = fields.One2many('cps.expense.billeterie','task_id', string='Bielleterie')
    # expenses_ids = fields.One2many('hr.expense', 'task_id', string='Expense')    # Budget
    budget_initial = fields.Float(string='Initial Budget', store=True)
    budget_remaining = fields.Float(compute='get_remaining_budget', string=' Remaining budget', store=True)
    budget_consumed = fields.Float(string='consumed budget',compute='get_consumed_budget', store=True)
    order_ids = fields.One2many('purchase.order', 'task_id', string="Order lines")
    transfer_ids = fields.One2many('dh.budget.transfert', 'task_ids', string="Transfers ")
    transfer_ids1 = fields.One2many('dh.budget.transfert', 'task_dest_id', string="Transfers ")
    transfer_ids11 = fields.Many2many('dh.budget.transfert', string="Transfers ",compute="_get_transferts")
    expert_task = fields.Many2one('hr.employee', string="Responsible expert ")
    notes = fields.Text(translate=True,string="Notes")




    # @api.model
    # def create(self, vals):
    #     vals['code_activity'] = self.env['ir.sequence'].next_by_code('sequence_code_activity.project.task') or _(
    #         'New')
    #     return super(DhTask, self).create(vals)

    @api.depends("transfer_ids","transfer_ids1")
    def _get_transferts(self):
        for rec in self:
            rec.transfer_ids11 = False
            # for line in self.env['dh.budget.transfert'].search([]).filtered(lambda x: rec.id in x.transfer_ids.ids or  rec.id in x.transfer_ids1.ids):
            for line in self.env['dh.budget.transfert'].search([]).filtered(lambda x: rec.id == x.task_ids.id  or  rec.id == x.task_dest_id.id):
                # print("budgetreee",self.env['dh.budget.transfert'].search([]).filtered(lambda x: rec.id in x.transfer_ids.ids or  rec.id in x.transfer_ids1.ids))
                rec.transfer_ids11 = [(4, line.id)]
    percent_consumed_icesco = fields.Float(compute='percentage_consumed_icesco', string=' Budget accuracy', store=True)

    @api.depends('budget_icesco', 'budget_consumed')
    def percentage_consumed_icesco(self):
        for rec in self:
            rec.percent_consumed_icesco = False
            if rec.budget_consumed and rec.budget_icesco != 0:
                rec.percent_consumed_icesco = rec.budget_consumed/rec.budget_icesco

            # rec.percent_consumed_icesco = False
            # if sum(self.env["project.task"].mapped("budget_icesco")):
            #
            #     rec.percent_consumed_icesco = sum(self.env["project.task"].mapped("budget_consumed"))/sum(self.env["project.task"].mapped("budget_icesco"))


    @api.depends('budget_initial', 'budget_consumed')
    def get_remaining_budget(self):
        for rec in self:
            rec.budget_remaining = False
            if rec.budget_initial and rec.budget_consumed:
                rec.budget_remaining = rec.budget_initial - rec.budget_consumed

    @api.depends('expenses_ids','order_ids')
    def get_consumed_budget(self):
        for rec in self:
            rec.budget_consumed = 0
            if rec.expenses_ids or rec.order_ids:
                rec.budget_consumed = sum(rec.expenses_ids.filtered(lambda x:x.state in ['approved', 'done']).mapped('total_amount')) + sum(rec.order_ids.filtered(lambda x:x.state in ['purchase', 'done']).mapped('amount_total'))




    name = fields.Char(string='النشاط')
    sector_id = fields.Many2one('dh.perf.sector', string='القطاع', default=lambda self: self.project_id.sector_id.id)
    orientation_id = fields.Many2one('dh.orientations', string='الهدف', store=True)
    pilliar_id = fields.Many2one('dh.pilliar', string='المحور', store=True)
    # task_id = fields.Many2one('project.task')
    milestones = fields.One2many('dh.perf.operation', 'project_task_id', string='عمليات')

    type_activity = fields.Many2one('dh.perf.type.activity',store="True", string='نوع النشاط')

    rate_ratio = fields.Integer(string='نسبة الإنجاز')
    state_ratio = fields.Selection([
        ('programmed', 'Programmed'),
        ('encours', 'In Progress'),
        ('succes', 'succes'),
    ], string='Phases ratio', compute='compute_state_ratio')

    @api.depends('rate_ratio')
    def compute_state_ratio(self):
        for rec in self:
            if rec.rate_ratio == 0:
                rec.state_ratio = 'programmed'
            elif rec.rate_ratio == 100:
                rec.state_ratio = 'succes'
            else:
                rec.state_ratio = 'encours'

    date_start = fields.Date(string='تاريخ البدء')
    date_end = fields.Date(string='تاريخ الإنتهاء')

    partenaire_ids = fields.Many2many('res.partner', relation='rel_perff_partner_partenairee_ids', string='الشركاء المقترحين',store=True)

    pays_members_cibles = fields.Many2many('res.partner', relation='rel_perf_pays_member_partner_partenairee_ids', string='الدول الأعضاء المستهدفة', domain=[('is_member_state', '=', True)])
    pays_no_members_cibles = fields.Many2many('res.partner', relation='rel_perf_pays_non_member_partner_partenairee_ids', string='الدول غير الأعضاء المستهدفة', domain=[('is_member_state', '=', False)])

    nombre_beneficiaires = fields.Integer(string='عدد المستفيدين')

    mode_convo = fields.Selection([('face_to_face', 'حضوريا'), ('remote', 'عن بعد'), ('both', 'حضوري/عن بعد'), ('export', 'إصدار'), ('virtual', 'افتراضية')], string='طريقة الإنعقاد')

    budget_icesco = fields.Float(string='الميزانية المخصصة للإيسيسكو')
    budget_out_icesco = fields.Float(string='الميزانية المخصصة خارج الإيسيسكو', store=True) # , compute='get_budget_out_icesco' : comment to import data
    office_id = fields.Many2one('dh.icesco.office', string='The administration concerned')
    @api.depends('budget_extra_reel', 'budget_extra_indirect')
    def get_budget_out_icesco(self):
        for rec in self:
            rec.budget_out_icesco = rec.budget_extra_reel + rec.budget_extra_indirect

    budget_employers = fields.Float(string='ميزانية الموظفين')

    equipe_responsable_ids = fields.Many2many('res.partner', relation='rel_perff_partner_equipe_responsablee_ids',
                                              string='الخبير / الفريق المسؤول')

    equipe_responsable_id = fields.Many2one('res.partner', string='الخبير / الفريق المسؤول')

    result_attendus = fields.Char(string='المخرجات المتوقعة')


    operational_indecator_id = fields.One2many('dh.icesco.operational.indicators', 'task_id', string='المؤشرات التشغيلية')

    operational_indecator_result_id = fields.One2many('dh.icesco.operational.indicators.result', 'task_id', string='نتائج المؤشرات')

    percentage_of_done = fields.Integer(string='نسبة النتائج')

    percentage_of_done_percent = fields.Integer(string='نسبة النتائج', compute='compute_percentage_of_done_percent')

    @api.depends('percentage_of_done')
    def compute_percentage_of_done_percent(self):
        for rec in self:
            rec.percentage_of_done_percent = rec.percentage_of_done / 100

    respect_time = fields.Integer(string='الالتزام بالوقت')

    target = fields.Integer(string='المستهدف', compute='compute_target_actual')
    actual = fields.Integer(string='الفعلي', compute='compute_target_actual')
    target_of_actual = fields.Float(string='المستهدف/الفعلي', compute='compute_target_actual', store=True)

    @api.depends('operational_indecator_id')
    def compute_target_actual(self):
        for rec in self:
            if len(rec.operational_indecator_id) == 0:
                rec.target = 0
                rec.actual = 0
                rec.target_of_actual = 0
            else:
                target_of_actual = 0
                for indicator in rec.operational_indecator_id:
                    if indicator.target > 0:
                        target_of_actual += indicator.actual / indicator.target

                rec.target = sum(rec.operational_indecator_id.mapped('target')) / len(rec.operational_indecator_id)
                rec.actual = sum(rec.operational_indecator_id.mapped('actual')) / len(rec.operational_indecator_id)

                if rec.target_of_actual > 0:
                    rec.target_of_actual = (target_of_actual / len(rec.operational_indecator_id)) * 100
                else:
                    rec.target_of_actual = 0

    budget_total_icesco = fields.Float(compute='get_total_budget',string='الميزانية',store=True)
    year_bud = fields.Date(string='العام',store=True)

    dh_state = fields.Selection([('draft', 'Draft'), ('dg_approval', 'DG Approval'),
                                 ('admin_affair_approval', 'Administrative affairs approval'),
                                 ('financial_affair_approval', 'Financial affairs approval'), ('validate', 'Validate')], default='draft')
    event_id = fields.Many2one('event.event', string='Event')
    date_validation = fields.Date(string='Date Validation')
    dh_attachment_ids = fields.One2many('task.attachment', 'task_id', string='Attachments')

    # supports
    translation = fields.Boolean('Translation')
    is_support_designing = fields.Boolean('Designing & printing')
    is_support_legal = fields.Boolean('Legal')
    is_support_logistics = fields.Boolean('Logistics')
    is_support_protocol = fields.Boolean('Protocol')
    is_support_finance = fields.Boolean('Finance')
    is_support_admin = fields.Boolean('Procurement')
    is_support_it = fields.Boolean('IT')
    is_support_media = fields.Boolean('Media')

    list_translation_service = fields.Many2one('dh.service.department', string="List of Translation services",
                                               domain=[("type_department", "=", 'translation')])
    list_designing_service = fields.Many2one('dh.service.department', string="List of Designing & printing  services",
                                             domain=[("type_department", "=", 'designing_printing')])
    list_legal_service = fields.Many2one('dh.service.department', string="List of Legal services",
                                         domain=[("type_department", "=", 'legal')])
    list_finance_service = fields.Many2one('dh.service.department', string="List of Finance services",
                                           domain=[("type_department", "=", 'finance')])
    list_logistics_service = fields.Many2one('dh.service.department', string="List of Logistics services",
                                             domain=[("type_department", "=", 'logistics')])
    list_admin_service = fields.Many2one('dh.service.department', string="List of Procurement services",
                                         domain=[("type_department", "=", 'procurement')])
    list_it_service = fields.Many2one('dh.service.department', string="List of IT services",
                                      domain=[("type_department", "=", 'it')])
    list_media_service = fields.Many2one('dh.service.department', string="List of Media services",
                                         domain=[("type_department", "=", 'media')])
    list_protocol_service = fields.Many2one('dh.service.department', string="List of Protocol services",
                                            domain=[("type_department", "=", 'protocol')])


    def button_draft(self):
        for rec in self:
            rec.dh_state = 'draft'

    def button_dg_approval(self):
        for rec in self:
            rec.dh_state = 'dg_approval'

    def button_admin_affair_approval(self):
        for rec in self:
            rec.dh_state = 'admin_affair_approval'

    def button_validate(self):
        for rec in self:
            rec.code_activity = self.env['ir.sequence'].next_by_code('sequence_code_activity.project.task')
            rec.dh_state = 'validate'

    def button_financial_affair_approval(self):
        for rec in self:
            if rec.budget_compta == 0:
                raise ValidationError(
                    _("Il n'est pas possible de valider l'activité si le montant reçu en comptabilité est nul.")
                )
            rec.dh_state = 'financial_affair_approval'
            rec.date_validation = fields.Date.today()
            # notifications au cabdg
            for user in self.env['res.users'].search([("groups_id", "=", self.env.ref("dh_icesco_project.group_cabdg").id)]):
                self.env['mail.activity'].create({
                    'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                    'user_id': user.id,
                    'summary': 'Financial affair approved Activity',
                    'note': 'The Activity %s has approved by the financial affair' % (rec.name),
                    'res_model_id': self.env['ir.model']._get('project.task').id,
                    'res_id': rec.id
                })

            # notifications aux differents support defini sur event
            if rec.translation == True:
                for user in self.env['res.users'].search([('is_translation', '=', True)]):
                    self.env['mail.activity'].create({
                        'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                        'user_id': user.id,
                        'summary': 'Financial affair approved Activity',
                        'note': 'The Activity %s has approved by the financial affair' % (rec.name),
                        'res_model_id': self.env['ir.model']._get('project.task').id,
                        'res_id': rec.id
                    })
            if rec.is_support_designing == True:
                for user in self.env['res.users'].search([('is_design', '=', True)]):
                    self.env['mail.activity'].create({
                        'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                        'user_id': user.id,
                        'summary': 'Financial affair approved Activity',
                        'note': 'The Activity %s has approved by the financial affair' % (rec.name),
                        'res_model_id': self.env['ir.model']._get('project.task').id,
                        'res_id': rec.id
                    })

            if rec.is_support_legal == True:
                for user in self.env['res.users'].search([('is_legal', '=', True)]):
                    self.env['mail.activity'].create({
                        'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                        'user_id': user.id,
                        'summary': 'Financial affair approved Activity',
                        'note': 'The Activity %s has approved by the financial affair' % (rec.name),
                        'res_model_id': self.env['ir.model']._get('project.task').id,
                        'res_id': rec.id
                    })

            if rec.is_support_logistics == True:
                for user in self.env['res.users'].search([('is_logistics', '=', True)]):
                    self.env['mail.activity'].create({
                        'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                        'user_id': user.id,
                        'summary': 'Financial affair approved Activity',
                        'note': 'The Activity %s has approved by the financial affair' % (rec.name),
                        'res_model_id': self.env['ir.model']._get('project.task').id,
                        'res_id': rec.id
                    })

            if rec.is_support_protocol == True:
                for user in self.env['res.users'].search([('is_protocol', '=', True)]):
                    self.env['mail.activity'].create({
                        'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                        'user_id': user.id,
                        'summary': 'Financial affair approved Activity',
                        'note': 'The Activity %s has approved by the financial affair' % (rec.name),
                        'res_model_id': self.env['ir.model']._get('project.task').id,
                        'res_id': rec.id
                    })

            if rec.is_support_finance == True:
                for user in self.env['res.users'].search([('is_finance', '=', True)]):
                    self.env['mail.activity'].create({
                        'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                        'user_id': user.id,
                        'summary': 'Financial affair approved Activity',
                        'note': 'The Activity %s has approved by the financial affair' % (rec.name),
                        'res_model_id': self.env['ir.model']._get('project.task').id,
                        'res_id': rec.id
                    })

            if rec.is_support_it == True:
                for user in self.env['res.users'].search([('is_it', '=', True)]):
                    self.env['mail.activity'].create({
                        'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                        'user_id': user.id,
                        'summary': 'Financial affair approved Activity',
                        'note': 'The Activity %s has approved by the financial affair' % (rec.name),
                        'res_model_id': self.env['ir.model']._get('project.task').id,
                        'res_id': rec.id
                    })

            if rec.is_support_admin == True:
                for user in self.env['res.users'].search([('is_admin', '=', True)]):
                    self.env['mail.activity'].create({
                        'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                        'user_id': user.id,
                        'summary': 'Financial affair approved Activity',
                        'note': 'The Activity %s has approved by the financial affair' % (rec.name),
                        'res_model_id': self.env['ir.model']._get('project.task').id,
                        'res_id': rec.id
                    })

            if rec.is_support_media == True:
                for user in self.env['res.users'].search([('is_media', '=', True)]):
                    self.env['mail.activity'].create({
                        'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                        'user_id': user.id,
                        'summary': 'Financial affair approved Activity',
                        'note': 'The Activity %s has approved by the financial affair' % (rec.name),
                        'res_model_id': self.env['ir.model']._get('project.task').id,
                        'res_id': rec.id
                    })

    def mail_notif_attach_tasks(self):
        for rec in self.env['project.task'].search(
                [('dh_state', '=', 'financial_affair_approval'), ('dh_attachment_ids', '=', False)]):
            if rec.date_validation != False:
                if (fields.Date.today() - rec.date_validation).days == int(
                        self.env['ir.config_parameter'].sudo().get_param('cps_icesco.duree_notif_attach')):
                    if len(self.env['mail.activity'].search(
                            [('user_id', '=', rec.create_uid.id),
                             ('summary', 'ilike', 'Task need Attachments'), ('res_id', '=', rec.id)])) == 0:
                        self.env['mail.activity'].create({
                            'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                            'user_id': rec.create_uid.id,
                            'summary': 'Task need Attachments',
                            'note': 'Please fill the attachments of the activity %s' % (rec.name),
                            'res_model_id': self.env['ir.model']._get('project.task').id,
                            'res_id': rec.id
                        })

                    for user in self.env['res.users'].search(
                            [("groups_id", "=", self.env.ref("cps_icesco.icesco_financial_controller").id)]):
                        if len(self.env['mail.activity'].search(
                                [('user_id', '=', user.id),
                                 ('summary', 'ilike', 'Task need Attachments'), ('res_id', '=', rec.id)])) == 0:
                            self.env['mail.activity'].create({
                                'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                                'user_id': user.id,
                                'summary': 'Task need Attachments',
                                'note': 'Please fill the attachments of the activity %s' % (rec.name),
                                'res_model_id': self.env['ir.model']._get('project.task').id,
                                'res_id': rec.id
                            })

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if 'pays_members_cibles' in vals:
            res.change_count_tasks()
        if 'budget_icesco' in vals or 'budget_out_icesco' in vals:
            if res.sector_id.id != False:
                res.sector_id._compute_budget_prevision()
                res.sector_id._compute_budget_hors_prevision()
        return res

    def write(self, vals):
        res = super().write(vals)
        if 'pays_members_cibles' in vals:
            self.change_count_tasks()
        if 'budget_icesco' in vals or 'budget_out_icesco' in vals:
            if self.sector_id.id != False:
                self.sector_id._compute_budget_prevision()
                self.sector_id._compute_budget_hors_prevision()
        return res

    @api.onchange('pays_members_cibles')
    def change_count_tasks(self):
        for rec in self:
            for partner in rec.pays_members_cibles:
                partner._compute_count_activities()

    @api.onchange('project_id')
    def get_sector_pilliar(self):
        for rec in self:
            rec.sector_id = rec.project_id.sector_id.id
            rec.pilliar_id = rec.project_id.pilliar_id.id
            rec.orientation_id = rec.project_id.pilliar_id.orientation_id.id

    @api.depends('budget_icesco','budget_total_icesco')
    def get_total_budget(self):
        for rec in self :
            rec.budget_total_icesco = rec.budget_icesco + rec.budget_out_icesco


    def view_group_by_goal(self):
        return {
            'name': ".",
            'res_model': 'project.task',
            'view_mode': 'tree',
            'view_type': 'tree',
            'views': [(self.env.ref("dh_icesco_project.dh_perf_project_task_tree").id, 'list')],
            'type': 'ir.actions.act_window',
            'domain': self.ids,
            'context': {
                'group_by': 'orientation_id',
            },
        }

    def view_group_by_expert(self):
        return {
            'name': ".",
            'res_model': 'project.task',
            'view_mode': 'tree,form',
            'view_type': 'tree',
            'views': [(self.env.ref("dh_icesco_project.dh_perf_project_task_tree").id, 'list')],
            'type': 'ir.actions.act_window',
            'domain': self.ids,
            'context': {
                'group_by': 'expert_task',
            },
        }

    def view_group_by_sector(self):
        return {
            'name': ".",
            'res_model': 'project.task',
            'view_mode': 'tree,form',
            'view_type': 'tree',
            'views': [(self.env.ref("dh_icesco_project.dh_perf_project_task_tree").id, 'list')],
            'type': 'ir.actions.act_window',
            'domain': self.ids,
            'context': {
                'group_by': 'sector_id',
            },
        }

    def view_indicators_details(self):
        return {
            'name': ".",
            'res_model': 'project.task',
            'view_mode': 'tree,form',
            'view_type': 'tree',
            'views': [(self.env.ref("dh_icesco_project.dh_perf_project_task_details_tree").id, 'list')],
            'type': 'ir.actions.act_window',
            'domain': self.ids,
            'context': self.env.context.get('context', {}),
        }

    def view_indicators_reduits(self):
        return {
            'name': ".",
            'res_model': 'project.task',
            'view_mode': 'tree,form',
            'view_type': 'tree',
            'views': [(self.env.ref("dh_icesco_project.dh_perf_project_task_tree").id, 'list')],
            'type': 'ir.actions.act_window',
            'domain': self.ids,
            'context': self._context.get('context', {}),
        }

    def view_show_indicators(self):
        for rec in self:
            return {
                'name': "المؤشرات التشغيلية",
                'res_model': 'dh.icesco.operational.indicators',
                'view_mode': 'tree',
                'view_type': 'tree',
                'views': [(self.env.ref("dh_icesco_project.cps_dh_icesco_capacity_operational_indicators_tree").id, 'list')],
                'type': 'ir.actions.act_window',
                "domain": [("task_id", "=", rec.id)],
                'context': "{'default_task_id': %s}" % rec.id
            }

    def view_form_activity(self):
        for rec in self:
            return {
                'name': "التفاصيل",
                'res_model': 'project.task',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': rec.id,
                'view_id': self.env.ref("project.view_task_form2").id,
            }

class DhSubTask(models.Model):
    _name = 'project.sub.task'

    name = fields.Char(string='فرع النشاط')

class ReportProjectTaskUser(models.Model):
    _inherit = "report.project.task.user"

    sector_id = fields.Many2one('dh.perf.sector', string='القطاع')

    def _select(self):
        select_str = """
             SELECT
                    (select 1 ) AS nbr,
                    t.id as id,
                    t.date_assign as date_assign,
                    t.date_end as date_end,
                    t.date_last_stage_update as date_last_stage_update,
                    t.date_deadline as date_deadline,
                    t.user_id,
                    t.sector_id,
                    t.project_id,
                    t.priority,
                    t.name as name,
                    t.company_id,
                    t.partner_id,
                    t.stage_id as stage_id,
                    t.kanban_state as state,
                    t.working_days_close as working_days_close,
                    t.working_days_open  as working_days_open,
                    (extract('epoch' from (t.date_deadline-(now() at time zone 'UTC'))))/(3600*24)  as delay_endings_days
        """
        return select_str

    def _group_by(self):
        group_by_str = """
                GROUP BY
                    t.id,
                    t.create_date,
                    t.write_date,
                    t.date_assign,
                    t.date_end,
                    t.date_deadline,
                    t.date_last_stage_update,
                    t.user_id,
                    t.project_id,
                    t.priority,
                    t.name,
                    t.company_id,
                    t.partner_id,
                    t.stage_id,
                    t.sector_id
        """
        return group_by_str