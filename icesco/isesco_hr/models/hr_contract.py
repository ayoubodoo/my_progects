# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class HrContract(models.Model):
    _inherit = 'hr.contract'

    category_id = fields.Many2one('hr.category', string="Category")
    is_rubrique_dependent = fields.Boolean("is rubrique dependent?", compute='_compute_is_rubrique_dependent')

    def no_rubrique_dependent(self):
        raise ValidationError(_("Please confiqure a rubrique for dependent!"))

    def _compute_is_rubrique_dependent(self):
        for rec in self:
            if rec.company_id.rubrique_dependent_id:
                rec.is_rubrique_dependent = rec.rubrique_ids.filtered(lambda line: line.rubrique_id == rec.company_id.rubrique_dependent_id)
            else:
                rec.is_rubrique_dependent = False

    def generate_rubrique_dependent(self):
        for rec in self:
            if rec.employee_id and rec.company_id.rubrique_dependent_id:
                rubrique_id = rec.rubrique_ids.filtered(lambda l: l.rubrique_id == rec.company_id.rubrique_dependent_id)
                if rubrique_id:
                    rubrique_id[0].montant = rec.employee_id.total_amount
                    rubrique_id[0].permanent = True
                else:
                    dependent_rubrique = {
                        'rubrique_id': rec.company_id.rubrique_dependent_id.id,
                        'montant': rec.employee_id.total_amount,
                        'permanent': True,
                    }
                    rec.rubrique_ids = [(0, 0, dependent_rubrique)]
            elif not rec.company_id.rubrique_dependent_id:
                self.no_rubrique_dependent()

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        super(HrContract, self)._onchange_employee_id()
        if self.employee_id:
            self.name = ' '.join([self.employee_id.name, self.employee_id.prenom])
            self.category_id = self.employee_id.category_id

    @api.onchange('category_id')
    def _onchange_category_id(self):
        if self.category_id:
            self.wage = self.category_id.amount


class HrContractCategory(models.Model):
    _name = 'hr.contract.category'
    _description = 'HR Contract Category'

    code = fields.Char(string="Code", required=True)
    name = fields.Char(translate=True,string="Description", required=True)
    grade_ids = fields.Many2many('hr.contract.grade', string="Grades")


class HrContractGrade(models.Model):
    _name = 'hr.contract.grade'
    _description = 'HR Contract Grade'

    code = fields.Char(string="Code", required=True)
    name = fields.Char(translate=True,string="Description", required=True)
