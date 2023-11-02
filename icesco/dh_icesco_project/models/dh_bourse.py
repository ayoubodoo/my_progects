# -*- coding: utf-8 -*-
from odoo import models, fields, api
import requests

class Dhbourse(models.Model):
    _name = 'dh.bourse'

    pilliar_id = fields.Many2one('dh.pilliar',translate=True , string='المحور')
    pays_id = fields.Many2one('res.partner',store=True, string='الدولة')
    is_member_state = fields.Boolean(string='Is member state ?', related='pays_id.is_member_state')
    etudiants = fields.Many2many('res.partner',store=True, string='أسماء الطلبة')
    niveau_scolaire = fields.Char(store=True,string='المستوى الدراسي')
    anee_bourse = fields.Char(store=True,string='سنة المنحة')
    annee_bourse = fields.Date(store=True,string='سنة المنحة')
    etablissement = fields.Char(store=True,translate=True,string='المؤسسة')
    etat_bourse = fields.Char(store=True,string='وضعية المنحة لعام')
    symbol = fields.Char(store=True,string=' العملة')
    suivi = fields.Char(store=True,string='متابعة')
    periode_avalibality= fields.Integer(store=True,string='مدة المنحة')
    fin_avalibality= fields.Char(store=True,string=' تاريخ نهاية المنحة')
    bourse= fields.Float(store=True,string='قيمة المنحة شهريا')

