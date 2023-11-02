# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase
from odoo import tools
from odoo.exceptions import ValidationError
from odoo.fields import Datetime, Date


class PayrollMaTest(TransactionCase):
    """ HR Payroll ma test"""

    def setUp(self):
        super(PayrollMaTest, self).setUp()
        self.date_range = self.env["date.range"]
        self.hr_payroll_ma = self.env['hr.payroll_ma']
        self.type = self.env["date.range.type"].create(
            {"name": "Fiscal year", "company_id": False, "allow_overlap": False}
        )
        self.journal = self.env['account.journal'].create({
            'name': 'Bank Test',
            'code': 'BNKT',
            'type': 'bank',
            'company_id': self.env.company.id,
        })

    def test_check_unicity_periode(self):
        dr = self.date_range.create(
            {
                "name": "FS2016",
                "date_start": "2015-01-01",
                "date_end": "2016-12-31",
                "type_id": self.type.id,
            }
        )

        payroll_ma_1 = self.hr_payroll_ma.create({
            "name": "PayRollS11111",
            "period_id": dr.id,
            "journal_id": self.journal.id,
        })
        with self.assertRaises(ValidationError) as cm:
            self.hr_payroll_ma.create(
                {
                    "name": "PayRollS222222",
                    "period_id": dr.id,
                    "journal_id": self.journal.id,
                }
            )
        self.assertEqual(
            cm.exception.name, "On ne peut pas avoir deux paies pour la même période !"
        )

    def test_unlink(self):
        dr = self.date_range.create(
            {
                "name": "FS2016",
                "date_start": "2015-01-01",
                "date_end": "2016-12-31",
                "type_id": self.type.id,
            }
        )
        payroll_ma = self.hr_payroll_ma.create({
            "name": "PayRoll",
            "period_id": dr.id,
            "journal_id": self.journal.id,
            "state": 'confirmed',
        })
        with self.assertRaises(ValidationError) as cm:
            payroll_ma.unlink()
        self.assertEqual(
            cm.exception.name, "Suppression impossible"
        )


    def test_dates_name(self):
        dr = self.date_range.create(
            {
                "name": "FS2016",
                "date_start": "2015-01-01",
                "date_end": "2016-12-31",
                "type_id": self.type.id,
            }
        )

        payroll_ma = self.hr_payroll_ma.create({
            "name": "PayRoll",
            "period_id": dr.id,
            "journal_id": self.journal.id,
            "state": 'confirmed',
        })
        payroll_ma.onchange_period_id()
        self.assertEqual(dr.date_start, payroll_ma.date_start)
        self.assertEqual(dr.date_end, payroll_ma.date_end)


class HrPayrollMaBulletin(TransactionCase):
    """ hr Payroll Ma Bulletin """

    def setUp(self):
        super(HrPayrollMaBulletin, self).setUp()
        print("llllllllllllllll")
        self.employee = self.env['hr.employee']
        self.company = self.env['res.company']
        self.contract = self.env['hr.contract']
        self.job = self.env['hr.job']
        self.contract_type = self.env['hr.contract.type']
        self.department = self.env['hr.department']
        self.calendar = self.env['resource.calendar']
        self.cotisition = self.env['hr.payroll_ma.cotisation.type']
        self.hr_payroll_ma = self.env['hr.payroll_ma']
        self.date_range = self.env["date.range"]
        self.type = self.env["date.range.type"]
        print("llllllllllllllll")
        self.journal = self.env['account.journal'].create({
            'name': 'Bank Test',
            'code': 'BNKT',
            'type': 'bank',
            'company_id': self.env.company.id,
        })

    def test__salaire_net_a_payer(self):
        print("1")
        contract_type = self.contract_type.create({'name': 'CDI'})
        job = self.job.create({'name': 'Responsable IT'})
        company = self.company.create({'name': 'Hallis','currency_id': self.env.ref('base.MAD').id,})
        department = self.department.create({'name': 'IT',})
        employee = self.employee.create({
            'name': 'Boulahya Meryem',
            'work_phone': '	0990 67 93 09',
            'company_id': company.id,
            'address_home_id': self.env['res.partner'].create({'name': 'Boulahya Meryem', 'type': 'private'}).id,

        })
        print("2")
        calendar=self.calendar.create({
            'name': 'Standard 40 hours/week',
            'hours_per_day': 8.0})
        contract = self.contract.create({
            'date_start': Date.to_date('2013-09-01'),
            'name': 'CONTRAT MERYEM BOULAHYA',
            'wage': 5321,
            'type_id': contract_type.id,
            'type': 'mensuel',
            'working_days_per_month': 26,
            'employee_id': employee.id,
            'state': 'open',
            'job_id': job.id,
            'company_id': company.id,
            'department_id': department.id,
            'resource_calendar_id': calendar.id,
        })
        print("3")
        type = self.type.create(
            {"name": "Fiscal Period",
             "company_id": False,
             "allow_overlap": False,
             "active": True,
             "fiscal_period": True,
             }
        )
        dr = self.date_range.create(
            {
                "name": "	08/2020",
                "date_start": "2020-08-01",
                "date_end": "2020-08-31",
                "type_id": type.id,
                "active": True,
            }
        )
        print("4")

        payroll_ma = self.hr_payroll_ma.create({
            "name": "Paie Hallis de la période 08/2020",
            "number": 'Salaire/00007',
            "date_salary": '2020-08-31',
            "period_id": dr.id,
            "journal_id": self.journal.id,
            "state": 'draft',


        })
        payroll_ma.onchange_period_id()

        self.assertEqual(dr.date_start, payroll_ma.date_start)
        self.assertEqual(dr.date_end, payroll_ma.date_end)

        for contract in employee.contract_ids:
            if contract.state == 'open':
                self.assertEqual(contract.name, 'CONTRAT MERYEM BOULAHYA')
                break
        payroll_ma.compute_all_lines()


