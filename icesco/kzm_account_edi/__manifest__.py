# -*- coding: utf-8 -*-
{
    'name': "Account Edi",
    'summary': """Liasse Fiscale""",
    'description': """""",
    'author': "Capital Project Strategies",
    'website': "",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base',
                'kzm_base',
                'account_accountant',
                'account',
                'report_xlsx',
                'kzm_account_fiscalyear_type',
                ],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'views/balance_view.xml',
        'views/conf_view.xml',
        'views/extra_tab_view.xml',
        'views/liasse_fiche_signalitique.xml',
        'views/liasse_sequence.xml',
        'data/code_edi.xml',
        'data/codification_tableaux.xml',
        'data/code_compte.xml',
        'data/compte.xml',
        'data/check_list_data.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'active': False,
    'installable': True,
}