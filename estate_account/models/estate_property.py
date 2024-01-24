from odoo import models
from odoo.fields import Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):
        print("action_sold_property() in 'estate.account' inherited from 'estate.property'")
        super(EstateProperty, self).action_sold_property()

        # Create invoice in Invoicing / Customers / Invoices
        move_type = 'out_invoice'
        invoice_vals_list = []
        for a_property in self:
            # Invoice contains One2many field 'invoice_line_ids'
            # One2many and Many2many use special ‘commands’ which are made by human-readable Command namespace.
            invoice_line_vals = [
                Command.create({
                    'sequence': 0,
                    'name': a_property.name,
                    'quantity': 1,
                    'price_unit': a_property.best_price
                }),
                Command.create({
                    'sequence': 1,
                    'name': 'Administrative fees',
                    'quantity': 1,
                    'price_unit': a_property.best_price / 200
                })
            ]
            invoice_vals = {
                'partner_id': a_property.buyer.id,
                'move_type': move_type,
                'invoice_line_ids': invoice_line_vals
            }
            invoice_vals_list.append(invoice_vals)
        return self.env['account.move'].sudo().with_context(default_move_type=move_type).create(invoice_vals_list)

