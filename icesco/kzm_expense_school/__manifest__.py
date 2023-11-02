# -*- coding: utf-8 -*-
{
    'name': "ICESCO: School Expense",
    'summary': """This module is use for the management of school expenses""",
    'description': """Create a school expense > Get it approve > Generate an expense """,
    'author': "Capital Project Strategies",
    'website': "",
    'category': 'Uncategorized',
    'version': '13.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'kzm_payroll_ma', 'isesco_hr', 'hr_expense'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/expense_sequence_data.xml',
        'data/data.xml',
        'views/expenses_views.xml',
        'views/categories_views.xml',
        'views/res_config_settings.xml',
        'views/menus.xml',
        'views/hr_bulletin_view.xml',
        'reports/report_school_fees_expense_request.xml',
    ],
}
