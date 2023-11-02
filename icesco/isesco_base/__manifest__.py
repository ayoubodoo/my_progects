# -*- coding: utf-8 -*-
{
    'name': 'ISESCO Base',
    'version': '13.0',
    'category': '',
    'complexity': "normal",
    'description': """
                    ISESCO Base
                   """,
    'author': 'Capital Project Strategies',
    'website': '',
    'images': [],
    'depends': ['base',
                'account',
                'purchase',
                'stock',
                'purchase_request',
                'stock_account',
                'account_asset',
                'cps_icesco'],
    'data': [
            'security/ir.model.access.csv',
            'security/security.xml',
            'views/res_partner_views.xml',
            'views/stock_wizard.xml',
            'views/account_move_line.xml',
            'views/menu.xml',
            'reports/purchase_order.xml',
            'reports/stock_picking.xml',
            'reports/transfer_letter_report.xml',
            'reports/report_supplier_return_slip.xml',
            'reports/purchase_footers_templates.xml',
            'reports/stock_situation_report.xml',
            'reports/report_out_of_stock_destination.xml',
            'wizard/out_of_stock_wizard_views.xml',
            'wizard/account_move_wizard_views.xml',
            'wizard/account_asset_wizard_views.xml',
            'views/account_move.xml',
            'views/account_asset_views.xml',
            'views/cps_purchase_order.xml',
            'views/account_asset.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}
