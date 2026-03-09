import pytz
from odoo import http, fields
from odoo.http import request, Response
import json
from datetime import datetime, timedelta
from .error_or_response_parser import *

class DailyRoutineCheckerController(http.Controller):

    @http.route('/api/challenge_complete_reminder/<string:token>', type='http', auth='public', website=True)
    def challenge_complete_routine_reminder(self, token=None, **kwargs):
        try:
            template = request.env.ref('daily_routine_checker.email_template_challenge_reminder_today')
        except Exception as e:
            msg = {"message": f"Something Went Wrong.{e}", "status": 400}
            return return_Response_error(msg)
        res = {"isSucess": True, "message": 'E-Mail Sent Successfully.', "status": 200}
        return return_Response(res)

    @http.route(['/api/challenge_reminder'], type='http', auth="public", methods=['GET'], csrf=False, cors='*', website=True)
    def challenge_missed_reminder(self, **kwargs):
        try:
            # today = fields.Date.today()
            # today = pytz.utc.localize(fields.Datetime.now()).astimezone(pytz.timezone('Asia/Calcutta')).date()
            template = request.env.ref('daily_routine_checker.mail_template_routine_missed', raise_if_not_found=False)
            challenges = request.env['daily.routine.checker'].sudo().search([('state', '=', 'running'),
                ('missed_streak', '>', 0),('missed_streak_date', '=', fields.Date.today())
            ])
            for challenge in challenges:
                template.send_mail(challenge.id, 
                    email_values={
                    'email_to': challenge.user_id.email,
                    'email_from': 'developer111095@gmail.com'
                }, force_send=True)
        except Exception as e:
            msg = {"message": f"Something Went Wrong.{e}", "status": 400}
            return return_Response_error(msg)
        res = {"isSucess": True, "message": 'Mail Sent Successfully.', "status": 200}
        return return_Response(res)

    @http.route(['/api/daily_routine_check'], type='http', auth="public", csrf=False, website=True)
    def daily_routine_update(self, **kwargs):
        try:
            today = datetime.now().date()
            next_day = today + timedelta(days=1)
            challenges = request.env['daily.routine.checker'].sudo().search([('state', '=', 'running')])
            exists = request.env['daily.routine.checker.line'].sudo()
            if not challenges:
                return
            for challenge in challenges:
                lines = exists.search([
                    ('daily_routine_checker_id', '=', challenge.id),
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
                    # challenge.write({
                    #     'routine_line_ids': [(0, 0, {
                    #         'routine_date': next_day,
                    #     })]
                    # })
                    exists.create({
                        'daily_routine_checker_id': challenge.id,
                        'routine_date': next_day,
                    })
        except Exception as e:
            msg = {"message": f"Something Went Wrong.{e}", "status": 400}
            return msg
        res = {
            "isSucess": True, 
            "message": "Today's routine is checked Updated Successfully.", 
            "status": 200
        }
        return Response(
            json.dumps(res),
            content_type='application/json',
            status=200
        )