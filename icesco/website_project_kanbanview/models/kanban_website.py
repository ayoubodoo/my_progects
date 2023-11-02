# -*- coding: utf-8 -*-
###############################################################################
#
#   Copyright (C) 2004-today OpenERP SA (<http://www.openerp.com>)
#   Copyright (C) 2016-today Geminate Consultancy Services (<http://geminatecs.com>).
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from odoo import api, fields, models
from odoo.exceptions import ValidationError



class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    tasks_page_count=fields.Integer(string="Kanban set per page for website task")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        conf = self.env['ir.config_parameter']
        res.update({'tasks_page_count': int(conf.get_param('website_project_kanbanview.tasks_page_count'))})
        return res

    # @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        conf = self.env['ir.config_parameter']
        conf.set_param('website_project_kanbanview.tasks_page_count', str(self.tasks_page_count))

    @api.constrains('tasks_page_count')
    def check_range(self):
        for rec in self:
            if rec.tasks_page_count == 0:
                raise ValidationError("Please keep 'Task per page in kanbanview' greater than 0!")

class ProjectType(models.Model):
    _inherit = 'project.task.type'

    def project_states(self,states_list):
        seq_list = []
        for state in states_list:
            seq_list.append(state.sequence)

        state_list = []
        if seq_list:
            for seq in sorted(seq_list):
                for sta in states_list:
                    if sta.sequence == seq:
                        state_list.append(sta)
        
        return state_list
