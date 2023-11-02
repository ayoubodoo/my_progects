# -*- coding: utf-8 -*-
# from datetime import timedelta
from odoo import fields, models, _, api
from odoo.exceptions import ValidationError
import odoo.addons.decimal_precision as dp
from datetime import timedelta
import datetime, calendar


class FyType(models.Model):
    _inherit = 'date.range.type'

    # fiscal_period = fields.Boolean("Is period")
    kzm_is_quinzaine = fields.Boolean("Is quinzaine")


class FyDateRange(models.Model):
    _inherit = 'date.range'

    fiscal_period = fields.Boolean("Is period", related='type_id.fiscal_period',
                                   store=True)
    kzm_is_quinzaine = fields.Boolean("Is quinzaine",
                                      related='type_id.kzm_is_quinzaine', store=True)
    kzm_is_fiscalyear = fields.Boolean("Is fiscal year", related='type_id.fiscal_year',
                                       store=True)
    mois = fields.Selection([
        ('01', '01'), ('02', '02'), ('03', '03'),
        ('04', '04'), ('05', '05'), ('06', '06'),
        ('07', '07'), ('08', '08'), ('09', '09'),
        ('10', '10'), ('11', '11'), ('12', '12')],
        string='Month', compute='month_from_date_start', store=True)
    annee = fields.Integer("Year", compute='month_from_date_start', store=True)
    quinzaine_ids = fields.One2many('date.range', 'fiscal_year_id',
                                    string="Quinzaines", domain=[(
            'kzm_is_quinzaine', '=', True)])
    period_ids = fields.One2many(comodel_name="date.range",
                                 inverse_name="fiscal_year_id", string=u"Périodes",
                                 required=False, domain=[(
            'fiscal_period', '=', True)])

    sequence = fields.Integer(string=_(u"Séquence"), default=1,
                              help=_(
                                  u"La séquence de la période - 1 ou 2 pour les "
                                  u"quinzaine-"))

    @api.depends('date_start')
    def month_from_date_start(self):
        for rec in self:
            if rec.date_start:
                rec.mois = str(rec.date_start.month).zfill(2)
                rec.annee = rec.date_start.year

    def quinzaine(self):
        for rec in self:
            periode = self.env['date.range']
            qz = self.env['date.range.type'].search([(
                        'kzm_is_quinzaine', '=', True)], limit=1)
            if not len(qz):
                raise ValidationError("Merci de créer le type du période quinzaine.")
            
            if not (rec.date_start and rec.date_end and rec.kzm_is_fiscalyear):
                raise ValidationError("Date start/end undifined or is not a fiscal year")
            date_start = fields.Date.from_string(rec.date_start)
            date_end = fields.Date.from_string(rec.date_end)
            v_anne_start = date_start.year
            v_month_start =date_start.month
            v_anne_end = rec.date_end.year
            v_month_end = rec.date_end.month
            self.env.cr.execute("""delete from date_range where fiscal_year_id=%s 
                 and type_id=%s""", (rec.id, qz.id))
            # for j in range(v_month_start, 13):
            #     v_dernier_j = calendar.monthrange(v_anne_start, j)[1]
            #     v_mois = datetime.date(v_anne_start, j, 1).strftime('%b')
            #     date_deb_q1 = datetime.date(v_anne_start, j, 1)
            #     date_fin_q1 = datetime.date(v_anne_start, j, 15)
            #     date_deb_q2 = datetime.date(v_anne_start, j, 16)
            #     date_fin_q2 = datetime.date(v_anne_start, j, v_dernier_j)
            #     v_titre1 = v_mois + " " + str(v_anne_start) + " (Q1)"
            #     v_titre2 = v_mois + " " + str(v_anne_start) + " (Q2)"
            #
            #     periode.create(
            #         {'name': v_titre1,
            #          'date_start': date_deb_q1,
            #          'date_end': date_fin_q1,
            #          'sequence': 1,
            #          'fiscal_year_id': rec.id,
            #          'type_id': qz.id,
            #          })
            #     periode.create(
            #         {'name': v_titre2,
            #          'date_start': date_deb_q2,
            #          'date_end': date_fin_q2,
            #          'sequence': 2,
            #          'fiscal_year_id': rec.id,
            #          'type_id': qz.id})

            for j in range(1, v_month_end+1):
                v_dernier_j = calendar.monthrange(v_anne_end, j)[1]
                v_mois = datetime.date(v_anne_end, j, 1).strftime('%b')
                date_deb_q1 = datetime.date(v_anne_end, j, 1)
                date_fin_q1 = datetime.date(v_anne_end, j, 15)
                date_deb_q2 = datetime.date(v_anne_end, j, 16)
                date_fin_q2 = datetime.date(v_anne_end, j, v_dernier_j)
                v_titre1 = v_mois + " " + str(v_anne_end) + " (Q1)"
                v_titre2 = v_mois + " " + str(v_anne_end) + " (Q2)"
                
                periode.create(
                    {'name': v_titre1, 
                     'date_start': date_deb_q1,
                     'date_end': date_fin_q1,
                     'sequence': 1,
                     'fiscal_year_id': rec.id,
                     'type_id': qz.id,
                     })
                periode.create(
                    {'name': v_titre2,
                     'date_start': date_deb_q2,
                     'date_end': date_fin_q2,
                     'sequence': 2,
                     'fiscal_year_id': rec.id,
                     'type_id': qz.id})
        # r.invalidate_cache()
