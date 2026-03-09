from odoo import models, fields, api, _

routine = [
    ('challenge_missed', 'Challenge Missed'), 
    ('challenge_fail', 'Challenge Fail'),
    ('50%_challenge_complete', '50% Challenge complete')
]

class MailAutomation(models.Model):
    _name = "mail.automation"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Mail Automation"

    name = fields.Char(string="Title",required=True)
    contact_ids = fields.Many2many('res.partner', string="Contacts")
    state = fields.Selection(routine)
    active = fields.Boolean('Active', default=True, help="If unchecked, it will allow you to hide removing it.", tracking=True)
