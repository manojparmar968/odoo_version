# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ticket_price = fields.Float(string="Ticket Price", config_parameter='cinema_management.ticket_price')