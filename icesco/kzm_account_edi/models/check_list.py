#from openerp.osv import fields, osv
from odoo import models, fields, api


class check_list(models.Model):
    
    _name = "check.list.erp"
    _description = "check.list.erp"

    def _is_errone(self):
        for record in self:
            record.exercice_errone = True
            if record.exercice == 0:
                record.exercice_errone = False

    def _is_erronep(self):
        for record in self:
            record.exercicep_errone = True
            if record.exercicep == 0:
                record.exercicep_errone = False



    etat = fields.Char('Etat')
    name = fields.Char('Nom')
    exercice = fields.Float('Exercice N')
    exercice_errone = fields.Boolean(compute=_is_errone, string='Compte errone')
    exercicep = fields.Float('Exercice N-1')
    exercicep_errone = fields.Boolean(compute=_is_erronep, string='Compte errone')

    
class check_rubrique(models.Model):
    
    def _is_errone(self):
        for record in self:
            record.errone = True
            if (record.valeurbal - record.valeurres) == 0:
                record.errone = False

    _name = "check.rubrique.erp"
    _description = "check.rubrique.erp"

    name = fields.Char('Rubrique')
    compte = fields.Char('Compte')
    valeurbal = fields.Float('Balance')
    valeurres = fields.Float('Resultat')
    errone = fields.Boolean(compute=_is_errone, string='Etat')
