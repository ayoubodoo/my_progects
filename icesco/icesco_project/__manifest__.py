# -*- coding: utf-8 -*-
{
    'name': "icesco project",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Capital Project Strategies",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','project','project_team','purchase_request',
                'kzm_expense_shifting','purchase','event','base_continent', 'product'],

    # always loaded
    'data': [
        'data/ir_cron.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/project_project.xml',
        'views/purchase_order.xml',
        'views/purchase_request.xml',
        'views/hr_expense.xml',
        'views/hr_expense_shifting.xml',
        'views/event_event.xml',
        'views/res_geographical.xml',
        'views/project_nature.xml',
        'views/project_beneficiary_category.xml',
        'views/intervention_type_views.xml',
        'views/res_stakeholder_views.xml',
        # 'views/project_task_views.xml',
        'views/activity_reference_views.xml',
        'views/res_city_views.xml',
        'views/menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
