# -*- coding: utf-8 -*-
from odoo import models, fields, api

class DhProjectProject(models.Model):
    _inherit = 'project.project'


    name = fields.Char("Name", index=True, required=True, tracking=True,translate=True )
    dh_code = fields.Char(string='Numérotation', compute='compute_dh_code')

    def name_get(self):
        result = []
        for rec in self:

            name = rec.name
            if rec.code:
                name = " . ".join([rec.code, name])
            result.append((rec.id, name))
        return result



    @api.depends('code', 'pilliar_id')
    def compute_dh_code(self):
        for rec in self:
            if rec.code and rec.pilliar_id.code != False and rec.pilliar_id.orientation_id.code != False:
                rec.dh_code = rec.pilliar_id.orientation_id.code + '/' + rec.pilliar_id.code + '/' + rec.code
            elif rec.code and rec.pilliar_id.code != False and rec.pilliar_id.orientation_id.code == False:
                rec.dh_code = rec.pilliar_id.code + '/' + rec.code
            elif rec.code and rec.pilliar_id.code == False and rec.pilliar_id.orientation_id.code == False:
                rec.dh_code = rec.code
            else:
                rec.dh_code = False



    task_count = fields.Integer(compute='_compute_task_count', string="Activity Count")

    # Budget
    # budget_total = fields.Float(string='Total Budget',store=True)
    budget_remaining = fields.Float(compute='get_project_remaining_budget',string=' Remaining budget',store=True)
    budget_consumed = fields.Float(string=' consumed budget',compute='get_project_consumed_budget',store=True)
    rate_ratio = fields.Integer(string='نسبة الإنجاز', compute='get_project_rate_ratio',store=True)
    budget_icesco = fields.Float(string='الميزانية المخصصة للإيسيسكو', compute='get_project_budget_icesco',store=True)
    budget_out_icesco = fields.Float(string='الميزانية المخصصة خارج الإيسيسكو', compute='get_project_budget_out_icesco',store=True)
    budget_employers = fields.Float(string='ميزانية الموظفين', compute='get_project_budget_employers',store=True)
    percentage_of_done = fields.Integer(string='نسبة النتائج', compute='get_project_percentage_of_done',store=True)
    percentage_of_done_percent = fields.Char(string='نسبة النتائج', compute='get_project_percentage_of_done', store=True)
    respect_time = fields.Integer(string='الالتزام بالوقت', compute='get_project_respect_time',store=True)
    target = fields.Integer(string='المستهدف', compute='get_project_target',store=True)
    actual = fields.Integer(string='الفعلي', compute='get_project_actual',store=True)
    budget_total_icesco = fields.Float(compute='get_total_budget', string='إجمالي ميزانية المشروع', store=True)
    unite = fields.Many2one("uom.uom")

    @api.depends('budget_icesco', 'budget_total_icesco')
    def get_total_budget(self):
        for rec in self:
            rec.budget_total_icesco = rec.budget_icesco + rec.budget_out_icesco

    @api.depends('task_ids.percentage_of_done')
    def get_project_percentage_of_done(self):
        for rec in self:
            rec.percentage_of_done = 0
            rec.percentage_of_done_percent = 0
            if rec.task_ids:
                rec.percentage_of_done = sum(rec.task_ids.mapped('percentage_of_done')) / len(rec.task_ids.mapped('percentage_of_done'))
                rec.percentage_of_done_percent = rec.percentage_of_done / 100

    @api.depends('task_ids.respect_time')
    def get_project_respect_time(self):
        for rec in self:
            rec.respect_time = 0
            if rec.task_ids:
                rec.respect_time = sum(rec.task_ids.mapped('respect_time')) / len(rec.task_ids.mapped('respect_time'))

    @api.depends('task_ids.target')
    def get_project_target(self):
        for rec in self:
            rec.target = 0
            if rec.task_ids:
                rec.target = sum(rec.task_ids.mapped('target')) / len(rec.task_ids.mapped('target'))

    @api.depends('task_ids.actual')
    def get_project_actual(self):
        for rec in self:
            rec.actual = 0
            if rec.task_ids:
                rec.actual = sum(rec.task_ids.mapped('actual')) / len(rec.task_ids.mapped('actual'))

    @api.depends('task_ids.budget_employers')
    def get_project_budget_employers(self):
        for rec in self:
            rec.budget_employers = 0
            if rec.task_ids:
                rec.budget_employers = sum(rec.task_ids.mapped('budget_employers')) / len(rec.task_ids.mapped('budget_employers'))

    @api.depends('task_ids.budget_icesco')
    def get_project_budget_icesco(self):
        for rec in self:
            rec.budget_icesco = 0
            if rec.task_ids:
                rec.budget_icesco = sum(rec.task_ids.mapped('budget_icesco')) / len(rec.task_ids.mapped('budget_icesco'))

    @api.depends('task_ids.budget_out_icesco')
    def get_project_budget_out_icesco(self):
        for rec in self:
            rec.budget_out_icesco = 0
            if rec.task_ids:
                rec.budget_out_icesco = sum(rec.task_ids.mapped('budget_out_icesco')) / len(rec.task_ids.mapped('budget_out_icesco'))
    @api.depends('task_ids.rate_ratio')
    def get_project_rate_ratio(self):
        for rec in self:
            rec.rate_ratio = 0
            if rec.task_ids:
                rec.rate_ratio = sum(rec.task_ids.mapped('rate_ratio')) / len(rec.task_ids.mapped('rate_ratio'))

    @api.depends('task_ids.budget_consumed')
    def get_project_consumed_budget(self):
        for rec in self:
            rec.budget_consumed = 0
            if rec.task_ids:
                rec.budget_consumed = sum(rec.task_ids.mapped('budget_consumed'))

    @api.depends('budget','task_ids.budget_consumed')
    def get_project_remaining_budget(self):
        for rec in self :
            rec.budget_remaining = False
            if rec.budget and rec.budget_consumed:
                rec.budget_remaining = rec.budget - rec.budget_consumed

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if 'is_mission' in vals:
            res.sector_id.compute_projects_sector()
        return res

    def write(self, vals):
        res = super().write(vals)
        if 'is_mission' in vals:
            self.sector_id.compute_projects_sector()
        return res

    # not used (juste affiche message on delete)
    ###############################"
    chef_secteur = fields.Many2one('res.partner', string="Chef de secteur")
    expert = fields.Many2one('hr.employee', string="Expert")
    directeur_administratif = fields.Many2one('res.partner', string='Directeur administratif')
    employee_res_id = fields.Many2one(related='user_id.employee_id')
    paren_employee_res_id = fields.Many2one(related='employee_res_id.parent_id')
    user_paren_employee_res_id = fields.Many2one(related='paren_employee_res_id.user_id')
    expense_ids = fields.Many2many('hr.expense', string='Expense')
    is_mission = fields.Boolean('Is mission?') # not use
    state2 = fields.Selection([('draft', 'Bruillon '), ('approuve', 'Approuve'), ('en_cours', 'En cours '), ('valide', 'Valide '), ('termine', 'Termine ')], "State", default='draft')
    goals_mission_ids = fields.Many2many('dh.mission.goal')
    ###############################
    involved_country_ids = fields.One2many('dh.involved.country', 'project_id', string='Involved countries')
    engaged_partner_ids = fields.One2many('dh.engaged.partner', 'project_id', string='Engaged partners')

    total_depense = fields.Float('Total depense', compute='get_total_depense')

    @api.depends('task_ids')
    def get_total_depense(self):
        for rec in self:
            rec.total_depense = 0
            if rec.task_ids:
                rec.total_depense = sum(rec.task_ids.mapped('expenses_ids').filtered(lambda x:x.state in ['approved', 'done']).mapped('total_amount'))

    orientation_id = fields.Many2one('dh.orientations', string='الهدف', related='pilliar_id.orientation_id')
    respect_time = fields.Integer(string='الالتزام بالوقت', compute='compute_respect_time')
    target = fields.Integer(string='المستهدف', compute='compute_target')
    actual = fields.Integer(string='الفعلي', compute='compute_actual')
    percentage_of_done = fields.Integer(string='نسبة النتائج', compute='compute_percentage_of_done')
    percentage_of_done_percent = fields.Integer(string='نسبة النتائج', compute='compute_percentage_of_done', store=True)
    pilliar_id = fields.Many2one('dh.pilliar', string='المحور', store=True)
    sector_id = fields.Many2one('dh.perf.sector', string='القطاع', store=True)
    pays_member_cible_id = fields.Many2one('res.partner', string='الدولة', domain=[('is_member_state', '=', True)], store=True)
    pencentage_done = fields.Integer(string='نسبة تحقيق أهداف', compute='compute_percentage_done', store=True)
    pencentage_report = fields.Integer(string='نسبة تسليم تقارير')
    goals_ids = fields.One2many('dh.mission.goal', 'project_id')

    @api.depends('goals_ids')
    def compute_percentage_done(self):
        for rec in self:
            if rec.goals_ids:
                rec.pencentage_done = (len(rec.goals_ids.filtered(lambda x:x.done == True)) / len(rec.goals_ids)) * 100
            else:
                rec.pencentage_done = 0

    @api.depends('task_ids.percentage_of_done')
    def compute_percentage_of_done(self):
        for rec in self:
            if len(rec.mapped('task_ids')) > 0:
                rec.percentage_of_done = sum(rec.mapped('task_ids').mapped('percentage_of_done')) / len(
                    rec.mapped('task_ids'))
                rec.percentage_of_done_percent = rec.percentage_of_done / 100
            else:
                rec.percentage_of_done = 0
                rec.percentage_of_done_percent = 0

    @api.depends('task_ids.respect_time')
    def compute_respect_time(self):
        for rec in self:
            if len(rec.mapped('task_ids')) > 0:
                rec.respect_time = sum(rec.mapped('task_ids').mapped('respect_time')) / len(
                    rec.mapped('task_ids'))
            else:
                rec.respect_time = 0

    @api.depends('task_ids.target')
    def compute_target(self):
        for rec in self:
            if len(rec.mapped('task_ids')) > 0:
                rec.target = sum(rec.mapped('task_ids').mapped('target')) / len(rec.mapped('task_ids'))
            else:
                rec.target = 0

    @api.depends('task_ids.actual')
    def compute_actual(self):
        for rec in self:
            if len(rec.mapped('task_ids')) > 0:
                rec.actual = sum(rec.mapped('task_ids').mapped('actual')) / len(rec.mapped('task_ids'))
            else:
                rec.actual = 0


    def view_show_tasks(self):
        for rec in self:
            return {
                'name': "الأنشطة",
                'res_model': 'project.task',
                'view_mode': 'kanban,form',
                'view_type': 'kanban',
                'views': [(self.env.ref("dh_icesco_project.view_dh_project_task_kanban_2").id, 'kanban')],
                'type': 'ir.actions.act_window',
                "domain": [("project_id", "=", rec.id)],
                'context': "{'default_project_id': %s}" % rec.id
            }

    def view_form_project(self):
        for rec in self:
            return {
                'name': "التفاصيل",
                'res_model': 'project.project',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': rec.id,
                'view_id': self.env.ref("project.edit_project").id,
            }

    @api.model
    def projects_possible_search_read(self, **args):
        res = self.env['project.project'].sudo().search_read(domain=[(
            'pilliar_id', '=', args['pillar'])], offset=args['offset'], limit=args['limit'], fields=args['fields'])
        return res