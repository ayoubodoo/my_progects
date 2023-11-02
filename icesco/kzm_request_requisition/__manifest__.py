# -*- coding: utf-8 -*-

{
    "name": "Cps request requisition",
    "version": "13.0",
    "depends": ["purchase_request", "purchase_requisition", "account_accountant", "kzm_supplier_type"],
    "author": "Capital Project Strategies",
    'website': '',
    "category": "",
    "description": "Add contract in Multiple consultation in DP Generation",
                        
    "init_xml": [],
    'data': [
        "data/data.xml",
        "views/purchase_order_views.xml",
        "wizard/purchase_request_line_views_inherit.xml",
        "views/request_requesition_appel_offre_views.xml",
        "views/purchase_request_line_views.xml",
        "views/res_config_views.xml",
    ],
    'demo_xml': [],
    'installable': True,
    'active': False,
}
