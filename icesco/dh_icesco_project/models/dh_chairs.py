# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import requests

class DhChairs(models.Model):
    _name = 'dh.chairs'



    numero = fields.Char("الرقم", readonly=True, copy=False)

    sector_id = fields.Many2one('dh.perf.sector', string='القطاع')
    name = fields.Char(translate=True, store=True,string='الكرسي')
    university = fields.Char(translate=True ,store=True,string='الجامعة')
    pays_id = fields.Many2one('res.partner',store=True, string='البلد المستضيف')
    date = fields.Char(store=True,string='تاريخ التوقيع على اتفاقية الكرسي')
    date_chairs = fields.Date(store=True,string='تاريخ التوقيع على اتفاقية الكرسي')
    budget_chairs = fields.Float(store=True,compute="get_budget_chairs",string=' ميزانيةالكرسي ')
    budget_icesco = fields.Float(store=True,string='ميزانيةالإيسيسكو')
    budget_externe = fields.Float(store=True,string='الميزانية الخرجية')
    tatal_budget_chairs = fields.Float(store=True,compute="tatal_total_budget_chairs",string='إجمالي ميزانية الكراسي ')
    consumed_budget = fields.Float(store=True,string='الميزانية المستهلكة ')
    percentage_budget = fields.Float(store=True,string='نسبة الميزانية المستهلكة', compute="percentage_consumed_budget")
    percentage = fields.Float('النسبة',compute='get_percentage_goal',store=True,)

    @api.depends("gaol_cairs_id")
    def get_percentage_goal(self):
        for rec in self:
            rec.percentage = sum(self.env['dh.chairs.line'].search([]).mapped("percentage_realisation"))


    # gaol_cairs_id = fields.One2many("dh.chairs.goa","chairs_id")
    gaol_cairs_id = fields.One2many("dh.chairs.line",'chair_id',string="Goals")
    @api.depends("budget_chairs")
    def tatal_total_budget_chairs(self):
        for rec in self :
            # rec.tatal_budget_chairs = False
            # if rec.budget_chairs:
            rec.tatal_budget_chairs = sum(self.env['dh.chairs'].search([]).mapped("budget_chairs"))

    @api.depends("budget_externe","budget_icesco")
    def get_budget_chairs(self):
        for rec in self:
            rec.budget_chairs = False
            if rec.budget_icesco and rec.budget_externe:
                rec.budget_chairs = rec.budget_externe + rec.budget_icesco


    @api.depends("tatal_budget_chairs","consumed_budget")
    def percentage_consumed_budget(self):
        for rec in self:
            rec.percentage_budget = False
            if rec.consumed_budget and rec.tatal_budget_chairs != 0:
                rec.percentage_budget = rec.consumed_budget / rec.tatal_budget_chairs


    @api.model
    def create(self, vals):
        if vals.get('numero', _('New')) == _('New'):
            vals['numero'] = self.env['ir.sequence'].next_by_code('sequence_chairs.dh.chairs') or _(
                'New')
        return super(DhChairs, self).create(vals)

class DhChairslines(models.Model):
    _name = 'dh.chairs.line'

    orientation_id = fields.Many2one('dh.orientations', string='الربط الاستراتيجي')
    pilliar_id = fields.Many2one('dh.pilliar', string='المحور')
    chair_goal_id = fields.Many2one('dh.chairs.goal', string='هدف الكرسي')
    chair_id = fields.Many2one('dh.chairs', string='الكرسي')
    chair_indicators_id = fields.Many2one('ddh.chair.indicators.goal', string='هدف الكرسي')
    target = fields.Float(store=True,string='المستهدف')
    result = fields.Float(store=True,string='الناتج')
    percentage_realisation = fields.Float('نسبة الإنجاز',compute='get_percentage_realisation',store=True,)
    @api.depends("target","result")
    def get_percentage_realisation(self):
        for rec in self:
            rec.percentage_realisation = False
            if rec.target and rec.result != 0:
                rec.percentage_realisation = rec.result/rec.target


class DhChairsGoals(models.Model):
    _name = 'dh.chairs.goal'

    name = fields.Char('Name')
class DhChairsIndicators(models.Model):
    _name = 'dh.chair.indicators.goal'
    _order = 'seq'
    seq = fields.Char(required=False, readonly=True, copy=False,string="الرقم")

    @api.model
    def create(self, vals):
        if vals.get('seq', _('New')) == _('New'):
            vals['seq'] = self.env['ir.sequence'].next_by_code(
                'sdh_icesco_project.chair.indicators.goal.sequence') or _(
                'New')
        return super(DhChairsIndicators, self).create(vals)


    method_mesure = fields.Float('طريقة القياس')
    percentage = fields.Float('النسبة')


