# -*- encoding: utf-8 -*-
import base64
import csv
import itertools
import datetime as dt
from lxml import etree

from odoo import models, fields, api, _
# from openerp.osv import fields, osv
from odoo import tools


class credit_bail(models.Model):
    _name = "credi.bail.erp"
    _description = "credi.bail.erp"

    rubrique = fields.Char('Rubriques')
    date_first_ech = fields.Date('Date de la 1ere echeance')
    duree_contrat = fields.Integer('Duree du contrat en mois')
    val_estime = fields.Float('Valeur estimee du bien a la date du contrat')
    duree_theo = fields.Integer('Duree theorique d amortissement du bien ')
    cumul_prec = fields.Float('Cumul des exercices precedents des redevances')
    montant_rev = fields.Float('Montant de l exercice des redevances')
    rev_moins = fields.Float('redevances restant a payer (A moins d un an)')
    rev_plus = fields.Float('redevances restant a payer (A plus d un an)')
    prix_achat = fields.Float('Prix d achat residuel en fin de contrat')
    observation = fields.Char('Observations')
    balance_id = fields.Many2one('liasse.balance.erp', 'liasse conf', ondelete='cascade', index=True)

    company_id = fields.Many2one("res.company", ondelete='cascade',
                                 string=_("Ferme"), required=True,
                                 default=lambda self: self.env.company
                                 )


class pm_value(models.Model):
    _name = "pm.value.erp"
    _description = "pm.value.erp"

    date_cession = fields.Date('Date de cession ou de retrait')
    compte_princ = fields.Float('Compte principal')
    montant_brut = fields.Float('Montant brut')
    amort_cumul = fields.Float('Amortissements cumules')
    val_net_amort = fields.Float('Valeur nette d\'amortissements')
    prod_cess = fields.Float('Produit de cession')
    plus_value = fields.Float('Plus values')
    moins_value = fields.Float('Moins values')
    balance_id = fields.Many2one('liasse.balance.erp', 'liasse conf', ondelete='cascade', index=True)

    company_id = fields.Many2one("res.company", ondelete='cascade',
                                 string=_("Ferme"), required=True,
                                 default=lambda self: self.env.company
                                 )


class titre_particip(models.Model):
    _name = "titre.particip.erp"
    _description = "titre.particip.erp"

    raison_soc = fields.Char('Raison sociale de la société émettrice')
    sect_activity = fields.Char('Secteur d\'activité')
    capit_social = fields.Float('Capital social')
    particip_cap = fields.Float('Participation au capital %')
    prix_global = fields.Float('Prix d\'acquisition global ')
    val_compt = fields.Float('Valeur comptable nette')
    extr_date = fields.Date('Extrait des derniers états de synthèse de la société émettrice(Date de clôture)')
    extr_situation = fields.Float('Extrait des derniers états de synthèse de la société émettrice(Situation nette)')
    extr_resultat = fields.Float('Extrait des derniers états de synthèse de la société émettrice(résultat net)')
    prod_inscrit = fields.Float('Produits inscrits au C.P.C de l\'exercice ')
    balance_id = fields.Many2one('liasse.balance.erp', 'liasse conf', ondelete='cascade', index=True)

    company_id = fields.Many2one("res.company", ondelete='cascade',
                                 string=_("Ferme"), required=True,
                                 default=lambda self: self.env.company
                                 )


class repart_cs(models.Model):
    _name = "repart.cs.erp"
    _description = "repart.cs.erp"

    name = fields.Char('Nom, prenom ou raison sociale des principaux associes')
    id_fisc = fields.Integer('IF')
    cin = fields.Char('CIN')
    adress = fields.Char('Adresse')
    number_prec = fields.Integer('NOMBRE DE TITRES (Exercice precedent)')
    number_actual = fields.Integer('NOMBRE DE TITRES (Exercice actual)')
    val_nom = fields.Float('Valeur nominale de chaque action ou part sociale')
    val_sousc = fields.Float('MONTANT DU CAPITAL(Souscrit)')
    val_appele = fields.Float('MONTANT DU CAPITAL(Appele)')
    val_lib = fields.Float('MONTANT DU CAPITAL(libere)')
    balance_id = fields.Many2one('liasse.balance.erp', 'liasse conf', ondelete='cascade', index=True)

    company_id = fields.Many2one("res.company", ondelete='cascade',
                                 string=_("Ferme"), required=True,
                                 default=lambda self: self.env.company
                                 )

class interets(models.Model):
    _name = "interets.erp"
    _description = "interets.erp"

    name = fields.Char('Nom, prenom ou raison sociale des principaux associes')
    adress = fields.Char('Adresse')
    cin = fields.Char('N C.I.N. ou Article I.S.')
    mont_pretl = fields.Float('Montant du pret')
    date_pret = fields.Date('Date du  pret ')
    duree_mois = fields.Integer('Duree du pret (en mois)')
    taux_inter = fields.Float('Taux d\'interet')
    charge_global = fields.Float('Charge financiere globale')
    remb_princ = fields.Float('Remboursement exercices anterieurs(Principal)')
    remb_inter = fields.Float('Remboursement exercices anterieurs(Interet)')
    remb_actual_princ = fields.Float('Remboursement exercice actuel(Principal)')
    remb_actual_inter = fields.Float('Remboursement exercice actuel(Interet)')
    observation = fields.Char('Observations')
    type = fields.Selection([('0', 'Associe'), ('1', 'Tier')], 'A/T')
    balance_id = fields.Many2one('liasse.balance.erp', 'liasse conf', ondelete='cascade', index=True)

    company_id = fields.Many2one("res.company", ondelete='cascade',
                                 string=_("Ferme"), required=True,
                                 default=lambda self: self.env.company
                                 )


"""        
class interets_tier(models.Model):
        _name = "interets.tier"
        
            'name = fields.Char('Nom, prénom ou raison sociale des principaux associés')
            'adress = fields.Char('Adresse')
            'cin = fields.Char('N° C.I.N. ou Article I.S.')
            'mont_pretl = fields.Float('Montant du prêt')
            'date_pret = fields.Date('Date du  prêt ')
            'duree_mois = fields.Integer('Durée du prêt (en mois)')
            'taux_inter = fields.Float('Taux d\'intérêt')
            'charge_global = fields.Float('Charge financière globale')
            'remb_princ = fields.Float('Remboursement exercices antérieurs(Principal)')
            'remb_inter = fields.Float('Remboursement exercices antérieurs(Intérêt)')
            'remb_actual_princ = fields.Float('Remboursement exercice actuel(Principal)')
            'remb_actual_inter = fields.Float('Remboursement exercice actuel(Intérêt)')
            'observation = fields.Char('Observations')
            'balance_id = fields.Many2one('liasse.balance', 'liasse conf', ondelete='cascade', index=True)

    } 
 """


class beaux(models.Model):
    _name = "beaux.erp"
    _description = "beaux.erp"

    nature = fields.Char('Nature du bien loué')
    lieu = fields.Char('Lieu de situation')
    name = fields.Char('Nom et prénoms ou Raison sociale et adresse du propriétaire')
    date_loc = fields.Date('Date de conclusion de l\'acte de location')
    mont_annuel = fields.Float('Montant annuel de location')
    mont_loyer = fields.Float('Montant du loyer compris dans les charges de l\'exercice')
    nature_bail = fields.Char('Nature du contrat Bail-ordinaire')
    nature_periode = fields.Char('Nature du contrat(Nème période)')
    balance_id = fields.Many2one('liasse.balance.erp', 'liasse conf', ondelete='cascade', index=True)

    company_id = fields.Many2one( "res.company", ondelete='cascade',
                                 string=_("Ferme"), required=True,
                                 default=lambda self: self.env.company
                                 )


class passage(models.Model):
    _name = 'passage.erp'
    _description = 'passage.erp'

    name = fields.Char(u'intitulé')
    montant1 = fields.Float('Montant +')
    montant2 = fields.Float('Montant -')
    type = fields.Selection(
        [('0', 'REINTEGRATIONS FISCALES COURANTES'),
         ('1', 'REINTEGRATIONS FISCALES NON COURANTES'),
         ('2', 'DEDUCTIONS FISCALES COURANTES'),
         ('3', 'DEDUCTIONS FISCALES NON COURANTES ')], 'Type')
    balance_id = fields.Many2one('liasse.balance.erp', 'liasse conf', ondelete='cascade', index=True)


class dotation_amort(models.Model):
    _name = "dotation.amort.erp"
    _description = "dotation.amort.erp"

    code0 = fields.Char('Immobilisations concernees')
    code1 = fields.Date('Date entree')
    code2 = fields.Float('Valeur a amortir (Prix dacquisition)')
    code3 = fields.Float(u'Valeur a amortir - Valeur comptable apres reevaluation')
    code4 = fields.Float('Amortissements anterieurs')
    code5 = fields.Float('Amortissements deduits du Benefice brut de l exercice (Taux)')
    code6 = fields.Integer('Amortissements deduits du Benefice brut de l exercice Duree')
    code7 = fields.Float(
        'Amortissements deduits du Benefice brut de l exercice Amortissements normaux ou acceleres de l exercice')
    code8 = fields.Float('Total des amortissements a la fin de l exercice')
    code9 = fields.Char('observations')
    balance_id = fields.Many2one('liasse.balance.erp', 'liasse conf', ondelete='cascade', index=True)

    company_id = fields.Many2one("res.company", ondelete='cascade',
                                 string=_("Ferme"), required=True,
                                 default=lambda self: self.env.company
                                 )


class declaration(models.Model):
    _name = 'declarationrvt.declaration.erp'
    _description = 'declarationrvt.declaration.erp'
    _rec_name = "id_declar"

    id_declar = fields.Char('Nom de la declaration RVT:', required=True)
    #  'date_debut = fields.Date('Date debut:',required=True)
    # 'date_fin = fields.Date('Date fin:',required=True)
    output = fields.Binary('Declaration_xml:', readonly=True)
    output_nom = fields.Char('File name', default='declaration.xml')
    ben_ids = fields.One2many('declarationrvt.beneficiaire.erp', 'ben_id', 'Beneficiaires', required=True)
    date_id = fields.Many2one('liasse.fiche.signalitique.erp', 'Fiche signalitique', required=True)

    company_id = fields.Many2one("res.company", ondelete='cascade',
                                 string=_("Ferme"), required=True,
                                 default=lambda self: self.env.company
                                 )

    #
    # def generatexml(self):
    #     for rec in self:
    #         id_fiscal = rec.id_declar
    #         # date_deb = rec.Date_debut
    #         # date_f = rec.Date_fin
    #         benids = rec.ben_ids
    #         dateid = rec.Date_id
    #
    #         doc = etree.Element("DeclarationRVT", nsmap={})
    #         id = etree.SubElement(doc, "identifiantFiscal")
    #         id.text = str(id_fiscal)
    #
    #         dated = etree.SubElement(doc, "exerciceFiscalDu")
    #         dated.text = str(dateid.Date_start)
    #         datef = etree.SubElement(doc, "exerciceFiscalAu")
    #         datef.text = str(dateid.Date_end)
    #
    #         for ben in benids:
    #             id_fis = ben.idfiscal
    #             honorair = ben.honoraires
    #             commission = ben.commissions
    #             rab = ben.rab
    #             r_soc = ben.raison_sociale
    #             adres = ben.adress
    #             numtp = ben.numtaxe
    #             numcnss = ben.num_cnss
    #             vv = ben.villeben
    #             prof = ben.professionben
    #             natio = ben.nationaliteben
    #             sommes = etree.SubElement(doc, "sommesAllouees")
    #             somme = etree.SubElement(sommes, "sommesAllouee")
    #             honoraire = etree.SubElement(somme, "honoraires")
    #             honoraire.text = str(honorair)
    #             commis = etree.SubElement(somme, "commissions")
    #             commis.text = str(commission)
    #             rabais = etree.SubElement(somme, "rabais")
    #             rabais.text = str(rab)
    #             benef = etree.SubElement(somme, "beneficiaire")
    #             id_fisc = etree.SubElement(benef, "identifiantFiscal")
    #             id_fisc.text = str(id_fis)
    #             rais_soc = etree.SubElement(benef, "raisonSociale")
    #             rais_soc.text = str(r_soc)
    #             adr = etree.SubElement(benef, "adresse")
    #             adr.text = str(adres)
    #             ntp = etree.SubElement(benef, "numeroTP")
    #             ntp.text = str(numtp)
    #             ncnss = etree.SubElement(benef, "numCNSS")
    #             ncnss.text = str(numcnss)
    #             v = etree.SubElement(benef, "ville")
    #             v.text = str(vv)
    #             pro = etree.SubElement(benef, "profession")
    #             pro.text = str(prof)
    #             nat = etree.SubElement(benef, "nationalite")
    #             nat.text = str(natio)
    #
    #     xml_data = "%s" % (
    #         etree.tostring(doc, pretty_print=True, xml_declaration=True, encoding='UTF-8')
    #     )
    #
    #     self.write({
    #         'output': base64.b64encode(xml_data.encode('utf8')),
    #     })
    #     return True


class beneficiaire(models.Model):
    _name = 'declarationrvt.beneficiaire.erp'
    _description = 'declarationrvt.beneficiaire.erp'

    raison_sociale = fields.Char('Nom et prénom ou raison_sociale', required=True)
    idfiscal = fields.Char('Identifiant fiscal', required=True)
    numtaxe = fields.Char('Numéro de la taxe professionnelle', required=True)
    num_registre = fields.Char('Numéro du registre de commerce')
    num_cnss = fields.Char('Numéro affiliation CNSS', required=True)
    adress = fields.Char(' ', required=True)
    villeben = fields.Char('Ville', required=True)
    telephone = fields.Char('Téléphone')
    fax = fields.Char('Fax')
    email = fields.Char('Email')
    forme_juridique = fields.Char('Forme juridique')
    professionben = fields.Char('Profession ou activités exercées', required=True)
    honoraires = fields.Float('honoraires', required=True)
    commissions = fields.Float('commissions', required=True)
    rab = fields.Float('rabais', required=True)
    nationaliteben = fields.Char('Nationalité', required=True)
    ben_id = fields.Many2one('declarationrvt.declaration.erp', 'ben_ids', required=True)


class actif(models.Model):
    _name = "bilan.actif.fiscale.erp"
    _description = "bilan.actif.fiscale.erp"

    lib = fields.Char('Libelle', required=True)
    code1 = fields.Float('Brut', required=True)
    code2 = fields.Float('Amortissement et provisions', required=True)
    code3 = fields.Float('Net', required=True)
    code4 = fields.Float('Net Precedent', required=True)
    code0 = fields.Many2one('liasse.bilan.actif.erp', 'codification')
    balance_id = fields.Many2one('liasse.balance.erp', 'liasse conf', ondelete='cascade', index=True)
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Entete'),
        ('2', u'Total'),
    ],
        'Type', default='0', required=True)
    sequence = fields.Integer('Sequence', required=True)


class passif(models.Model):
    _name = "bilan.passif.fiscale.erp"
    _description = "bilan.passif.fiscale.erp"

    lib = fields.Char('Libelle', required=True)
    code1 = fields.Float('Exercice', required=True)
    code2 = fields.Float('Exercice precedent', required=True)
    code0 = fields.Many2one('liasse.bilan.passif.erp', 'codification')
    balance_id = fields.Many2one('liasse.balance.erp', 'liasse conf', ondelete='cascade', index=True)
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Entete'),
        ('2', 'Total'),
    ],
        'Type', default='0', required=True)
    sequence = fields.Integer('Sequence', required=True)


class cpc(models.Model):
    _name = "cpc.fiscale.erp"
    _description = "cpc.fiscale.erp"

    lib = fields.Char('Nature', required=True)
    code1 = fields.Float('Operations propres à l\'exercice ', required=True)
    code2 = fields.Float('Operations concernant les exercices precedents', required=True)
    code3 = fields.Float('TOTAUX DE L\'EXERCICE ', required=True)
    code4 = fields.Float('TOTAUX DE L\'EXERCICE PRECEDENT', required=True)
    code0 = fields.Many2one('liasse.cpc.erp', 'codification')
    balance_id = fields.Many2one('liasse.balance.erp', 'liasse conf', ondelete='cascade', index=True)
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Entete'),
        ('2', 'Total'),
    ],
        'Type', default='0', required=True)
    sequence = fields.Integer('Sequence', required=True)


class det_cpc(models.Model):
    _name = "det.cpc.fiscale.erp"
    _description = "det.cpc.fiscale.erp"

    poste = fields.Char('Poste')
    lib = fields.Char('Libelle', required=True)
    code1 = fields.Float('Exercice', required=True)
    code2 = fields.Float('Exercice precedent', required=True)
    code0 = fields.Many2one('liasse.det.cpc.erp', 'codification')
    balance_id = fields.Many2one('liasse.balance.erp', 'liasse conf', ondelete='cascade', index=True)
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Entete'),
        ('2', 'Total'),
    ],
        'Type', default='0', required=True)
    sequence = fields.Integer('Sequence', required=True)


class tfr(models.Model):
    _name = "tfr.fiscale.erp"
    _description = "tfr.fiscale.erp"

    lettre = fields.Char('Lettre')
    num = fields.Char('Num')
    op = fields.Char('Operateur')
    lib = fields.Char('Libelle', required=True)
    code1 = fields.Float('Exercice', required=True)
    code2 = fields.Float('Exercice precedent', required=True)
    code0 = fields.Many2one('liasse.tfr.erp', 'codification')
    balance_id = fields.Many2one('liasse.balance.erp', 'liasse conf', ondelete='cascade', index=True)
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Entete'),
        ('2', 'Total'),
    ],
        'Type', default='0', required=True)
    sequence = fields.Integer('Sequence', required=True)


class caf(models.Model):
    _name = "caf.fiscale.erp"
    _description = "caf.fiscale.erp"

    lettre = fields.Char('Lettre')
    num = fields.Char('Num')
    op = fields.Char('Operateur')
    lib = fields.Char('Libelle', required=True)
    code1 = fields.Float('Exercice', required=True)
    code2 = fields.Float('Exercice precedent', required=True)
    code0 = fields.Many2one('liasse.caf.erp', 'codification')
    balance_id = fields.Many2one('liasse.balance.erp', 'liasse conf', ondelete='cascade', index=True)
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Entete'),
        ('2', 'Total'),
    ],
        'Type', default='0', required=True)
    sequence = fields.Integer('Sequence', required=True)


class amort(models.Model):
    _name = "amort.fiscale.erp"
    _description = "amort.fiscale.erp"

    lib = fields.Char('Nature', required=True)
    code1 = fields.Float('Cumul debut', required=True)
    code2 = fields.Float('Dotation', required=True)
    code3 = fields.Float('Amortissement', required=True)
    code4 = fields.Float('Cumul d amortissement', required=True)
    code0 = fields.Many2one('liasse.amort.erp', 'codification')
    balance_id = fields.Many2one('liasse.balance.erp', 'liasse conf', ondelete='cascade', index=True)
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Entete'),
        ('2', 'Total'),
    ],
        'Type', default='0', required=True)
    sequence = fields.Integer('Sequence', required=True)


class provision(models.Model):
    _name = "provision.fiscale.erp"
    _description = "provision.fiscale.erp"

    lib = fields.Char('Nature', required=True)
    code1 = fields.Float('Montant debut', required=True)
    code2 = fields.Float('Dot exp', required=True)
    code3 = fields.Float('Dot fin', required=True)
    code4 = fields.Float('Dot nc', required=True)
    code5 = fields.Float('Rep exp', required=True)
    code6 = fields.Float('Rep fin', required=True)
    code7 = fields.Float('Rep nc', required=True)
    code8 = fields.Float('Montant fin', required=True)
    code0 = fields.Many2one('liasse.provision.erp', 'codification')
    balance_id = fields.Many2one('liasse.balance.erp', 'liasse conf', ondelete='cascade', index=True)
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Entete'),
        ('2', 'Total'),
    ],
        'Type', default='0', required=True)
    sequence = fields.Integer('Sequence', required=True)


class liasse_stock(models.Model):
    _name = "stock.fiscale.erp"
    _description = "stock.fiscale.erp"

    lib = fields.Char('STOCKS', required=True)
    code1 = fields.Float('S.F. Montant Brut', required=True)
    code2 = fields.Float(u'S.F. Provision pour depreciation', required=True)
    code3 = fields.Float('S.F. Montant net', required=True)
    code4 = fields.Float(' S.I. Montant brut', required=True)
    code5 = fields.Float('S.I.Provision pour depreciation', required=True)
    code6 = fields.Float('S.I.Montant net', required=True)
    code0 = fields.Many2one('liasse.stock.erp', 'codification')
    balance_id = fields.Many2one('liasse.balance.erp', 'liasse conf', ondelete='cascade', index=True)
    code7 = fields.Float('Variation de stock en valeur', required=True)
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Entete'),
        ('2', 'Total'),
    ],
        'Type', default='0', required=True)
    sequence = fields.Integer('Sequence', required=True)


class fusion(models.Model):
    _name = "fusion.fiscale.erp"
    _description = "fusion.fiscale.erp"

    lib = fields.Char('Elements', required=True)
    code1 = fields.Float('Valeur d aport', required=True)
    code2 = fields.Float('Valeur nette comptable', required=True)
    code3 = fields.Float('Plus-value constatee et differee', required=True)
    code4 = fields.Float('Fraction de la plus-value rapportee aux l exercices anterieurs (cumul) en %', required=True)
    code5 = fields.Float('Fraction de la plus-value rapportee a l exercices actuel en %', required=True)
    code6 = fields.Float('Cumul des plus-values rapportees', required=True)
    code7 = fields.Float('Solde des plus-values non imputees', required=True)
    code8 = fields.Char('Observations')
    code0 = fields.Many2one('liasse.fusion.erp', 'codification')
    balance_id = fields.Many2one('liasse.balance.erp', 'liasse conf', ondelete='cascade', index=True)
    type = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Entete'),
        ('2', u'Total'),
    ],
        'Type', default='0', required=True)
    sequence = fields.Integer('Sequence', required=True)


    @api.onchange('code1', 'code0')
    def onchange_code1(self):
        for r in self:
            fusion = r.env['liasse.fusion.erp']
            fusion_ids = fusion.browse([r.code0.id])
            for row in fusion_ids:
                row.code1.write({'valeur': r.code1})
        return True

    @api.onchange('code2', 'code0')
    def onchange_code2(self):
        for r in self:
            fusion = r.env['liasse.fusion.erp']
            fusion_ids = fusion.browse([r.code0])
            for row in fusion_ids:
                row.code2.write({'valeur': r.code2})
        return True

    @api.onchange('code3', 'code0')
    def onchange_code3(self):
        for r in self:
            fusion = self.env['liasse.fusion.erp']
            fusion_ids = fusion.browse([r.code0])
            for row in fusion_ids:
                row.code3.write({'valeur': r.code3})
        return True

    @api.onchange('code4', 'code0')
    def onchange_code4(self):
        for r in self:
            fusion = self.env['liasse.fusion.erp']
            fusion_ids = fusion.browse([r.code0])
            for row in fusion_ids:
                row.code4.write({'valeur': r.code4})
        return True

    @api.onchange('code5', 'code0')
    def onchange_code5(self):
        for r in self:
            fusion = self.env['liasse.fusion.erp']
            fusion_ids = fusion.browse([r.code0])
            for row in fusion_ids:
                row.code5.write({'valeur': r.code5})
        return True

    @api.onchange('code6', 'code0')
    def onchange_code6(self):
        for r in self:
            fusion = self.env['liasse.fusion.erp']
            fusion_ids = fusion.browse([r.code0])
            for row in fusion_ids:
                row.code6.write( {'valeur': r.code6})
        return True

    @api.onchange('code7', 'code0')
    def onchange_code7(self):
        for r in self:
            fusion = self.env['liasse.fusion.erp']
            fusion_ids = fusion.browse([r.code0])
            for row in fusion_ids:
                row.code7.write({'valeur': r.code7})
        return True

    @api.onchange('code8', 'code0')
    def onchange_code8(self):
        for r in self:
            fusion = self.env['liasse.fusion.erp']
            fusion_ids = fusion.browse([r.code0])
            for row in fusion_ids:
                row.code8.write({'valeur': r.code8})
        return True
