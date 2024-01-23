# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    """
    Generates table name `estate_property`
    """
    _name = 'estate.property'
    _description = 'Model summarizes information about real estate property'
    _order = 'id desc'

    # Below there are model fields
    # Related docs: https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#reference-orm-fields

    """
    Common field attributes:
    * `string`: The label of the field in UI
    * `required`: If `true`, the field cannot be empty
    * `help`: Provides long-form help tooltip for users in the UI
    * `index`: Requests that Odoo create a database index on the column
    """

    """
    Automatic Fields: https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#reference-fields-automatic
    Odoo automatically creates a few system fields in all models managed by framework that can't be written to.
    * `id`: The unique identifier for a record of the model
    * `create_date`: Creation date of the record
    * `create_uid`: User who created the record
    * `write_date`: Last modification date of the record
    * `write_uid`: User who last modified the record
    
    It is possible to disable automatic creation of some fields:
    https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#reference-fields-automatic-log-access
    """

    name = fields.Char('Title', required=True)    # required=True means "NOT NULL" in db
    property_type_id = fields.Many2one('estate.property.type', 'Property Type')
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available From',
                                    default=fields.Date.add(fields.Date.today(), months=3), copy=False)
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2, help='Integer amount of bedrooms')
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(string='Garden Orientation',
        selection=[('n', 'North'), ('s', 'South'), ('e', 'East'), ('w', 'West')],
        help='Geographical garden orientation')
    total_area = fields.Integer('Total Area (sqm)', compute='_compute_total_area')
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(string='Status', selection=[('new', 'New'), ('received', 'Offer Received'),
                                                        ('accepted', 'Offer Accepted'), ('sold', 'Sold'),
                                                        ('canceled', 'Canceled')],
                             required=True, default='new', copy=False)
    # available computed field should be stored (store=True) in order to filter in view.
    available = fields.Boolean('Available', compute='_compute_available', store=True)
    buyer = fields.Many2one('res.partner', string='Buyer', copy=False)

    # `self.env.user` is the current user's record
    salesperson = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag')

    # In One2many field first parameter is co-model of relationship
    # and the second parameter is the field we want to inverse from co-model.
    # Both are mandatory except in the case of related fields or field extensions.
    offer_ids = fields.One2many('estate.property.offer', 'property_id')

    best_price = fields.Float('Best Offer', compute='_compute_best_price')

    _sql_constraints = [
        ('check_expected_price_strict_positive', 'CHECK(expected_price > 0)',
         'The expected price of the property must be strictly positive.'),
        ('check_selling_price_is_positive', 'CHECK(selling_price >= 0)',
         'The selling price of the property must be positive.')
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) if record.offer_ids else 0

    @api.depends('state')
    def _compute_available(self):
        for record in self:
            record.available = record.state in ['new', 'received']

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'n'
            return {'warning': {
                'title': 'Info',
                'message': 'Set garden area to %s and orientation to %s.' % (self.garden_area, self.garden_orientation),
                'type': 'notification'}}   # Remove 'type' to show message as a dialog
        else:
            self.garden_area = 0
            self.garden_orientation = None
            return {'warning': {
                'title': 'Info',
                'message': 'Clear garden area and orientation',
                'type': 'notification'}}  # Remove 'type' to show message as a dialog

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if ((not float_is_zero(record.selling_price, precision_digits=2))
                    and (float_compare(record.expected_price * .9, record.selling_price, precision_digits=2) == 1)):
                raise ValidationError('The selling price must be at least 90% of the expected price! '
                                      'You must reduce the expected price if you want to accept the offer.')

    @api.ondelete(at_uninstall=False)
    def _unlink_property(self):
        """
        Prevent deletion of a property if its state is not ‘New’ or ‘Canceled’.
        """
        for a_property in self:
            if a_property.state not in ['new', 'canceled']:
                raise UserError('Only new and canceled properties can be deleted.')

    def action_sold_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('Estate property "%s" is already sold.' % record.name)
            elif record.state == 'canceled':
                raise UserError('Canceled estate properties cannot be sold.')
            else:
                record.state = 'sold'

    def action_cancel_property(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError('Estate property "%s" is already cancelled.' % record.name)
            elif record.state == 'sold':
                raise UserError('Sold estate properties cannot be canceled.')
            else:
                record.state = 'canceled'
