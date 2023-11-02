from odoo import api, fields, models


class ProjectStatus(models.Model):
    _name = "project.status"
    _order = "status_sequence"
    _description = "Project Status"


    name = fields.Char(string="Name", required=True, translate=True)
    description = fields.Char(string="Description", translate=True)
    status_sequence = fields.Integer(string="Sequence")
    is_closed = fields.Boolean(
        string="Is Closed Status", help="Specify if this is a closing status."
    )
    fold = fields.Boolean(string="Folded")
    state = fields.Selection(
        [('initial', 'Initial Stage'), ('in_progress', 'In progress'),
         ('executed', 'Executed')], string="State", default='initial')

    @api.model
    def create(self, vals):
        seq = self.env["ir.sequence"].next_by_code("project.status") or 0
        vals["status_sequence"] = seq
        return super(ProjectStatus, self).create(vals)
