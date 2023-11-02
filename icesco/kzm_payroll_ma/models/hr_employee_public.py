# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class HrEmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    prenom = fields.Char(u'Prénom')
    matricule = fields.Char('Matricule', copy=False, track_visibility='always')
    employee_externe = fields.Boolean(string='External employee', track_visibility='always')
    cin = fields.Char('CIN', copy=False, track_visibility='always')
    date = fields.Date(string=u"Date d'embauche", default=fields.Date.today,
                       help=u"Cette date est requise pour le calcul de la prime d'ancienneté",track_visibility='always')
    anciennete = fields.Boolean(string=u"Prime d'ancienneté?", default=True,
                                help=u"Est ce que cet employé bénificie de la prime d'ancienneté",
                                track_visibility='always')
    mode_reglement = fields.Selection(selection=[('virement', 'Virement'),
                                                 ('cheque', u'Chèque'),
                                                 ('espece', u'Espèce')],
                                      string=u'Mode de règlement', default='virement', track_visibility='always')
    agence = fields.Char(string=u'Agence', track_visibility='always')
    bank = fields.Many2one('res.bank', string='Banque Marocaine', track_visibility='always')
    compte = fields.Char(string=u'Compte bancaire', track_visibility='always')
    chargefam = fields.Integer(string=u'Nombre de personnes à charge', default=0, track_visibility='always')
    logement = fields.Float('Abattement Fr Logement', default=0.0, track_visibility='always')
    type_logement = fields.Selection(selection=[('normal', 'Normal'),
                                                ('social', 'Social')], default='normal',
                                     string='Type logement', track_visibility='always')
    superficie_logement = fields.Float(string=u'Superficie(m²)', track_visibility='always')
    prix_acquisition_logement = fields.Float(string=u"Prix d'acquisition", track_visibility='always')
    affilie = fields.Boolean(string=u'Affilié', default=True,
                             help=u'Est ce qu on va calculer les cotisations pour cet employé',
                             track_visibility='always')
    address_home = fields.Char(string=u'Adresse Personnelle', track_visibility='always')
    address = fields.Char(string=u'Adresse Professionnelle', track_visibility='always')
    phone_home = fields.Char(string=u'Téléphone Personnel', track_visibility='always')
    ssnid = fields.Char(string='CNSS', copy=False, track_visibility='always')
    # payslip_count = fields.Integer(compute='get_payslip_count', track_visibility='always')
    # Ces champs "temporaire et type_employe" sont ajoutés pour les occasionnels
    # notament pour etat 9421
    temporaire = fields.Boolean(string="Temporaire", track_visibility='always')
    type_employe = fields.Selection([
        ('horaire', 'Journalier'),
        ('mensuel', 'Mensuel'),
    ], string="Type employé", default='mensuel', store=True, track_visibility='always'
    )
    # anciennete
    # annees_anciennete = fields.Float(string=u'Ancienneté', compute='calc_seniority', track_visibility='always')
    nb_jours_pointees_horaire = fields.Float('Nbr. jour pointés', track_visibility='always')
    # taux_anciennete = fields.Float(string=u'Taux ancienneté(%)',
    #                                compute='calc_seniority', track_visibility='always')
    carte_de_sejour = fields.Char("N° Carte de séjour", track_visibility='always')

    category_id = fields.Many2one('hr.category', string="Category",track_visibility='always')
    # dependent_ids = fields.One2many('hr.employee.dependent', 'employee_id', string="Dependents",track_visibility='always')
    # total_amount = fields.Float(string="Total amount", compute='_compute_total_amount',track_visibility='always')
    retirement_date = fields.Date(string="Retirement date" ,track_visibility='always')
    partner = fields.Char(string="Partner" ,track_visibility='always')
    is_translation = fields.Boolean(string='Translation', track_visibility='always')
    is_design = fields.Boolean(string='Design', track_visibility='always')
    is_legal = fields.Boolean(string='Legal', track_visibility='always')
    is_finance = fields.Boolean(string='Finance', track_visibility='always')
    is_admin = fields.Boolean(string='Admin', track_visibility='always')
    is_it = fields.Boolean(string='IT', track_visibility='always')
    is_media = fields.Boolean(string='Media', track_visibility='always')
    is_dg = fields.Boolean(string='DG Office', track_visibility='always')
    is_coverage = fields.Boolean(string='Coverage', track_visibility='always')
    is_dpt_participation = fields.Boolean(string='Dpt participation', track_visibility='always')

    # cps_leaves_count = fields.Float('Cps Number of Time Off', compute='_cps_compute_remaining_leaves',
    #                                 track_visibility='always')
    # cps_allocation_display = fields.Char(compute='_cps_compute_allocation_count', track_visibility='always')
    # cps_allocation_used_display = fields.Char(compute='_cps_compute_total_allocation_used', track_visibility='always')
    # cps_remaining_leaves = fields.Float(
    #     compute='_cps_compute_remaining_leaves', string='Cps Remaining Paid Time Off', track_visibility='always')
    # cps_allocation_count = fields.Float('Cps Total number of days allocated.', compute='_cps_compute_allocation_count',
    #                                     track_visibility='always')
    # cps_allocation_used_count = fields.Float('Cps Total number of days off used',
    #                                          compute='_cps_compute_total_allocation_used', track_visibility='always')

    # inherit

    # mobile_phone = fields.Char('Work Mobile', track_visibility='always')
    # work_phone = fields.Char('Work Phone', track_visibility='always')
    # work_email = fields.Char('Work Email', track_visibility='always')
    # work_location = fields.Char('Work Location', track_visibility='always')
    # company_id = fields.Many2one('res.company', 'Company', track_visibility='always')
    # department_id = fields.Many2one('hr.department', 'Department',
    #                                 domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    #                                 track_visibility='always')
    # job_id = fields.Many2one('hr.job', 'Job Position',
    #                          domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    #                          track_visibility='always')
    # parent_id = fields.Many2one('hr.employee', 'Manager',
    #                             domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    #                             track_visibility='always')
    # address_id = fields.Many2one('res.partner', 'Work Address',
    #                              domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    #                              track_visibility='always')
    # coach_id = fields.Many2one('hr.employee', 'Coach',
    #                            domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    #                            track_visibility='always')
    # leave_manager_id = fields.Many2one(
    #     'res.users', string='Time Off',
    #     help="User responsible of leaves approval.", track_visibility='always')

    last_ferm_pointage = fields.Many2one("res.company",
                                         string=_("Ferme de dernier pointage"), required=False, )

    last_date_pointage = fields.Datetime(string=_("Date de dernier pointage"), required=False, )