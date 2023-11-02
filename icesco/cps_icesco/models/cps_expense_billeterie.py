# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CpsExpenseBilleterie(models.Model):
    _name = 'cps.expense.billeterie'
    _description = 'Cps expense billeterie'

    name = fields.Char(string='Nom', required=True)
    date = fields.Date("Date", required=True)
    employee_id = fields.Many2one('hr.employee', string="Employé", required=True)
    type_ids = fields.Many2many('cps.expense.type', string="Type", required=True)
    montant = fields.Float(string="Montant Total", compute='_compute_montant_total')
    line_ids = fields.One2many('cps.hr.expense', 'billeterie_id', string='Détails du billet')
    state = fields.Selection(
        selection=[("draft", "Brouillon"), ("valide", "Validé")],
        string="Status",
        default="draft",
        readonly=True,
    )
    expense_count = fields.Integer(compute='compute_count')

    ville_depart = fields.Many2one('res.city', string='Ville depart')
    ville_arrivee = fields.Many2one('res.city', string='Ville arrivee')

    def compute_count(self):
        for record in self:
            record.expense_count = self.env['hr.expense'].search_count(
                [('id', 'in', self.env['hr.expense'].search([('billeterie_id', '=', self.id)]).ids)])

    def get_expense(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Expense',
            'view_mode': 'tree,form',
            'res_model': 'hr.expense',

            'domain': [('id', 'in', self.env['hr.expense'].search([('billeterie_id', '=', self.id)]).ids)],
            'context': "{'create': False}"
        }

    @api.depends('line_ids', 'line_ids.montant')
    def _compute_montant_total(self):
        for rec in self:
            amount = 0
            tva = 0
            if len(rec.line_ids) > 0:
                for line in rec.line_ids:
                    amount += line.montant
                    if line.product_id.supplier_taxes_id.ids:
                        for line_tva in line.product_id.supplier_taxes_id:
                            tva += line.montant * line_tva.amount / 100

            rec.montant = amount + tva

    def button_regenerate_lines(self):
        for rec in self:
            for line in rec.line_ids:
                line.unlink()
            cps_hr_expense = []
            for type in rec.type_ids:
                for product in type.product_ids:
                    expense = self.env['cps.hr.expense'].create({'product_id': product.id, 'billeterie_id':rec.id, 'date':rec.date, 'employee_id':rec.employee_id.id})
                    cps_hr_expense.append(expense.id)

            rec.line_ids = [(6, 0, cps_hr_expense)]

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
                    self.env['hr.expense'].create(
                        {'name': ("Expense Billet %s pour %s le %s") % (rec.name, line.employee_id.name, line.date),
                         'employee_id': line.employee_id.id, 'date': line.date, 'product_id': line.product_id.id,
                         'tax_ids': [[6, 0, line.product_id.supplier_taxes_id.ids]] if line.product_id.supplier_taxes_id.ids else False,
                         'unit_amount': line.montant, 'quantity': 1,
                         'passager_id': line.passager_id.id if line.passager_id.id else False,
                         'payment_mode': line.payment_mode, 'billeterie_id': line.billeterie_id.id,
                         'account_id': self.env['product.product'].search([('id', '=', line.product_id.id)]).categ_id.property_account_expense_categ_id.id})

                rec.state = 'valide'