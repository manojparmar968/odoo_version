# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class MovieShowing(models.Model):
    _name = 'movie.showing'
    _description = 'Movie Showing'

    def _default_ticket_price(self):
        ticket_price = self.env['ir.config_parameter'].sudo().get_param('cinema_management.ticket_price')
        return round(float(ticket_price), 2)

    movie_id = fields.Many2one('cinema.movie', string='Movie')
    movie_theater_id = fields.Many2one('movie.theater', string='Movie theater')
    theater_room_id = fields.Many2one('theater.room', string='Theater room')
    seats_number = fields.Integer(related='theater_room_id.seats_number', store=True)
    # attendee_ids = fields.Many2many('res.partner', string='Attendees')
    line_ids = fields.One2many('movie.showing.line', 'showing_id', string='Attendees')
    total_attendees = fields.Integer(string='Total audience', compute='_compute_total_attendees', store=True)
    date_start = fields.Datetime(string='Date start')
    date_end = fields.Datetime(string='Date end')
    ticket_price = fields.Float(string="Ticket Price", default=lambda self: self._default_ticket_price())
    is_past = fields.Boolean(string='Is Past', compute='_compute_is_past', store=True)
    status = fields.Selection([('open', 'Open'), ('playing', 'Playing'), ('ended', 'Ended')], default='open')

    def write(self, vals):
        if vals and 'status' in vals:
            if self.env.user.has_group('cinema_management.cinema_manager_user_group'):
                raise ValidationError('Only Managers can modify the showing status')
        res = super(MovieShowing, self).write(vals)
        return res

    def _compute_is_past(self):
        today = fields.Datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        for showing in self:
            if showing.date_start and showing.date_start < today:
                showing.is_past = True
            else:
                showing.is_past = False

    def _update_showing_price(self):
        self.search([('movie_id.category','=', 'sci_fi')]).write({'ticket_price': 12})
        self.search([('movie_id.category','!=', 'sci_fi')]).write({'ticket_price': 8})

    @api.depends('line_ids')
    def _compute_total_attendees(self):
        for showing in self:
            showing.total_attendees = len(showing.line_ids)

class MovieShowingLines(models.Model):
    _name = 'movie.showing.line'
    _description = 'Movie Showing Line'

    showing_id = fields.Many2one('movie.showing', string='Movie Showing')
    customer_id = fields.Many2one('res.partner', string='Customer')
    order_id = fields.Many2one('sale.order', string='Sale Order')
    state = fields.Selection([('attended', 'Attended'), ('canceled', 'Canceled')], string='State', default='attended')

    def create(self, vals):
        res = super(MovieShowingLines, self).create(vals)
        for line in res:
            order = self.env['sale.order'].with_context(ticket_price=res.showing_id.ticket_price).create(
                {'partner_id': line.customer_id.id})
            line.order_id = order
        return res