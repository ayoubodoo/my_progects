# -*- coding: utf-8 -*-

from odoo import models, fields, api
import locale


class ResPartner(models.Model):
    _inherit = 'res.partner'

    display_name = fields.Char(string='Display Name', required=False, readonly=False, index=False, translate=True)
    name = fields.Char(index=True, translate=True)
    is_ioc_organization = fields.Boolean('OIC Organizations')
    is_un_organization = fields.Boolean('UN Organizations')
    is_au_organization = fields.Boolean('AU Organizations')
    is_al_organization = fields.Boolean('AL Organizations')
    #

    date = fields.Date(string='Date')
    official_leaders = fields.Char(string='Official Leaders Name', translate=True)
    official_country_name = fields.Char(string='Official country name', translate=True)
    population = fields.Float(string='Population Number', digits=(24, 0))
    muslim_population = fields.Integer(string='Muslim Population')
    gpd_per_capital = fields.Float(string='GPD per capital')
    national_day = fields.Char(string='National day', translate=True)
    portal_national_day = fields.Char(string='Portal National Day', compute='compute_portal_national_day', translate=True)
    name_national_day = fields.Char(string='Name National day', translate=True)
    other_national_days = fields.One2many('dh.national.days','partner_id', string='Other national days')
    # other_national_days = fields.Many2many('dh.national.days', string='other_national_days')
    flag_color = fields.One2many('dh.flag.reference', 'partner_id', string='Flag Color references')
    # country_flag = fields.Binary(string='Country flag')
    country_flag = fields.Many2many("ir.attachment", string="Invitation")
    official_language = fields.Many2many('dh.lang', string='Official language')
    used_language = fields.Many2many('dh.lang',relation="relation_used_language", string='Used language')
    country_capital = fields.Many2one('res.city', string='Country capital', translate=True)
    country_type = fields.Selection(
        [('president', 'President'), ('king_queen', 'King / Queen')],
        string="Type"
    )
    # National commission secretary general
    official_name = fields.Char(string='Official name', translate=True)
    work_official_name = fields.Char(string='Work official name', translate=True)
    commission_title = fields.Char(string='Title')
    phone_commission = fields.Char(string='Phone')
    email_commission = fields.Char(string='Contact email')
    since = fields.Char(string='Since')
    photo = fields.Many2many("ir.attachment", relation='dh_res_partner_photo_rel', string="Photo of Secretary General ")
    # photo = fields.Many2many("ir.attachment", string="Photo")

    # National commission deputy secretary general or his representative
    official_name_deputy = fields.Char(string='Official name')
    commission_title_deputy = fields.Char(string='Title')
    phone_commission_deputy = fields.Char(string='Phone')
    email_commission_deputy = fields.Char(string='Contact email')
    since_deputy = fields.Char(string='Since')
    photo_deputy = fields.Many2many("ir.attachment", relation='dh_res_partner_photo_deputy_rel', string="Photo of Deputy Secretary General")
    # photo = fields.Many2many("ir.attachment", string="Photo of Deputy Secretary General")
    # Government Officials
    government_officials = fields.One2many('dh.government.official','governement_id', string='Government Officials')
    # National Commission
    year_fondation_national_commission = fields.Date(string="Year of foundation")
    location_national_commission = fields.Char(string='Location', translate=True)
    contact_national_commission = fields.Char(string='Contact')
    name_head_national_commission = fields.Char(string='Name Head national commission', translate=True)
    tasks_head_national_commission = fields.Char(string='Tasks Head national commission', translate=True)
    fax_national_commission = fields.Char(string='Fax')
    website_national_commission = fields.Char(string='Official Website')
    email_national_commission = fields.Char(string='Email')

    # National Commission Team
    commission_team_ids = fields.One2many('dh.national.commission','commission_team_id', string='National Commission Team')
    is_member_state = fields.Boolean('Is member state ?')

    is_commission = fields.Boolean('Is commission ?')
    is_amana = fields.Boolean('Is Amana ?')

    @api.depends('national_day')
    def compute_portal_national_day(self):
        for rec in self:
            rec.portal_national_day = rec.national_day
            # rec.portal_national_day = ''
            # if rec.national_day != False:
            #     if self.env.context['lang'][:2] != 'ar':
            #         locale.setlocale(locale.LC_TIME, self.env.context['lang'] + '.utf8')
            #     else:
            #         locale.setlocale(locale.LC_TIME, 'ar_MA.utf8')
            #     rec.portal_national_day = rec.national_day.strftime('%d %B')

    @api.model
    def my_search_read_official_language(self, **args):
        official_language = self.env['res.users'].sudo().search([('id', '=', self.env.uid)]).partner_id.official_language
        res = []
        for language in official_language:
            res.append({'key': language['id'], 'value': language['display_name']})
        return res

    @api.model
    def my_search_read_national_days(self, **args):
        other_national_days = self.env['res.users'].sudo().search([('id', '=', self.env.uid)]).partner_id.other_national_days
        res = []
        for national_day in other_national_days:
            res.append({'name': national_day['name'], 'date': national_day['date']})
        return res

    @api.model
    def my_search_read_flag_color(self, **args):
        flag_color = self.env['res.users'].sudo().search([('id', '=', self.env.uid)]).partner_id.flag_color
        res = []
        for flag_col in flag_color:
            res.append({'hex': flag_col['hex'], 'rgb': flag_col['rgb']})
        return res

    @api.model
    def my_search_read_government_officials(self, **args):
        government_officials = self.env['res.users'].sudo().search([('id', '=', self.env.uid)]).partner_id.government_officials
        res = []
        for government_official in government_officials:
            res.append({'title': government_official['title'], 'official_name': government_official['official_name'], 'position': government_official['position'], 'contact_email': government_official['contact_email'], 'phone': government_official['phone'], 'since': government_official['since'], 'website': government_official['website']})
        return res

    @api.model
    def my_search_read_commission_teams(self, **args):
        commission_teams = self.env['res.users'].sudo().search([('id', '=', self.env.uid)]).partner_id.commission_team_ids
        res = []
        for commission_team in commission_teams:
            res.append({'title': commission_team['title'], 'official_name': commission_team['official_name'], 'contact_email': commission_team['contact_email'], 'phone': commission_team['phone']})
        return res
