
from odoo import _, models


class TrialBalanceXslx(models.AbstractModel):
    _inherit = "report.a_f_r.report_trial_balance_xlsx"

    def _get_report_columns(self, report):
        if not report.show_partner_details:
            res = {
                0: {"header": _("Code"), "field": "code", "width": 10},
                1: {"header": _("Account"), "field": "name", "width": 60},
                2: {
                    "header": _("Initial balance"),
                    "field": "initial_balance",
                    "type": "amount",
                    "width": 14,
                },
                3: {
                    "header": _("Debit"),
                    "field": "debit",
                    "type": "amount",
                    "width": 14,
                },
                4: {
                    "header": _("Credit"),
                    "field": "credit",
                    "type": "amount",
                    "width": 14,
                },
                5: {
                    "header": _("Period balance"),
                    "field": "balance",
                    "type": "amount",
                    "width": 14,
                },
                6: {
                    "header": _("Ending balance"),
                    "field": "ending_balance",
                    "type": "amount",
                    "width": 14,
                },
                7: {
                    "header": _("Total"),
                    "field": "total_test",
                    "type": "amount",
                    "width": 14,
                },
            }
            if report.foreign_currency:
                foreign_currency = {
                    7: {
                        "header": _("Cur."),
                        "field": "currency_id",
                        "field_currency_balance": "currency_id",
                        "type": "many2one",
                        "width": 7,
                    },
                    8: {
                        "header": _("Initial balance"),
                        "field": "initial_currency_balance",
                        "type": "amount_currency",
                        "width": 14,
                    },
                    9: {
                        "header": _("Ending balance"),
                        "field": "ending_currency_balance",
                        "type": "amount_currency",
                        "width": 14,
                    },
                    10: {
                        "header": _("Tolal2"),
                        "field": "total",
                        "type": "ending_balance",
                        "width": 14,
                    },
                }
                res = {**res, **foreign_currency}
            return res
        else:
            res = {
                0: {"header": _("Partner"), "field": "name", "width": 70},
                1: {
                    "header": _("Initial balance"),
                    "field": "initial_balance",
                    "type": "amount",
                    "width": 14,
                },
                2: {
                    "header": _("Debit"),
                    "field": "debit",
                    "type": "amount",
                    "width": 14,
                },
                3: {
                    "header": _("Credit"),
                    "field": "credit",
                    "type": "amount",
                    "width": 14,
                },
                4: {
                    "header": _("Period balance"),
                    "field": "balance",
                    "type": "amount",
                    "width": 14,
                },
                5: {
                    "header": _("Ending balance"),
                    "field": "ending_balance",
                    "type": "amount",
                    "width": 14,
                },
                6: {
                    "header": _("Tolal3"),
                    "field": "total",
                    "type": "ending_balance",
                    "width": 14,
                },
                7: {
                    "header": _("Tolal4"),
                    "field": "total",
                    "type": "ending_balance",
                    "width": 14,
                },
            }
            if report.foreign_currency:
                foreign_currency = {
                    6: {
                        "header": _("Cur."),
                        "field": "currency_id",
                        "field_currency_balance": "currency_id",
                        "type": "many2one",
                        "width": 7,
                    },
                    7: {
                        "header": _("Initial balance"),
                        "field": "initial_currency_balance",
                        "type": "amount_currency",
                        "width": 14,
                    },
                    8: {
                        "header": _("Ending balance"),
                        "field": "ending_currency_balance",
                        "type": "amount_currency",
                        "width": 14,
                    },
                    9: {
                        "header": _("Tolal6"),
                        "field": "total",
                        "type": "ending_balance",
                        "width": 14,
                    },
                }
                res = {**res, **foreign_currency}
            return res
