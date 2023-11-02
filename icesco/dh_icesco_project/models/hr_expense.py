# -*- coding: utf-8 -*-
from odoo import models, fields, api
import json
from odoo.exceptions import ValidationError

class DHHrExpense(models.Model):
    _inherit = 'hr.expense'

    @api.model
    def create(self, vals):
        res = res = super(DHHrExpense, self).create(vals)
        if 'unit_amount' in vals or 'quantity' in vals or 'task_id' in vals:
            if res.task_id.id != False and res.task_id.is_mission == True:
                if res.task_id.sector_id.id != False:
                    res.task_id.sector_id.compute_expense_mission()
        return res

    def write(self, vals):
        res = super(DHHrExpense, self).write(vals)
        if 'unit_amount' in vals or 'quantity' in vals or 'task_id' in vals:
            if self.task_id.id != False and self.task_id.is_mission == True:
                if self.task_id.sector_id.id != False:
                    self.task_id.sector_id.compute_expense_mission()
        return res

    @api.constrains('task_id')
    def check_project(self):
        for rec in self:
            if rec.task_id.is_mission == True and rec.task_id.state2 != 'valide':
                raise ValidationError("la mission n'est pas encore valider.")