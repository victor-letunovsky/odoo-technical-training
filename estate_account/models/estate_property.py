from odoo import models
from odoo.fields import Command
from odoo.exceptions import AccessError

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold_property(self):
        print("action_sold_property() in 'estate.account' inherited from 'estate.property'")
        super(EstateProperty, self).action_sold_property()

        if not self.env['account.move'].check_access_rights('create', False):
            # Before creating the invoice `check_access_rights` and `check_access_rule` are used to ensure that
            # the current user can update properties in general as well as the specific property the invoice is for.
            try:
                self.check_access_rights('write')
                self.check_access_rule('write')
            except AccessError:
                return self.env['account.move']

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
                    'price_unit': a_property.selling_price
                }),
                Command.create({
                    'sequence': 1,
                    'name': 'Administrative fees',
                    'quantity': 1,
                    'price_unit': a_property.selling_price / 200
                })
            ]
            invoice_vals = {
                'partner_id': a_property.buyer.id,
                'move_type': move_type,
                'invoice_line_ids': invoice_line_vals
            }
            invoice_vals_list.append(invoice_vals)
        print(" reached ".center(100, '='))
        # `sudo()` is needed to bypass the normal security checks in Odoo in order to create an invoice despite the
        # current user not having the right to do so.
        # Because we want Agents to be able to confirm a sale without them having full invoicing access.
        # Manage the creation of invoices in sudo because a salesperson must be able to generate an invoice from a
        # sale order without "billing" access rights.
        return self.env['account.move'].sudo().with_context(default_move_type=move_type).create(invoice_vals_list)

