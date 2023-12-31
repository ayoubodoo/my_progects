# -*- coding: utf-8 -*-
{
    'name': 'Dashboard Ninja',

    'summary': """
Ksolves Dashboard Ninja gives you a wide-angle view of your business that you might have missed. Get smart visual data with interactive and engaging dashboards for your Odoo ERP.  Odoo Dashboard, CRM Dashboard, Inventory Dashboard, Sales Dashboard, Account Dashboard, Invoice Dashboard, Revamp Dashboard, Best Dashboard, Odoo Best Dashboard, Odoo Apps Dashboard, Best Ninja Dashboard, Analytic Dashboard, Pre-Configured Dashboard, Create Dashboard, Beautiful Dashboard, Customized Robust Dashboard, Predefined Dashboard, Multiple Dashboards, Advance Dashboard, Beautiful Powerful Dashboards, Chart Graphs Table View, All In One Dynamic Dashboard, Accounting Stock Dashboard, Pie Chart Dashboard, Modern Dashboard, Dashboard Studio, Dashboard Builder, Dashboard Designer, Odoo Studio.  Revamp your Odoo Dashboard like never before! It is one of the best dashboard odoo apps in the market.
""",

    'description': """
Dashboard Ninja v13.0,
        Odoo Dashboard,
        Dashboard,
	    Dashboards,
        Odoo apps,
        Dashboard app,
        HR Dashboard,
        Sales Dashboard,
        inventory Dashboard,
        Lead Dashboard,
        Opportunity Dashboard,
        CRM Dashboard,
	    POS,
	    POS Dashboard,
	    Connectors,
	    Web Dynamic,
	    Report Import/Export,
	    Date Filter,
	    HR,
	    Sales,
	    Theme,
	    Tile Dashboard,
	    Dashboard Widgets,
	    Dashboard Manager,
	    Debranding,
	    Customize Dashboard,
	    Graph Dashboard,
	    Charts Dashboard,
	    Invoice Dashboard,
	    Project management,
	    dashboard,
        odoo dashboard,
        odoo apps,
        all in one dashboard,
        dashboard odoo,
        dashboard items,
        multiple dashboards,
        dashboard menu,
        dashboard view,
        create multiple dashboards,
        multiple dashboard menu,
        edit dashboard items,
        dahsboard view,
""",

    'author': 'Ksolves India Ltd.',

    'license': 'OPL-1',

    'currency': 'EUR',

    'price': '290.4',

    'website': 'https://www.ksolves.com',

    'maintainer': 'Ksolves India Ltd.',

    'live_test_url': 'https://dn15demo.kappso.com/web#cids=1&menu_id=599&ks_dashboard_id=1&action=835',

    'category': 'Tools',

    'version': '13.0.4.5.2',

    'support': 'sales@ksolves.com',

    'images': ['static/description/dn_sale_opt.gif'],

    'depends': ['base', 'web', 'base_setup', 'bus', 'account', 'isesco_base'],

    'data': ['security/ir.model.access.csv', 'security/ks_security_groups.xml', 'data/ks_default_data.xml',
             'views/ks_dashboard_ninja_view.xml', 'views/ks_dashboard_ninja_item_view.xml',
             'views/ks_dashboard_ninja_assets.xml', 'views/ks_dashboard_action.xml',
             'views/ks_import_dashboard_view.xml', 'wizard/ks_create_dashboard_wizard_view.xml',
             'wizard/ks_duplicate_dashboard_wiz_view.xml', 'views/account_move_line.xml'],

    'qweb': ['static/src/xml/ks_dn_global_filter.xml', 'static/src/xml/ks_dashboard_ninja_templates.xml',
             'static/src/xml/ks_dashboard_ninja_item_templates.xml', 'static/src/xml/ks_dashboard_ninja_item_theme.xml',
             'static/src/xml/ks_widget_toggle.xml', 'static/src/xml/ks_dashboard_pro.xml',
             'static/src/xml/ks_quick_edit_view.xml', 'static/src/xml/ks_to_do_template.xml'],

    'demo': ['demo/ks_dashboard_ninja_demo.xml'],

    'uninstall_hook': 'uninstall_hook',
}
