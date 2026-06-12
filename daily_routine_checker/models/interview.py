from odoo import models, fields, api, _

class Interview(models.Model):
    _name = "interview"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Interview"

    date = fields.Date(string="Date", readonly=True, store=True, default=fields.Date.today())
    company_name = fields.Char(string="Company Name")
    description = fields.Text()
    detail_data = fields.Html(string="Detail Data")
    daily_routine_checker_id = fields.Many2one('daily.routine.checker',  ondelete='cascade')

    binary_fields = fields.Many2many('ir.attachment', string="Multi File Upload")
    binary_field = fields.Binary(string="Upload File")
    binary_file_name = fields.Char("Binary File Name")
