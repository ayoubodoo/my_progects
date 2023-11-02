# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DhActivityType(models.Model):
    _name = 'dh.activity.type'
    _description = 'Dh Activity Type'
    _rec_name = 'name'

    name = fields.Char(string="Name", translate=True)

class DhScopeType(models.Model):
    _name = 'dh.scope.type'
    _description = 'Dh Scope Type'
    _rec_name = 'name'

    name = fields.Char(string="Name", translate=True)
    type_activity = fields.Selection(
        [('formation', 'دورة تدريبية'), ('soutien', 'دعم'), ('etude', 'دراسة'), ('conspiration', 'مؤتمر'),
         ('project', 'مشروع'), ('chaise', 'كرسي')], string='نوع النشاط')

class DhTasks(models.Model):
    _inherit = 'project.task'
    _description = 'Dh Tasks'

    name = fields.Char(string='Title', tracking=True, required=True, index=True, translate=True)
    activity_id = fields.Many2one('dh.activity.type', string='')
    activity_scope = fields.Many2one('dh.scope.type', string="Activity Scope")
    # activity_scope = fields.Char(string="Activity Scope")
    proposed_date = fields.Date(string="Proposed Date")
    is_budget_required = fields.Boolean('Budget Required ')
    amount_usd = fields.Float(string="Amount in USD", domain=[("is_budget_required", "=", True)])
    proposal_note = fields.Many2many("ir.attachment", string="Proposal / Concept note")
    remarks = fields.Char(translate=True,string="Remarks ")
    purpose = fields.Char(translate=True,string="Activity Purpose ")
    event_id = fields.Many2one('event.event', string='Event')

    def name_get(self):
        result = []
        for rec in self:

            name = rec.name
            if rec.sequence:
                name = " . ".join([str(rec.sequence), name])
            result.append((rec.id, name))
        return result

    @api.model
    def tasks_possible_search_read(self, **args):
        res = self.env['project.task'].sudo().search_read(domain=[(
            'project_id', '=', args['project'])], offset=args['offset'], limit=args['limit'], fields=args['fields'])
        return res

