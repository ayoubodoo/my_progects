# -*- coding: utf-8 -*-
{
    'name': "ICESCO: Shifting Expense",
    'summary': """This module is use for the management of shifting expenses""",
    'description': """Create a shifting expense > Get it approve > Generate an expense """,
    'author': "Capital Project Strategies",
    'website': "",
    'category': 'Uncategorized',
    'version': '13.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'isesco_hr', 'hr_expense'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/expense_sequence_data.xml',
        'views/expenses_views.xml',
        'views/categories_views.xml',
        'views/hr_expense.xml',
        'views/menus.xml',
    ],
}
