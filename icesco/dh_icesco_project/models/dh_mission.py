# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class DhProjectBudgetWizard(models.TransientModel):
    _name = 'dh.project.budget.wizard'

    project_dest_id = fields.Many2one('project.project', string='Origin project')
    task_dest_id = fields.Many2one('project.task', string='Destination activity ')
    task_dest = fields.Many2one('project.task', string='Destination activity ')
    montant = fields.Float('Montant')
    description = fields.Text(translate=True,string='Description d’opération')
    task_ids = fields.Many2one('project.task', string='Origin Activity ')
    # task_id = fields.Many2one('project.task')


    def action_done_show_wizard(self):
        for rec in self:
            if rec.montant > rec.task_ids.budget_remaining:
                raise ValidationError(
                    (
                            "You cannot perform this operation, the amount is higher than the remaining budget of the selected activity( %s ).You could complete the amount from another activity" % (
                        rec.task_ids.budget_remaining))
                )

            self.env['dh.budget.transfert'].create({
                'project_dest_id': rec.project_dest_id.id,
                'task_dest_id': rec.task_dest_id.id,
                'montant': rec.montant,
                'description': rec.description,
                'task_ids': rec.task_ids.id,

            })



        # project_id = self.env['project.project'].browse(self._context.get('active_ids', False))
        #
        # for rec in self:
        #     # if rec.montant <= project_id.budget_remaining:
        #     if rec.montant <= rec.task_ids.budget_remaining:
        #         rec.task_dest_id.budget_initial = rec.task_dest_id.budget_initial + rec.montant
        #         rec.task_ids.budget_initial = rec.task_ids.budget_initial - rec.montant
        #     else:
        #         raise ValidationError(
        #             (
        #                 "Vous ne pouvez pas effectuer cet opération,la somme est supérieur au budget restant d'activité selectionné( %s )Vous pouviez compléter la somme à partir d'un autre activité" % (rec.task_ids.budget_remaining))
        #         )
        #     # else:
        #     #     raise ValidationError(
        #     #         ('Vous ne pouvez pas effectuer cet opération,la somme est supérieur au budget restant de projet parent')
        #     #     )
        #
        #
        # return {
        #
        #     'name': 'Retirer un montant',
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'project.project',
        #     'view_type': 'form',
        #     'view_mode': 'tree,form',
        #     'domain': [('id', '=', rec.task_dest_id.id)],
        # }


class DhBudgetTransfert(models.Model):
    _name = 'dh.budget.transfert'

    project_dest_id = fields.Many2one(related='task_dest_id.project_id', string='Projet')
    task_dest_id = fields.Many2one('project.task', string='Destination activity ')
    montant = fields.Float('Montant')
    description = fields.Text(translate=True,string='Description d’opération')
    task_ids = fields.Many2one('project.task', string='Origin Activity ')
    state = fields.Selection(
        [("draft", "Draft"), ("valide", "validé")],

        default="draft",
    )
    def action_valide(self):
        for rec in self:
            rec.state ='valide'
            project_id = self.env['project.project'].browse(self._context.get('active_ids', False))
            if rec.montant <= rec.task_ids.budget_remaining:
                rec.task_dest_id.budget_initial = rec.task_dest_id.budget_initial + rec.montant
                rec.task_ids.budget_initial = rec.task_ids.budget_initial - rec.montant
            else:
                raise ValidationError(
                    (
                            "You cannot perform this operation, the amount is higher than the remaining budget of the selected activity( %s ).You could complete the amount from another activity" % (
                        rec.task_ids.budget_remaining))
                )






class DhMissionGoal(models.Model):
    _name = 'dh.mission.goal'

    name = fields.Char(translate=True,string='goals')
    done = fields.Boolean('Done')
    task_id = fields.Many2one('project.task')
    project_id = fields.Many2one('project.project', related='task_id.project_id')


class DhcpsExpenseBilleterie(models.Model):
    _inherit = 'cps.expense.billeterie'

    project_id = fields.Many2one('project.project')
    task_id = fields.Many2one('project.task')


    def button_validate(self):
        for rec in self:
            if len(rec.line_ids) == 0:
                raise ValidationError(
                    ('Vous ne pouvez pas valider le billet avec des lignes vides')
                )
            else:
                for line_unlink in self.env['hr.expense'].search([('billeterie_id', '=', rec.id)]):
                    line_unlink.unlink()

                for line in rec.line_ids:
                    if line.montant == 0:
                        line.unlink()

                for line in rec.line_ids:
                    self.env['hr.expense'].create(
                        {'name': ("Expense Billet %s pour %s le %s") % (rec.name, line.employee_id.name, line.date),
                         'employee_id': line.employee_id.id, 'date': line.date, 'product_id': line.product_id.id,
                         'tax_ids': [[6, 0, line.product_id.supplier_taxes_id.ids]] if line.product_id.supplier_taxes_id.ids else False,
                         'unit_amount': line.montant, 'quantity': 1,
                         'passager_id': line.passager_id.id if line.passager_id.id else False,
                         'payment_mode': line.payment_mode, 'billeterie_id': line.billeterie_id.id, 'project_id': line.billeterie_id.project_id.id, 'task_id': line.billeterie_id.task_id.id,
                         'account_id': self.env['product.product'].search([('id', '=', line.product_id.id)]).categ_id.property_account_expense_categ_id.id})

                rec.state = 'valide'

class DhTaskMission(models.Model):
    _name = 'project.task'
    _inherit = ['project.task', 'mail.thread']

    languages = fields.Many2one('res.lang')
    budget = fields.Float(string="Global Budget") # not use
    is_mission = fields.Boolean('Is mission?')
    billeterie_ids = fields.One2many('cps.expense.billeterie', 'task_id', string='Billeteries')
    expenses_ids = fields.One2many('hr.expense', 'task_id', string='Expenses')
    goals_mission_ids = fields.One2many('dh.mission.goal', 'task_id')
    total_depense = fields.Float('Total depense', compute='get_total_depense')
    total_depense_stored = fields.Float('الميزانية المحققة', compute='get_total_depense', store=True)
    chef_secteur = fields.Many2one('res.partner', string="Chef de secteur")
    expert = fields.Many2one('hr.employee', string="Expert")
    directeur_administratif = fields.Many2one('res.partner', string='Directeur administratif')
    employee_res_id = fields.Many2one(related='user_id.employee_id')
    paren_employee_res_id = fields.Many2one(related='employee_res_id.parent_id')
    user_paren_employee_res_id = fields.Many2one(related='paren_employee_res_id.user_id')
    state2 = fields.Selection([
        ('draft', 'Bruillon '),
        ('approuve', 'Approuve'),
        ('en_cours', 'En cours '),
        ('valide', 'Valide '),
        ('termine', 'Termine ')
    ], "State", default='draft')


    fournisseur = fields.Char( string='Fournisseur')
    pays_member_cible_id = fields.Many2one('res.partner', string='الدولة', domain=[('is_member_state', '=', True)], store=True)

    pencentage_done = fields.Integer(string='نسبة تحقيق أهداف المهمة', compute='compute_percentage_done', store=True)
    pencentage_report = fields.Integer(string='نسبة تسليم تقارير')

    @api.depends('goals_mission_ids')
    def compute_percentage_done(self):
        for rec in self:
            if rec.goals_mission_ids:
                rec.pencentage_done = (len(rec.goals_mission_ids.filtered(lambda x: x.done == True)) / len(
                    rec.goals_mission_ids)) * 100
            else:
                rec.pencentage_done = 0

    @api.depends('expenses_ids')
    def get_total_depense(self):
        for rec in self:
            rec.total_depense = False
            rec.total_depense_stored = False
            if rec.expenses_ids:
                for line in rec.expenses_ids.filtered(lambda x:x.state in ['approved', 'done']):
                    rec.total_depense = rec.total_depense + line.total_amount
                    rec.total_depense_stored = rec.total_depense + line.total_amount

    def action_draft(self):
        for rec in self:
            rec.state2 = 'draft'

    def action_aprouvee(self):
        for rec in self:
            rec.state2 = 'approuve'
            rec.env['mail.activity'].create({
                'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                'user_id': rec.user_id.id,

                'summary': 'Approuvation Manager',
                'note': 'Approuvation Mission ',
                'res_model_id': self.env['ir.model']._get('project.task').id,
                'res_id': rec.id
            })

    def action_valide(self):
        for rec in self:
            rec.state2 = 'valide'
            if rec.user_id.id:
                rec.env['mail.activity'].create({
                    'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                    'user_id': rec.user_id.id,

                    'summary': 'Approuvation DG',
                    'note': 'Approuvation Mission ',
                    'res_model_id': self.env['ir.model']._get('project.task').id,
                    'res_id': rec.id
                })
            if rec.user_paren_employee_res_id.id:
                rec.env['mail.activity'].create({
                    'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                    'user_id': rec.user_paren_employee_res_id.id,

                    'summary': 'Approuvation DG',
                    'note': 'Approuvation Mission ',
                    'res_model_id': self.env['ir.model']._get('project.task').id,
                    'res_id': rec.id
                })
            if len(self.env.ref("dh_icesco_project.icesco_directeur_administratif").users.ids) > 0:
                rec.env['mail.activity'].create({
                    'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                    'user_id': self.env.ref("dh_icesco_project.icesco_directeur_administratif").users[0].id,

                    'summary': 'Approuvation DG',
                    'note': 'Approuvation Mission ',
                    'res_model_id': self.env['ir.model']._get('project.task').id,
                    'res_id': rec.id
                })

    def action_en_cours(self):
        for rec in self:
            rec.state2 = 'en_cours'

    def action_termine(self):
        for rec in self:
            rec.state2 = 'termine'

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if 'is_mission' in vals:
            res.expert.get_nb_mission()

        if 'budget_initial' in vals:
            if res.project_id:
                res.project_id.get_project_initial_budget()
        if 'budget_consumed' in vals:
            if res.project_id:
                res.project_id.get_project_consumed_budget()
        if 'budget_remaining' in vals:
            if res.project_id:
                res.project_id.get_project_remaining_budget()
        return res

    def write(self, vals):
        res = super().write(vals)
        if 'is_mission' in vals:
            self.expert.get_nb_mission()
        if 'budget_initial' in vals:
            if self.project_id:
                self.project_id.get_project_initial_budget()
        if 'budget_consumed' in vals:
            if self.project_id:
                self.project_id.get_project_consumed_budget()
        if 'budget_remaining' in vals:
            if self.project_id:
                self.project_id.get_project_remaining_budget()
        return res

    mission_count = fields.Integer(compute='compute_missions', string='Missions')
    depense_count = fields.Integer(compute='compute_depenses', string='Depenses')
    billeterie_count = fields.Integer(compute='compute_billeterie', string='Billeterie')
    budget_icesco_count = fields.Integer(compute='compute_budget_icesco', string='Budget icesco')
    budget_extra_reel_count = fields.Integer(compute='compute_budget_extra_reel', string='Budget Extra-reel')
    budget_extra_indirect_count = fields.Integer(compute='compute_budget_extra_indirect', string='Budget Extra-indirect')
    budget_extra_reel = fields.Float(compute='compute_budget_extra_reel', string='Budget Extra-reel', store=True)
    budget_extra_indirect = fields.Float(compute='compute_budget_extra_indirect', string='Budget Extra-indirect', store=True)
    type_budget_extra_indirect = fields.Char(string='Type Budget Extra-indirect')
    move_lines = fields.One2many('account.move.line', 'task_id', string='Move lines')
    budget_compta = fields.Float(string=' المبلغ المستلم في المحاسبة ', store=True, compute='compute_budget_compta')
    expected_outputs = fields.Text(translate=True,string='المخرجات المتوقعة ', store=True)
    budget_transfer_count = fields.Integer(compute='compute_budget_transfer_count', string='Budget Transfers')

    risks_addressing = fields.Many2many('risks.addressing', string='Addressing global risks', store=True) # المخاطر العالمية المتصدي لها
    link_dev_goals = fields.Many2many('link.dev.goals', string='Linking to the sustainable development goals', store=True) # الربط بأهداف التنمية المستدامة
    key_performance_indicators = fields.Many2one('key.performance.indicators', string='Key performance indicators', store=True) # مؤشرات الأداء الرئيسية

    @api.depends('move_lines')
    def compute_budget_compta(self):
        for rec in self:
            rec.budget_compta = sum(rec.move_lines.mapped('debit'))

    def compute_budget_icesco(self):
        for rec in self:

            rec.budget_icesco_count = len(
                self.env['crossovered.budget.lines'].search([('task_id', '=', rec.id)]).filtered(
                    lambda x: x.crossovered_budget_id.is_budget_icesco == True))


    def compute_budget_transfer_count(self):
        for rec in self:
            rec.budget_transfer_count = len(rec.transfer_ids11)
            print('budget_transfer_count',rec.budget_transfer_count)

    def compute_budget_extra_reel(self):
        for rec in self:
            rec.budget_extra_reel_count = len(
                self.env['crossovered.budget.lines'].search([('task_id', '=', rec.id)]).filtered(
                    lambda x: x.crossovered_budget_id.is_budget_extra_reel == True))
            rec.budget_extra_reel = sum(
                self.env['crossovered.budget.lines'].search([('task_id', '=', rec.id)]).filtered(
                    lambda x: x.crossovered_budget_id.is_budget_extra_reel == True).mapped('planned_amount'))


    def compute_budget_extra_indirect(self):
        for rec in self:
            rec.budget_extra_indirect_count = len(
                self.env['crossovered.budget.lines'].search([('task_id', '=', rec.id)]).filtered(
                    lambda x: x.crossovered_budget_id.is_budget_extra_indirect == True))
            rec.budget_extra_indirect = sum(
                self.env['crossovered.budget.lines'].search([('task_id', '=', rec.id)]).filtered(
                    lambda x: x.crossovered_budget_id.is_budget_extra_indirect == True).mapped('planned_amount'))

    def compute_missions(self):
        for rec in self:
            rec.mission_count = len(rec.child_ids)

    def compute_depenses(self):
        for rec in self:
            rec.depense_count = len(rec.expenses_ids)

    def compute_billeterie(self):
        for rec in self:
            rec.billeterie_count = len(rec.billeterie_ids)

    def get_missions(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Missions'),
            'view_mode': 'tree,form',
            'res_model': 'project.task',
            'domain': [('is_mission', '=', True), ('parent_id', '=', self.id)],
            'views': [(self.env.ref("dh_icesco_project.view_dh_mission_tree").id, 'tree'),
                      (self.env.ref("dh_icesco_project.view_dh_mission_formm").id, 'form')],
            'context': "{'default_is_mission': True}"
        }

    def get_depenses(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Depenses'),
            'view_mode': 'tree,form',
            'res_model': 'hr.expense',
            'domain': [('task_id', '=', self.id)],
            'context': "{'default_project_id' : %s, 'default_task_id': %s}" % (self.project_id.id, self.id)
        }

    def get_billeterie(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Billeteries'),
            'view_mode': 'tree,form',
            'res_model': 'cps.expense.billeterie',
            'domain': [('task_id', '=', self.id)],
            'context': "{'default_project_id' : %s, 'default_task_id': %s}" % (self.project_id.id, self.id)
        }

    def get_budget_icesco(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Détails Budget icesco'),
            'view_mode': 'tree',
            'res_model': 'crossovered.budget.lines',
            'domain': [('task_id', '=', self.id), ('is_budget_icesco', '=', True)],
            'context': "{'create': False, 'delete': False, 'edit': False}"
        }

    def get_budget_extra_reel(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Détails Budget extra reel'),
            'view_mode': 'tree',
            'res_model': 'crossovered.budget.lines',
            'domain': [('task_id', '=', self.id), ('is_budget_extra_reel', '=', True)],
            'context': "{'create': False, 'delete': False, 'edit': False}"
        }

    def get_budget_extra_indirect(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Détails Budget extra indirect'),
            'view_mode': 'tree',
            'res_model': 'crossovered.budget.lines',
            'domain': [('task_id', '=', self.id), ('is_budget_extra_indirect', '=', True)],
            'context': "{'create': False, 'delete': False, 'edit': False}"
        }

    def get_budget_transfers(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Budget Transfers'),
            'view_mode': 'tree,form',
            'res_model': 'dh.budget.transfert',
            'domain': ['|',('task_ids', '=', self.id),('task_dest_id', '=', self.id)],
            'context': "{'default_task_ids': active_id}"
        }