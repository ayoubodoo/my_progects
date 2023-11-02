# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "GCLOUD AUTO-BACKUP, OCA AUTO-BACKUP EXTENSION",
    "version": "0.2.3",
    "author": "Capital Project Strategies",
    "license": 'AGPL-3',
    "description": """
      Nedd OCA/SEREVER-TOOLS
    """,
    "summary": "",
    "website": "",
    "category": 'Tools',
    "sequence": 20,
    "depends": [
        'auto_backup',
    ],
    "data": [
        'views/db_backup.xml',
    ],
    "qweb": [
    ],
    "auto_install": False,
    "installable": True,
    "application": False,
}
