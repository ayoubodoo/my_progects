# -*- coding: utf-8 -*-
{
    'name': 'CPS HR Pointeuse Absence',
    'version': '13.0',
    'category': 'HR',
    'complexity': "normal",
    'description': """
                    Module qui gére les Absences
                   """,
    'author': 'Capital Project Strategies',
    'website': '',
    'images': [],
    'depends': ['base','kzm_hr_pointeuse'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_absence.xml',
        'data/crons.xml',

    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}

