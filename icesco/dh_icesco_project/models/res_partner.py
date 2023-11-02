# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from datetime import datetime, date



class ResPartner(models.Model):
    _inherit = 'res.partner'



    ref = fields.Char(string='Reference', index=True,copy=False, default=lambda self: _('New'))
    city = fields.Char(required=True)
    email = fields.Char(required=True)
    phone = fields.Char(required=True)
    vat = fields.Char(string='Tax ID', index=True,required=True ,help="The Tax Identification Number. Complete it if the contact is subjected to government taxes. Used in some legal statements.")
    category_id = fields.Many2many('res.partner.category', column1='partner_id',required=True,
                                   column2='category_id', string='Tags')

    @api.model
    def create(self, vals):
        if vals.get('ref', _('New')) == _('New'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('sequence_ref_fournisseur.res.partner') or _('New')
        return super(ResPartner, self).create(vals)

    def _default_category(self):
        return self.env['res.partner.category'].browse(self._context.get('category_id'))

    financal_support = fields.One2many("dh.fianancal.support", "partner_id")
    contrubutions_ids = fields.One2many("dh.contrubution","partner_id")
    contribution_budget = fields.Float("Percentage of contribution to the general budget")
    received_amount = fields.Float("Received amount")
    amount = fields.Float("Amount")
    date_last_batch = fields.Date("Date of the last batch")
    years = fields.Selection(string='Year', selection='years_selection')


    def years_selection(self):
        year_list = []
        for y in range(datetime.now().year - 15, datetime.now().year +1):
            year_list.append((str(y), str(y)))
        return year_list
    institution_gouv_etat_member = fields.Boolean(string='مؤسسة حكومية')
    institution_gouv_etat_non_member = fields.Boolean(string='مؤسسة العمل الإنساني')
    organisation_mondiale_rare = fields.Boolean(string='الدول غير الأعضاء')
    organisation_locale = fields.Boolean(string='الدول الأعضاء')
    organisation_regional = fields.Boolean(string='القطاع الخاص')
    count_activities = fields.Integer(string='عدد الأنشطة', compute='_compute_count_activities', store=True)
    dh_count_activities = fields.Integer(string='عدد الأنشطة', compute='_compute_count_activities')
    # dh_activities = fields.Many2many('project.task', string='الأنشطة', compute='_compute_count_activities')
    mission_ids = fields.One2many('project.task', 'pays_member_cible_id', string='المهام')
    dh_task_ids = fields.One2many('project.task', 'country_id', string='الأنشطة')
    count_mission = fields.Integer(string='عدد المهام', compute='_compute_missions', store=True)
    dh_order = fields.Integer(string='Number order', store=True)
    type_partenaire = fields.Selection([('institution_gouv_etat_member', 'مؤسسة حكومية'),
                                        ('institution_gouv_etat_non_member', 'مؤسسة العمل الإنساني'),
                                        ('organisation_mondiale_rare', 'الدول غير الأعضاء'),
                                        ('organisation_locale', 'الدول الأعضاء'),
                                        ('organisation_regional', 'القطاع الخاص')], compute='_compute_type_partenaire', store=True)

    @api.depends('institution_gouv_etat_member', 'institution_gouv_etat_non_member', 'organisation_mondiale_rare', 'organisation_locale', 'organisation_regional')
    def _compute_type_partenaire(self):
        for rec in self:
            rec.type_partenaire = False
            if rec.institution_gouv_etat_member == True:
                rec.type_partenaire = 'institution_gouv_etat_member'
            if rec.institution_gouv_etat_non_member == True:
                rec.type_partenaire = 'institution_gouv_etat_non_member'
            if rec.organisation_mondiale_rare == True:
                rec.type_partenaire = 'organisation_mondiale_rare'
            if rec.organisation_locale == True:
                rec.type_partenaire = 'organisation_locale'
            if rec.organisation_regional == True:
                rec.type_partenaire = 'organisation_regional'

    @api.depends('mission_ids')
    def _compute_missions(self):
        for rec in self:
            rec.count_mission = len(rec.mission_ids)

    def _compute_count_activities(self):
        for rec in self:
            if rec.is_member_state == True:
                rec.count_activities = len(
                    self.env['project.task'].search([]).filtered(lambda x: rec.id in x.pays_members_cibles.ids))
                rec.dh_count_activities = len(
                    self.env['project.task'].search([]).filtered(lambda x: rec.id in x.pays_members_cibles.ids))
                # rec.dh_activities = [(4, task.id) for task in self.env['project.task'].search([]).filtered(lambda x: rec.id in x.pays_members_cibles.ids)]
            else:
                rec.count_activities = 0
                rec.dh_count_activities = 0
                # rec.dh_activities = False

    def action_view_activities(self):
        for rec in self:
            if len(self.env['project.task'].search([]).filtered(lambda x: rec.id in x.pays_members_cibles.ids)) > 0:
                result = {
                    'name': "الأنشطة",
                    'res_model': 'project.task',
                    'view_mode': 'tree,form',
                    'view_type': 'tree',
                    'views': [(self.env.ref("dh_icesco_project.dh_perf_project_task_details_tree").id, 'list')],
                    'domain': [('id', 'in', self.env['project.task'].search([]).filtered(
                        lambda x: rec.id in x.pays_members_cibles.ids).ids)],
                    'type': 'ir.actions.act_window',
                    'target': 'current',
                }
                return result

    count_agreements = fields.Integer(string='عدد الإتفاقيات', compute='_compute_count_agreements')
    agreements = fields.One2many('dh.agreements.international', 'partner_id', string='الإتفاقيات')

    def _compute_count_agreements(self):
        for rec in self:
            if rec.is_member_state == True:
                rec.count_agreements = len(
                    self.env['dh.agreements.international'].search([('partner_id', '=', rec.id)]))
            else:
                rec.count_agreements = 0

    def action_view_agreements(self):
        for rec in self:
            # if len(self.env['dh.agreements.international'].search([('partner_id', '=', rec.id)])) > 0:
            result = {
                'name': "الإتفاقيات",
                'res_model': 'dh.agreements.international',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'domain': [
                    ('id', 'in', self.env['dh.agreements.international'].search([('partner_id', '=', rec.id)]).ids)],
                'type': 'ir.actions.act_window',
                'target': 'current',
                'context': {'default_partner_id': rec.id},
            }
            return result

    count_chaises = fields.Integer(string='عدد الكراسي', compute='_compute_count_chaises')
    chaises = fields.One2many('dh.chairs', 'pays_id', string='الكراسي')

    def _compute_count_chaises(self):
        for rec in self:
            if rec.is_member_state == True:
                rec.count_chaises = len(
                    self.env['dh.chairs'].search([('pays_id', '=', rec.id)]))
            else:
                rec.count_chaises = 0

    def action_view_chaises(self):
        for rec in self:
            # if len(self.env['dh.chairs'].search([('pays_id', '=', rec.id)])) > 0:
            result = {
                'name': "الكراسي",
                'res_model': 'dh.chairs',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', self.env['dh.chairs'].search([('pays_id', '=', rec.id)]).ids)],
                'type': 'ir.actions.act_window',
                'target': 'current',
                'context': {'default_pays_id': rec.id},
            }
            return result

    count_recompenses = fields.Integer(string='عدد الجوائز', compute='_compute_count_recompenses')
    recompenses = fields.One2many('dh.awards', 'pays_id', string='الجوائز')

    def _compute_count_recompenses(self):
        for rec in self:
            if rec.is_member_state == True:
                rec.count_recompenses = len(
                    self.env['dh.awards'].search([('pays_id', '=', rec.id)]))
            else:
                rec.count_recompenses = 0

    def action_view_recompenses(self):
        for rec in self:
            # if len(self.env['dh.awards'].search([('pays_id', '=', rec.id)])) > 0:
            result = {
                'name': "الجوائز",
                'res_model': 'dh.awards',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'domain': [('id', 'in',
                            self.env['dh.awards'].search([('pays_id', '=', rec.id)]).ids)],
                'type': 'ir.actions.act_window',
                'target': 'current',
                'context': {'default_pays_id': rec.id},
            }
            return result

    count_subventions = fields.Integer(string='عدد المنح', compute='_compute_count_subventions')
    subventions = fields.One2many('dh.bourse', 'pays_id', string='عدد المنح')

    def _compute_count_subventions(self):
        for rec in self:
            if rec.is_member_state == True:
                rec.count_subventions = len(
                    self.env['dh.bourse'].search([('pays_id', '=', rec.id)]))
            else:
                rec.count_subventions = 0

    def action_view_subventions(self):
        for rec in self:
            # if len(self.env['dh.bourse'].search([('pays_id', '=', rec.id)])) > 0:
            result = {
                'name': "المنح",
                'res_model': 'dh.bourse',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', self.env['dh.bourse'].search([('pays_id', '=', rec.id)]).ids)],
                'type': 'ir.actions.act_window',
                'target': 'current',
                'context': {'default_pays_id': rec.id},
            }
            return result

    count_type_projects = fields.Integer(string='عدد نوع المشاريع', compute='_compute_count_type_projects')

    def _compute_count_type_projects(self):
        for rec in self:
            if rec.is_member_state == True:
                rec.count_type_projects = len(
                    self.env['project.task'].search([]).filtered(
                        lambda x: rec.id in x.pays_members_cibles.ids).mapped('project_id').mapped('project_type'))
            else:
                rec.count_type_projects = 0

    def action_view_type_projects(self):
        for rec in self:
            if len(self.env['project.task'].search([]).filtered(
                        lambda x: rec.id in x.pays_members_cibles.ids).mapped('project_id').ids) > 0:
                result = {
                    'name': "نوع المشاريع",
                    'res_model': 'project.project',
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'domain': [
                        ('id', 'in', self.env['project.task'].search([]).filtered(
                        lambda x: rec.id in x.pays_members_cibles.ids).mapped('project_id').ids)],
                    'type': 'ir.actions.act_window',
                    # 'context': {'group_by': 'project_type'},
                    'context': {},
                    'target': 'current',
                }
                return result

    count_projects = fields.Integer(string='عدد المشاريع', compute='_compute_count_projects')
    count_missions = fields.Integer(string='Mission Number', compute='_compute_count_missions')

    def _compute_count_missions(self):
        for rec in self:
            if rec.is_member_state == True:
                rec.count_missions = len(
                    self.env['project.task'].search([('is_mission','=',True)]).filtered(
                        lambda x: rec.id in x.pays_members_cibles.ids).mapped('project_id'))
            else:
                rec.count_missions = 0
    def _compute_count_projects(self):
        for rec in self:
            if rec.is_member_state == True:
                rec.count_projects = len(
                    self.env['project.task'].search([]).filtered(
                        lambda x: rec.id in x.pays_members_cibles.ids).mapped('project_id'))
            else:
                rec.count_projects = 0

    def action_view_projects(self):
        for rec in self:
            if len(self.env['project.task'].search([]).filtered(
                        lambda x: rec.id in x.pays_members_cibles.ids).mapped('project_id').ids) > 0:
                result = {
                    'name': "عدد المشاريع",
                    'res_model': 'project.project',
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'domain': [
                        ('id', 'in', self.env['project.task'].search([]).filtered(
                        lambda x: rec.id in x.pays_members_cibles.ids).mapped('project_id').ids)],
                    'type': 'ir.actions.act_window',
                    # 'context': {'group_by': 'sector_id'},
                    'context': {},
                    'target': 'current',
                }
                return result
    def action_view_missions(self):
        for rec in self:
            if len(self.env['project.task'].search([('is_mission','=',True)]).filtered(
                        lambda x: rec.id in x.pays_members_cibles.ids).mapped('project_id').ids) > 0:
                result = {
                    'name': "Missions Number",
                    'res_model': 'project.project',
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'domain': [
                        ('id', 'in', self.env['project.task'].search([('is_mission','=',True)]).filtered(
                        lambda x: rec.id in x.pays_members_cibles.ids).mapped('project_id').ids)],
                    'type': 'ir.actions.act_window',
                    # 'context': {'group_by': 'sector_id'},
                    'context': {},
                    'target': 'current',
                }
                return result
class AdditionalFianancalSupport(models.Model):
    _name = 'dh.fianancal.support'

    count_number = fields.Integer(string='Count Number', store=True, default=1)
    active = fields.Boolean(string='Active', default=True)
    amount = fields.Float("Amount")
    date = fields.Date("Date")
    partner_id = fields.Many2one("res.partner",string="Country")
    project_id = fields.Many2one("project.project",string='Project')
    sector_id = fields.Many2one('dh.perf.sector', string='Sector')
    support_foundation = fields.Char(string='Support Foundation')

    @api.model
    def create(self, vals):
        if 'project_id' in vals:
            vals['sector_id'] = self.env['project.project'].search([('id', '=', vals['project_id'])]).sector_id.id
        res = super().create(vals)

        return res

    def write(self, vals):
        if 'project_id' in vals:
            vals['sector_id'] = self.env['project.project'].search([('id', '=', vals['project_id'])]).sector_id.id
        res = super().write(vals)
        return res
