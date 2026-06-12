from odoo import api, fields, models, _
from odoo import osv
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
from datetime import timedelta


class PurchaseOrder(models.Model):
    _inherit =  "purchase.order"