# -*- coding: utf-8 -*-
from odoo import models, fields, api,  _
from ast import literal_eval


class PaieSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # note = fields.Char(string='Default Note')
    # module_crm = fields.Boolean(string='CRM')
    retard_time = fields.Float(string='Durée de retard maximum')
    marge_horaire = fields.Float(string='Marge Affectation Horaire')

    date_cin = fields.Integer(string=("Expération CIN/passeport/carte diplomatique(nombre des jours)"))
    notif_fin_contrat = fields.Integer(string=("Fin contrat (nombre des jours)"))

    notif_fin_periode_essai = fields.Integer(string=("Fin période d'essai (nombre des jours)"))
    notif_retraite = fields.Integer(string=("Retraite (nombre des jours)"))
    notif_evaluation = fields.Integer(string=("Evaluation (nombre des jours)"))
    date_evaluation = fields.Date(string=("Date d'Evaluation"))
    date_reevaluation = fields.Date(string=("Date de Réévaluation"))
    notif_reevaluation = fields.Integer(string="Réévaluation (nombre des jours)")

    duree_notif_attach = fields.Integer(string='Durée Notif Attachment Tasks')

    def set_values(self):
        res = super(PaieSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('cps_icesco.retard_time',
                                                  self.retard_time)
        self.env['ir.config_parameter'].set_param('cps_icesco.marge_horaire',
                                                  self.marge_horaire)
        self.env['ir.config_parameter'].set_param('cps_icesco.date_cin',
                                                  self.date_cin)
        self.env['ir.config_parameter'].set_param('cps_icesco.notif_fin_contrat',
                                                  self.notif_fin_contrat)
        self.env['ir.config_parameter'].set_param('cps_icesco.notif_fin_periode_essai',
                                                  self.notif_fin_periode_essai)
        self.env['ir.config_parameter'].set_param('cps_icesco.notif_retraite',
                                                  self.notif_retraite)
        self.env['ir.config_parameter'].set_param('cps_icesco.notif_evaluation',
                                                  self.notif_evaluation)
        self.env['ir.config_parameter'].set_param('cps_icesco.date_evaluation',
                                                  self.date_evaluation)
        self.env['ir.config_parameter'].set_param('cps_icesco.notif_reevaluation',
                                                  self.notif_reevaluation)
        self.env['ir.config_parameter'].set_param('cps_icesco.duree_notif_attach',
                                                  self.duree_notif_attach)
        self.env['ir.config_parameter'].set_param('cps_icesco.date_reevaluation',
                                                  self.date_reevaluation)
        return res

    @api.model
    def get_values(self):
        res = super(PaieSettings, self).get_values()
        res.update(
            retard_time=self.env['ir.config_parameter'].sudo().get_param('cps_icesco.retard_time'))
        res.update(
            marge_horaire=self.env['ir.config_parameter'].sudo().get_param('cps_icesco.marge_horaire'))
        res.update(
            date_cin=int(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.date_cin')))
        res.update(
            notif_fin_contrat=int(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.notif_fin_contrat')))
        res.update(
            notif_fin_periode_essai=int(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.notif_fin_periode_essai')))
        res.update(
            notif_retraite=int(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.notif_retraite')))
        res.update(
            notif_evaluation=int(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.notif_evaluation')))
        res.update(
            date_evaluation=self.env['ir.config_parameter'].sudo().get_param('cps_icesco.date_evaluation'))
        res.update(
            notif_reevaluation=int(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.notif_reevaluation')))
        res.update(
            duree_notif_attach=int(self.env['ir.config_parameter'].sudo().get_param('cps_icesco.duree_notif_attach')))
        res.update(
            date_reevaluation=self.env['ir.config_parameter'].sudo().get_param('cps_icesco.date_reevaluation'))
        return res