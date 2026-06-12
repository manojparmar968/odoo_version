# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class MovieReview(models.Model):
    _name = 'movie.review'
    _description = 'Movie Review'

    customer_id = fields.Many2one('res.partner', string='Customer')
    movie_id = fields.Many2one('cinema.movie', string='Movie')
    rating = fields.Integer(string='Rating')
    customer_review = fields.Text(string='Review')
    staff_response = fields.Text(string='Response')

    @api.constrains('rating')
    def check_rating(self):
        for movie in self:
            if movie.rating < 1 or movie.rating > 10:
                raise UserError('Please enter a rating from 0 to 10')