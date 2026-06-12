# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MovieTheater(models.Model):
    _name = 'movie.theater'
    _description = 'Movie Theater'

    name = fields.Char(string='Name')
    address = fields.Char(string='Address')
    is_vip = fields.Boolean(string='Is VIP', compute='_compute_is_vip', store=True)
    customer_ids = fields.Many2many('res.partner', string='Customers', compute="_compute_customer_ids", store=True)
    available_movie_ids = fields.Many2many('cinema.movie', string='Available movies')
    theater_room_ids = fields.One2many('theater.room', 'movie_theater_id',string='Theater rooms')
    movie_showing_ids = fields.One2many('movie.showing', 'movie_theater_id', string='Movie showings')
    bestselling_movie_ids = fields.Many2many('cinema.movie', string='Bestselling movies', 
                                            compute='_compute_bestselling_movie_ids')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    total_sales = fields.Float(string="Globals Sales", compute='_compute_total_sales')

    def _compute_total_sales(self):
        movie_theater = self.sudo().search([])
        for theater in self:
            theater.total_sales = sum(movie_theater.mapped('movie_showing_ids.line_ids.order_id.amount_total'))
    
    @api.depends('available_movie_ids', 'available_movie_ids.showing_ids')
    def _compute_bestselling_movie_ids(self):
        for theater in self:
            theater.bestselling_movie_ids = theater.available_movie_ids.sorted(
                lambda mov: sum(mov.mapped('showing_ids.total_attendees')), reverse=True)

    @api.depends('movie_showing_ids','movie_showing_ids.line_ids')
    def _compute_customer_ids(self):
        for theater in self:
            theater.customer_ids = theater.mapped('movie_showing_ids.line_ids.customer_id')

    @api.depends('theater_room_ids', 'theater_room_ids.has_vip_seats')
    def _compute_is_vip(self):
        for theater in self:
            if theater.theater_room_ids.filtered(lambda room: room.has_vip_seats and room.seats_number >= 10):
                theater.is_vip = True
            else:
                theater.is_vip = False
