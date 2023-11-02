# -*- coding: utf-8 -*-
{
    'name': 'CPS Payslip Email',
    'version': '13.0',
    'category': 'HR',
    'complexity': "normal",
    'description': """
                    CPS Payslip Send Email
                   """,
    'author': 'Capital Project Strategies',
    'website': '',
    'images': [],
    'depends': ['kzm_payroll_ma'],
    'data': [
        'views/hr_payroll_views.xml',
        'data/mail_template.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}

