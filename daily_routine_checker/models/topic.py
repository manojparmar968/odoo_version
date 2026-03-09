from odoo import models, fields, api, _

class Topic(models.Model):
    _name = "topic"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Topic"

    sequence = fields.Integer("Sequence")
    name = fields.Char(string="Title",required=True)
    state = fields.Selection([('pending', 'Pending'),('complete', 'Complete')], default='pending')