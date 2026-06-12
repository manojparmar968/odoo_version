from odoo import models, fields, api, _

topic = [
    ('odoo','Odoo'),('aws','AWS'),('pending','Pending'),('other','Other')
]

odoo = [
    ('website','Website'),('ecommerce','eCommerce'),('survey','Survey'),('marketing','Marketing'),('ai','AI'),
    ('project','Project'),('timesheet','TimeSheet'),('spreadsheet','Spreadsheet'),('knowledge','Knowledge'),
    ('pos','POS'),
    ('purchase', 'Purchase'), ('inventory', 'Inventory'), ('sales', 'Sales'), ('accounting', 'Accounting'),
    ('crm','CRM'),('hr','HR'), ('odoo_studio','odoo Studio'),('manufacturing','Manufacturing'),
    ('not_in_list','Not In List')
]

aws = [
    ('compute','Compute'),('storage','Storage Services'),('vpc_networking','VPC NetWorking'),('databases','Databases'),
    ('security_iam','Security & IAM'),('serverless_application','Serverless & Application Services'),('monitoring','Monitoring & Automation'),
    ('container','Container Service'),('not_in_list','Not In List')
]

class OdooPractise(models.Model):
    _name = "odoo.practise"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Odoo Practise"

    date = fields.Date(string="Date", readonly=True, store=True, default=fields.Date.today())
    topic = fields.Selection(topic)
    odoo_state = fields.Selection(odoo)
    aws_state = fields.Selection(aws)
    status = fields.Selection([('pending', 'Pending'),('completed', 'Completed')], default='pending')
    topic_name = fields.Char(string="Topic Name")
    functional = fields.Boolean()
    topic_id = fields.Many2one('topic')
    daily_routine_checker_id = fields.Many2one('daily.routine.checker', required=True, ondelete='cascade')