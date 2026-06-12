# -*- coding: utf-8 -*-

from odoo import models, fields, _


class CinemaMovie(models.Model):
    _name = 'cinema.movie'
    _description = 'Movie'

    name = fields.Char(string='Name')
    category = fields.Selection([('sci_fi', 'Sci-fi'), ('thriller', 'thriller'),
                                 ('action', 'Action'), ('comedy', 'Comedy')], string='Category')
    rating = fields.Selection([('g_rating', 'G'), ('pg_rating', 'PG'), ('pg12_rating', 'PG-13'),
                               ('r_rating', 'R'), ('nc17_rating', 'NC-17')], string='Rating')
    showing_ids = fields.One2many('movie.showing', 'movie_id', string='Showings')
    review_ids = fields.One2many('movie.review', 'movie_id', string='Reviews')

    def action_update_response(self):
        for movie in self:
            self._cr.execute("SELECT r.id, m.name, r.rating FROM movie_review r JOIN cinema_movie m " \
            "ON r.movie_id = m.id WHERE r.movie_id = %s" % movie.id)
            reviews = self._cr.fetchall()
            for review in reviews:
                if review[2] > 6:
                    self._cr.execute("UPDATE movie_review SET staff_response = " \
                    "'Thank you for your review' WHERE id = %s" % review[0])
                else:
                    self._cr.execute("UPDATE movie_review SET staff_response = " \
                    "'Sorry for your experience with the movie %s, we hope to see you soon' WHERE id = %s" % (review[1], review[0]))
                self._cr.commit()
