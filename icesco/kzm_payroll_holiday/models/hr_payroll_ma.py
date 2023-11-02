# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, time, date

class HrPayrollMa(models.Model):
    _inherit = "hr.payroll_ma"

    def generate_employees(self):
        for rec in self:
            employee_non_res = []
            first_user = False
            remain_user_ids = []
            if len(self.env['res.users'].search(
                    [("groups_id", "=", self.env.ref("hr.group_hr_manager").id)])) > 0:
                first_user = self.env['res.users'].search(
                    [("groups_id", "=", self.env.ref("hr.group_hr_manager").id)])[0]

            for user in self.env['res.users'].search(
                    [("groups_id", "=", self.env.ref("hr.group_hr_manager").id)]):
                if user.id != first_user.id:
                    remain_user_ids.append(user.id)
            employee_non_res = []
            employee_obj = self.env['hr.employee']
            obj_contract = self.env['hr.contract']
            employees = employee_obj.search([('active', '=', True),('employee_externe', '=', False),
                                             ('date', '<=', rec.date_end),
                                             ('company_id', '=', rec.company_id.id),
                                             ])
            if rec.state == 'draft':
                sql = '''
                    DELETE from hr_payroll_ma_bulletin where id_payroll_ma = %s
                        '''
                self.env.cr.execute(sql, (rec.id,))

            for employee in employees:
                contract = obj_contract.search([('employee_id', '=', employee.id),
                                                ('state', 'in', ('pending', 'open'))], order='date_start', limit=1)

                # absences = '''  select sum(number_of_days)
                #                 from    hr_holidays h
                #                 left join hr_holidays_status s on (h.holiday_status_id=s.id)
                #                 where date_from >= '%s' and date_to <= '%s'
                #                 and employee_id = %s
                #                 and state = 'validate'
                #                 and s.payed=False''' % (rec.period_id.date_start, rec.period_id.date_end, employee.id)
                # self.env.cr.execute(absences)
                # res = self.env.cr.fetchone()
                # if res[0] is None:
                #     days = 0
                # else:
                #     days = res[0]

                absences = '''  select sum(number_of_days)
                                    from    hr_leave h
                                    left join hr_leave_type s on (h.holiday_status_id=s.id)
                                    where date_from >= '%s' and date_to <= '%s'
                                    and employee_id = %s
                                    and state = 'validate'
                                    and s.unpaid=True''' % (
                    rec.period_id.date_start, rec.period_id.date_end, employee.id)
                self.env.cr.execute(absences)
                res = self.env.cr.fetchone()
                if res[0] is None:
                    days = 0
                else:
                    days = res[0]

                if contract:
                    line = {
                        'employee_id': employee.id,
                        'employee_contract_id': contract.id,
                        'working_days': contract.working_days_per_month + days,
                        'normal_hours': contract.monthly_hour_number,
                        'hour_base': contract.hour_salary,
                        'salaire_base': contract.wage,
                        'id_payroll_ma': rec.id,
                        'period_id': rec.period_id.id,
                        'date_start': rec.date_start,
                        'date_end': rec.date_end,
                        'date_salary': rec.date_salary,
                        'taux_anciennete': employee.anciennete and self.env['hr.payroll_ma.bulletin'].calc_seniority(
                            employee.date, rec.date_end, type_employe=employee.type_employe, wk_days=0) or 0.0
                    }
                    bulletin = self.env['hr.payroll_ma.bulletin'].create(line)




                    if employee.non_resident == True and employee.date.year == date.today().year and employee.date.month == date.today().month:
                        self.env['mail.activity'].create({
                            'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                             'user_id': self.env['res.users'].search([('login', '=', 'rh@icesco.org')]).id,

                            'summary': 'Residence facilities allowance',
                            'note': 'The employee :  %s' % (employee.name +'/Matricule: ' + employee.matricule)+ ' must have a facility allowance',
                            'res_model_id': self.env['ir.model']._get('hr.payroll_ma.bulletin').id,
                            'res_id': bulletin.id
                        })

                        employee_non_res.append(employee)
            text = ''
            for employee in employee_non_res:
                char = '<p> - '+ employee.name + ' with matricule:' + str(employee.matricule)+'<p>'
                text = text + char


            self.env['mail.activity'].create({
                'activity_type_id': self.env.ref('mail.mail_activity_data_call').id,
                 'user_id': self.env['res.users'].search([('login', '=', 'rh@icesco.org')]).id,
                 # 'multiple_users': [(6, 0, remain_user_ids)],
                'summary': 'Residence facilities allowance',
                'note': '<p>The following employees must have a facility allowance:<p>%s' % (text),
                'res_model_id': self.env['ir.model']._get('hr.payroll_ma').id,
                'res_id': rec.id
                        })


        return True


class HrPayrollMaBulletin(models.Model):
    _inherit = "hr.payroll_ma.bulletin"

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        if self.env.context.get('period_id'):
            self.period_id = self.env.context.get('period_id')
        if self.env.context.get('date_start'):
            self.date_start = self.env.context.get('date_start')
        if self.env.context.get('date_end'):
            self.date_end = self.env.context.get('date_end')
        if not self.period_id:
            raise ValidationError(u"Vous devez d'abord spécifier une période !")
        if self.period_id and self.employee_id:
            if not self.employee_id.contract_id:
                return True
            else:
                sql = '''select sum(number_of_days) 
                            from    hr_leave h
                                    left join hr_leave_type s on (h.holiday_status_id=s.id)
                            where date_from >= '%s' and date_to <= '%s'
                                  and employee_id = %s
                                  and state = 'validate'
                                  and s.unpaid=True''' % (
                    self.period_id.date_start, self.period_id.date_end, self.employee_id.id)
                self.env.cr.execute(sql)
                res = self.env.cr.fetchone()
                if res[0] is None:
                    days = 0
                else:
                    days = res[0]
                self.employee_contract_id = self.employee_id.contract_id.id
                self.salaire_base = self.employee_id.contract_id.wage
                self.hour_base = self.employee_id.contract_id.hour_salary
                self.normal_hours = self.employee_id.contract_id.monthly_hour_number
                self.working_days = 26 - abs(days)
                self.period_id = self.period_id.id

class HrHolidaysStatus(models.Model):
    _inherit = "hr.leave.type"
    _description = 'Holidays'

    payed = fields.Boolean('Payed', required=False, default=False)
    is_urgent = fields.Boolean('Urgent', required=False, default=False)
    is_maternite = fields.Boolean(string='Est maternité?')
    is_maladie = fields.Boolean(string='Est maladie?')