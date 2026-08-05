from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import UserError, AccessError, ValidationError
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class DailyRoutineShifFirst(models.Model):
    _name = 'daily.routine.shift.first'
    _description = 'Daily Routine Shift First'

    daily_routine_checker_id = fields.Many2one('daily.routine.checker', required=True, ondelete='cascade')
    shift_start = fields.Datetime(string='Shift start')
    shift_end = fields.Datetime(string='Shift end')

class DailyRoutineShifSecond(models.Model):
    _name = 'daily.routine.shift.second'
    _description = 'Daily Routine Shift Second'

    daily_routine_checker_id = fields.Many2one('daily.routine.checker', required=True, ondelete='cascade')
    shift_start = fields.Datetime(string='Shift start')
    shift_end = fields.Datetime(string='Shift end')

class DailyRoutineShifThird(models.Model):
    _name = 'daily.routine.shift.third'
    _description = 'Daily Routine Shift Third'

    daily_routine_checker_id = fields.Many2one('daily.routine.checker', required=True, ondelete='cascade')
    shift_start = fields.Datetime(string='Shift start')
    shift_end = fields.Datetime(string='Shift end')