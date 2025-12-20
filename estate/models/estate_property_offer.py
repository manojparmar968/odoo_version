# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo import osv
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = "price desc"

    price = fields.Float('Price')
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], string='Status', copy=False)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer("Validity (days)", default = 7)
    date_deadline = fields.Date("Deadline", compute="_compute_date_deadline", inverse='_inverse_date_deadline', store=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id', string='Property Type', store=True)
    

    _price_check = models.Constraint(
        'CHECK(price > 0)',
        'Offer Price should be positive.',
    )

    @api.constrains('price')
    def _check_offer_price(self):
        if self.price < (self.property_id.expected_price * 0.90):
            raise ValidationError(_("A selling Price must be at least 90'%' of the expected price."))

    @api.depends('validity')
    def _compute_date_deadline(self):
        for day in self:
            print(day.validity)
            if day.create_date and day.validity:
                day.date_deadline = day.create_date + timedelta(days = day.validity)

    def _inverse_date_deadline(self): # Inverse is not working
        for record in self:
            if record.date_deadline and record.create_date:
                # If date_deadline is set, calculate the validity
                delta = record.date_deadline - record.create_date.date()
                record.validity = delta.days
            elif record.create_date: # elif record.validity and record.create_date:
                # If validity is set, calculate the date_deadline
                record.date_deadline = record.create_date + timedelta(days=record.validity)

    def action_accept_offer(self):
        self.ensure_one()
        self.status = 'accepted'
        self.property_id.write({
            'selling_price' : self.price,
            'buyer_id' : self.partner_id.id,
            'state': 'offer_accepted'
        })
        return True

    def action_refuse_offer(self):
        self.ensure_one()
        self.status = 'refused'

    @api.model_create_multi
    def create(self, vals_list):
        print("vals_list: ",vals_list)
        res = super().create(vals_list)
        # rec = self.env['estate.property'].browse(vals_list[0]['property_id'])
        # print(rec.offer_ids,rec.best_price)
        # existing_offer = self.search([('property_id', '=', vals_list[0]['property_id'])], 
        #     limit=1, order='create_date desc')
        # print(existing_offer)
        # for last_offer in rec.offer_ids:
        #     print(last_offer,last_offer.price,)
        # if rec:
        #     rec.state = 'offer_received'
        print()
        return res