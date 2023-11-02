# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AppraisalRatingFactorValue(models.Model):
    _name = 'appraisal.rating.factor.value'
    _description = 'appraisal rating factor value'

    name = fields.Integer("Note")
    level = fields.Selection([
        ('weak', 'Weak'),
        ('good', 'Good'),
        ('very_good', 'Very good'),
        ('excellent', 'Excellent'),
        ('very_satisfied', 'Very satisfied'),
        ('somewhat_satisfied', 'Somewhat satisfied'),
        ('neither_satisfied', 'Neither satisfied nor dissatisfied'),
        ('somewhat_dissatisfied', 'Somewhat dissatisfied'),
        ('very_dissatisfied', 'Very dissatisfied'),
    ], string="Level")
    evaluation_pays_member = fields.Boolean(string='Pays Member Evaluation')

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False,
                access_rights_uid=None):
        context = self._context
        if context.get('factor_id'):
            factor = self.env['appraisal.rating.factor'].browse(context.get('factor_id'))
            domain = []
            for note in factor.value_ids:
                    domain.append(note.id)
            args += [('id', 'in', domain)]
        return super(AppraisalRatingFactorValue, self)._search(args, offset, limit,
                                                               order,
                                                               count=count,
                                                               access_rights_uid=access_rights_uid)
