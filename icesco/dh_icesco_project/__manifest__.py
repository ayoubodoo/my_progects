# -*- coding: utf-8 -*-
{
    'name': "Icesco Project Strategies",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Dynamic Horizon : Mehdi Errzieq",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web_one2many_kanban', 'cps_icesco', 'project', 'account_budget', 'purchase', 'icesco_project', 'many2many_tags_link'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'data/template_mail.xml',
        # 'wizard/dh_budget_project_wizard.xml',
        'views/account_move_line.xml',
        'views/dh_icesco_plan_strategies.xml',
        'views/dh_icesco_goal_strategies.xml',
        'views/dh_agreements_international.xml',
        'views/dh_agreement_type.xml',
        'views/dh_agreement_category.xml',
        'views/dh_icesco_operational_plan.xml',
        'views/dh_icesco_performance_strategies.xml',
        'views/dh_icesco_performance_analysis.xml',
        'views/dh_icesco_office.xml',
        'views/dh_icesco_informations.xml',
        'views/templates.xml',
        'views/project_task.xml',
        'views/res_partner.xml',

        'views/dh_employee.xml',
        'views/dh_perf_operation.xml',
        'views/project_task.xml',
        'views/dh_orientations.xml',
        'views/dh_perf_sector.xml',
        'views/dh_perf_type_activity.xml',
        'views/dh_mission.xml',
        'views/project_project.xml',
        'views/dh_pilliar.xml',
        'views/dh_bourse.xml',
        'views/dh_awards.xml',
        'views/dh_chairs.xml',
        'views/dh_agreements_international_sectors.xml',
        'views/key_performance_indicators.xml',
        'views/link_dev_goals.xml',
        'views/risks_addressing.xml',
        'views/cps_expense_billeterie.xml',
        'views/dh_non_sector_programme.xml',
        'views/dh_etapes_done.xml',
        'views/dh_indicator_result_type.xml',
        'views/dh_expense_purchase.xml',
        'views/dh_contrucutions.xml',
        'views/account_budget.xml',
        'views/dh_menus.xml',
        'views/dh_orientation_graph.xml',
        'views/dh_pilliar_graph.xml',
        'views/dh_sector_dpt.xml',
        'views/dh_task_graph.xml',
        'views/analyse_budget_approved_graph.xml',
        'views/dh_agreements_international_graph.xml',
        'views/project_task_budget_graph.xml',
        'views/dh_contribution_graph.xml',
        'views/dh_icesco_proposition.xml',
        'views/dh_menus.xml',
        'views/analyse_budget_approved.xml',
        'static/src/xml/templates.xml',
    ],
    'qweb': [
        'static/src/xml/operational_groupby.xml',
    ],
}
