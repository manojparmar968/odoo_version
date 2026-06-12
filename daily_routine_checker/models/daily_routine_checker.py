import pytz
import uuid
from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import UserError, AccessError, ValidationError
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta

local_time = pytz.utc.localize(fields.Datetime.now()).astimezone(pytz.timezone('Asia/Calcutta'))

no_of_days = [
    ('7', '7 Days'), 
    ('30', '30 Days'),
    ('90', '3 Months'), 
    ('180', '6 Months')
]

class DailyRoutineChecker(models.Model):
    _name = 'daily.routine.checker'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Daily Routine Checker'
    _order = "id, current_streak desc"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    challenge_accept_datetime = fields.Datetime('Challenge Accept Date', default=fields.Datetime.now, readonly=True)
    no_of_days_challenge = fields.Selection(no_of_days, string="Number OF Days Challenge")
    active = fields.Boolean(default=True, help="Set active to false to hide the record without removing it.")
    routine_line_ids = fields.One2many('daily.routine.checker.line', 'daily_routine_checker_id', string='Routine Check')
    odoo_practise_line_ids = fields.One2many('odoo.practise', 'daily_routine_checker_id', string='Odoo Practise')
    interview_line_ids = fields.One2many('interview', 'daily_routine_checker_id', string='interview')
    current_streak = fields.Integer(default=0, readonly=True, store=True)
    streak_updated = fields.Boolean(default=False, readonly=True, store=True)
    missed_streak = fields.Integer(default=0, readonly=True, store=True, tracking=True)
    missed_streak_date = fields.Date(string="Missed Streak Date", readonly=True, store=True, tracking=True)
    state = fields.Selection([
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('fail', 'Fail'),
    ], default='running')
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user, required=True)
    partner_id = fields.Many2one('res.partner')
    employee_id = fields.Many2one('hr.employee')
    progress = fields.Float(compute="_compute_progress", store=True)
    token = fields.Char(default=lambda self: str(uuid.uuid4()))

    @api.depends('current_streak', 'no_of_days_challenge')
    def _compute_progress(self):
        for rec in self:
            days = int(rec.no_of_days_challenge) if rec.no_of_days_challenge else 0
            rec.progress = (rec.current_streak / days) * 100 if days else 0.0

    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            if 'no_of_days_challenge' in rec and rec.get('no_of_days_challenge'):
                rec['routine_line_ids'] = [(0, 0, {
                'routine_date': fields.Date.today(),
            })]
        return super().create(vals)

    def write(self, vals):
        if 'no_of_days_challenge' in vals and vals.get('no_of_days_challenge'):
            vals['routine_line_ids'] = [(0, 0, {
                'routine_date': fields.Date.today(),
            })]
        return super().write(vals)

    # This Cron will Run at 6 PM Daily & same will run by controller '/api/'
    def _todays_challenge_reminder(self):
        template = self.env.ref('daily_routine_checker.email_template_challenge_reminder_today')
        # if not template:
        #     return
        outgoing_server_name = self.env['ir.mail_server'].sudo().search([], limit=1).smtp_user
        today = fields.Date.today()
        # challenges = self.search([('state', '=', 'running')])
        challenges = self.search([
            ('routine_line_ids.routine_date', '=', today),
            ('routine_line_ids.success', '=', False)
        ])
        for challenge in challenges:
            # challenges_line = self.env['daily.routine.checker.line'].sudo().search([
            #     ('daily_routine_checker_id', '=', challenge.id),
            #         ('routine_date', '=', today)
            # ], limit=1)
            # if challenges_line and not challenges_line.success:
                template.send_mail(challenge.id,
                    email_values={
                        'email_to': challenge.user_id.email,
                        'email_from': outgoing_server_name
                    }, 
                force_send=True)

    # This Cron will Run at 10:30 PM Daily or send mail who miss the challange 
    # & same will run by controller '/api/challenge_reminder'
    def send_missed_reminder(self):
        today = fields.Date.today()
        template = self.env.ref('daily_routine_checker.mail_template_routine_missed')
        # if not template:
        #     return
        challenges = self.search([
            ('state', '=', 'running'),
            ('missed_streak', '>', 0),
            ('missed_streak_date', '=', today)
        ])
        for challenge in challenges:
            template.send_mail(challenge.id, 
                email_values={
                'email_to': challenge.user_id.email,
                'email_from': 'developer111095@gmail.com'
            }, force_send=True)

    # This Cron will Run at 10 PM Daily & same will run by controller '/api/daily_routine_check'
    @api.model
    def _cron_daily_logs_routine_checker(self):
        today = fields.Date.today()
        next_day = today + timedelta(days=1)
        challenges = self.search([('state', '=', 'running')])
        for challenge in challenges:
            challenges_line = self.env['daily.routine.checker.line'].sudo()
            if challenge.no_of_days_challenge:
                lines = challenges_line.search([('daily_routine_checker_id', '=', challenge.id),
                    ('routine_date', 'in', [today, next_day])])
                lines_by_date = {line.routine_date: line for line in lines}
                today_line = lines_by_date.get(today)
                next_day_exists = lines_by_date.get(next_day)
                if today_line and today_line.success:
                    challenge.current_streak += 1
                else:
                    challenge.current_streak = 0
                    challenge.progress = 0
                    challenge.missed_streak += 1
                    challenge.missed_streak_date = today
                if challenge.current_streak >= int(challenge.no_of_days_challenge):
                    challenge.state = 'completed'
                if challenge.missed_streak >= 3:
                    challenge.state = 'fail'
                if not next_day_exists and challenge.missed_streak < 3:
                    challenges_line.create({
                        'daily_routine_checker_id': challenge.id,
                        'routine_date': next_day,
                    })