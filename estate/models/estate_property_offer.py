# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'A property offer is a potential buyer offer to the seller.'
    _order = 'price desc'

    price = fields.Float('Price')
    status = fields.Selection(string='Status', selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date('Deadline', compute="_compute_deadline", inverse="_inverse_deadline")
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    _sql_constraints = [
        ('check_price_strictly_positive', 'CHECK(price > 0)', 'An offer price must be strictly positive.')
    ]

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for record in self:
            a_create_date = record.create_date if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(a_create_date, days=record.validity)

    def _inverse_deadline(self):
        """
        Note that the inverse method is called when saving the record, while the compute method is called
        at each change of its dependencies.
        """
        for record in self:
            a_create_date = (record.create_date if record.create_date else fields.Date.today()).date()
            record.validity = (record.date_deadline - a_create_date).days

    @api.model_create_multi
    def create(self, vals_list):
        """
        At offer creation, set the property state to ‘Offer Received’.
        Also raise an error if the user tries to create an offer with a lower amount than an existing offer.
        """
        for vals in vals_list:
            a_property = self.env['estate.property'].browse(vals['property_id'])
            if a_property.state == 'new':
                a_property.state = 'received'
            elif a_property.state == 'sold':
                raise UserError('You cannot make an offer on a sold property')
            if vals['price'] < a_property.best_price:
                raise UserError('The offer must be higher than %s' % a_property.best_price)
        return super(EstatePropertyOffer, self).create(vals_list)

    def action_accept_offer(self):
        for record in self:
            for offer in record.property_id.offer_ids:
                # Only one offer can be accepted for a given property!
                if offer.status == 'accepted' and offer.id != record.id:
                    raise UserError('Offer from partner "%s" with price %d is already accepted'
                                    % (offer.partner_id.name, offer.price))
            record.status = 'accepted'
            record.property_id.state = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer = record.partner_id

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
