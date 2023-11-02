# -*- encoding: utf-8 -*-

from odoo import models, fields, api
# from openerp.osv import fields, osv
from odoo import tools


class liasse_configuration(models.Model):
    _name = "liasse.configuration.erp"
    _description = "liasse.configuration.erp"

    code = fields.Many2one('liasse.code.erp', 'Code EDI', required=True)
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Somme'),
        ('2', 'Total'),
        ('3', 'Si positive'),
        ('4', 'Si negative'),
    ], 'Type', default='0')
    code_ids = fields.Many2many('liasse.code.erp', 'conf_code_rel_erp', 'conf_id', 'code_id', string="Codes Somme")
    code_min_ids = fields.Many2many('liasse.code.erp', 'conf_code_min_rel_erp', 'conf_id', 'code_id',
                                    string="Codes Minus")
    compte = fields.One2many('liasse.compte.erp', 'conf_id', 'Compte', required=True)
    comptem = fields.One2many('liasse.compte.erp', 'conf_idm', 'Compte negatif')

    _rec_name = 'code'

    _sql_constraints = [('code_uniq', 'unique(code)', 'Ce compte est déjà attribué avec ce code!')
                        ]


class liasse_compte(models.Model):
    _name = "liasse.compte.erp"
    _description = "liasse.compte.erp"

    compte = fields.Char('Compte', required=True)
    conf_id = fields.Many2one('liasse.configuration.erp', 'Code EDI', ondelete='cascade', index=True)
    conf_idm = fields.Many2one('liasse.configuration.erp', 'Code EDI Exclus', ondelete='cascade', index=True)


"""    
class liasse_plan_comptable(models.Model):
    _name="liasse.plan.comptable"
    
        'compte = fields.Char('Compte',required=True)
              }  
"""


class liasse_code(models.Model):
    _name = "liasse.code.erp"
    _description = "liasse.code.erp"

    code = fields.Char('Code EDI', required=True)
    valeur = fields.Char('Valeur')
    conf_ids = fields.Many2many('liasse.configuration.erp', 'conf_code_rel_erp', 'code_id', 'conf_id', string="Conf")
    conf_min_ids = fields.Many2many('liasse.configuration.erp', 'conf_code_min_rel_erp', 'code_id', 'conf_id',
                                    string="Conf")
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Extra field'),
        ('2', u'Illimite'),
    ], 'Type', default='0', required=True)
    valeur_ids = fields.One2many('liasse.code.line.erp', 'code_id', 'Valeurs')

    _rec_name = 'code'

    _sql_constraints = [('code_liasse_uniq', 'unique(code)', 'Le code doit etre unique!')]

    def write(self, values):
        res = super(liasse_code, self).write(values)
        for r in self:
            if r.code == "499":
                print("UPDATE !!!!!!!!!!!!!!", r.valeur)
        return res


class liasse_code_line(models.Model):
    _name = "liasse.code.line.erp"
    _description = "liasse.code.line.erp"

    valeur = fields.Char('Valeur')
    ligne = fields.Integer('Ligne')
    code_id = fields.Many2one('liasse.code.erp', 'code_id', ondelete='cascade', index=True)


class liasse_actif(models.Model):
    _name = "liasse.bilan.actif.erp"
    _description = "liasse.bilan.actif.erp"

    def default_liasse_bilan_sequence(self):
        return self.env['ir.sequence'].next_by_code('liasse.bilan.actif.erp') or ''

    lib = fields.Char('Libelle', required=True)
    code1 = fields.Many2one('liasse.code.erp', 'Brut', required=True)
    code2 = fields.Many2one('liasse.code.erp', 'Amortissement et provisions', required=True)
    code3 = fields.Many2one('liasse.code.erp', 'Net', required=True)
    code4 = fields.Many2one('liasse.code.erp', 'Net Precedent', required=True)
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Entete'),
        ('2', u'Total'),
    ], 'Type', default='0', required=True)
    sequence = fields.Integer('Sequence', required=True, default=default_liasse_bilan_sequence)


class liasse_passif(models.Model):
    _name = "liasse.bilan.passif.erp"
    _description = "liasse.bilan.passif.erp"

    def default_liasse_bilan_sequence(self):
        return self.env['ir.sequence'].next_by_code('liasse.bilan.actif.erp') or ''

    lib = fields.Char('Libelle', required=True)
    code1 = fields.Many2one('liasse.code.erp', 'Exercice', required=True)
    code2 = fields.Many2one('liasse.code.erp', 'Exercice precedent', required=True)
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Entete'),
        ('2', 'Total'),
    ], 'Type', default='0', required=True)
    sequence = fields.Integer('Sequence', required=True, default=default_liasse_bilan_sequence)

    # _defaults = {
    #     'type': '0',
    #     'sequence': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'liasse.bilan.actif.erp'),
    # }


class liasse_cpc(models.Model):
    _name = "liasse.cpc.erp"
    _description = "liasse.cpc.erp"

    def default_liasse_bilan_sequence(self):
        return self.env['ir.sequence'].next_by_code('liasse.bilan.actif.erp') or ''

    lib = fields.Char('Nature', required=True)
    code1 = fields.Many2one('liasse.code.erp', 'Operations propres à l\'exercice ', required=True)
    code2 = fields.Many2one('liasse.code.erp', 'Operations concernant les exercices precedents', required=True)
    code3 = fields.Many2one('liasse.code.erp', 'TOTAUX DE L\'EXERCICE ', required=True)
    code4 = fields.Many2one('liasse.code.erp', 'TOTAUX DE L\'EXERCICE PRECEDENT', required=True)
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Entete'),
        ('2', 'Total'),
    ],
        'Type', default='0', required=True)
    sequence = fields.Integer('Sequence', required=True, default=default_liasse_bilan_sequence)

    # _defaults = {
    #     'type': '0',
    #     'sequence': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'liasse.bilan.actif.erp'),
    # }


class liasse_tfr(models.Model):
    _name = "liasse.tfr.erp"
    _description = "liasse.tfr.erp"

    def default_liasse_bilan_sequence(self):
        return self.env['ir.sequence'].next_by_code('liasse.bilan.actif.erp') or ''

    lettre = fields.Char('Lettre')
    num = fields.Char('Num')
    op = fields.Char('Operateur')
    lib = fields.Char('Libelle', required=True)
    code1 = fields.Many2one('liasse.code.erp', 'Exercice', required=True)
    code2 = fields.Many2one('liasse.code.erp', 'Exercice precedent', required=True)
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Entete'),
        ('2', 'Total'),
    ], 'Type', default='0', required=True)
    sequence = fields.Integer('Sequence', required=True, default=default_liasse_bilan_sequence)

    # _defaults = {
    #     'type': '0',
    #     'sequence': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'liasse.bilan.actif.erp'),
    # }


class liasse_caf(models.Model):
    _name = "liasse.caf.erp"
    _description = "liasse.caf.erp"

    def default_liasse_bilan_sequence(self):
        return self.env['ir.sequence'].next_by_code('liasse.bilan.actif.erp') or ''

    lettre = fields.Char('Lettre')
    num = fields.Char('Num')
    op = fields.Char('Operateur')
    lib = fields.Char('Libelle', required=True)
    code1 = fields.Many2one('liasse.code.erp', 'Exercice', required=True)
    code2 = fields.Many2one('liasse.code.erp', 'Exercice precedent', required=True)
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Entete'),
        ('2', 'Total'),
    ], 'Type', default='0', required=True)
    sequence = fields.Integer('Sequence', required=True, default=default_liasse_bilan_sequence)

    # _defaults = {
    #     'type': '0',
    #     'sequence': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'liasse.bilan.actif.erp'),
    # }


class liasse_det_cpc(models.Model):
    _name = "liasse.det.cpc.erp"
    _description = "liasse.det.cpc.erp"

    def default_liasse_bilan_sequence(self):
        return self.env['ir.sequence'].next_by_code('liasse.bilan.actif.erp') or ''

    poste = fields.Char('Poste')
    lib = fields.Char('Libelle', required=True)
    code1 = fields.Many2one('liasse.code.erp', 'Exercice', required=True)
    code2 = fields.Many2one('liasse.code.erp', 'Exercice precedent', required=True)
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Entete'),
        ('2', 'Total'),
    ],
        'Type', default='0', required=True)
    sequence = fields.Integer('Sequence', required=True, default=default_liasse_bilan_sequence)

    # _defaults = {
    #     'type': '0',
    #     'sequence': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'liasse.bilan.actif.erp'),
    # }


class liasse_amort(models.Model):
    _name = "liasse.amort.erp"
    _description = "liasse.amort.erp"

    def default_liasse_bilan_sequence(self):
        return self.env['ir.sequence'].next_by_code('liasse.bilan.actif.erp') or ''

    lib = fields.Char('Nature', required=True)
    code1 = fields.Many2one('liasse.code.erp', 'Cumul debut', required=True)
    code2 = fields.Many2one('liasse.code.erp', 'Dotation', required=True)
    code3 = fields.Many2one('liasse.code.erp', 'Amortissement', required=True)
    code4 = fields.Many2one('liasse.code.erp', 'Cumul d amortissement', required=True)
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Entete'),
        ('2', 'Total'),
    ],
        'Type', default='0', required=True)
    sequence = fields.Integer('Sequence', required=True, default=default_liasse_bilan_sequence)

    # _defaults = {
    #     'type': '0',
    #     'sequence': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'liasse.bilan.actif.erp'),
    # }


class liasse_provision(models.Model):
    _name = "liasse.provision.erp"
    _description = "liasse.provision.erp"

    def default_liasse_bilan_sequence(self):
        return self.env['ir.sequence'].next_by_code('liasse.bilan.actif.erp') or ''

    lib = fields.Char('Nature', required=True)
    code1 = fields.Many2one('liasse.code.erp', 'Montant debut', required=True)
    code2 = fields.Many2one('liasse.code.erp', 'Dot exp', required=True)
    code3 = fields.Many2one('liasse.code.erp', 'Dot fin', required=True)
    code4 = fields.Many2one('liasse.code.erp', 'Dot nc', required=True)
    code5 = fields.Many2one('liasse.code.erp', 'Rep exp', required=True)
    code6 = fields.Many2one('liasse.code.erp', 'Rep fin', required=True)
    code7 = fields.Many2one('liasse.code.erp', 'Rep nc', required=True)
    code8 = fields.Many2one('liasse.code.erp', 'Montant fin', required=True)
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Entete'),
        ('2', 'Total'),
    ],
        'Type', default='0', required=True)
    sequence = fields.Integer('Sequence', required=True, default=default_liasse_bilan_sequence)

    # _defaults = {
    #     'type': '0',
    #     'sequence': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'liasse.bilan.actif.erp'),
    # }


class liasse_stock(models.Model):
    _name = "liasse.stock.erp"
    _description = "liasse.stock.erp"

    def default_liasse_bilan_sequence(self):
        return self.env['ir.sequence'].next_by_code('liasse.bilan.actif.erp') or ''

    lib = fields.Char('STOCKS', required=True)
    code1 = fields.Many2one('liasse.code.erp', 'S.F. Montant Brut', required=True)
    code2 = fields.Many2one('liasse.code.erp', u'S.F. Provision pour depreciation', required=True)
    code3 = fields.Many2one('liasse.code.erp', 'S.F. Montant net', required=True)
    code4 = fields.Many2one('liasse.code.erp', ' S.I. Montant brut', required=True)
    code5 = fields.Many2one('liasse.code.erp', 'S.I.Provision pour depreciation', required=True)
    code6 = fields.Many2one('liasse.code.erp', 'S.I.Montant net', required=True)
    code7 = fields.Many2one('liasse.code.erp', 'Variation de stock en valeur', required=True)
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Entete'),
        ('2', 'Total'),
    ],
        'Type', default='0', required=True)
    sequence = fields.Integer('Sequence', required=True, default=default_liasse_bilan_sequence)

    # _defaults = {
    #     'type': '0',
    #     'sequence': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'liasse.bilan.actif.erp'),
    # }


class credit_bail(models.Model):
    _name = "liasse.credit.bail.erp"
    _description = "liasse.credit.bail.erp"

    extra_field_clos = fields.Many2one('liasse.code.erp', 'Exercice clos le', required=True)
    credit_bail_ids = fields.One2many('liasse.credit.bail.line.erp', 'credit_bail_id', 'Credit bail', required=True)

    _rec_name = 'extra_field_clos'


class credit_bail_line(models.Model):
    _name = "liasse.credit.bail.line.erp"
    _description = "liasse.credit.bail.line.erp"

    code0 = fields.Many2one('liasse.code.erp', 'Rubriques', required=True)
    code1 = fields.Many2one('liasse.code.erp', 'Date de la 1ère échéance', required=True)
    code2 = fields.Many2one('liasse.code.erp', 'Durée du contrat en mois', required=True)
    code3 = fields.Many2one('liasse.code.erp', 'Valeur estimée du bien à la date du contrat', required=True)
    code4 = fields.Many2one('liasse.code.erp', 'Durée théorique d\'amortissement du bien ', required=True)
    code5 = fields.Many2one('liasse.code.erp', 'Cumul des exercices précédents des redevances', required=True)
    code6 = fields.Many2one('liasse.code.erp', 'Montant de l\'exercice des redevances', required=True)
    code7 = fields.Many2one('liasse.code.erp', 'redevances restant à payer (A moins d\'un an)', required=True)
    code8 = fields.Many2one('liasse.code.erp', 'redevances restant à payer (A plus d\'un an)', required=True)
    code9 = fields.Many2one('liasse.code.erp', 'Prix d\'achat résiduel en fin de contrat', required=True)
    code10 = fields.Many2one('liasse.code.erp', 'Observations', required=True)
    credit_bail_id = fields.Many2one('liasse.credit.bail.erp', 'credit_bail_id', ondelete='cascade', index=True)
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Entete'),
        ('2', 'Total'),
    ],
        'Type', default='0', required=True)
    # sequence = fields.Integer('Sequence',required=True)


class pm_value(models.Model):
    _name = "liasse.pm.value.erp"
    _description = "liasse.pm.value.erp"

    extra_field_clos = fields.Many2one('liasse.code.erp', 'Exercice clos le', required=True)
    compte_princ = fields.Many2one('liasse.code.erp', 'Compte principal', required=True)
    montant_brut = fields.Many2one('liasse.code.erp', 'Montant brut', required=True)
    amort_cumul = fields.Many2one('liasse.code.erp', 'Amortissements cumulés', required=True)
    val_net_amort = fields.Many2one('liasse.code.erp', 'Valeur nette d\'amortissements', required=True)
    prod_cess = fields.Many2one('liasse.code.erp', 'Produit de cession', required=True)
    plus_value = fields.Many2one('liasse.code.erp', 'Plus values', required=True)
    moins_value = fields.Many2one('liasse.code.erp', 'Moins values', required=True)
    pm_val_ids = fields.One2many('liasse.pm.value.line.erp', 'pm_val_id', 'Section illimitee', required=True)


class pm_value_line(models.Model):
    _name = "liasse.pm.value.line.erp"
    _description = "liasse.pm.value.erp"

    code0 = fields.Many2one('liasse.code.erp', 'Date de cession ou de retrait', required=True)
    code1 = fields.Many2one('liasse.code.erp', 'Compte principal', required=True)
    code2 = fields.Many2one('liasse.code.erp', 'Montant brut', required=True)
    code3 = fields.Many2one('liasse.code.erp', u'Amortissements cumulés', required=True)
    code4 = fields.Many2one('liasse.code.erp', 'Valeur nette d\'amortissements', required=True)
    code5 = fields.Many2one('liasse.code.erp', 'Produit de cession', required=True)
    code6 = fields.Many2one('liasse.code.erp', 'Plus values', required=True)
    code7 = fields.Many2one('liasse.code.erp', 'Moins values', required=True)
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Entete'),
        ('2', 'Total'),
    ],
        'Type', default='0', required=True)
    # sequence = fields.Integer('Sequence',required=True)
    pm_val_id = fields.Many2one('liasse.pm.value.erp', 'pm_val_id', ondelete='cascade', index=True)


class titre_particip(models.Model):
    _name = "liasse.titre.particip.erp"
    _description = "liasse.titre.particip.erp"

    # code1 = fields.Many2one('liasse.code.erp',u'Secteur d\'activité',required=True)
    code2 = fields.Many2one('liasse.code.erp', u'Capital social', required=True)
    code3 = fields.Many2one('liasse.code.erp', u'Participation au capital %', required=True)
    code4 = fields.Many2one('liasse.code.erp', u'Prix d\'acquisition global', required=True)
    code5 = fields.Many2one('liasse.code.erp', u'Valeur comptable nette', required=True)
    code6 = fields.Many2one('liasse.code.erp', u'Extrait (Date de clôture)', required=True)
    code7 = fields.Many2one('liasse.code.erp', u'Extrait (Situation nette)', required=True)
    code8 = fields.Many2one('liasse.code.erp', u'Extrait (résultat net)', required=True)
    code9 = fields.Many2one('liasse.code.erp', u'Produits inscrits au C.P.C de l\'exercice', required=True)
    titre_particip_ids = fields.One2many('liasse.titre.particip.line.erp', 'titre_partic_id', 'Section illimitee',
                                         required=True)


class titre_particip_line(models.Model):
    _name = "liasse.titre.particip.line.erp"
    _description = "liasse.titre.particip.line.erp"

    code0 = fields.Many2one('liasse.code.erp', u'Raison sociale de la société émettrice', required=True)
    code1 = fields.Many2one('liasse.code.erp', u'Secteur d\'activité', required=True)
    code2 = fields.Many2one('liasse.code.erp', u'Capital social', required=True)
    code3 = fields.Many2one('liasse.code.erp', u'Participation au capital %', required=True)
    code4 = fields.Many2one('liasse.code.erp', u'Prix d\'acquisition global', required=True)
    code5 = fields.Many2one('liasse.code.erp', u'Valeur comptable nette', required=True)
    code6 = fields.Many2one('liasse.code.erp',
                            u'Extrait des derniers états de synthèse de la société émettrice(Date de clôture)',
                            required=True)
    code7 = fields.Many2one('liasse.code.erp',
                            u'Extrait des derniers états de synthèse de la société émettrice(Situation nette)',
                            required=True)
    code8 = fields.Many2one('liasse.code.erp',
                            u'Extrait des derniers états de synthèse de la société émettrice(résultat net)',
                            required=True)
    code9 = fields.Many2one('liasse.code.erp', u'Produits inscrits au C.P.C de l\'exercice', required=True)
    titre_partic_id = fields.Many2one('liasse.titre.particip.erp', 'titre_partic_id', ondelete='cascade', index=True)
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Entete'),
        ('2', 'Total'),
    ],
        'Type', default='0', required=True)
    # sequence = fields.Integer('Sequence',required=True)


class repart_cs(models.Model):
    _name = "liasse.repart.cs.erp"
    _description = "liasse.repart.cs.erp"

    montant_capital = fields.Many2one('liasse.code.erp', 'Montant du capital', required=True)
    repart_cs_ids = fields.One2many('liasse.repart.cs.line.erp', 'repart_cs_id', 'Section illimitee', required=True)


class repart_cs_line(models.Model):
    _name = "liasse.repart.cs.line.erp"
    _description = "liasse.repart.cs.line.erp"

    code0 = fields.Many2one('liasse.code.erp', u'Nom, prénom ou raison sociale des principaux associés', required=True)
    code1 = fields.Many2one('liasse.code.erp', u'IF', required=True)
    code2 = fields.Many2one('liasse.code.erp', u'CIN', required=True)
    code3 = fields.Many2one('liasse.code.erp', u'Adresse', required=True)
    code4 = fields.Many2one('liasse.code.erp', u'NOMBRE DE TITRES (Exercice précédent)', required=True)
    code5 = fields.Many2one('liasse.code.erp', u'NOMBRE DE TITRES (Exercice actual)', required=True)
    code6 = fields.Many2one('liasse.code.erp', u'Valeur nominale de chaque action ou part sociale', required=True)
    code7 = fields.Many2one('liasse.code.erp', u'MONTANT DU CAPITAL(Souscrit)', required=True)
    code8 = fields.Many2one('liasse.code.erp', u'MONTANT DU CAPITAL(Appelé)', required=True)
    code9 = fields.Many2one('liasse.code.erp', u'MONTANT DU CAPITAL(libéré)', required=True)
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Entete'),
        ('2', 'Total'),
    ],
        'Type', default='0', required=True)
    # sequence = fields.Integer('Sequence',required=True)
    repart_cs_id = fields.Many2one('liasse.repart.cs.line.erp', 'repart_cs_id', ondelete='cascade', index=True)


class interets(models.Model):
    _name = "liasse.interets.erp"
    _description = "liasse.interets.erp"

    code0 = fields.Many2one('liasse.code.erp', u'Exercice clos le', required=True)
    code1 = fields.Many2one('liasse.code.erp', u'Montant du prêt', required=True)
    code2 = fields.Many2one('liasse.code.erp', u'Charge financière globale', required=True)
    code3 = fields.Many2one('liasse.code.erp', u'Remboursement exercices antérieurs(Principal)', required=True)
    code4 = fields.Many2one('liasse.code.erp', u'Remboursement exercices antérieurs(Intérêt)', required=True)
    code5 = fields.Many2one('liasse.code.erp', u'Remboursement exercice actuel(Principal)', required=True)
    code6 = fields.Many2one('liasse.code.erp', u'Remboursement exercice actuel(Intérêt)', required=True)
    interets_associe = fields.One2many('liasse.interets.line.erp', 'interet_id', string='Interets Associe',
                                       domain=[('type_in', '=', '0')], context={'default_type_in': '0'})
    interets_tier = fields.One2many('liasse.interets.line.erp', 'interet_id', 'Interets Associe ',
                                    domain=[('type_in', '=', '1')], context={'default_type_in': '1'})


class interets_line(models.Model):
    _name = "liasse.interets.line.erp"
    _description = "liasse.interets.line.erp"

    code0 = fields.Many2one('liasse.code.erp', u'Nom, prénom ou raison sociale des principaux associés', required=True)
    code1 = fields.Many2one('liasse.code.erp', u'Adresse', required=True)
    code2 = fields.Many2one('liasse.code.erp', u'N° C.I.N. ou Article I.S.', required=True)
    code3 = fields.Many2one('liasse.code.erp', u'Montant du prêt', required=True)
    code4 = fields.Many2one('liasse.code.erp', u'Date du  prêt', required=True)
    code5 = fields.Many2one('liasse.code.erp', u'Durée du prêt (en mois)', required=True)
    code6 = fields.Many2one('liasse.code.erp', u'Taux d\'intérêt', required=True)
    code7 = fields.Many2one('liasse.code.erp', u'Charge financière globale', required=True)
    code8 = fields.Many2one('liasse.code.erp', u'Remboursement exercices antérieurs(Principal)', required=True)
    code9 = fields.Many2one('liasse.code.erp', u'Remboursement exercices antérieurs(Intérêt)', required=True)
    code10 = fields.Many2one('liasse.code.erp', u'Remboursement exercice actuel(Principal)', required=True)
    code11 = fields.Many2one('liasse.code.erp', 'Remboursement exercice actuel(Intérêt)', required=True)
    code12 = fields.Many2one('liasse.code.erp', 'Observations', required=True)
    type_in = fields.Selection([
        ('0', 'Associe'),
        ('1', 'Tier'),
    ], 'A/T')
    interet_id = fields.Many2one('liasse.interets.erp', 'Interet_id', ondelete='cascade', index=True)
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Entete'),
        ('2', 'Total'),
    ],
        'Type', default='0', required=True)
    # sequence = fields.Integer('Sequence',required=True)


class beaux(models.Model):
    _name = "liasse.beaux.erp"
    _description = "liasse.beaux.erp"

    code0 = fields.Many2one('liasse.code.erp', 'Montant annuel de location', required=True)
    code1 = fields.Many2one('liasse.code.erp', 'Montant du loyer compris dans les Charges de l\'exercice',
                            required=True)
    beaux_ids = fields.One2many('liasse.beaux.line.erp', 'beaux_id', 'Section illimitee', required=True)


class beaux_line(models.Model):
    _name = "liasse.beaux.line.erp"
    _description = "liasse.beaux.line.erp"

    code0 = fields.Many2one('liasse.code.erp', 'Nature du bien loué', required=True)
    code1 = fields.Many2one('liasse.code.erp', 'Lieu de situation', required=True)
    code2 = fields.Many2one('liasse.code.erp', 'Nom et prénoms ou Raison sociale et adresse du propriétaire',
                            required=True)
    code3 = fields.Many2one('liasse.code.erp', u'Date de conclusion de l\'acte de location', required=True)
    code4 = fields.Many2one('liasse.code.erp', 'Montant annuel de location', required=True)
    code5 = fields.Many2one('liasse.code.erp', 'Montant du loyer compris dans les Charges de l\'exercice',
                            required=True)
    code6 = fields.Many2one('liasse.code.erp', 'Nature du contrat Bail-ordinaire', required=True)
    code7 = fields.Many2one('liasse.code.erp', 'Nature du contrat(Nème période)', required=True)
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Entete'),
        ('2', 'Total'),
    ],
        'Type', rdefault='0', equired=True)
    # sequence = fields.Integer('Sequence',required=True)
    beaux_id = fields.Many2one('liasse.beaux.erp', 'beaux_id', ondelete='cascade', index=True)


class passage(models.Model):
    _name = "liasse.passage.erp"
    _description = "liasse.passage.erp"

    code0 = fields.Many2one('liasse.code.erp', u'Bénéfice net (+)', required=True)
    code1 = fields.Many2one('liasse.code.erp', u'Bénéfice net (-)', required=True)
    code2 = fields.Many2one('liasse.code.erp', u'Perte nette (+)', required=True)
    code3 = fields.Many2one('liasse.code.erp', u'Perte nette (-)', required=True)
    passages_rfc = fields.One2many('liasse.passage.line.erp', 'passage_id', 'Reintegrations fiscales courantes',
                                   domain=[('type_in', '=', '0')], context={'default_type_in': '0'})
    passages_rfnc = fields.One2many('liasse.passage.line.erp', 'passage_id', 'Reintegrations fiscales non courantes',
                                    domain=[('type_in', '=', '1')], context={'default_type_in': '1'})
    passages_dfc = fields.One2many('liasse.passage.line.erp', 'passage_id', 'Déductions fiscales courantes',
                                   domain=[('type_in', '=', '2')], context={'default_type_in': '2'})
    passages_dfnc = fields.One2many('liasse.passage.line.erp', 'passage_id', 'Déductions fiscales non courantes',
                                    domain=[('type_in', '=', '3')], context={'default_type_in': '3'})
    code4 = fields.Many2one('liasse.code.erp', u'Total mantant(+)', required=True)
    code5 = fields.Many2one('liasse.code.erp', u'Total mantant(-)', required=True)
    code6 = fields.Many2one('liasse.code.erp', u'Bénéfice brut si T1> T2 (+)', required=True)
    code7 = fields.Many2one('liasse.code.erp', u'Bénéfice brut si T1> T2 (-)', required=True)
    code8 = fields.Many2one('liasse.code.erp', u'Déficit brut fiscal si T2> T1 (+)', required=True)
    code9 = fields.Many2one('liasse.code.erp', u'Déficit brut fiscal si T2> T1 (-)', required=True)
    code10 = fields.Many2one('liasse.code.erp', u'Exercice n-4 (+)', required=True)
    # 'code11 = fields.Many2one('liasse.code.erp',u'Exercice n-4 (-)',required=True)
    code12 = fields.Many2one('liasse.code.erp', u'Exercice n-3 (+)', required=True)
    # 'code13 = fields.Many2one('liasse.code.erp',u'Exercice n-3 (-)',required=True)
    code14 = fields.Many2one('liasse.code.erp', u'Exercice n-2 (+)', required=True)
    # code15 = fields.Many2one('liasse.code.erp',u'Exercice n-2 (-)',required=True)
    code16 = fields.Many2one('liasse.code.erp', u'Exercice n-1 (+)', required=True)
    # code17 = fields.Many2one('liasse.code.erp',u'Exercice n-1 (-)',required=True)
    code18 = fields.Many2one('liasse.code.erp', u'Bénéfice net fiscal(+)')
    code19 = fields.Many2one('liasse.code.erp', u'Bénéfice net fiscal(-)')
    code20 = fields.Many2one('liasse.code.erp', u'déficit net fiscal(+)')
    code21 = fields.Many2one('liasse.code.erp', u'déficit net fiscal(-)')
    code22 = fields.Many2one('liasse.code.erp', u'CUMUL DES AMORTISSEMENTS FISCALEMENT DIFFERES(-)')
    code23 = fields.Many2one('liasse.code.erp', 'Exercice n-4 (+)')
    code24 = fields.Many2one('liasse.code.erp', 'Exercice n-3 (+)')
    code25 = fields.Many2one('liasse.code.erp', 'Exercice n-2 (+)')
    code26 = fields.Many2one('liasse.code.erp', 'Exercice n-1 (+)')


class passage_line(models.Model):
    _name = "liasse.passage.line.erp"
    _description = "liasse.passage.line.erp"

    code0 = fields.Many2one('liasse.code.erp', u'Intitulé', required=True)
    code1 = fields.Many2one('liasse.code.erp', u'montant +')
    code2 = fields.Many2one('liasse.code.erp', u'montant -')
    type_in = fields.Selection([
        ('0', 'REINTEGRATIONS FISCALES COURANTES'),
        ('1', 'REINTEGRATIONS FISCALES NON COURANTES'),
        ('2', 'DEDUCTIONS FISCALES COURANTES'),
        ('3', 'DEDUCTIONS FISCALES NON COURANTES '),
    ], 'Type')
    passage_id = fields.Many2one('liasse.passage.erp', 'passage_id', ondelete='cascade', index=True)
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Entete'),
        ('2', 'Total'),
    ],
        'Type', default='0', required=True)


class liasse_affect(models.Model):
    _name = "liasse.affect.erp"
    _description = "liasse.affect.erp"

    code0 = fields.Many2one('liasse.code.erp', u'Report à nouveau', required=True)
    code1 = fields.Many2one('liasse.code.erp', u'Résultats nets en instance d\'affectation', required=True)
    code2 = fields.Many2one('liasse.code.erp', u'Résultat net de l\'exercice', required=True)
    code3 = fields.Many2one('liasse.code.erp', u'Prélèvements sur les réserves', required=True)
    code4 = fields.Many2one('liasse.code.erp', u'Autres prélèvements', required=True)
    code5 = fields.Many2one('liasse.code.erp', u'Total A', required=True)

    code6 = fields.Many2one('liasse.code.erp', u'Réserve légale', required=True)
    code7 = fields.Many2one('liasse.code.erp', u'Autres réserves', required=True)
    code8 = fields.Many2one('liasse.code.erp', u'Tantièmes', required=True)
    code9 = fields.Many2one('liasse.code.erp', u'Dividendes', required=True)
    code10 = fields.Many2one('liasse.code.erp', u'Autres affectations', required=True)
    code11 = fields.Many2one('liasse.code.erp', u'Report à nouveau', required=True)
    code12 = fields.Many2one('liasse.code.erp', u'Total B', required=True)


class liasse_encour(models.Model):
    _name = "liasse.encour.erp"
    _description = "liasse.encour.erp"

    code0 = fields.Many2one('liasse.code.erp', 'Vente imposable', help="Ensemble des produits", required=True)
    code1 = fields.Many2one('liasse.code.erp', 'Vente imposable',
                            help="Ensemble des produits correspondant à la base imposable", required=True)
    code2 = fields.Many2one('liasse.code.erp', 'Vente imposable',
                            help="Ensemble des produits correspondant au numérateur taxable", required=True)
    code3 = fields.Many2one('liasse.code.erp', 'Ventes exonérées à 100% ', help="Ensemble des produits", required=True)
    code4 = fields.Many2one('liasse.code.erp', 'Ventes exonérées à 100% ',
                            help="Ensemble des produits correspondant à la base imposable", required=True)
    code5 = fields.Many2one('liasse.code.erp', 'Ventes exonérées à 100% ',
                            help="Ensemble des produits correspondant au numérateur taxable", required=True)
    code6 = fields.Many2one('liasse.code.erp', 'Ventes exonérées à 50% ', help="Ensemble des produits", required=True)
    code7 = fields.Many2one('liasse.code.erp', 'Ventes exonérées à 50% ',
                            help="Ensemble des produits correspondant à la base imposable", required=True)
    code8 = fields.Many2one('liasse.code.erp', 'Ventes exonérées à 50% ',
                            help="Ensemble des produits correspondant au numérateur taxable", required=True)

    code9 = fields.Many2one('liasse.code.erp', 'Ventes et locations imposables', help="Ensemble des produits",
                            required=True)
    code10 = fields.Many2one('liasse.code.erp', 'Ventes et locations imposables',
                             help="Ensemble des produits correspondant à la base imposable", required=True)
    code11 = fields.Many2one('liasse.code.erp', 'Ventes et locations imposables',
                             help="Ensemble des produits correspondant au numérateur taxable", required=True)
    code12 = fields.Many2one('liasse.code.erp', 'Ventes et locations exclues à 100% ', help="Ensemble des produits",
                             required=True)
    code13 = fields.Many2one('liasse.code.erp', 'Ventes et locations exclues à 100%  ',
                             help="Ensemble des produits correspondant à la base imposable", required=True)
    code14 = fields.Many2one('liasse.code.erp', 'Ventes et locations exclues à 100%  ',
                             help="Ensemble des produits correspondant au numérateur taxable", required=True)
    code15 = fields.Many2one('liasse.code.erp', 'Ventes et locations exclues à 50%  ', help="Ensemble des produits",
                             required=True)
    code16 = fields.Many2one('liasse.code.erp', 'Ventes et locations exclues à 50%  ',
                             help="Ensemble des produits correspondant à la base imposable", required=True)
    code17 = fields.Many2one('liasse.code.erp', 'Ventes et locations exclues à 50% ',
                             help="Ensemble des produits correspondant au numérateur taxable", required=True)

    code18 = fields.Many2one('liasse.code.erp', 'Imposables', help="Ensemble des produits", required=True)
    code19 = fields.Many2one('liasse.code.erp', 'Imposables',
                             help="Ensemble des produits correspondant à la base imposable", required=True)
    code20 = fields.Many2one('liasse.code.erp', 'Imposables',
                             help="Ensemble des produits correspondant au numérateur taxable", required=True)
    code21 = fields.Many2one('liasse.code.erp', 'Exonérées à 100% ', help="Ensemble des produits", required=True)
    code22 = fields.Many2one('liasse.code.erp', 'Exonérées à 100% ',
                             help="Ensemble des produits correspondant à la base imposable", required=True)
    code23 = fields.Many2one('liasse.code.erp', 'Exonérées à 100% ',
                             help="Ensemble des produits correspondant au numérateur taxable", required=True)
    code24 = fields.Many2one('liasse.code.erp', 'Exonérées à 50% ', help="Ensemble des produits", required=True)
    code25 = fields.Many2one('liasse.code.erp', 'Exonérées à 50% ',
                             help="Ensemble des produits correspondant à la base imposable", required=True)
    code26 = fields.Many2one('liasse.code.erp', 'Exonérées à 50% ',
                             help="Ensemble des produits correspondant au numérateur taxable", required=True)

    code27 = fields.Many2one('liasse.code.erp', u'Produits accessoires. Produits financiers, dons et libéralités',
                             help="Ensemble des produits", required=True)
    code28 = fields.Many2one('liasse.code.erp', u'Produits accessoires. Produits financiers, dons et libéralités ',
                             help="Ensemble des produits correspondant à la base imposable", required=True)
    code29 = fields.Many2one('liasse.code.erp', u'Produits accessoires. Produits financiers, dons et libéralités ',
                             help="Ensemble des produits correspondant au numérateur taxable", required=True)
    code30 = fields.Many2one('liasse.code.erp', 'Subventions d\'équipement', help="Ensemble des produits",
                             required=True)
    code31 = fields.Many2one('liasse.code.erp', 'Subventions d\'équipement ',
                             help="Ensemble des produits correspondant à la base imposable", required=True)
    code32 = fields.Many2one('liasse.code.erp', 'Subventions d\'équipement ',
                             help="Ensemble des produits correspondant au numérateur taxable", required=True)

    code33 = fields.Many2one('liasse.code.erp', u'Subventions d\'équilibre', help="Ensemble des produits",
                             required=True)
    code34 = fields.Many2one('liasse.code.erp', u'Subventions d\'équilibre ',
                             help="Ensemble des produits correspondant à la base imposable", required=True)
    code35 = fields.Many2one('liasse.code.erp', u'Subventions d\'équilibre',
                             help="Ensemble des produits correspondant au numérateur taxable", required=True)
    code36 = fields.Many2one('liasse.code.erp', 'Imposables', help="Ensemble des produits", required=True)
    code37 = fields.Many2one('liasse.code.erp', 'Imposables',
                             help="Ensemble des produits correspondant à la base imposable", required=True)
    code38 = fields.Many2one('liasse.code.erp', 'Imposables',
                             help="Ensemble des produits correspondant au numérateur taxable", required=True)
    code39 = fields.Many2one('liasse.code.erp', u'Exonérées à 100%', help="Ensemble des produits", required=True)
    code40 = fields.Many2one('liasse.code.erp', u'Exonérées à 100%',
                             help="Ensemble des produits correspondant à la base imposable", required=True)
    code41 = fields.Many2one('liasse.code.erp', u'Exonérées à 100%',
                             help="Ensemble des produits correspondant au numérateur taxable", required=True)
    code42 = fields.Many2one('liasse.code.erp', u'Exonérées à 50%', help="Ensemble des produits", required=True)
    code43 = fields.Many2one('liasse.code.erp', u'Exonérées à 50%',
                             help="Ensemble des produits correspondant à la base imposable", required=True)
    code44 = fields.Many2one('liasse.code.erp', u'Exonérées à 50%',
                             help="Ensemble des produits correspondant au numérateur taxable", required=True)

    code45 = fields.Many2one('liasse.code.erp', 'Totaux partiels', help="Ensemble des produits", required=True)
    code46 = fields.Many2one('liasse.code.erp', 'Totaux partiels',
                             help="Ensemble des produits correspondant à la base imposable", required=True)
    code47 = fields.Many2one('liasse.code.erp', 'Totaux partiels',
                             help="Ensemble des produits correspondant au numérateur taxable", required=True)

    code48 = fields.Many2one('liasse.code.erp', u'Profit net global des cessions après abattement pondéré',
                             help="Ensemble des produits", required=True)
    code49 = fields.Many2one('liasse.code.erp', u'Profit net global des cessions après abattement pondéré',
                             help="Ensemble des produits correspondant à la base imposable", required=True)
    code50 = fields.Many2one('liasse.code.erp', u'Profit net global des cessions après abattement pondéré',
                             help="Ensemble des produits correspondant au numérateur taxable", required=True)
    code51 = fields.Many2one('liasse.code.erp', u'Autres profils exceptionnels', help="Ensemble des produits",
                             required=True)
    code52 = fields.Many2one('liasse.code.erp', u'Autres profils exceptionnels',
                             help="Ensemble des produits correspondant à la base imposable", required=True)
    code53 = fields.Many2one('liasse.code.erp', u'Autres profils exceptionnels',
                             help="Ensemble des produits correspondant au numérateur taxable", required=True)

    code54 = fields.Many2one('liasse.code.erp', 'Total général', help="Ensemble des produits", required=True)
    code55 = fields.Many2one('liasse.code.erp', 'Total général',
                             help="Ensemble des produits correspondant à la base imposable", required=True)
    code56 = fields.Many2one('liasse.code.erp', 'Total général',
                             help="Ensemble des produits correspondant au numérateur taxable", required=True)


class liasse_fusion(models.Model):
    _name = "liasse.fusion.erp"
    _description = "liasse.fusion.erp"

    def default_liasse_bilan_sequence(self):
        return self.env['ir.sequence'].next_by_code('liasse.bilan.actif.erp') or ''

    lib = fields.Char('Elements', required=True)
    code1 = fields.Many2one('liasse.code.erp', 'Valeur d aport', required=True)
    code2 = fields.Many2one('liasse.code.erp', 'Valeur nette comptable', required=True)
    code3 = fields.Many2one('liasse.code.erp', 'Plus-value constatee et differee', required=True)
    code4 = fields.Many2one('liasse.code.erp',
                            'Fraction de la plus-value rapportee aux l exercices anterieurs (cumul) en %',
                            required=True)
    code5 = fields.Many2one('liasse.code.erp', 'Fraction de la plus-value rapportee a l exercices actuel en %',
                            required=True)
    code6 = fields.Many2one('liasse.code.erp', 'Cumul des plus-values rapportees', required=True)
    code7 = fields.Many2one('liasse.code.erp', 'Solde des plus-values non imputees', required=True)
    code8 = fields.Many2one('liasse.code.erp', 'Observations', required=True)
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Entete'),
        ('2', u'Total'),
    ],
        'Type', default='0', required=True)
    sequence = fields.Integer('Sequence', required=True, default=default_liasse_bilan_sequence)

    # _defaults = {
    #     'type': '0',
    #     'sequence': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'liasse.bilan.actif.erp'),
    # }


class liasse_tva(models.Model):
    _name = "liasse.tva.erp"
    _description = "liasse.tva.erp"

    tva_facsd = fields.Many2one('liasse.code.erp', string='tva', help="solde au début de l\'exercice")
    tva_faco = fields.Many2one('liasse.code.erp', string='tva', help="Opérations comptables de l\'exercice")
    tva_facd = fields.Many2one('liasse.code.erp', string='tva', help="Déclarations T.V.A de l\'exercice")
    tva_facsf = fields.Many2one('liasse.code.erp', string='tva', help="Solde fin d\'exercice")

    tva_recsd = fields.Many2one('liasse.code.erp', string='tva', help="solde au début de l\'exercice")
    tva_reco = fields.Many2one('liasse.code.erp', string='tva', help="Opérations comptables de l\'exercice")
    tva_recd = fields.Many2one('liasse.code.erp', string='tva', help="Déclarations T.V.A de l\'exercice")
    tva_recsf = fields.Many2one('liasse.code.erp', string='tva', help="Solde fin d\'exercice")

    tva_charsd = fields.Many2one('liasse.code.erp', string='tva', help="solde au début de l\'exercice")
    tva_charo = fields.Many2one('liasse.code.erp', string='tva', help="Opérations comptables de l\'exercice")
    tva_chard = fields.Many2one('liasse.code.erp', string='tva', help="Déclarations T.V.A de l\'exercice")
    tva_charsf = fields.Many2one('liasse.code.erp', string='tva', help="Solde fin d\'exercice")

    tva_immosd = fields.Many2one('liasse.code.erp', string='tva', help="solde au début de l\'exercice")
    tva_immoo = fields.Many2one('liasse.code.erp', string='tva', help="Opérations comptables de l\'exercice")
    tva_immod = fields.Many2one('liasse.code.erp', string='tva', help="Déclarations T.V.A de l\'exercice")
    tva_immosf = fields.Many2one('liasse.code.erp', string='tva', help="Solde fin d\'exercice")

    tva_totalsd = fields.Many2one('liasse.code.erp', string='tva', help="solde au début de l\'exercice")
    tva_totalo = fields.Many2one('liasse.code.erp', string='tva', help="Opérations comptables de l\'exercice")
    tva_totald = fields.Many2one('liasse.code.erp', string='tva', help="Déclarations T.V.A de l\'exercice")
    tva_totalsf = fields.Many2one('liasse.code.erp', string='tva', help="Solde fin d\'exercice")


class liasse_immo(models.Model):
    _name = "liasse.immo.erp"
    _description = "liasse.immo.erp"

    code0 = fields.Many2one('liasse.code.erp', 'IMMOBILISATIONS CORPORELLES', required=True,
                            help="Montant brut debut exercice")
    code1 = fields.Many2one('liasse.code.erp', 'IMMOBILISATIONS CORPORELLES', required=True,
                            help="Augmentation: acquisition")
    code2 = fields.Many2one('liasse.code.erp', 'IMMOBILISATIONS CORPORELLES', required=True,
                            help="Augmentation: Production par l'entreprise pour elle-même")
    code3 = fields.Many2one('liasse.code.erp', 'IMMOBILISATIONS CORPORELLES', required=True,
                            help="Augmentation: Virement")
    code4 = fields.Many2one('liasse.code.erp', 'IMMOBILISATIONS CORPORELLES', required=True, help="Diminution: cession")
    code5 = fields.Many2one('liasse.code.erp', 'IMMOBILISATIONS CORPORELLES', required=True, help="Diminution: retrait")
    code6 = fields.Many2one('liasse.code.erp', 'IMMOBILISATIONS CORPORELLES', required=True,
                            help="Diminution: virement")
    code7 = fields.Many2one('liasse.code.erp', 'IMMOBILISATIONS CORPORELLES', required=True,
                            help="Montant brut fin exercice")

    fp_mb = fields.Many2one('liasse.code.erp', 'Frais preliminaires', required=True, help="Montant brut debut exercice")
    fp_aug_acq = fields.Many2one('liasse.code.erp', 'Frais preliminaires', required=True,
                                 help="Augmentation: acquisition")
    fp_aug_pd = fields.Many2one('liasse.code.erp', 'Frais preliminaires', required=True,
                                help="Augmentation: Production par l'entreprise pour elle-même")
    fp_aug_vir = fields.Many2one('liasse.code.erp', 'Frais preliminaires', required=True, help="Augmentation: Virement")
    fp_dim_cess = fields.Many2one('liasse.code.erp', 'Frais preliminaires', required=True, help="Diminution: cession")
    fp_dim_ret = fields.Many2one('liasse.code.erp', 'Frais preliminaires', required=True, help="Diminution: retrait")
    fp_dim_vir = fields.Many2one('liasse.code.erp', 'Frais preliminaires', required=True, help="Diminution: virement")
    fp_mbf = fields.Many2one('liasse.code.erp', 'Frais preliminaires', required=True, help="Montant brut fin exercice")

    charge_mb = fields.Many2one('liasse.code.erp', 'Charges a repartir sur plusieurs exercices', required=True,
                                help="Montant brut debut exercice")
    charge_aug_acq = fields.Many2one('liasse.code.erp', 'Charges a repartir sur plusieurs exercices', required=True,
                                     help="Augmentation: acquisition")
    charge_aug_pd = fields.Many2one('liasse.code.erp', 'Charges a repartir sur plusieurs exercices', required=True,
                                    help="Augmentation: Production par l'entreprise pour elle-même")
    charge_aug_vir = fields.Many2one('liasse.code.erp', 'Charges a repartir sur plusieurs exercices', required=True,
                                     help="Augmentation: Virement")
    charge_dim_cess = fields.Many2one('liasse.code.erp', 'Charges a repartir sur plusieurs exercices', required=True,
                                      help="Diminution: cession")
    charge_dim_ret = fields.Many2one('liasse.code.erp', 'Charges a repartir sur plusieurs exercices', required=True,
                                     help="Diminution: retrait")
    charge_dim_vir = fields.Many2one('liasse.code.erp', 'Charges a repartir sur plusieurs exercices', required=True,
                                     help="Diminution: virement")
    charge_mbf = fields.Many2one('liasse.code.erp', 'Charges a repartir sur plusieurs exercices', required=True,
                                 help="Montant brut fin exercice")
    # Charge_mbf = fields.Many2one('liasse.code.erp')

    prime_mb = fields.Many2one('liasse.code.erp', 'Primes de remboursement obligations', required=True,
                               help="Montant brut debut exercice")
    prime_aug_acq = fields.Many2one('liasse.code.erp', 'Primes de remboursement obligations', required=True,
                                    help="Augmentation: acquisition")
    prime_aug_pd = fields.Many2one('liasse.code.erp', 'Primes de remboursement obligations', required=True,
                                   help="Augmentation: Production par l'entreprise pour elle-même")
    prime_aug_vir = fields.Many2one('liasse.code.erp', 'Primes de remboursement obligations', required=True,
                                    help="Augmentation: Virement")
    prime_dim_cess = fields.Many2one('liasse.code.erp', 'Primes de remboursement obligations', required=True,
                                     help="Diminution: cession")
    prime_dim_ret = fields.Many2one('liasse.code.erp', 'Primes de remboursement obligations', required=True,
                                    help="Diminution: retrait")
    prime_dim_vir = fields.Many2one('liasse.code.erp', 'Primes de remboursement obligations', required=True,
                                    help="Diminution: virement")
    prime_mbf = fields.Many2one('liasse.code.erp', 'Primes de remboursement obligations', required=True,
                                help="Montant brut fin exercice")

    code8 = fields.Many2one('liasse.code.erp', 'IMMOBILISATIONS INCORPORELLES', required=True,
                            help="Montant brut debut exercice")
    code9 = fields.Many2one('liasse.code.erp', 'IMMOBILISATIONS INCORPORELLES', required=True,
                            help="Augmentation: acquisition")
    code10 = fields.Many2one('liasse.code.erp', 'IMMOBILISATIONS INCORPORELLES', required=True,
                             help="Augmentation: Production par l'entreprise pour elle-même")
    code11 = fields.Many2one('liasse.code.erp', 'IMMOBILISATIONS INCORPORELLES', required=True,
                             help="Augmentation: Virement")
    code12 = fields.Many2one('liasse.code.erp', 'IMMOBILISATIONS INCORPORELLES', required=True,
                             help="Diminution: cession")
    code13 = fields.Many2one('liasse.code.erp', 'IMMOBILISATIONS INCORPORELLES', required=True,
                             help="Diminution: retrait")
    code14 = fields.Many2one('liasse.code.erp', 'IMMOBILISATIONS INCORPORELLES', required=True,
                             help="Diminution: virement")
    code15 = fields.Many2one('liasse.code.erp', 'IMMOBILISATIONS INCORPORELLES', required=True,
                             help="Montant brut fin exercice")

    immord_mb = fields.Many2one('liasse.code.erp', 'Immobilisation en recherche et developpement', required=True,
                                help="Montant brut debut exercice")
    immord_aug_acq = fields.Many2one('liasse.code.erp', 'Immobilisation en recherche et developpement', required=True,
                                     help="Augmentation: acquisition")
    immord_aug_pd = fields.Many2one('liasse.code.erp', 'Immobilisation en recherche et developpement', required=True,
                                    help="Augmentation: Production par l'entreprise pour elle-même")
    immord_aug_vir = fields.Many2one('liasse.code.erp', 'Immobilisation en recherche et developpement', required=True,
                                     help="Augmentation: Virement")
    immord_dim_cess = fields.Many2one('liasse.code.erp', 'Immobilisation en recherche et developpement', required=True,
                                      help="Diminution: cession")
    immord_dim_ret = fields.Many2one('liasse.code.erp', 'Immobilisation en recherche et developpement', required=True,
                                     help="Diminution: retrait")
    immord_dim_vir = fields.Many2one('liasse.code.erp', 'Immobilisation en recherche et developpement', required=True,
                                     help="Diminution: virement")
    immord_mbf = fields.Many2one('liasse.code.erp', 'Immobilisation en recherche et developpement', required=True,
                                 help="Montant brut fin exercice")

    brevet_mb = fields.Many2one('liasse.code.erp', 'Brevets, marques, droits et valeurs similaires', required=True,
                                help="Montant brut debut exercice")
    brevet_aug_acq = fields.Many2one('liasse.code.erp', 'Brevets, marques, droits et valeurs similaires', required=True,
                                     help="Augmentation: acquisition")
    brevet_aug_pd = fields.Many2one('liasse.code.erp', 'Brevets, marques, droits et valeurs similaires', required=True,
                                    help="Augmentation: Production par l'entreprise pour elle-même")
    brevet_aug_vir = fields.Many2one('liasse.code.erp', 'Brevets, marques, droits et valeurs similaires', required=True,
                                     help="Augmentation: Virement")
    brevet_dim_cess = fields.Many2one('liasse.code.erp', 'Brevets, marques, droits et valeurs similaires',
                                      required=True, help="Diminution: cession")
    brevet_dim_ret = fields.Many2one('liasse.code.erp', 'Brevets, marques, droits et valeurs similaires', required=True,
                                     help="Diminution: retrait")
    brevet_dim_vir = fields.Many2one('liasse.code.erp', 'Brevets, marques, droits et valeurs similaires', required=True,
                                     help="Diminution: virement")
    brevet_mbf = fields.Many2one('liasse.code.erp', 'Brevets, marques, droits et valeurs similaires', required=True,
                                 help="Montant brut fin exercice")

    fond_mb = fields.Many2one('liasse.code.erp', 'Fonds commercial', required=True, help="Montant brut debut exercice")
    fond_aug_acq = fields.Many2one('liasse.code.erp', 'Fonds commercial', required=True,
                                   help="Augmentation: acquisition")
    fond_aug_pd = fields.Many2one('liasse.code.erp', 'Fonds commercial', required=True,
                                  help="Augmentation: Production par l'entreprise pour elle-même")
    fond_aug_vir = fields.Many2one('liasse.code.erp', 'Fonds commercial', required=True, help="Augmentation: Virement")
    fond_dim_cess = fields.Many2one('liasse.code.erp', 'Fonds commercial', required=True, help="Diminution: cession")
    fond_dim_ret = fields.Many2one('liasse.code.erp', 'Fonds commercial', required=True, help="Diminution: retrait")
    fond_dim_vir = fields.Many2one('liasse.code.erp', 'Fonds commercial', required=True, help="Diminution: virement")
    fond_mbf = fields.Many2one('liasse.code.erp', 'Fonds commercial', required=True, help="Montant brut fin exercice")

    autre_incorp_mb = fields.Many2one('liasse.code.erp', 'Autres immobilisations incorporelles', required=True,
                                      help="Montant brut debut exercice")
    autre_incorp_aug_acq = fields.Many2one('liasse.code.erp', 'Autres immobilisations incorporelles', required=True,
                                           help="Augmentation: acquisition")
    autre_incorp_aug_pd = fields.Many2one('liasse.code.erp', 'Autres immobilisations incorporelles', required=True,
                                          help="Augmentation: Production par l'entreprise pour elle-même")
    autre_incorp_aug_vir = fields.Many2one('liasse.code.erp', 'Autres immobilisations incorporelles', required=True,
                                           help="Augmentation: Virement")
    autre_incorp_dim_cess = fields.Many2one('liasse.code.erp', 'Autres immobilisations incorporelles', required=True,
                                            help="Diminution: cession")
    autre_incorp_dim_ret = fields.Many2one('liasse.code.erp', 'Autres immobilisations incorporelles', required=True,
                                           help="Diminution: retrait")
    autre_incorp_dim_vir = fields.Many2one('liasse.code.erp', 'Autres immobilisations incorporelles', required=True,
                                           help="Diminution: virement")
    autre_incorp_mbf = fields.Many2one('liasse.code.erp', 'Autres immobilisations incorporelles', required=True,
                                       help="Montant brut fin exercice")

    code16 = fields.Many2one('liasse.code.erp', 'IMMOBILISATIONS CORPORELLES', required=True,
                             help="Montant brut debut exercice")
    code17 = fields.Many2one('liasse.code.erp', 'IMMOBILISATIONS CORPORELLES', required=True,
                             help="Augmentation: acquisition")
    code18 = fields.Many2one('liasse.code.erp', 'IMMOBILISATIONS CORPORELLES', required=True,
                             help="Augmentation: Production par l'entreprise pour elle-même")
    code19 = fields.Many2one('liasse.code.erp', 'IMMOBILISATIONS CORPORELLES', required=True,
                             help="Augmentation: Virement")
    code20 = fields.Many2one('liasse.code.erp', 'IMMOBILISATIONS CORPORELLES', required=True,
                             help="Diminution: cession")
    code21 = fields.Many2one('liasse.code.erp', 'IMMOBILISATIONS CORPORELLES', required=True,
                             help="Diminution: retrait")
    code22 = fields.Many2one('liasse.code.erp', 'IMMOBILISATIONS CORPORELLES', required=True,
                             help="Diminution: virement")
    code23 = fields.Many2one('liasse.code.erp', 'IMMOBILISATIONS CORPORELLES', required=True,
                             help="Montant brut fin exercice")

    terrain_mb = fields.Many2one('liasse.code.erp', 'Terrains', required=True, help="Montant brut debut exercice")
    terrain_aug_acq = fields.Many2one('liasse.code.erp', 'Terrains', required=True, help="Augmentation: acquisition")
    terrain_aug_pd = fields.Many2one('liasse.code.erp', 'Terrains', required=True,
                                     help="Augmentation: Production par l'entreprise pour elle-même")
    terrain_aug_vir = fields.Many2one('liasse.code.erp', 'Terrains', required=True, help="Augmentation: Virement")
    terrain_dim_cess = fields.Many2one('liasse.code.erp', 'Terrains', required=True, help="Diminution: cession")
    terrain_dim_ret = fields.Many2one('liasse.code.erp', 'Terrains', required=True, help="Diminution: retrait")
    terrain_dim_vir = fields.Many2one('liasse.code.erp', 'Terrains', required=True, help="Diminution: virement")
    terrain_mbf = fields.Many2one('liasse.code.erp', 'Terrains', required=True, help="Montant brut fin exercice")

    constructions_mb = fields.Many2one('liasse.code.erp', 'Constructions', required=True,
                                       help="Montant brut debut exercice")
    constructions_aug_acq = fields.Many2one('liasse.code.erp', 'Constructions', required=True,
                                            help="Augmentation: acquisition")
    constructions_aug_pd = fields.Many2one('liasse.code.erp', 'Constructions', required=True,
                                           help="Augmentation: Production par l'entreprise pour elle-même")
    constructions_aug_vir = fields.Many2one('liasse.code.erp', 'Constructions', required=True,
                                            help="Augmentation: Virement")
    constructions_dim_cess = fields.Many2one('liasse.code.erp', 'Constructions', required=True,
                                             help="Diminution: cession")
    constructions_dim_ret = fields.Many2one('liasse.code.erp', 'Constructions', required=True,
                                            help="Diminution: retrait")
    constructions_dim_vir = fields.Many2one('liasse.code.erp', 'Constructions', required=True,
                                            help="Diminution: virement")
    constructions_mbf = fields.Many2one('liasse.code.erp', 'Constructionsins', required=True,
                                        help="Montant brut fin exercice")

    inst_mb = fields.Many2one('liasse.code.erp', 'Installat. techniques,materiel et outillage', required=True,
                              help="Montant brut debut exercice")
    inst_aug_acq = fields.Many2one('liasse.code.erp', 'Installat. techniques,materiel et outillage', required=True,
                                   help="Augmentation: acquisition")
    inst_aug_pd = fields.Many2one('liasse.code.erp', 'Installat. techniques,materiel et outillage', required=True,
                                  help="Augmentation: Production par l'entreprise pour elle-même")
    inst_aug_vir = fields.Many2one('liasse.code.erp', 'Installat. techniques,materiel et outillage', required=True,
                                   help="Augmentation: Virement")
    inst_dim_cess = fields.Many2one('liasse.code.erp', 'Installat. techniques,materiel et outillage', required=True,
                                    help="Diminution: cession")
    inst_dim_ret = fields.Many2one('liasse.code.erp', 'Installat. techniques,materiel et outillage', required=True,
                                   help="Diminution: retrait")
    inst_dim_vir = fields.Many2one('liasse.code.erp', 'Installat. techniques,materiel et outillage', required=True,
                                   help="Diminution: virement")
    inst_mbf = fields.Many2one('liasse.code.erp', 'Installat. techniques,materiel et outillage', required=True,
                               help="Montant brut fin exercice")

    mat_mb = fields.Many2one('liasse.code.erp', 'Materiel de transport', required=True,
                             help="Montant brut debut exercice")
    mat_aug_acq = fields.Many2one('liasse.code.erp', 'Materiel de transport', required=True,
                                  help="Augmentation: acquisition")
    mat_aug_pd = fields.Many2one('liasse.code.erp', 'Materiel de transport', required=True,
                                 help="Augmentation: Production par l'entreprise pour elle-même")
    mat_aug_vir = fields.Many2one('liasse.code.erp', 'Materiel de transport', required=True,
                                  help="Augmentation: Virement")
    mat_dim_cess = fields.Many2one('liasse.code.erp', 'Materiel de transport', required=True,
                                   help="Diminution: cession")
    mat_dim_ret = fields.Many2one('liasse.code.erp', 'Materiel de transport', required=True, help="Diminution: retrait")
    mat_dim_vir = fields.Many2one('liasse.code.erp', 'Materiel de transport', required=True,
                                  help="Diminution: virement")
    mat_mbf = fields.Many2one('liasse.code.erp', 'Materiel de transport', required=True,
                              help="Montant brut fin exercice")

    mob_mb = fields.Many2one('liasse.code.erp', 'Mobilier, materiel bureau et amenagements', required=True,
                             help="Montant brut debut exercice")
    mob_aug_acq = fields.Many2one('liasse.code.erp', 'Mobilier, materiel bureau et amenagements', required=True,
                                  help="Augmentation: acquisition")
    mob_aug_pd = fields.Many2one('liasse.code.erp', 'Mobilier, materiel bureau et amenagements', required=True,
                                 help="Augmentation: Production par l'entreprise pour elle-même")
    mob_aug_vir = fields.Many2one('liasse.code.erp', 'Mobilier, materiel bureau et amenagements', required=True,
                                  help="Augmentation: Virement")
    mob_dim_cess = fields.Many2one('liasse.code.erp', 'Mobilier, materiel bureau et amenagements', required=True,
                                   help="Diminution: cession")
    mob_dim_ret = fields.Many2one('liasse.code.erp', 'Mobilier, materiel bureau et amenagements', required=True,
                                  help="Diminution: retrait")
    mob_dim_vir = fields.Many2one('liasse.code.erp', 'Mobilier, materiel bureau et amenagements', required=True,
                                  help="Diminution: virement")
    mob_mbf = fields.Many2one('liasse.code.erp', 'Mobilier, materiel bureau et amenagements', required=True,
                              help="Montant brut fin exercice")

    autre_corp_mb = fields.Many2one('liasse.code.erp', 'Immobilisations corporelles diverses', required=True,
                                    help="Montant brut debut exercice")
    autre_corp_aug_acq = fields.Many2one('liasse.code.erp', 'Immobilisations corporelles diverses', required=True,
                                         help="Augmentation: acquisition")
    autre_corp_aug_pd = fields.Many2one('liasse.code.erp', 'Immobilisations corporelles diverses', required=True,
                                        help="Augmentation: Production par l'entreprise pour elle-même")
    autre_corp_aug_vir = fields.Many2one('liasse.code.erp', 'Immobilisations corporelles diverses', required=True,
                                         help="Augmentation: Virement")
    autre_corp_dim_cess = fields.Many2one('liasse.code.erp', 'Immobilisations corporelles diverses', required=True,
                                          help="Diminution: cession")
    autre_corp_dim_ret = fields.Many2one('liasse.code.erp', 'Immobilisations corporelles diverses', required=True,
                                         help="Diminution: retrait")
    autre_corp_dim_vir = fields.Many2one('liasse.code.erp', 'Immobilisations corporelles diverses', required=True,
                                         help="Diminution: virement")
    autre_corp_mbf = fields.Many2one('liasse.code.erp', 'Immobilisations corporelles diverses', required=True,
                                     help="Montant brut fin exercice")

    immocc_mb = fields.Many2one('liasse.code.erp', 'Immobilisations corporelles en cours', required=True,
                                help="Montant brut debut exercice")
    immocc_aug_acq = fields.Many2one('liasse.code.erp', 'Immobilisations corporelles en cours', required=True,
                                     help="Augmentation: acquisition")
    immocc_aug_pd = fields.Many2one('liasse.code.erp', 'Immobilisations corporelles en cours', required=True,
                                    help="Augmentation: Production par l'entreprise pour elle-même")
    immocc_aug_vir = fields.Many2one('liasse.code.erp', 'Immobilisations corporelles en cours', required=True,
                                     help="Augmentation: Virement")
    immocc_dim_cess = fields.Many2one('liasse.code.erp', 'Immobilisations corporelles en cours', required=True,
                                      help="Diminution: cession")
    immocc_dim_ret = fields.Many2one('liasse.code.erp', 'Immobilisations corporelles en cours', required=True,
                                     help="Diminution: retrait")
    immocc_dim_vir = fields.Many2one('liasse.code.erp', 'Immobilisations corporelles en cours', required=True,
                                     help="Diminution: virement")
    immocc_mbf = fields.Many2one('liasse.code.erp', 'Immobilisations corporelles en cours', required=True,
                                 help="Montant brut fin exercice")

    mati_mb = fields.Many2one('liasse.code.erp', 'Materiel informatique', required=True,
                              help="Montant brut debut exercice")
    mati_aug_acq = fields.Many2one('liasse.code.erp', 'Materiel informatique', required=True,
                                   help="Augmentation: acquisition")
    mati_aug_pd = fields.Many2one('liasse.code.erp', 'Materiel informatique', required=True,
                                  help="Augmentation: Production par l'entreprise pour elle-même")
    mati_aug_vir = fields.Many2one('liasse.code.erp', 'Materiel informatique', required=True,
                                   help="Augmentation: Virement")
    mati_dim_cess = fields.Many2one('liasse.code.erp', 'Materiel informatique', required=True,
                                    help="Diminution: cession")
    mati_dim_ret = fields.Many2one('liasse.code.erp', 'Materiel informatique', required=True,
                                   help="Diminution: retrait")
    mati_dim_vir = fields.Many2one('liasse.code.erp', 'Materiel informatique', required=True,
                                   help="Diminution: virement")
    mati_mbf = fields.Many2one('liasse.code.erp', 'Materiel informatique', required=True,
                               help="Montant brut fin exercice")


class liasse_check(models.Model):
    _name = "liasse.check.erp"
    _description = "liasse.check.erp"

    etat = fields.Char('Etat', required=True)
    code = fields.Char('Nome de la regle', required=True)
    coden_ids = fields.Many2many('liasse.code.erp', 'check_coden_rel_erp', 'check_id', 'code_id', string="Codes Somme")
    coden_min_ids = fields.Many2many('liasse.code.erp', 'check_coden_min_rel_erp', 'check_id', 'code_id',
                                     string="Codes Minus")
    codenp_ids = fields.Many2many('liasse.code.erp', 'check_codenp_rel_erp', 'check_id', 'code_id',
                                  string="Codes Somme")
    codenp_min_ids = fields.Many2many('liasse.code.erp', 'check_codenp_min_rel_erp', 'check_id', 'code_id',
                                      string="Codes Minus")

    _rec_name = 'code'


class dotation(models.Model):
    _name = "liasse.dotation.erp"
    _description = "liasse.dotation.erp"

    montant_global = fields.Many2one('liasse.code.erp', 'Montant global', required=True)
    clos = fields.Many2one('liasse.code.erp', 'Exercice clos le', required=True)
    date_from = fields.Many2one('liasse.code.erp', 'Amortissements de l exercice allant du', required=True)
    date_end = fields.Many2one('liasse.code.erp', 'Au', required=True)
    val_acq = fields.Many2one('liasse.code.erp', 'Valeur a amortir (Prix d acquisition)', required=True)
    val_compt = fields.Many2one('liasse.code.erp', 'Valeur a amortir - Valeur comptable apres reevaluation',
                                required=True)
    amort_ant = fields.Many2one('liasse.code.erp', 'Amortissements anterieurs', required=True)
    amort_ded_et = fields.Many2one('liasse.code.erp', 'Amortissements deduits du Benefice brut de l exercice (Taux)',
                                   required=True)
    amort_ded_e = fields.Many2one('liasse.code.erp',
                                  'Amortissements deduits du Benefice brut de l exercice Amortissements normaux ou acceleres de l exercice',
                                  required=True)
    amort_fe = fields.Many2one('liasse.code.erp', 'Total des amortissements a la fin de l exercice', required=True)
    dotation_line_ids = fields.One2many('liasse.dotation.line.erp', 'pm_val_id', 'Section illimitee', required=True)


class dotation_line(models.Model):
    _name = "liasse.dotation.line.erp"
    _description = "liasse.dotation.line.erp"

    code0 = fields.Many2one('liasse.code.erp', 'Immobilisations concernees', required=True)
    code1 = fields.Many2one('liasse.code.erp', 'Date entree', required=True)
    code2 = fields.Many2one('liasse.code.erp', 'Valeur a amortir (Prix dacquisition)', required=True)
    code3 = fields.Many2one('liasse.code.erp', u'Valeur a amortir - Valeur comptable apres reevaluation', required=True)
    code4 = fields.Many2one('liasse.code.erp', 'Amortissements anterieurs', required=True)
    code5 = fields.Many2one('liasse.code.erp', 'Amortissements deduits du Benefice brut de l exercice (Taux)',
                            required=True)
    code6 = fields.Many2one('liasse.code.erp', 'Amortissements deduits du Benefice brut de l exercice Duree',
                            required=True)
    code7 = fields.Many2one('liasse.code.erp',
                            'Amortissements deduits du Benefice brut de l exercice Amortissements normaux ou acceleres de l exercice',
                            required=True)
    code8 = fields.Many2one('liasse.code.erp', 'Total des amortissements a la fin de l exercice', required=True)
    code9 = fields.Many2one('liasse.code.erp', 'observations', required=True)
    pm_val_id = fields.Many2one('liasse.dotation.erp', 'pm_val_id', ondelete='cascade', index=True)


class liasse_check_rub(models.Model):
    _name = "liasse.check.rub.erp"
    _description = "liasse.check.rub.erp"

    rub = fields.Char('Rubrique', required=True)
    compte = fields.Char('Compte', required=True)
    code_ids = fields.Many2many('liasse.code.erp', 'check_codecompte_rel_erp', 'check_id', 'code_id',
                                string="Codes EDI", required=True)

    _rec_name = 'rub'


class liasse_extra_field(models.Model):
    _name = "liasse.extra.field.erp"
    _description = "liasse.extra.field.erp"

    code0cpc = fields.Many2one('liasse.code.erp', 'exercice clos', required=True)
    code1prov = fields.Many2one('liasse.code.erp', 'exercice clos', required=True)
    code2fusion = fields.Many2one('liasse.code.erp', 'exercice clos', required=True)
