# -*- coding: utf-8 -*-

from odoo import fields, models


class EstateProperty(models.Model):
    """
    Generates table name `estate_property`
    """
    _name = 'estate.property'
    _description = 'Model summarizes information about real estate property'

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
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(string='Status', selection=[('new', 'New'), ('received', 'Offer Received'),
                                                        ('accepted', 'Offer Accepted'), ('sold', 'Sold'),
                                                        ('canceled', 'Canceled')],
                             required=True, default='new', copy=False)
