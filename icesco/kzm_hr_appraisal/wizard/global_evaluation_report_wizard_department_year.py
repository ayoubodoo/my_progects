from odoo import api, fields, models
from itertools import groupby
from collections import Counter


class ReportDepartmentEvaluationWizard(models.TransientModel):
    _name = 'appraisal.report.department.wizard'
    _description = 'Appraisal Report Department Evaluation'

    start_date = fields.Date("Start Date", default=fields.Date.from_string(
        str(fields.Date.today().year) + '-01-01'))
    end_date = fields.Date("End Date", default=fields.Date.from_string(
        str(fields.Date.today().year) + '-12-31'))
    model_evaluation_id = fields.Many2one('appraisal.model', string="Model")

    def return_axes(self):
        return self.model_evaluation_id.factor_ids.mapped('axe_id')

    def return_len_axes(self):
        return len(self.model_evaluation_id.factor_ids.mapped('axe_id'))

    def set_data_report(self):
        grouped_evaluations = groupby(
            sorted(self.env['appraisal.appraisal'].search(
                [('model_evaluation_id', '=', self.model_evaluation_id.id),
                 ('evaluation_date', '>=', self.start_date), # ('evaluator_id','=',self.env.user.id)
                 ('evaluation_date', '<=', self.end_date)]).filtered(lambda x: x.department_id.id == self.env.user.employee_id.department_id.id),
                key=lambda m: m.employee_id.department_id),
            key=lambda d: d.department_id)

        l = []
        total = 0

        axis_ids = self.model_evaluation_id.factor_ids.mapped('axe_id')
        counter = {axe.id: 0 for axe in axis_ids}
        for k, v in grouped_evaluations:
            li = []
            lens = 0
            for evaluation in v:
                lens += 1
                d = {axe.id: 0 for axe in axis_ids}
                for line in evaluation.appraisal_line_ids:
                    d[line.axe_id.id] += line.note_id.name
                training_action_comment = ""
                area_comment = ""
                for comment in evaluation.appraisal_comment_ids:
                    if comment.evaluation_axe_id.is_training_action:
                        training_action_comment = comment.evaluator_comment
                    else:
                        area_comment = comment.evaluator_comment
                counter = dict(Counter(counter) + Counter(d))
                li.append([evaluation, d, training_action_comment, area_comment,
                           sum(d.values())])
                total += sum(d.values())
            l.append([k, li, lens])
        di = {axe.id: 0 for axe in axis_ids}
        for key, value in counter.items():
            di[key] = value
        return [l, di, total]

    def action_print_model(self):
        return self.env.ref(
            'kzm_hr_appraisal.report_department_this_year_evaluation_menu_id').report_action(self)
