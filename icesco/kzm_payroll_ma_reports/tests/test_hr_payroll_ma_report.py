# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase
from odoo import tools
from odoo.exceptions import ValidationError
from odoo.fields import Datetime, Date


class HrPayrollMaBulletinReports(TransactionCase):
    """ hr Payroll Ma Bulletin Reports """



    def setUp(self):
        super(HrPayrollMaBulletinReports, self).setUp()
        self.employee = self.env['hr.employee']
        self.company = self.env['res.company']
        self.contract = self.env['hr.contract']
        self.job = self.env['hr.job']
        self.contract_type = self.env['hr.contract.type']
        self.department = self.env['hr.department']
        self.cotisition = self.env['hr.payroll_ma.cotisation.type']
        self.hr_payroll_ma = self.env['hr.payroll_ma']
        self.hr_payroll_ma_bulletin = self.env['hr.payroll_ma.bulletin']
        self.date_range = self.env["date.range"]
        self.type = self.env["date.range.type"]
        self.rubrique = self.env["hr.payroll_ma.rubrique"]
        self.calendar = self.env['resource.calendar']
        self.journal = self.env['account.journal'].create({
            'name': 'Bank Test',
            'code': 'BNKT',
            'type': 'bank',
            'company_id': self.env.company.id,
        })

    def test__salaire_net_a_payer(self):
        contract_type = self.contract_type.create({'name': 'CDI'})
        job = self.job.create({'name': 'Responsable IT'})
        company = self.company.create({'name': 'Company', 'currency_id': self.env.ref('base.MAD').id, })
        department = self.department.create({'name': 'IT', })
        employee = self.employee.create({
            'name': 'Test',
            'work_phone': '	0121 12 33 29',
            'company_id': company.id,
            'address_home_id': self.env['res.partner'].create({'name': 'Test 2', 'type': 'private'}).id,

        })
        calendar = self.calendar.create({
            'name': 'Standard 40 hours/week',
            'hours_per_day': 8.0})

        reubrique1 = self.rubrique.create({
            'name': 'Indemnité de panier ou de casse-croute',
            'categorie': 'majoration',
            'company_id': company.id,
            'afficher': 'True',
            'type': 'indemnite',
            'anciennete': True,
            'absence': True,
            'sequence': 1,
        })
        reubrique2 = self.rubrique.create({
            'name': 'Indemnité de transport',
            'categorie': 'majoration',
            'company_id': company.id,
            'afficher': 'True',
            'type': 'indemnite',
            'anciennete': True,
            'absence': True,
            'sequence': 1,
        })

        cotisation = self.cotisition.create({
            'name': 'AMO + CNSS HALLIS',
            'company_id': company.id,
            'cotisation_ids': [(0, 0, {
                'code': 'Cnss',
                'name': 'CNSS',
                'tauxsalarial': 4.84,
                'tauxpatronal': 8.98,
                'plafonee': True,
                'plafond': 6000,
                # 'credit_account_id': 6000,
                'company_id': company.id,

            }), (0, 0, {
                'code': 'AllocFam',
                'name': 'Couverture des allocations familiales',
                'tauxsalarial': 0.0,
                'tauxpatronal': 6.40,
                'plafond': 0.0,
                # 'credit_account_id': 6000,
                'company_id': company.id,

            }), (0, 0, {
                'code': 'Amo',
                'name': 'AMO',
                'tauxsalarial': 2.26,
                'tauxpatronal': 2.26,
                'plafond': 0.0,
                # 'credit_account_id': 6000,
                'company_id': company.id,

            }), (0, 0, {
                'code': 'participationAMO',
                'name': 'Participation AMO',
                'tauxsalarial': 0.0,
                'tauxpatronal': 1.85,
                'plafond': 0.0,
                # 'credit_account_id': 6000,
                'company_id': company.id,

            }),

                               ],

        })

        contract = self.contract.create({
            'date_start': Date.to_date('2013-09-01'),
            # 'date_start': Date.to_date('2015-01-01'),
            'name': 'CONTRAT TEST',
            # 'resource_calendar_id': self.calendar_35h.id,
            'wage': 5321,
            'type_id': contract_type.id,
            'type': 'mensuel',
            'working_days_per_month': 26,
            'employee_id': employee.id,
            'state': 'open',
            'cotisation': cotisation.id,
            'job_id': job.id,
            'company_id': company.id,
            'department_id': department.id,
            'resource_calendar_id': calendar.id,
            'ir': True,
            'rubrique_ids': [(0, 0, {
                'rubrique_id': reubrique1.id,
                'montant': 550,
                'permanent': True,

            }), (0, 0, {
                'rubrique_id': reubrique2.id,
                'montant': 500,
                'permanent': True}
                 )],
        })
        print("Anciennete", employee.annees_anciennete)
        print("Taux Anciennete", employee.taux_anciennete)
        for reb in contract.rubrique_ids:
            print("rub", reb.montant)
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

        payroll_ma = self.hr_payroll_ma.create({
            "name": "Paie Hallis de la période 08/2020",
            "number": 'Salaire/00007',
            "date_salary": '2020-08-31',
            "period_id": dr.id,
            "journal_id": self.journal.id,
            "state": 'draft',

        })
        hr_payroll_ma_bulletin = self.hr_payroll_ma_bulletin.create({
            "date_start": payroll_ma.date_start,
            "date_end": payroll_ma.date_end,
            "employee_id": employee.id,
            "employee_contract_id": contract.id,
            "taux_anciennete": 10,

        })
        payroll_ma.onchange_period_id()
        self.assertEqual(dr.date_start, payroll_ma.date_start)
        self.assertEqual(dr.date_end, payroll_ma.date_end)
        for contract in employee.contract_ids:
            if contract.state == 'open':
                self.assertEqual(contract.name, 'CONTRAT TEST')
                break

        hr_payroll_ma_bulletin.onchange_employee_id()
        self.assertEqual(hr_payroll_ma_bulletin.working_days, 26)
        self.assertEqual(hr_payroll_ma_bulletin.cumul_work_days, 26)
        self.assertEqual(hr_payroll_ma_bulletin.salaire_base, 5321)
        self.assertEqual(hr_payroll_ma_bulletin.salaire_base_mois, 5321)
        self.assertEqual(hr_payroll_ma_bulletin.employee_contract_id.id, contract.id)

        hr_payroll_ma_bulletin.compute_all_lines()
        print(" ////////////////// salaire brute ", hr_payroll_ma_bulletin.salaire_brute)
        print(" ////////////////// salaire brute imposable ", hr_payroll_ma_bulletin.salaire_brute_imposable)
        print(" ////////////////// salaire net imposable ", hr_payroll_ma_bulletin.salaire_net_imposable)
        print(" ////////////////// cotisisation employee ", hr_payroll_ma_bulletin.cotisations_employee)
        print(" ////////////////// cotisisation employer ", hr_payroll_ma_bulletin.cotisations_employer)
        print(" ////////////////// salaire net ", hr_payroll_ma_bulletin.salaire_net)
        print(" ////////////////// igr", hr_payroll_ma_bulletin.igr)
        self.assertEqual(hr_payroll_ma_bulletin.salaire_brute, 5321)


    def test_periods_generation(self):
        company = self.company.create({'name': 'Company TE', 'currency_id': self.env.ref('base.MAD').id, })
        contract_type = self.contract_type.create({'name': 'CDI'})
        type2 = self.type.create(
            {"name": "Fiscal Period",
             "company_id": company.id,
             "allow_overlap": False,
             "active": True,
             "fiscal_year": True,
             }
        )

        dr = self.date_range.create(
            {
                "name": "Année fiscale",
                "date_start": "2030-01-01",
                "date_end": "2030-12-31",
                "active": True,
                "company_id": company.id,
                "type_id": type2.id,
            }
        )
        dr.create_period()
        self.assertEqual(str(dr.period_ids[0].date_start), '2030-01-01')
        # for period in dr.period_ids:
        #     print(period.date_start)
        employee1 = self.employee.create({
            'name': 'Employee Number1',
            'work_phone': '	0990 67 93 09',
            'company_id': self.env.company.id,
            'active': True,
            'address_home_id': self.env['res.partner'].create({'name': 'Address Number1', 'type': 'private'}).id,

        })
        employee2 = self.employee.create(
            {
                'name': 'Employee Number2',
                'work_phone': '	0990 67 93 09',
                'company_id': self.env.company.id,
                'active': True,
                'address_home_id': self.env['res.partner'].create({'name': 'Address Number2', 'type': 'private'}).id,

        })
        reubrique1 = self.rubrique.create({
            'name': 'Indemnité de panier ou de casse-croute',
            'categorie': 'majoration',
            'company_id': company.id,
            'afficher': 'True',
            'type': 'indemnite',
            'anciennete': True,
            'absence': True,
            'sequence': 1,
        })
        reubrique2 = self.rubrique.create({
            'name': 'Indemnité de transport',
            'categorie': 'majoration',
            'company_id': company.id,
            'afficher': 'True',
            'type': 'indemnite',
            'anciennete': True,
            'absence': True,
            'sequence': 1,
        })

        cotisation = self.cotisition.create({
            'name': 'AMO + CNSS HALLIS',
            'company_id': company.id,
            'cotisation_ids': [(0, 0, {
                'code': 'Cnss',
                'name': 'CNSS',
                'tauxsalarial': 4.84,
                'tauxpatronal': 8.98,
                'plafonee': True,
                'plafond': 6000,
                # 'credit_account_id': 6000,
                'company_id': company.id,

            }), (0, 0, {
                'code': 'AllocFam',
                'name': 'Couverture des allocations familiales',
                'tauxsalarial': 0.0,
                'tauxpatronal': 6.40,
                'plafond': 0.0,
                # 'credit_account_id': 6000,
                'company_id': company.id,

            }), (0, 0, {
                'code': 'Amo',
                'name': 'AMO',
                'tauxsalarial': 2.26,
                'tauxpatronal': 2.26,
                'plafond': 0.0,
                # 'credit_account_id': 6000,
                'company_id': company.id,

            }), (0, 0, {
                'code': 'participationAMO',
                'name': 'Participation AMO',
                'tauxsalarial': 0.0,
                'tauxpatronal': 1.85,
                'plafond': 0.0,
                # 'credit_account_id': 6000,
                'company_id': company.id,

            }),

                               ],

        })

        contract_employee1 = self.contract.create({
            'date_start': Date.to_date('2030-09-01'),
            # 'date_start': Date.to_date('2015-01-01'),
            'name': 'CONTRAT EMP 1',
            # 'resource_calendar_id': self.calendar_35h.id,
            'wage': 5321,
            'type_id': contract_type.id,
            'type': 'mensuel',
            'working_days_per_month': 26,
            'employee_id': employee1.id,
            'state': 'open',
            'cotisation': cotisation.id,
            # 'job_id': job.id,
            'company_id': company.id,
            # 'department_id': department.id,
            # 'resource_calendar_id': calendar.id,
            'ir': True,
            'rubrique_ids': [(0, 0, {
                'rubrique_id': reubrique1.id,
                'montant': 550,
                'permanent': True,

            }), (0, 0, {
                'rubrique_id': reubrique2.id,
                'montant': 500,
                'permanent': True}
                 )],
        })
        contract_employee2 = self.contract.create({
            'date_start': Date.to_date('2030-09-01'),
            # 'date_start': Date.to_date('2015-01-01'),
            'name': 'CONTRAT EMP 1',
            # 'resource_calendar_id': self.calendar_35h.id,
            'wage': 5321,
            'type_id': contract_type.id,
            'type': 'mensuel',
            'working_days_per_month': 26,
            'employee_id': employee2.id,
            'state': 'open',
            'cotisation': cotisation.id,
            # 'job_id': job.id,
            'company_id': company.id,
            # 'department_id': department.id,
            # 'resource_calendar_id': calendar.id,
            'ir': True,
            'rubrique_ids': [(0, 0, {
                'rubrique_id': reubrique1.id,
                'montant': 550,
                'permanent': True,

            }), (0, 0, {
                'rubrique_id': reubrique2.id,
                'montant': 500,
                'permanent': True}
                 )],
        })

        payroll_ma = self.hr_payroll_ma.create({
            "name": "Paie Hallis de la période 08/2030",
            "number": 'Salaire/00009',
            "date_salary": '2030-08-31',
            "period_id": dr.id,
            "journal_id": self.journal.id,
            "state": 'draft',
        })
        payroll_ma.onchange_period_id()
        # generate employees
        payroll_ma.generate_employees()

        for emp in payroll_ma.bulletin_line_ids:
            print("emp",emp.employee_id.name)
            # print("working days",emp.employee_id.working_days)
            # print("working days",emp.employee_id.normal_hours)
            # print("working days",emp.employee_id.salaire_brute)
            # print("working days",emp.employee_id.salaire_brute_imposable)

        # payroll_ma.compute_all_lines()

