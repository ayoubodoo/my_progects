# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.osv import expression

class AccountAsset(models.Model):
    _inherit = 'account.asset'

    code = fields.Char(string="Code", store=True)
    taux = fields.Float(string="Taux")
    employee_id = fields.Many2one('hr.employee', string="Employée")
    num_serie = fields.Char(string='Numéro de série')

    def dh_get_name(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s - %s' % (rec.code, rec.name)))
        return res

    @api.model
    def _name_search(self, name, args=None, operator="ilike", limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = [
                "|",
                ("code", "ilike", name),
                ("name", operator, name),
            ]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ["&", "!"] + domain[1:]
        rec_ids = self._search(
            expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid
        )
        return self.browse(rec_ids).sorted(key=lambda r: r.code).dh_get_name()

    # @api.model
    # def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
    #     if args is None:
    #         args = []
    #     args = args + ['|', '|', ('name', operator, name), ('display_name', operator, name), ('code', operator, name)]
    #     return super(AccountAsset, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)