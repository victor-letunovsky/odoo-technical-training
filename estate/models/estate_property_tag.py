# -*- coding: utf-8 -*-

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'A property tag is, for example, a property which is ‘cozy’ or ‘renovated’.'

    name = fields.Char('Name', required=True)
