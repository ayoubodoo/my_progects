# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectBeneficiaryCategory(models.Model):
    _name = 'project.beneficiary.category'
    _description = 'project_beneficiary_category'

    name = fields.Char(string='name')