# encoding: utf-8
{
    'name': 'CPS Account Update',
    'version': '12.0',
    'author': 'Capital Project Strategies',
    'category': 'Account',
    'summary': 'CPS Account Update',
    'description': """
CPS Account Update
================================

    """,
    'website': '',
    'images': [],
    'depends': ['account'],
    'external_dependencies': {'python': ['pandas']},
    'data': [
        'security/ir.model.access.csv',
        'views/account_update_wizard.xml'

    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
