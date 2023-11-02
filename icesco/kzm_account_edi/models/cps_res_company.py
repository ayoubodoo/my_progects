# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class res_company(models.Model):
    _inherit = 'res.company'

    cnss = fields.Char(string=_("CNSS"), required=True, )
    patente = fields.Char(string=_("Patente"), related='partner_id.patente_code', store=True)
    ice = fields.Char(related='partner_id.ice')
    designation_bien_service = fields.Char(related='partner_id.designation_bien_service')

    @api.onchange('cnss')
    def change_cnss(self):
        self.validation_cnss()

    def validation_cnss(self):
        if self.cnss:
            if len(self.cnss) == 7:
                chaine = chaine_com = str(self.cnss)
                somme = 0
                somme = 2 * (int(chaine[1]) + int(chaine[3]) + int(chaine[5])) + (
                        int(chaine[0]) + int(chaine[2]) + int(chaine[4]))
                # chaine = str(somme)
                # reste = 10 - int(chaine[1])
                reste = 10 - somme % 10
                if reste == 10:
                    reste = 0
                if int(chaine_com[6]) == reste:
                    return True
                else:
                    raise ValidationError(u"Le numéro CNSS que vous avez saisie est inccorect.")
            else:
                raise ValidationError(u"Le numéro CNSS doit contient 7 chiffres")

    @api.constrains('cnss')
    def check_cnss(self):
        self.validation_cnss()
