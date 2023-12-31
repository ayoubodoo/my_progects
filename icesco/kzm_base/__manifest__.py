# encoding: utf-8
##############################################################################
#
#    Localisation marocaine module for OpenERP, Localisation marocaine, Les bases
#    Copyright (C) 2014 (<http://www.example.org>) Anonym
#
#    This file is a part of Localisation marocaine
#
#    Localisation marocaine is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Localisation marocaine is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Base Localisation Marocaine',
    'version': '1.1',
    'author': 'Capital Project Strategies',
    'category': 'Localisation marocaine',
    'summary': 'Paie, Liasse fiscale, TVA, Immobilisation',
    'description': """
Localisation marocaine - La base
================================

    """,
    'website': '',
    'images': [],
    'depends': ['base','web'],
    'data': [
        'security/ir.model.access.csv',
        'data/precision.xml',
        'data/bank.xml',
        'data/commune.xml',
        'data/forme_juridique.xml',
        'views/templates.xml',
        'views/company.xml',
        'views/commune.xml',
        'views/partner_view.xml',
        'views/ir_qweb.xml',
        'views/base_config_view.xml',

    ],


    'test': [
        'test/users.yml',
        'test/sequence.yml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
