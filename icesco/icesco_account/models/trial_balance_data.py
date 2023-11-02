# © 2016 Julien Coux (Camptocamp)
# © 2018 Forest and Biomass Romania SA
# Copyright 2020 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, models


class TrialBalanceReport(models.AbstractModel):
    _inherit = "report.account_financial_report.trial_balance"

    @api.model
    def _compute_account_amount(
            self, total_amount, tb_initial_acc, tb_period_acc, foreign_currency
    ):
        for tb in tb_period_acc:
            acc_id = tb["account_id"][0]
            total_amount[acc_id] = {}
            total_amount[acc_id]["credit"] = tb["credit"]
            total_amount[acc_id]["debit"] = tb["debit"]
            total_amount[acc_id]["balance"] = tb["balance"]
            total_amount[acc_id]["initial_balance"] = 0.0
            total_amount[acc_id]["total"] = tb["total"]
            total_amount[acc_id]["ending_balance"] = tb["balance"]
            if foreign_currency:
                total_amount[acc_id]["initial_currency_balance"] = 0.0
                total_amount[acc_id]["ending_currency_balance"] = round(
                    tb["amount_currency"], 2
                )
        for tb in tb_initial_acc:
            acc_id = tb["account_id"]
            if acc_id not in total_amount.keys():
                total_amount[acc_id] = {}
                total_amount[acc_id]["credit"] = 0.0
                total_amount[acc_id]["debit"] = 0.0
                total_amount[acc_id]["balance"] = 0.0
                total_amount[acc_id]["initial_balance"] = tb["balance"]
                total_amount[acc_id]["ending_balance"] = tb["balance"]
                total_amount[acc_id]["total"] = tb["total"]
                if foreign_currency:
                    total_amount[acc_id]["initial_currency_balance"] = round(
                        tb["amount_currency"], 2
                    )
                    total_amount[acc_id]["ending_currency_balance"] = round(
                        tb["amount_currency"], 2
                    )
            else:
                total_amount[acc_id]["initial_balance"] = tb["balance"]
                total_amount[acc_id]["ending_balance"] += tb["balance"]
                total_amount[acc_id]["ending_balance"] += tb["total"]

                if foreign_currency:
                    total_amount[acc_id]["initial_currency_balance"] = round(
                        tb["amount_currency"], 2
                    )
                    total_amount[acc_id]["ending_currency_balance"] += round(
                        tb["amount_currency"], 2
                    )
        return total_amount

    @api.model
    def _compute_partner_amount(
            self, total_amount, tb_initial_prt, tb_period_prt, foreign_currency
    ):
        partners_ids = set()
        partners_data = {}
        for tb in tb_period_prt:
            acc_id = tb["account_id"][0]
            if tb["partner_id"]:
                prt_id = tb["partner_id"][0]
                if tb["partner_id"] not in partners_ids:
                    partners_data.update(
                        {prt_id: {"id": prt_id, "name": tb["partner_id"][1]}}
                    )
                total_amount[acc_id][prt_id] = {}
                total_amount[acc_id][prt_id]["credit"] = tb["credit"]
                total_amount[acc_id][prt_id]["debit"] = tb["debit"]
                total_amount[acc_id][prt_id]["balance"] = tb["balance"]
                total_amount[acc_id][prt_id]["total"] = tb["total"]
                total_amount[acc_id][prt_id]["initial_balance"] = 0.0
                total_amount[acc_id][prt_id]["ending_balance"] = tb["balance"]
                if foreign_currency:
                    total_amount[acc_id][prt_id]["initial_currency_balance"] = 0.0
                    total_amount[acc_id][prt_id]["ending_currency_balance"] = round(
                        tb["amount_currency"], 2
                    )
                    partners_ids.add(tb["partner_id"])
        for tb in tb_initial_prt:
            acc_id = tb["account_id"][0]
            if tb["partner_id"]:
                prt_id = tb["partner_id"][0]
                if tb["partner_id"] not in partners_ids:
                    partners_data.update(
                        {prt_id: {"id": prt_id, "name": tb["partner_id"][1]}}
                    )
                if acc_id not in total_amount.keys():
                    total_amount = self._compute_acc_prt_amount(
                        total_amount, tb, acc_id, prt_id, foreign_currency
                    )
                    partners_ids.add(tb["partner_id"])
                elif prt_id not in total_amount[acc_id].keys():
                    total_amount = self._compute_acc_prt_amount(
                        total_amount, tb, acc_id, prt_id, foreign_currency
                    )
                    partners_ids.add(tb["partner_id"])
                else:
                    total_amount[acc_id][prt_id]["initial_balance"] += tb["balance"]
                    total_amount[acc_id][prt_id]["ending_balance"] += tb["balance"]
                    if foreign_currency:
                        total_amount[acc_id][prt_id][
                            "initial_currency_balance"
                        ] += round(tb["amount_currency"], 2)
                        total_amount[acc_id][prt_id][
                            "ending_currency_balance"
                        ] += round(tb["amount_currency"], 2)
        return total_amount, partners_data

    @api.model
    def _get_data(
        self,
        account_ids,
        journal_ids,
        partner_ids,
        company_id,
        date_to,
        date_from,
        foreign_currency,
        only_posted_moves,
        show_partner_details,
        hide_account_at_0,
        unaffected_earnings_account,
        fy_start_date,
    ):
        accounts_domain = [("company_id", "=", company_id)]
        if account_ids:
            accounts_domain += [("id", "in", account_ids)]
        accounts = self.env["account.account"].search(accounts_domain)
        tb_initial_acc = []
        for account in accounts:
            tb_initial_acc.append(
                {"account_id": account.id, "balance": 0.0, "amount_currency": 0.0,"total":0.0}
            )
        initial_domain_bs = self._get_initial_balances_bs_ml_domain(
            account_ids,
            journal_ids,
            partner_ids,
            company_id,
            date_from,
            only_posted_moves,
            show_partner_details,
        )
        tb_initial_acc_bs = self.env["account.move.line"].read_group(
            domain=initial_domain_bs,
            fields=["account_id", "balance", "amount_currency","total"],
            groupby=["account_id"],
        )
        initial_domain_pl = self._get_initial_balances_pl_ml_domain(
            account_ids,
            journal_ids,
            partner_ids,
            company_id,
            date_from,
            only_posted_moves,
            show_partner_details,
            fy_start_date,
        )
        tb_initial_acc_pl = self.env["account.move.line"].read_group(
            domain=initial_domain_pl,
            fields=["account_id", "balance", "amount_currency","total"],
            groupby=["account_id"],
        )

        tb_initial_acc_rg = tb_initial_acc_bs + tb_initial_acc_pl
        for account_rg in tb_initial_acc_rg:
            element = list(
                filter(
                    lambda acc_dict: acc_dict["account_id"]
                    == account_rg["account_id"][0],
                    tb_initial_acc,
                )
            )
            if element:
                element[0]["balance"] += account_rg["balance"]
                element[0]["total"] += account_rg["total"]
                element[0]["amount_currency"] += account_rg["amount_currency"]
        if hide_account_at_0:
            tb_initial_acc = [p for p in tb_initial_acc if p["balance"] != 0]

        period_domain = self._get_period_ml_domain(
            account_ids,
            journal_ids,
            partner_ids,
            company_id,
            date_to,
            date_from,
            only_posted_moves,
            show_partner_details,
        )
        tb_period_acc = self.env["account.move.line"].read_group(
            domain=period_domain,
            fields=["account_id", "debit", "credit", "balance", "amount_currency","total"],
            groupby=["account_id"],
        )

        if show_partner_details:
            tb_initial_prt_bs = self.env["account.move.line"].read_group(
                domain=initial_domain_bs,
                fields=["account_id", "partner_id", "balance", "amount_currency","total"],
                groupby=["account_id", "partner_id"],
                lazy=False,
            )
            tb_initial_prt_pl = self.env["account.move.line"].read_group(
                domain=initial_domain_pl,
                fields=["account_id", "partner_id", "balance", "amount_currency","total"],
                groupby=["account_id", "partner_id"],
            )
            tb_initial_prt = tb_initial_prt_bs + tb_initial_prt_pl
            if hide_account_at_0:
                tb_initial_prt = [p for p in tb_initial_prt if p["balance"] != 0]
            tb_period_prt = self.env["account.move.line"].read_group(
                domain=period_domain,
                fields=[
                    "account_id",
                    "partner_id",
                    "debit",
                    "credit",
                    "balance",
                    "amount_currency",
                    "total",
                ],
                groupby=["account_id", "partner_id"],
                lazy=False,
            )

        total_amount = {}

        partners_data = []
        total_amount = self._compute_account_amount(
            total_amount, tb_initial_acc, tb_period_acc, foreign_currency
        )
        if show_partner_details:
            total_amount, partners_data = self._compute_partner_amount(
                total_amount, tb_initial_prt, tb_period_prt, foreign_currency
            )
        accounts_ids = list(total_amount.keys())
        unaffected_id = unaffected_earnings_account
        #total_amount[unaffected_id]['test'] = 100
        if unaffected_id not in accounts_ids:
            accounts_ids.append(unaffected_id)
            total_amount[unaffected_id] = {}
            total_amount[unaffected_id]["initial_balance"] = 0.0
            total_amount[unaffected_id]["balance"] = 0.0
            total_amount[unaffected_id]["credit"] = 0.0
            total_amount[unaffected_id]["debit"] = 0.0
            total_amount[unaffected_id]["ending_balance"] = 0.0
            total_amount[unaffected_id]["total"] = 0.0
            if foreign_currency:
                total_amount[unaffected_id]["initial_currency_balance"] = 0.0
                total_amount[unaffected_id]["ending_currency_balance"] = 0.0
        accounts_data = self._get_accounts_data(accounts_ids)
        pl_initial_balance, pl_initial_currency_balance = self._get_pl_initial_balance(
            account_ids,
            journal_ids,
            partner_ids,
            company_id,
            fy_start_date,
            only_posted_moves,
            show_partner_details,
            foreign_currency,
        )

        total_amount[unaffected_id]["ending_balance"] += pl_initial_balance
        total_amount[unaffected_id]["initial_balance"] += pl_initial_balance
        if foreign_currency:
            total_amount[unaffected_id][
                "ending_currency_balance"
            ] += pl_initial_currency_balance
            total_amount[unaffected_id][
                "initial_currency_balance"
            ] += pl_initial_currency_balance
        return total_amount, accounts_data, partners_data

    def _get_hierarchy_groups(
            self, group_ids, groups_data, old_groups_ids, foreign_currency
    ):
        new_parents = False
        for group_id in group_ids:
            if groups_data[group_id]["parent_id"]:
                new_parents = True
                nw_id = groups_data[group_id]["parent_id"]
                if nw_id in groups_data.keys():
                    groups_data[nw_id]["initial_balance"] += groups_data[group_id][
                        "initial_balance"
                    ]
                    groups_data[nw_id]["debit"] += groups_data[group_id]["debit"]
                    groups_data[nw_id]["credit"] += groups_data[group_id]["credit"]
                    groups_data[nw_id]["balance"] += groups_data[group_id]["balance"]
                    #groups_data[nw_id]["test"] =6
                    groups_data[nw_id]["ending_balance"] += groups_data[group_id][
                        "ending_balance"
                    ]
                    if foreign_currency:
                        groups_data[nw_id]["initial_currency_balance"] += groups_data[
                            group_id
                        ]["initial_currency_balance"]
                        groups_data[nw_id]["ending_currency_balance"] += groups_data[
                            group_id
                        ]["ending_currency_balance"]
                else:
                    groups_data[nw_id] = {}
                    groups_data[nw_id]["initial_balance"] = groups_data[group_id][
                        "initial_balance"
                    ]
                    groups_data[nw_id]["debit"] = groups_data[group_id]["debit"]
                    groups_data[nw_id]["credit"] = groups_data[group_id]["credit"]
                    groups_data[nw_id]["balance"] = groups_data[group_id]["balance"]
                    groups_data[nw_id]["ending_balance"] = groups_data[group_id][
                        "ending_balance"
                    ]
                    if foreign_currency:
                        groups_data[nw_id]["initial_currency_balance"] = groups_data[
                            group_id
                        ]["initial_currency_balance"]
                        groups_data[nw_id]["ending_currency_balance"] = groups_data[
                            group_id
                        ]["ending_currency_balance"]
        if new_parents:
            nw_groups_ids = []
            for group_id in list(groups_data.keys()):
                if group_id not in old_groups_ids:
                    nw_groups_ids.append(group_id)
                    old_groups_ids.append(group_id)
            groups = self.env["account.group"].browse(nw_groups_ids)
            for group in groups:
                groups_data[group.id].update(
                    {
                        "id": group.id,
                        "code": group.code_prefix,
                        "name": group.name,
                        "parent_id": group.parent_id.id,
                        "parent_path": group.parent_path,
                        "complete_code": group.complete_code,
                        "account_ids": group.compute_account_ids.ids,
                        "type": "group_type",
                    }
                )
            groups_data = self._get_hierarchy_groups(
                nw_groups_ids, groups_data, old_groups_ids, foreign_currency
            )
        return groups_data


    def _get_report_values(self, docids, data):
        show_partner_details = data["show_partner_details"]
        wizard_id = data["wizard_id"]
        company = self.env["res.company"].browse(data["company_id"])
        company_id = data["company_id"]
        partner_ids = data["partner_ids"]
        journal_ids = data["journal_ids"]
        account_ids = data["account_ids"]
        date_to = data["date_to"]
        date_from = data["date_from"]
        hide_account_at_0 = data["hide_account_at_0"]
        hierarchy_on = data["hierarchy_on"]
        show_hierarchy_level = data["show_hierarchy_level"]
        foreign_currency = data["foreign_currency"]
        only_posted_moves = data["only_posted_moves"]
        unaffected_earnings_account = data["unaffected_earnings_account"]
        fy_start_date = data["fy_start_date"]
        total_amount, accounts_data, partners_data = self._get_data(
            account_ids,
            journal_ids,
            partner_ids,
            company_id,
            date_to,
            date_from,
            foreign_currency,
            only_posted_moves,
            show_partner_details,
            hide_account_at_0,
            unaffected_earnings_account,
            fy_start_date,
        )
        trial_balance = []
        if not show_partner_details:
            for account_id in accounts_data.keys():
                accounts_data[account_id].update(
                    {
                        "initial_balance": total_amount[account_id]["initial_balance"],
                        "credit": total_amount[account_id]["credit"],
                        "debit": total_amount[account_id]["debit"],
                        "balance": total_amount[account_id]["balance"],
                        "ending_balance": total_amount[account_id]["ending_balance"],
                        "total_test": total_amount[account_id]["total"],
                        "type": "account_type",
                    }
                )
                if foreign_currency:
                    accounts_data[account_id].update(
                        {
                            "ending_currency_balance": total_amount[account_id][
                                "ending_currency_balance"
                            ],
                            "initial_currency_balance": total_amount[account_id][
                                "initial_currency_balance"
                            ],
                        }
                    )
            if hierarchy_on == "relation":
                groups_data = self._get_groups_data(
                    accounts_data, total_amount, foreign_currency
                )
                trial_balance = list(groups_data.values())
                trial_balance += list(accounts_data.values())
                trial_balance = sorted(trial_balance, key=lambda k: k["complete_code"])
                for trial in trial_balance:
                    counter = trial["complete_code"].count("/")
                    trial["level"] = counter
            if hierarchy_on == "computed":
                groups_data = self._get_computed_groups_data(
                    accounts_data, total_amount, foreign_currency
                )
                trial_balance = list(groups_data.values())
                trial_balance += list(accounts_data.values())
                trial_balance = sorted(trial_balance, key=lambda k: k["code"])
            if hierarchy_on == "none":
                trial_balance = list(accounts_data.values())
                trial_balance = sorted(trial_balance, key=lambda k: k["code"])
        else:
            if foreign_currency:
                for account_id in accounts_data.keys():
                    total_amount[account_id]["currency_id"] = accounts_data[account_id][
                        "currency_id"
                    ]
                    total_amount[account_id]["currency_name"] = accounts_data[
                        account_id
                    ]["currency_name"]
        return {
            "doc_ids": [wizard_id],
            "doc_model": "trial.balance.report.wizard",
            "docs": self.env["trial.balance.report.wizard"].browse(wizard_id),
            "foreign_currency": data["foreign_currency"],
            "company_name": company.display_name,
            "company_currency": company.currency_id,
            "currency_name": company.currency_id.name,
            "date_from": data["date_from"],
            "date_to": data["date_to"],
            "only_posted_moves": data["only_posted_moves"],
            "hide_account_at_0": data["hide_account_at_0"],
            "show_partner_details": data["show_partner_details"],
            "limit_hierarchy_level": data["limit_hierarchy_level"],
            "hierarchy_on": hierarchy_on,
            "trial_balance": trial_balance,
            "total_amount": total_amount,
            "accounts_data": accounts_data,
            "partners_data": partners_data,
            "show_hierarchy_level": show_hierarchy_level,
        }
