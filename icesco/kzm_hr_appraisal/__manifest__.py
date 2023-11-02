# -*- coding: utf-8 -*-
{
    'name': "kzm_hr_appraisal",

    'summary': """
    apparaisal rating factor
       """,

    'description': """
        cps apparaisal
    """,

    'author': "My Company",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'isesco_hr', 'hr'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'data/templates.xml',
        'views/appraisal_rating_factor.xml',
        'views/appraisal_axis_view.xml',
        'views/appraisal_axis_evaluation_view.xml',
        'views/appraisal_matrix_views.xml',
        'views/appraisal_model_view.xml',
        'views/appraisal_appraisal_view.xml',
        'views/hr_employee_view.xml',
        'views/appraisal_factor_value_view.xml',
        'views/menus.xml',
        'report/appraisal_global_evaluation_template.xml',
        'report/annual_performance_appraisal_employee_template.xml',
        'report/excel_global_evaluation.xml',
        'wizard/global_evaluation_report_wizard.xml',
        'wizard/global_evaluation_report_wizard_department_year.xml',
        'wizard/global_evaluation_excel_report.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
