# -*- coding: utf-8 -*-

from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'A property offer is a potential buyer offer to the seller.'

    price = fields.Float('Price')
    status = fields.Selection(string='Status', selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
