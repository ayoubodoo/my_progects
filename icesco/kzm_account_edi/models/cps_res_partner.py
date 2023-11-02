# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class res_partner(models.Model):
    _inherit = 'res.partner'
    id_fiscal = fields.Char(string=_(u"Identification fiscale"), required=False, )
    designation_bien_service = fields.Char(string=_(u"Désignation des biens et services"), required=False,
                        help=_(u"Cette valeur sera utille dans le Relevé de déduction demandé dans le processus de génération de la TVA"))

