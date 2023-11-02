# -*- coding: utf-8 -*-

{
    'name': 'Employee Loans & Advances',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """

    """,
    'author': 'Capital Project Strategies',
    'website': '',
    'images': [],
    'depends': ['hr', 'account', 'kzm_payroll_ma'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_loan_view.xml',
        'security/security.xml',
        'views/menus.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
