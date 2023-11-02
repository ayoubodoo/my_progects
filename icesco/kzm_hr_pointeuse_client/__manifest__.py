# -*- coding: utf-8 -*-
{
    'name': 'CPS HR Pointeuse Client',
    'version': '13.0',
    'category': 'HR',
    'complexity': "normal",
    'description': """
                    Module qui gére la pointeuse
                   """,
    'author': 'Capital Project Strategies',
    'website': '',
    'images': [],
    'depends': ['base','kzm_hr_pointeuse'],
    'data': [
        'security/security_view.xml',
        'views/res_config.xml',
        'views/cps_hr_pointeuse.xml',

    ],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}

