# -*- coding: utf-8 -*-

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'A property offer is a potential buyer offer to the seller.'

    price = fields.Float('Price')
    status = fields.Selection(string='Status', selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date('Deadline', compute="_compute_deadline", inverse="_inverse_deadline")

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
