# -*- coding: utf-8 -*-
{
    'name': 'ISESCO HR',
    'version': '13.0',
    'category': 'HR',
    'complexity': "normal",
    'description': """
                    ISESCO HR
                   """,
    'author': 'Capital Project Strategies',
    'website': '',
    'images': [],
    'depends': ['kzm_payroll_ma','hr_recruitment'],
    'data': [
            'security/ir.model.access.csv',
            'views/hr_contract_views.xml',
            'views/hr_category_views.xml',
            'views/hr_payroll_ma_views.xml',
            'views/hr_department.xml',
            'views/hr_employee_views.xml',
            'wizard/meeting_invitation.xml',
            'views/hr_applicant.xml',
            'views/res_config_settings_views.xml',
            'reports/bulletin_paies.xml',
            'reports/dh_offer_letter.xml',
            'reports/excel_reports.xml',

        'data/data.xml',
        'data/mail_templates.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}

