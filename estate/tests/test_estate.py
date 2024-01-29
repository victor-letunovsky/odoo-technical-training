from odoo.tests.common import TransactionCase, Form
from odoo.tests import tagged
from odoo.exceptions import UserError

@tagged('post_install', 'estate', '-at_install', '-standard')
class EstateTestCase(TransactionCase):

    buyer = None
    properties = None
    offers = None

    @classmethod
    def setUpClass(cls):
        super(EstateTestCase, cls).setUpClass()

        cls.buyer = cls.env['res.partner'].create({
            'name': 'buyer',
        })
        cls.properties = cls.env['estate.property'].create([{
            'name': 'prop1',
            'expected_price': 10000,
        }])
        cls.offers = cls.env['estate.property.offer'].create([{
            'partner_id': cls.buyer.id,
            'property_id': cls.properties[0].id,
            'price': 9000,
        }])


    def test_action_sold_property(self):
        # You cannot sell a property without an accepted offer
        with self.assertRaises(UserError):
            self.properties.action_sold_property()

        # accept the offer
        self.offers.action_accept_offer()

        # Now you can sell it
        self.properties.action_sold_property()
        self.assertRecordValues(self.properties, [{'state': 'sold'},])

        # You cannot create an offer for a sold property
        with self.assertRaises(UserError):
            self.env['estate.property.offer'].create([{
                'partner_id': self.buyer.id,
                'property_id': self.properties[0].id,
                'price': 10000,
            }])

    def test_property_form(self):
        """
        Test the form view of properties to click on `garden` checkbox
        """
        with Form(self.properties[0]) as prop:
            self.assertEqual(prop.garden_area, 0)
            self.assertIs(prop.garden_orientation, False)
            prop.garden = True
            self.assertEqual(prop.garden_area, 10)
            self.assertEqual(prop.garden_orientation, "n")
            prop.garden = False
            self.assertEqual(prop.garden_area, 0)
            self.assertIs(prop.garden_orientation, False)
