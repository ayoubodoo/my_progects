# -*- coding: utf-8 -*-
{
    'name': "l10n_ma_bp_check_printing",
    'version': '1.0',
    'category': 'Accounting/Accounting',
    'summary': 'Print MA Checks',
    'description': """
This module allows to print your payments on pre-printed check paper.
You can configure the output (layout, stubs informations, etc.) in company settings, and manage the
checks numbering (if you use pre-printed checks without numbers) in journal settings.

    """,
    'website': '',
    'depends' : ['account_check_printing', 'l10n_ma'],
    'data': [
        'data/ma_bp_check_printing.xml',
        'report/check_pb_print_report.xml',
        'report/check_ab_print_report.xml',
        'views/res_config_settings_views.xml',
        'wizard/print_check_wizard_views.xml',
    ],
    'installable': True,
    'auto_install': True,
}