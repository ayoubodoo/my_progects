# -*- coding: utf-8 -*-
{
    'name': "DB: CPS Gestion de Pointeuses",

    'summary': """
        Gestion des pointeuses & présences & badges """,

    'description': """
        Le module permet une gestion maitrisée des pointeuses. L'utilisateur pourra réaliser tous les opérations d'ajout, modification et suppression d'une pointeuse.
        Le module permet en outre de tester si une pointeuse est connectée ou pas.
        il permet aussi l'import automatiques des présences à partir des pointeuses gérées
        il permet aussi la gestion des badges, leur impression et la communication avec les pointeuses, (gestion des utilisateurs, des badges, ...)
    """,

    'author': "Capital Project Strategies",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Modules & Communication',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'hr_attendance',
        'hr_contract',
        'cps_icesco',
        # 'kzm_hr_payroll_ma',
        # 'kzm_type_contrat',
        'kzm_hr_contract_type'
    ],

    # always loaded
    'data': [
        'security/ir_rule.xml',
        'security/ir.model.access.csv',
        'data/cps_hr_pointeuse_data.xml',
        'data/cps_hr_employee_sequence.xml',
        'data/cps_hr_pointeuse_sequence.xml',
        'data/paperFormat.xml',
        'data/crons.xml',
        'kzm_hr_pointage_journalier/security/cps_security.xml',
        'kzm_hr_pointage_journalier/security/ir.model.access.csv',
        'kzm_hr_pointage_journalier/security/ir_rule.xml',
        'wizard/wizard_finalize_attendencies.xml',
        'views/cps_hr_pointeuse_view.xml',
        'views/cps_hr_pointeuse_badge_view.xml',
        'views/cps_hr_pointeuse_badge_report.xml',
        'views/zk_attendencies.xml',
        'views/menus.xml',
        'views/cps_import_attendance_view.xml',
        'views/hr_attendance_view.xml',
        'views/specific_holidays.xml',

        'wizard/cps_hr_pointeuse_connection_view.xml',
        'wizard/cps_hr_pointeuse_load_attendance_view.xml',
        'wizard/cps_hr_pointeuse_copie.xml',

        'kzm_hr_pointage_journalier/cps_hr_pointage_journalier.xml',
        'kzm_hr_pointage_journalier/cps_sequence.xml',
        'kzm_hr_pointage_journalier/cps_statistique_view.xml',
        'kzm_hr_pointage_journalier/hr_employee_view.xml',
        'kzm_hr_pointage_journalier/cps_presences_journalieres.xml',

    ],
    # only loaded in demonstration mode
    'demo': [

    ],

    'qweb': [
        "static/src/xml/attendance.xml",
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}
