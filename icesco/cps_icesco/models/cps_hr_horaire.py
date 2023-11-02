# # -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime, timedelta
import pytz
from pytz import timezone, UTC

class CpsHrHoraire(models.Model):
    _name = 'cps.hr.horaire'

    # date_debut = fields.Datetime('Début application horaire')
    # date_fin = fields.Datetime('Fin application horaire')

    dates = fields.One2many('cps.date.horaire', 'horaire_id', string='Dates')
    horaire_debut = fields.Datetime('Heure debut', required=True)
    horaire_debut_pytz = fields.Datetime('Heure debut Converted', compute='compute_horaire_debut_pytz')
    horaire_fin = fields.Datetime('Heure Fin', required=True)
    horaire_max_pointage = fields.Datetime('Heure Max Pointage', required=True)
    horaire_fin_pytz = fields.Datetime('Heure Fin Converted', compute='compute_horaire_fin_pytz')
    duree_pause = fields.Float('Durée pause')

    name = fields.Char("name", compute="compute_name", store=True)

    #HS
    horaire_debut_h25 = fields.Datetime('Debut HS 25%', required=True)
    horaire_fin_h25 = fields.Datetime('Fin HS 25% ', required=True)
    horaire_debut_h50 = fields.Datetime('Debut HS 50%', required=True)
    horaire_fin_h50 = fields.Datetime('Fin HS 50%', required=True)

    @api.depends('horaire_debut')
    def compute_horaire_debut_pytz(self):
        for rec in self:
            if rec.horaire_debut:
                today_utc = pytz.UTC.localize(rec.horaire_debut)
                if self.env.user.tz:
                    tz = self.env.user.tz
                else:
                    tz = 'UTC'
                today_tz = today_utc.astimezone(pytz.timezone(tz))
                rec.horaire_debut_pytz = rec.horaire_debut + timedelta(hours=int(str(today_tz)[-4]))
            else:
                rec.horaire_debut_pytz = False

    @api.depends('horaire_fin')
    def compute_horaire_fin_pytz(self):
        for rec in self:
            if rec.horaire_fin:
                today_utc = pytz.UTC.localize(rec.horaire_fin)
                if self.env.user.tz:
                    tz = self.env.user.tz
                else:
                    tz = 'UTC'
                today_tz = today_utc.astimezone(pytz.timezone(tz))
                rec.horaire_fin_pytz = rec.horaire_fin + timedelta(hours=int(str(today_tz)[-4]))
            else:
                rec.horaire_fin_pytz = False

    def name_get(self):
        res = []
        #designation_client, designation, type, couleur
        for rec in self:
            name = rec.name
            res.append((rec.id, name))
        return res

    @api.depends('horaire_debut','horaire_fin')
    def compute_name(self):
        recs = []
        for p in self:
            name = ""
            if p.horaire_debut is not False:
                today_utc = pytz.UTC.localize(p.horaire_debut)
                if self.env.user.tz:
                    tz = self.env.user.tz
                else:
                    tz = 'UTC'
                today_tz = today_utc.astimezone(pytz.timezone(tz))
                name = name + " DE " + (datetime.strptime(p.horaire_debut.strftime('%H:%M:%S'), '%H:%M:%S') + timedelta(hours=int(str(today_tz)[-4]))).strftime('%H:%M')
            if p.horaire_fin is not False:
                today_utc = pytz.UTC.localize(p.horaire_fin)
                if self.env.user.tz:
                    tz = self.env.user.tz
                else:
                    tz = 'UTC'
                today_tz = today_utc.astimezone(pytz.timezone(tz))
                name = name + " A " +(datetime.strptime(p.horaire_fin.strftime('%H:%M:%S'), '%H:%M:%S') + timedelta(hours=int(str(today_tz)[-4]))).strftime('%H:%M')
            p.name=name

class CpsDateHoraire(models.Model):
    _name = 'cps.date.horaire'

    date_debut = fields.Datetime('Début application horaire', required=True)
    date_fin = fields.Datetime('Fin application horaire', required=True)
    horaire_id = fields.Many2one('cps.hr.horaire', string='Horaire')