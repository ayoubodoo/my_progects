# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # name = fields.Char(translate=True)
    prenom = fields.Char(translate=True,track_visibility='always')
    category_id = fields.Many2one('hr.category', string="Category",track_visibility='always')
    dependent_ids = fields.One2many('hr.employee.dependent', 'employee_id', string="Dependents",track_visibility='always')
    total_amount = fields.Float(string="Total amount", compute='_compute_total_amount',track_visibility='always')
    retirement_date = fields.Date(string="Retirement date" ,track_visibility='always')
    partner = fields.Char(translate=True,string="Partner" ,track_visibility='always')
    # job_isesco_id = fields.Many2one('hr.job.isesco', string="Job")

    # recrutement
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
    societe_job = fields.Char(stranslate=True,tring='Société poste actuel/dernier')
    had_experience_international_organization = fields.Boolean(
        string='Avoir expérience dans organisation internationale')
    name_international_organization = fields.Char(translate=True,string='Nom organisation internationale')

    language_1 = fields.Char(translate=True,string='Langue 1')
    language_2 = fields.Char(translate=True,string='Langue 2')
    language_3 = fields.Char(translate=True,string='Langue 3')
    language_4 = fields.Char(translate=True,string='Langue 4')
    language_5 = fields.Char(translate=True,string='Langue 5')

    linkedin_profil = fields.Char('LinkedIn Profile')

    def _compute_total_amount(self):
        for rec in self:
            total_amount = 0
            for dependent in rec.dependent_ids:
                if dependent.type == 'child':
                    if dependent.age <= rec.company_id.age_limit:
                        total_amount += dependent.amount * dependent.discharge_rate / 100
                else:
                    total_amount += dependent.amount * dependent.discharge_rate / 100
            rec.total_amount = total_amount


class HrEmployeeDependent(models.Model):
    _name = 'hr.employee.dependent'
    _description = 'HR Employee Dependent'

    name = fields.Char(string="Person", required=True)
    birthday = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age", compute='_compute_age')
    type = fields.Selection([('child','Child'),('partner','Partner')], string="Type")
    amount = fields.Float(string="Amount")
    discharge_rate = fields.Float(string="% discharge")
    employee_id = fields.Many2one('hr.employee', string="Employee")

    @api.depends('birthday')
    def _compute_age(self):
        for rec in self:
            age = 0
            if rec.birthday:
                age = relativedelta(fields.Date.today(),rec.birthday).years
            rec.age = age
