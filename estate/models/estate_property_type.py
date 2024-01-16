# -*- coding: utf-8 -*-

from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = ('A property type is, for example, a house or an apartment.'
                    'We need type to categorize properties and refine filtering.')
    _order = 'sequence, name'

    name = fields.Char('Name', required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    sequence = fields.Integer('Sequence', default=1, help="Used to order property types.")

    _sql_constraints = [
        ('check_name_is_unique', 'UNIQUE(name)', 'A property type name must be unique')
    ]
