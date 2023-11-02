# -*- coding: utf-8 -*-

{
    'name': 'États Paie légaux Maroc',
    'version': '12.0',
    'category': 'HR',
    'complexity': "normal",
    'description': """
            Etats legaux Maroc : Journal de paie, Bulletin de paie, Bordereau de virement, Etat CNSS, Bordereau paiement CNSS""",
    'author': 'Capital Project Strategies',
    'website': '',
    'images': [],
    'depends': ['kzm_payroll_ma', 'l10n_ma'],
    'data': [
             'views/custom_bulletin_form_view.xml',
             'views/custom_payroll_parametres_view.xml',
             'views/company_virement_bank.xml',
             'report/reports_header_view.xml',
             'report/reports_view.xml',
             'report/journal_paie.xml',
             'report/bordereau_virement.xml',
             'report/etat_cnss.xml',
             'report/etat_igr.xml',
             'report/bordereau_paiement_cnss.xml',
             'report/etat_rubriques_par_departement.xml',
             'report/bordereau_paiement_multibanque.xml',
             'report/etat_paie.xml',
            'report/cps_hr_rep_amo.xml',

    ],
    'installable': True,
    'auto_install': False,
}

