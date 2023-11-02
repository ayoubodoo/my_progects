# -*- coding: utf-8 -*-
{
    'name': "ICESCO PORTAL",
    'summary': """icesco portal module""",
    'description': """Generic Module for the icesco portal""",
    'author': "Capital Project Strategies",
    'category': 'Uncategorized',
    'version': '13.0',
    'depends': ['base', 'website', 'portal', 'cps_icesco', 'website_helpdesk_form', 'project', 'dh_icesco_project'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/templates.xml',
        'views/portal_my_goal.xml',
        'views/portal_member_states.xml',
        'views/helpdesk_templates.xml',
        'views/appraisal_templates.xml',
        'views/contact_us.xml',
    ],

}