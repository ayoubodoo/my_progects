# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from lxml import etree
import json


class ResPartner(models.Model):
    _inherit = 'res.partner'

    fax = fields.Char(string=u'Fax', size=20, required=False)
    ice = fields.Char(string="ICE")
    patente_code = fields.Char('Patente Code', size=32)
    cin = fields.Char('CIN', copy=False)
    evaluation_class_name = fields.Char(string='Designation Classe du fournisseur', required=False, readonly=True,
                                        index=False)

    _sql_constraints = [
        ("cin_uniq", "unique(cin)", "le numero de la CIN doit etre unique "),
    ]

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        res = super(ResPartner, self).fields_view_get(view_id=view_id,
                                                     view_type=view_type,
                                                     toolbar=toolbar,
                                                     submenu=submenu)

        if (self.env.company.cin_partenaire_obligatoire):
            doc = etree.XML(res['arch'])
            for node in doc.xpath("//field[@name='cin']"):
                node.set("required", "1")
                modifiers = json.loads(node.get("modifiers"))
                modifiers['required'] = True
                node.set("modifiers", json.dumps(modifiers))
            res['arch'] = etree.tostring(doc)
        return res
