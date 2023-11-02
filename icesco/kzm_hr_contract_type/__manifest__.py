# Copyright 2013 Nicolas Bessi (Camptocamp SA)
# Copyright 2014 Agile Business Group (<http://www.agilebg.com>)
# Copyright 2015 Grupo ESOC (<http://www.grupoesoc.es>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'CPS Type contrat',
    'summary': "Add contract type to contrat, like V12",
    'version': '12.0.1.0.0',
    'author': "Capital Project Strategies",
    'license': "AGPL-3",
    'category': 'contrat',
    'website': '',
    'depends': ['hr_contract'],
    'data': [
         'data/hr_contract_type.xml',
         'security/ir.model.access.csv',
        'views/hr_contract.xml',
    ],
    'auto_install': False,
    'installable': True,
}
