# -*- coding: utf-8 -*-
{
    'name': "Cps Medical Insurance",

    'summary': """
        """,

    'description': """
        
    """,

    'author': "Capital Project Strategies",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'hr',
                'isesco_hr',
                'account_fiscal_period',
                'hr_expense',
                'kzm_payroll_ma',
                ],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'data/data_setting.xml',
        'data/mail_template.xml',
        'views/medical_record.xml',
        'views/medical_contract.xml',
        'views/medical_record_benifit.xml',
        'views/medical_record_type.xml',
        'views/medical_refund_request.xml',
        'views/medical_refund_request_run.xml',
        'views/res_config_settings.xml',
        'reports/before_meeting_template.xml',
        'reports/after_meeting_template.xml',
        'views/menu.xml',
        'reports/bank_transfert_report.xml',
        'reports/mensual_prestation_report.xml',
        'reports/report.xml',
         'wizard/dh_ir_reports.xml',

    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
