# -*- coding: utf-8 -*-
{
    'name': "CPS ACCOUNT FISCALYEAR TYPE / QUINZAINES",

    'summary': """
        Ajouter des flags pour le type de date range: period et quanzaine
        """,

    'description': """
        This module is for account fiscalyear type
    """,

    'author': "Capital Project Strategies",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Account',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'date_range',
        'account_fiscal_year',#OCA/account-financial-tools
        'account_fiscal_period',
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/account_fiscalyear_views.xml',

    ],
    'qweb': [
        "static/src/xml/account_reconciliation.xml",
    ],
    # only loaded in demonstration mode
    #'demo': [
    #    'demo/demo.xml',
    #],
}
