# # -*- coding: utf-8 -*-
import base64
from odoo.tools.float_utils import float_compare
from odoo import models, fields, api, exceptions, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import date, datetime, timedelta
from odoo.exceptions import UserError, ValidationError
import json
from dateutil.relativedelta import relativedelta
from odoo.addons.resource.models.resource_mixin import timezone_datetime
from collections import defaultdict
from pytz import timezone, UTC


class Dhresbank(models.Model):
    _inherit = 'res.bank'


    acn = fields.Char(string="A/C N°")
    bic = fields.Char('SWIFT', index=True, help="Sometimes called BIC or Swift.")


