# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DhNationalCommission(models.Model):
    _name = 'dh.national.commission'
    _description = 'National Commission'
    _rec_name = 'title'

    # year_fondation = fields.Date(string="Year of foundation")
    # location = fields.Char(string='Location')
    # contact = fields.Char(string='Contact')
    # website = fields.Char(string='Official Website')
    # email = fields.Char(string='Email')
    # team
    title = fields.Char(string='Title', translate=True)
    official_name = fields.Char(string='Official name', translate=True)
    phone = fields.Char(string='Phone')
    contact_email = fields.Char(string='Contact email')
    position = fields.Char(string='Position', translate=True)
    since = fields.Char(string='Since', translate=True)
    # photo = fields.Binary(string="Photo")
    photo = fields.Many2many("ir.attachment", string="Photo")


    commission_team_id = fields.Many2one('res.partner',string='National Commission Team')





















