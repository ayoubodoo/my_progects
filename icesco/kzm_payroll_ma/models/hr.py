# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from lxml import etree

import datetime
import json

class HrEmployee(models.Model):
    _inherit = 'hr.employee.public'

    prenom = fields.Char(u'Prénom')

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    employee_externe = fields.Boolean(string='External employee',track_visibility='always')
    category_id = fields.Many2one('hr.category', string="Category", track_visibility='always')

    def _compute_contract_id(self):
        """ get the lastest contract """
        Contract = self.env['hr.contract']
        for employee in self:
            employee.contract_id = Contract.search(
                [('employee_id', '=', employee.id),
                 ('state', 'in', ['open', 'pending'])], order='date_start desc',
                limit=1)

    matricule = fields.Char('Matricule', copy=False,track_visibility='always')
    cin = fields.Char('CIN', copy=False,track_visibility='always')
    prenom = fields.Char(u'Prénom',track_visibility='always')
    date = fields.Date(string=u"Date d'embauche", default=fields.Date.today,
                       help=u"Cette date est requise pour le calcul de la prime d'ancienneté",track_visibility='always')
    anciennete = fields.Boolean(string=u"Prime d'ancienneté?", default=True,
                                help=u"Est ce que cet employé bénificie de la prime d'ancienneté",track_visibility='always')
    mode_reglement = fields.Selection(selection=[('virement', 'Virement'),
                                                 ('cheque', u'Chèque'),
                                                 ('espece', u'Espèce')],
                                      string=u'Mode de règlement', default='virement',track_visibility='always')
    agence = fields.Char(string=u'Agence',track_visibility='always')
    bank = fields.Many2one('res.bank', string='Banque Marocaine',track_visibility='always')
    compte = fields.Char(string=u'Compte bancaire',track_visibility='always')
    chargefam = fields.Integer(string=u'Nombre de personnes à charge', default=0,track_visibility='always')
    logement = fields.Float('Abattement Fr Logement', default=0.0,track_visibility='always')
    type_logement = fields.Selection(selection=[('normal', 'Normal'),
                                                ('social', 'Social')], default='normal',
                                     string='Type logement',track_visibility='always')
    superficie_logement = fields.Float(string=u'Superficie(m²)',track_visibility='always')
    prix_acquisition_logement = fields.Float(string=u"Prix d'acquisition",track_visibility='always')
    affilie = fields.Boolean(string=u'Affilié', default=True,
                             help=u'Est ce qu on va calculer les cotisations pour cet employé',track_visibility='always')
    address_home = fields.Char(string=u'Adresse Personnelle',track_visibility='always')
    address = fields.Char(string=u'Adresse Professionnelle',track_visibility='always')
    phone_home = fields.Char(string=u'Téléphone Personnel',track_visibility='always')
    ssnid = fields.Char(string='CNSS', copy=False,track_visibility='always')
    payslip_count = fields.Integer(compute='get_payslip_count',track_visibility='always')
    # Ces champs "temporaire et type_employe" sont ajoutés pour les occasionnels
    # notament pour etat 9421
    temporaire = fields.Boolean(string="Temporaire",track_visibility='always')
    type_employe = fields.Selection([
        ('horaire', 'Journalier'),
        ('mensuel', 'Mensuel'),
    ], string="Type employé", default='mensuel', store=True,track_visibility='always'
    )
    # anciennete
    annees_anciennete = fields.Float(string=u'Ancienneté', compute='calc_seniority',track_visibility='always')
    nb_jours_pointees_horaire = fields.Float('Nbr. jour pointés',track_visibility='always')
    taux_anciennete = fields.Float(string=u'Taux ancienneté(%)',
                                   compute='calc_seniority',track_visibility='always')
    carte_de_sejour = fields.Char("N° Carte de séjour",track_visibility='always')

    _sql_constraints = [
        ("cin_uniq", "unique(cin)", "le numero de la CIN doit etre unique "),
    ]

    benifit_sup_heure = fields.Boolean(string='bénéficier heure sup', default=True)

    department_racine = fields.Many2one('hr.department', department='Racine department',
                                        compute='compute_racine_department', store=True)

    @api.depends('department_id')
    def compute_racine_department(self):
        for rec in self:
            rec.department_racine = False
            if rec.department_id.parent_id.parent_id.id == False:
                rec.department_racine = rec.department_id.id
            elif rec.department_id.parent_id.parent_id.parent_id.id == False:
                rec.department_racine = rec.department_id.parent_id.id
            elif rec.department_id.parent_id.parent_id.parent_id.parent_id.id == False:
                rec.department_racine = rec.department_id.parent_id.parent_id.id
            elif rec.department_id.parent_id.parent_id.parent_id.parent_id.parent_id.id == False:
                rec.department_racine = rec.department_id.parent_id.parent_id.parent_id.id
            elif rec.department_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.id == False:
                rec.department_racine = rec.department_id.parent_id.parent_id.parent_id.parent_id.id
            elif rec.department_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.id == False:
                rec.department_racine = rec.department_id.parent_id.parent_id.parent_id.parent_id.parent_id.id
            elif rec.department_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.id == False:
                rec.department_racine = rec.department_id.parent_id.parent_id.parent_id.parent_id.parent_id.parent_id.id
            else:
                rec.department_racine = False

    def name_get(self):
        res = []
        for p in self:
            name = ""
            if p.name is not False:
                name = p.name
            if p.prenom is not False:
                name = name + " " + p.prenom
            res.append((p.id, name))
        return res

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        res = super(HrEmployee, self).fields_view_get(view_id=view_id,
                                                      view_type=view_type,
                                                      toolbar=toolbar,
                                                      submenu=submenu)

        if (self.env.company.cin_employee_obligatoire):
            doc = etree.XML(res['arch'])
            for node in doc.xpath("//field[@name='cin']"):
                node.set("required", "1")
                modifiers = json.loads(node.get("modifiers"))
                modifiers['required'] = True
                node.set("modifiers", json.dumps(modifiers))
            res['arch'] = etree.tostring(doc)
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if name:
            domain = ['|', '|', ('matricule', operator, name), ('name', operator,
                                                                name), ('prenom',
                                                                        operator,
                                                                        name)] + (
                             args or [])
            return self.search(domain, limit=limit).name_get()
        return super(HrEmployee, self).name_search(name, args, operator, limit=limit)

    @api.onchange('bank_account_id')
    def onchange_bank_account_id(self):
        for rec in self:
            if rec.bank_account_id:
                rec.bank = rec.bank_account_id.bank_id
                rec.compte = rec.bank_account_id.acc_number

    @api.depends('date', 'type_employe', 'nb_jours_pointees_horaire')
    def calc_seniority(self):
        for rec in self:
            years = 0
            # ================== MENSUEL ================
            if rec.date and rec.type_employe == 'mensuel':
                seniority_date = fields.Date.from_string(rec.date)
                today = datetime.date.today()
                years = today.year - seniority_date.year
                if today.month < seniority_date.month or (
                        today.month == seniority_date.month and today.day < seniority_date.day):
                    years -= 1
            # ================== JOURNALIER =============
            if rec.nb_jours_pointees_horaire and rec.type_employe == 'horaire':
                years = int(rec.nb_jours_pointees_horaire / 365.0)

            rec.annees_anciennete = years
            rec.taux_anciennete = 0

            objet_anciennete = self.env['hr.payroll_ma.anciennete']
            liste = objet_anciennete.sudo().search([])
            for tranche in liste:
                if (years >= tranche.debuttranche) and (years < tranche.fintranche):
                    rec.taux_anciennete = tranche.taux
                    break

    # def get_parametre(self):
    #     params = self.env['hr.payroll_ma.parametres']
    #     return params.search([], limit=1)

    # Contrainte sur logement social
    @api.constrains('superficie_logement', 'prix_acquisition_logement', 'type_logement')
    def _check_param_logement_social(self):
        if self.type_logement == 'social':

            # dictionnaire = self.get_parametre()
            # On vérifie la superficie
            if self.superficie_logement > self.company_id.superficie_max_logement_social:
                raise ValidationError(
                    u"La superficie indiquée n'est pas conforme aux normes du logement social")
            # On vérifie le prix d'acquisition
            if self.prix_acquisition_logement > self.company_id.prix_achat_max_logement_social:
                raise ValidationError(
                    u"Le prix d'acquisition n'est pas conforme aux normes du logement social")

    # contrainte sur le RIB
    @api.constrains('compte')
    def _check_rib(self):
        if self.mode_reglement == 'virement':
            compte = self.compte.replace(' ', '')
            print(len(compte))
            if len(compte) != 24 or not compte.isdigit():
                raise ValidationError(u"Le RIB doit être constitué de 24 chiffres")

    # contrainte sur la matricule
    @api.constrains('matricule', 'company_id')
    def _check_matricule(self):
        if self.matricule:
            if self.company_id.matricule_by_company:
                employee_ids = self.env['hr.employee'].search(
                    [('matricule', '=', self.matricule), ('id', '!=', self.id),
                     ('company_id', '=', self.env.company.id)])
            else:
                employee_ids = self.env['hr.employee'].search(
                    [('matricule', '=', self.matricule), ('id', '!=', self.id)])
            if employee_ids:
                raise ValidationError(u"La matricule doit être unique")


    def get_payslip_count(self):
        for rec in self:
            count = len(self.env['hr.payroll_ma.bulletin'].sudo().search(
                [('employee_id', '=', rec.id)]))
            rec.payslip_count = count

    @api.model
    def create(self, values):
        if not values.get('matricule'):
            # employee_id = self.env['hr.employee'].search([], order='matricule desc', limit=1)
            # if employee_id and employee_id.matricule and employee_id.matricule.isdigit():
            #     values['matricule'] = str(int(employee_id.matricule) + 1).zfill(3)
            values['matricule'] = self.env['ir.sequence'].next_by_code(
                'hr.employee.matricule')
        return super(HrEmployee, self).create(values)

class ResPartnerType(models.Model):
    _inherit = "res.partner.bank"

    iban = fields.Char(string='IBAN', required=False, readonly=False, index=False, store=True)

class HrContract(models.Model):
    _inherit = "hr.contract"

    working_days_per_month = fields.Integer(string=u'Jours travaillés par mois',
                                            default=26)
    hour_salary = fields.Float(u'Salaire Horaire')
    monthly_hour_number = fields.Float(u'Nombre Heures par mois')
    ir = fields.Boolean(u'IR?')
    cotisation = fields.Many2one('hr.payroll_ma.cotisation.type',
                                 string=u'Type cotisation',
                                 company_dependent=True, required=True)
    rubrique_ids = fields.One2many('hr.payroll_ma.ligne_rubrique', 'id_contract',
                                   string='Rubriques')
    # actif = fields.Boolean(string="Actif", default=True)
    company_id = fields.Many2one(comodel_name='res.company',
                                 default=lambda self: self.env.company,
                                 string='Société', readonly=False, copy=False)
    type = fields.Selection(selection=[
        ('mensuel', 'Mensuel'),
        ('horaire', u'Horaire')
    ], string='Type', default='mensuel')

    appliquer_heure_sup = fields.Boolean(string='apply overtime')

    def write(self, vals):
        res = super().write(vals)
        if 'category_id' in vals or 'wage' in vals:
            for rub in self.rubrique_ids:
                if rub.permanent == True or rub.date_stop >= fields.Date.today():
                    rub.compute_montant_formule()
                    rub.onchange_rubrique_id()
        return res


    @api.onchange('type')
    def onchange_type(self):
        # params = self.env['hr.payroll_ma.parametres']
        # ids_params = params.search([('company_id', '=', self.company_id.id)], limit=1)
        for rec in self:
            if rec.type == 'mensuel':
                rec.hour_salary = 0
                rec.monthly_hour_number = 0
                rec.working_days_per_month = 26
            if rec.type == 'horaire':
                rec.wage = 0
                rec.working_days_per_month = 0
                # rec.monthly_hour_number = ids_params.hour_month // 
                rec.monthly_hour_number = rec.company_id.hour_month  # 

    @api.constrains('state', 'date_start')
    def _check_unicite_contrat(self):
        contrat_ids = self.env['hr.contract'].search(
            [('employee_id', '=', self.employee_id.id),
             ('state', 'in', ['open', 'pending']),
             ('id', '!=', self.id)])
        if contrat_ids and self.state in ['open', 'pending']:
            raise ValidationError(u'Plusieurs contrats actifs pour cet employé!')
        if self.state in ['open', 'pending']:
            self.employee_id.date = self.date_start

    # @api.one
    # @api.constrains('date_start','employee_id.date')
    # def _check_unicite_contrat_date(self):
    #     if self.date_start < self.employee_id.date:
    #         raise ValidationError(u'La date de contrat ne peut pas être avant la date d\'embauche.!')

    #
    # def cloturer_contrat(self):
    #     for rec in self:
    #         rec.actif = False
    #         rec.date_end = fields.Date.context_today(self)
    #
    #
    # def activer_contrat(self):
    #     for rec in self:
    #         rec.actif = True
    #         rec.date_end = None

    def net_to_brute(self):
        for rec in self:
            salaire_base = rec.wage
            cotisation = rec.cotisation
            personnes = rec.employee_id.chargefam
            # params = self.env['hr.payroll_ma.parametres']
            objet_ir = self.env['hr.payroll_ma.ir']

            liste = objet_ir.search([])
            # dictionnaire = rec.employee_id.get_parametre()
            abattement = personnes * rec.company_id.charge

            base = 0
            salaire_brute = salaire_base
            trouve = False
            trouve2 = False
            while (trouve == False):
                salaire_net_imposable = 0
                cotisations_employee = 0
                for cot in cotisation.cotisation_ids:
                    if cot.plafonee and salaire_brute >= cot.plafond:
                        base = cot.plafond
                    else:
                        base = salaire_brute

                    cotisations_employee += base * cot.tauxsalarial / 100
                fraispro = salaire_brute * rec.company_id.fraispro / 100
                if fraispro < rec.company_id.plafond:
                    salaire_net_imposable = salaire_brute - fraispro - cotisations_employee
                else:
                    salaire_net_imposable = salaire_brute - rec.company_id.plafond - cotisations_employee
                for tranche in liste:
                    if (salaire_net_imposable >= tranche.debuttranche / 12) and (
                            salaire_net_imposable < tranche.fintranche / 12):
                        taux = (tranche.taux)
                        somme = (tranche.somme / 12)

                ir = (salaire_net_imposable * taux / 100) - somme - abattement
                if (ir < 0): ir = 0
                salaire_net = salaire_brute - cotisations_employee - ir
                if (int(salaire_net) == int(salaire_base) and trouve2 == False):
                    trouve2 = True
                    salaire_brute -= 1
                if (round(salaire_net, 2) == salaire_base):
                    trouve = True
                elif trouve2 == False:
                    salaire_brute += 0.5
                elif trouve2 == True:
                    salaire_brute += 0.01

            rec.wage = round(salaire_brute, 2)
            return True

# class HRHolidaysStatus(models.Model):
#     _inherit = "hr.holidays.status"
#
#     payed = fields.Boolean(string=u'Payé', default=True)
