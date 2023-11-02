# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from odoo.tools import float_round
from datetime import date, datetime
from ast import literal_eval
from odoo.exceptions import ValidationError
from odoo.http import content_disposition, request, route
from dateutil.relativedelta import relativedelta

class HrEmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    is_member_state = fields.Boolean(string='Is member state ?')

class DHHrEmployee(models.AbstractModel):
    _inherit = "hr.employee"

    is_expert = fields.Boolean('Expert')
    # Nombre de pays visités
    nb_pays_visited = fields.Integer('عدد البلدان التي تمت زيارتها')
    # Nombre des missions
    nb_missions = fields.Integer(compute='get_nb_mission', store=True, string='عدد المهام')
    # Montant total des dépenses
    total_montant = fields.Float('المبلغ الإجمالي للمصروفات')
    tasks_ids = fields.One2many("project.task", 'expert', string='projects')

    is_member_state = fields.Boolean(string='Is member state ?')

    resume_cv = fields.Boolean(string='cv')
    lettre_motivation = fields.Boolean(string='lettre')

    @api.depends('tasks_ids')
    def get_nb_mission(self):
        for rec in self:
            rec.nb_missions = len(rec.tasks_ids.filtered(lambda x:x.is_mission == True))
