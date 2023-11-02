# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class DhAgreementsInternational(models.Model):
    _name = 'dh.agreements.international'

    name = fields.Char(string='إسم')
    year = fields.Char(string='السنة')
    date = fields.Date(string='السنة')

    type_agr = fields.Many2one('dh.agreement.type', string='نوع الاتفاقية')
    category = fields.Many2one('dh.agreement.category', string='الفئات')
    type_partenaire = fields.Selection([('type1', 'المؤسسات والمنظمات الحكومية'), ('type2', 'المؤسسات والمنظمات غير الحكومية')], string='حكومية أم غير حكومية ؟',)
    description = fields.Text(translate=True,string='التفاصيل', readonly=False)
    partner_id = fields.Many2one('res.partner', string='الشريك', domain=['|', '|', '|', '|', ('institution_gouv_etat_member', '=', True), ('institution_gouv_etat_non_member', '=', True), ('organisation_mondiale_rare', '=', True), ('organisation_locale', '=', True), ('organisation_regional', '=', True)])

    # not use (juste for data error)
    type = fields.Selection([('type1', 'اتفاقية شراكة '), ('type2', 'اتفاقية تعاون'), ('type3', 'اتفاقية تفاهم')],
                            string='type')

    received_amount = fields.Float(string='Obtained budget')
    received_amount_prevu = fields.Float(string='Expected budget')

    partnership_sector_ids = fields.One2many('dh.agreements.international.sectors', 'agreement_id', string='Partnership sectors')
    def action_view_partnership_sectors(self):
        for rec in self:
            result = {
                'name': _("Partnership sectors"),
                'res_model': 'dh.agreements.international.sectors',
                'view_mode': 'tree',
                'view_type': 'tree',
                'views': [(self.env.ref("dh_icesco_project.dh_agreement_international_sector_tree").id, 'list')],
                'domain': [('agreement_id', '=', rec.id)],
                'context': "{'default_agreement_id' : %s}" % (rec.id),
                'type': 'ir.actions.act_window',
                'target': 'current',
            }
            return result