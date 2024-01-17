# -*- coding: utf-8 -*-

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'A property tag is, for example, a property which is ‘cozy’ or ‘renovated’.'
    _order = 'name'

    name = fields.Char('Name', required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('check_name_is_unique', 'UNIQUE(name)', 'A property tag name must be unique')
    ]
