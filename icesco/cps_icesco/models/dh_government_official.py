# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DhGouvernmentOfficial(models.Model):
    _name = 'dh.government.official'
    _description = 'Gouvernment Official'

    official_name = fields.Char(string='Official name')
    title = fields.Char(string='Title')
    phone = fields.Char(string='Phone')
    fax = fields.Char(string='Fax')
    contact_email = fields.Char(string='Contact email')
    position = fields.Char(string='Position')
    since = fields.Char(string='Since')
    # photo = fields.Binary(string="Photo")
    photo = fields.Many2many("ir.attachment", string="Photo")
    website = fields.Char(string='Official Web site')

    governement_id = fields.Many2one('res.partner',string='Gouvernment Officials')




















