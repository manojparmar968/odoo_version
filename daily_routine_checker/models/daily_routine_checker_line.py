from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import UserError, AccessError, ValidationError
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class DailyRoutineCheckerLine(models.Model):
    _name = 'daily.routine.checker.line'
    _description = 'Daily Routine Checker Line'

    daily_routine_checker_id = fields.Many2one('daily.routine.checker', required=True, ondelete='cascade')
    routine_date = fields.Date('Date', readonly=True, store=True)
    smoking = fields.Boolean()
    drinking = fields.Boolean()
    study = fields.Boolean()
    interview = fields.Boolean()
    dry_fruits = fields.Boolean()
    interview_value = fields.Integer(default=0, store=True)
    interview_progress = fields.Float(string="Interview Progress (%)")
    odoo_certification = fields.Integer(default=0, store=True)
    odoo_certification_progress = fields.Float(string="Odoo Progress (%)")
    success = fields.Boolean(compute='_compute_success', store=True)

    @api.depends('smoking', 'drinking', 'study')
    def _compute_success(self):
        for rec in self:
            rec.success = rec.smoking and rec.drinking and rec.study

    # @api.constrains('routine_date')
    # def _check_date_sequence(self):
    #     for rec in self:
    #         last = self.search([
    #             ('daily_routine_checker_id', '=', rec.daily_routine_checker_id.id),
    #             ('id', '!=', rec.id)
    #         ], order='routine_date desc', limit=1)

    #         if last and rec.routine_date and last.routine_date:
    #             if rec.routine_date > last.routine_date + fields.date.delta(days=1):
    #                 raise ValidationError("You cannot skip days in the challenge.")