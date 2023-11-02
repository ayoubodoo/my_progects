# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DhIcescoOperationalPlanoperationalindicators(models.Model):
    _name = 'dh.icesco.operational.indicators'
    _order = 'sequence'




    indicator_type = fields.Many2one('dh.indicator.result.type', string='Indicator Type')
    task_id = fields.Many2one('project.task', string='النشاط')
    operational_plan_id = fields.Many2one('dh.icesco.operational.plan', string='الخطة التشغيلية')
    strategie = fields.Many2one('dh.strategies', string='الخطط الإستراتيجية', related='operational_plan_id.strategie')
    standard_government_system_id = fields.Many2many('dh.government.system', string='معايير منظومة التميز الحكومي', related='operational_plan_id.standard_government_system_id')
    strategic_indicator_id = fields.Many2one('dh.icesco.strategic.indicator', string='مؤشر استراتيجي', related='operational_plan_id.strategic_indicator_id')
    sequence_operational_plan = fields.Integer(string='متسلسل ', related='operational_plan_id.sequence')
    sequence = fields.Integer(string='متسلسل')
    orientation_id = fields.Many2one('dh.orientations', related='operational_plan_id.orientation_id', string='الهدف')
    level_one_id = fields.Many2one('dh.operational.plan.level.one', related='operational_plan_id.level_one_id', string='المستوى الأول')
    ability_id = fields.Many2one('dh.operational.plan.ability', related='operational_plan_id.ability_id', string='القدرة')
    type = fields.Selection([('project', 'مبادرة'), ('process', 'عملية')], related='operational_plan_id.type', string='النوع')
    type_2 = fields.Selection([('activity', 'نشاط'), ('service', 'خدمة'), ('process', 'عملية')], related='operational_plan_id.type_2', string='النوع 2')
    responsable_id = fields.Many2one('res.partner', related='operational_plan_id.responsable_id', string='المسؤول')
    priority = fields.Selection([('very_high', 'مرتفع جداً'), ('high', 'مرتفع'), ('average', 'متوسط')], related='operational_plan_id.priority', string='الأولوية')
    rate_ratio = fields.Integer(string='نسبة الإنجاز', related='operational_plan_id.rate_ratio')
    date_start = fields.Date(string='تاريخ البدء', related='operational_plan_id.date_start')
    date_end = fields.Date(string='تاريخ الإنتهاء', related='operational_plan_id.date_end')
    type_operation = fields.Selection([('operational', 'تشغيلية'), ('capacity', 'القدرات')], related='operational_plan_id.type_operation', string='نوع الادخال')
    name = fields.Char(string='الإسم')
    measure_cycle = fields.Selection([('year', 'سنوي'), ('month', 'شهري'), ('week', 'أسبوعي')], string='دورة القياس')
    target = fields.Integer(string='المستهدف')
    actual = fields.Integer(string='الفعلي')

    moyeu_id = fields.Many2one('dh.pilliar', string='المحور')
    projet_id = fields.Many2one('project.project', string='المشروع', related='task_id.project_id')
    partenaire_ids = fields.Many2many('res.partner', relation='rel_partner_partenaire_ids', string='الشركاء المقترحين',store=True)
    pays_members_cibles = fields.Many2many('res.partner', relation='rel_partner_pays_members_cibles', string='الدول الأعضاء المستهدفة', domain=[('is_member_state', '=', True)])
    pays_no_members_cibles = fields.Many2many('res.partner', relation='rel_partner_pays_no_members_cibles', string='الدول الأعضاء غير المستهدفة', domain=[('is_member_state', '=', False)])
    nombre_beneficiaires = fields.Integer(string='عدد المستفيدين')
    mode_convo = fields.Char(string='طريقة الإنعقاد')
    budget_icesco = fields.Float(string='الميزانية المخصصة للإيسيسكو')
    budget_out_icesco = fields.Float(string='الميزانية المخصصة خارج الإيسيسكو')
    equipe_responsable_ids = fields.Many2many('res.partner', relation='rel_partner_equipe_responsable_ids', string='الخبير / الفريق المسؤول')
    result_attendus = fields.Char(string='المخرجات المتوقعة')
    type_activity = fields.Selection([('formation', 'دورة تدريبية'), ('soutien', 'دعم'), ('etude', 'دراسة'), ('conspiration', 'مؤتمر'), ('project', 'مشروع'), ('chaise', 'كرسي')], string='نوع النشاط')
    # type_activity = fields.Many2one('dh.scope.type', string='نوع النشاط')

    class_id = fields.Many2one('dh.icesco.office', string='قسم')
    nbr_operations = fields.Integer('عدد العمليات')
    code = fields.Char(string='كود العملية')

    indicators_result_ids = fields.One2many('dh.icesco.operational.indicators.result', 'operational_indicator_id', string='Indicators results')

    deliverables = fields.Text(related="task_id.expected_outputs",string='Deliverables')
    state = fields.Char(string='State')

    @api.model
    def create(self, vals):
        vals['sequence'] = len(self.env['dh.icesco.operational.indicators'].search([])) + 1
        return super(DhIcescoOperationalPlanoperationalindicators, self).create(vals)

    def view_indicators_details(self):
        return {
            'name': ".",
            'res_model': 'dh.icesco.operational.indicators',
            'view_mode': 'tree,form',
            'view_type': 'tree',
            'views': [(self.env.ref("dh_icesco_project.dh_icesco_operational_indicators_details_tree").id, 'list')],
            'type': 'ir.actions.act_window',
            'domain': self.ids,
            'context': self._context.get('context', {}),
        }

class DhIcescoOperationalPlanoperationalindicatorsAll(models.Model):
    _name = 'dh.icesco.operational.indicators.all'
    _order = 'sequence'

    sequence = fields.Integer(string='متسلسل')
    orientation_id = fields.Many2one('dh.orientations', string='الهدف')
    type = fields.Selection([('project', 'مشروع'), ('service', 'خدمة'), ('process', 'عملية')], string='النوع')
    priority = fields.Selection([('very_high', 'مرتفع جداً'), ('high', 'مرتفع'), ('average', 'متوسط')],
                                string='الأولوية')
    indicators = fields.Char(string='المؤشرات')
    type_2 = fields.Selection([('indic_operat', 'مؤشر تشغيلي'), ('indic_strateg', 'مؤشر استراتيجي')], string='النوع 2')

    @api.model
    def create(self, vals):
        vals['sequence'] = len(self.env['dh.icesco.operational.indicators.all'].search([])) + 1
        return super(DhIcescoOperationalPlanoperationalindicatorsAll, self).create(vals)

class DhIcescoOperationalPlanoperationalindicatorsResult(models.Model):
    _name = 'dh.icesco.operational.indicators.result'

    operational_indicator_id = fields.Many2one('dh.icesco.operational.indicators', string='المؤشر التشغيلي')

    task_id = fields.Many2one('project.task', related='operational_indicator_id.task_id' ,string='النشاط')
    operational_plan_id = fields.Many2one('dh.icesco.operational.plan', string='الخطة التشغيلية')
    strategie = fields.Many2one('dh.strategies', string='الخطط الإستراتيجية', related='operational_plan_id.strategie')
    standard_government_system_id = fields.Many2many('dh.government.system', string='معايير منظومة التميز الحكومي', related='operational_plan_id.standard_government_system_id')
    strategic_indicator_id = fields.Many2one('dh.icesco.strategic.indicator', string='مؤشر استراتيجي', related='operational_plan_id.strategic_indicator_id')
    sequence_operational_plan = fields.Integer(string='متسلسل ', related='operational_plan_id.sequence')
    sequence = fields.Integer(string='متسلسل')
    orientation_id = fields.Many2one('dh.orientations', related='operational_plan_id.orientation_id', string='الهدف')
    level_one_id = fields.Many2one('dh.operational.plan.level.one', related='operational_plan_id.level_one_id', string='المستوى الأول')
    ability_id = fields.Many2one('dh.operational.plan.ability', related='operational_plan_id.ability_id', string='القدرة')
    type = fields.Selection([('project', 'مبادرة'), ('process', 'عملية')], related='operational_plan_id.type', string='النوع')
    type_2 = fields.Selection([('activity', 'نشاط'), ('service', 'خدمة'), ('process', 'عملية')], related='operational_plan_id.type_2', string='النوع 2')
    responsable_id = fields.Many2one('res.partner', related='operational_plan_id.responsable_id', string='المسؤول')
    priority = fields.Selection([('very_high', 'مرتفع جداً'), ('high', 'مرتفع'), ('average', 'متوسط')], related='operational_plan_id.priority', string='الأولوية')
    rate_ratio = fields.Integer(string='نسبة الإنجاز', related='operational_plan_id.rate_ratio')
    date_start = fields.Date(string='تاريخ البدء', related='operational_plan_id.date_start')
    date_end = fields.Date(string='تاريخ الإنتهاء', related='operational_plan_id.date_end')
    type_operation = fields.Selection([('operational', 'تشغيلية'), ('capacity', 'القدرات')], related='operational_plan_id.type_operation', string='نوع الادخال')
    name = fields.Char(string='الإسم', required=True)
    # measure_cycle = fields.Selection([('year', 'سنوي'), ('month', 'شهري'), ('week', 'أسبوعي')], string='دورة القياس')
    # target = fields.Integer(string='المستهدف')
    # actual = fields.Integer(string='الفعلي')


    is_done = fields.Boolean(string='تحقق')

    @api.model
    def create(self, vals):
        vals['sequence'] = len(self.env['dh.icesco.operational.indicators.result'].search([])) + 1
        return super(DhIcescoOperationalPlanoperationalindicatorsResult, self).create(vals)