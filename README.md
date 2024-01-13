# Odoo 16.0 - Technical Training

The Technical Training of Odoo 16.0 is available on the
[Tutorial](https://www.odoo.com/documentation/master/developer/howtos/rdtraining.html) or [Getting started](https://www.odoo.com/documentation/master/developer/tutorials/getting_started.html)

[Developer Mode](https://www.odoo.com/documentation/16.0/applications/general/developer_mode.html)

# A New Application

1. The model is defined in the file `estate/models/estate_property.py`
2. The file `estate_property.py` is imported in `estate/models/__init__.py`
3. The folder `models` is imported in `estate/__init__.py`

## Manifest
Our [manifest](estate/__manifest__.py).

Describes module:
- name
- category
- summary
- website
- dependencies (on other modules)
- etc...

Prepare the addon directory. [manifest](https://www.odoo.com/documentation/16.0/developer/reference/backend/module.html#reference-module-manifest) \

Example of manifest: [CRM file](https://github.com/odoo/odoo/blob/fc92728fb2aa306bf0e01a7f9ae1cfa3c1df0e10/addons/crm/__manifest__.py)

# Object-Relational Mapping
[ORM API](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html)

## Models

Model fields are defined as attributes on the model itself:
```python
from odoo import models, fields
class AModel(models.Model):
    _name = 'a.model.name'

    field1 = fields.Char()
```
> **Warning** \
> You cannot define a field and a method with the same name, the last one will silently overwrite the former ones.

By default, the field’s label (user-visible name) is a capitalized version of the field name, this can be overridden with the string parameter:
```python
from odoo import fields
field2 = fields.Integer(string="Field Label")
```

Default value:
```python
from odoo import fields
name = fields.Char(default="a value")
```

Default value as a compute function:
```python
from odoo import fields

def _default_name(self):
    return self.get_value()

name = fields.Char(default=lambda self: self._default_name())
```

# Security
Odoo provides a security mechanism to allow access to the data for specific groups of users.

Details: [Restrict access to data](https://www.odoo.com/documentation/16.0/developer/tutorials/restrict_data_access.html)

## Data Files (CSV)
For example [list of country states](https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/res.country.state.csv)
which is loaded at installation of the `base` module.
```csv
"id","country_id:id","name","code"
state_au_1,au,"Australian Capital Territory","ACT"
state_au_2,au,"New South Wales","NSW"
state_au_3,au,"Northern Territory","NT"
state_au_4,au,"Queensland","QLD"
...
```
These three fields are [defined](https://github.com/odoo/odoo/blob/2ad2f3d6567b6266fc42c6d2999d11f3066b282c/odoo/addons/base/models/res_country.py#L108-L111)
in `res.country.state` model.

Data folders:
* `data` contains a file importing data
* `security` - data related to security
* `views` - data related to views and actions

All of these files must be declared in the `data` section within the `__manifest__.py` file.
For example `res.country.state.csv` is defined in
[the manifest of the base module](https://github.com/odoo/odoo/blob/e8697f609372cd61b045c4ee2c7f0fcfb496f58a/odoo/addons/base/__manifest__.py#L29).

The content of the data files is only loaded when a module is installed or updated.

> **Warning** \
> The data files are sequentially loaded following their order in the `__manifest__.py` file.
> This means that if data `A` refers to data `B`, you must make sure that `B` is loaded before `A`.

## Access Rights
Documentation: [Access Rights](https://www.odoo.com/documentation/16.0/developer/reference/backend/security.html#reference-security-acl)

Access rights are records of model `ir.model.access` and usually defined in a CSV file named `security/ir.model.access.csv`.
Example of [base access rights model](https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/security/ir.model.access.csv).

Each access right is associated with:
1. model
2. group
3. set of permissions

Set of permissions:
1. create
2. read
3. write
4. unlink (equivalent of `delete`)

`model_id/id` refers to the model which the access right applies to. The standard way to refer to the model is
`model_<model_name>`, where `<model_name>` is the `_name` of the model with the `.` replaced by `_`. Seems cumbersome?
Indeed, it is...

# UI

## Data Files
Documentation: [Data Files](https://www.odoo.com/documentation/16.0/developer/reference/backend/data.html#reference-data)

XML is an alternative to CSV format of data files. When performance is important, the CSV format is preferred over the XML format.
When the format is complex (e.g. load the structure of a view or an email template), XML format is used.

When the data is linked to views, we add them to the `views` folder.

Actions and menus are standard records in the database loaded through an XML file.

In Odoo, the user interface (actions, menus and views) is largely defined by creating and composing records defined in
an XML file.
A common pattern is Menu > Action > View.
To access records the user navigates through several menu levels; the deepest level is an action which triggers the opening of a list of the records.

## Actions
Documentation: [Actions](https://www.odoo.com/documentation/16.0/developer/reference/backend/actions.html#reference-actions)

Actions can be triggered in three ways:
1. by clicking on menu items (linked to specific actions)
2. by clicking on buttons in views (if these are connected to actions)
3. as contextual actions on object

Example of action for `test_model`:
```xml
<record id="test_model_action" model="ir.actions.act_window">
    <field name="name">Test action</field>
    <field name="res_model">test_model</field>
    <field name="view_mode">tree,form</field>
</record>
```

Good example of [simple action](https://github.com/odoo/odoo/blob/09c59012bf80d2ccbafe21c39e604d6cfda72924/addons/crm/views/crm_lost_reason_views.xml#L57-L70) in Odoo.

## Menus
Documentation: [Shortcuts](https://www.odoo.com/documentation/16.0/developer/reference/backend/data.html#reference-data-shortcuts)

`<menuitem>` is a shortcut to `ir.ui.menu` record to reduce complexity in declaring a menu and connecting it to the corresponding action.

A basic menu for our `test_model_action` is:
```xml
<!-- The menu `test_model_menu_action` is linked to the action `test_model_action`,
    and the action is linked to the model `test_model`. -->
<menuitem id="test_model_menu_action" action="test_model_action"/>
```

The action here is link between the menu and the model (`menu -> action -> model`).

There are three levels of menus:
1. The root menu, displayed in App switcher
2. The first level menu, displayed in the top bar
3. The action menus

For example:
```xml
<menuitem id="test_menu_root" name="Test">
    <menuitem id="test_first_level_menu" name="First Level">
        <menuitem id="test_model_menu_action" action="test_model_action"/>
    </menuitem>
</menuitem>
```

## Fields, Attributes And View
Documentation: [Fields](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#fields)

Some examples of the view fine-tunings:
* some fields have a default value
* some fields are read-only
* some fields are not copied when duplicating the record

## Reserved Fields
Documentation: [Reserved Field names](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#reference-orm-fields-reserved)

A few field names are reserved for pre-defined behavior.
They should be defined on a model when the related behavior is desired:
* `name`
* `active` - toggles the global visibility of the record
* `state` - lifecycle stages of the object (used by `fields.states` attribute)
* `parent_id` - used to organize records in a tree structure
* `parent_path`
* `company_id` - used for Odoo multi-company behavior

# Basic Views
Documentation: [Views](https://www.odoo.com/documentation/16.0/developer/reference/backend/views.html)

In practice, the default view (from previous chapter [UI](#UI)) is **never** acceptable for a business application.

Views are defined as `ir.ui.view` model in XML with actions and menus.

In our real estate module we need following views customizations:
* in the list view we need more fields than just the name.
* in the form view the fields should be grouped.
* in the search view search on more fields than just the name.

Basic views structure (placeholders - in caps):
```xml
<record id="MODEL_view_TYPE" model="ir.ui.view">
  <field name="name">NAME</field>
  <field name="model">MODEL</field>
  <field name="arch" type="xml">
    <VIEW_TYPE>
      <VIEW_SPECIFICATIONS/>
    </VIEW_TYPE>
  </field>
</record>
```

## List
Documentation: [List](https://www.odoo.com/documentation/16.0/developer/reference/backend/views.html#reference-views-list)

List views root element is `<tree>`.

The most basic version of this view simply lists all the fields to display in the table (where each field is a column):
```xml
<tree string="Tests">
    <field name="name"/>
    <field name="last_seen"/>
</tree>
```

## Form
Documentation: [Form](https://www.odoo.com/documentation/16.0/developer/reference/backend/views.html#reference-views-form)

Root element is `<form>` and its XML is composed of:
1. high-level structure elements (groups and notebooks)
2. interactive elements (buttons and fields)

For example:
```xml
<form string="Test">
    <sheet>
        <group>
            <group>
                <field name="name"/>
            </group>
            <group>
                <field name="last_seen"/>
            </group>
            <notebook>
                <page string="Description">
                    <field name="description"/>
                </page>
            </notebook>
        </group>
    </sheet>
</form>
```

It is possible to use regular HTML tags such as `div` and `h1` as well as the `class` attribute (Odoo provides some built-in classes) to fine-tune the look.

[A simple example](https://github.com/odoo/odoo/blob/6da14a3aadeb3efc40f145f6c11fc33314b2f15e/addons/crm/views/crm_lost_reason_views.xml#L16-L44)

## Search
Documentation: [Search](https://www.odoo.com/documentation/16.0/developer/reference/backend/views.html#reference-views-search)

Root element is `<search>`, its most basic version lists necessary fields:
```xml
<search string="Tests">
    <field name="name"/>
    <field name="last_seen"/>
</search>
```

Search views can also contain `<filter>` elements, which act as toggles for predefined searches.
Filters must have one of the following attributes:
* `domain`: adds the given domain to the current search
* `context`: adds some context to the current search; uses the key `group_by` to group results on the given field name

[A simple example](https://github.com/odoo/odoo/blob/715a24333bf000d5d98b9ede5155d3af32de067c/addons/delivery/views/delivery_view.xml#L30-L44)

## Domains
Documentation: [Search domains](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#reference-orm-domains)

Domain encodes conditions on records. Domain is a list of criteria used to select a subset of a model’s records.

Each criterion is a triplet with a _field name_, an _operator_ and a _value_.

Example one:
```javascript
[('product_type', '=', 'service'), ('unit_price', '>', 1000)]
```

Example two:
```javascript
['|',
    ('product_type', '=', 'service'),
    '!', '&',
        ('unit_price', '>=', 1000),
        ('unit_price', '<', 2000)]
```

> **Notes** \
> XML does not allow `<` and `&` to be used inside XML elements. \
> To avoid parsing errors, entity references should be used:
> * `&lt;` for `<`
> * `&amp;` for `&`
> * `&gt;` for `>`
> * `&apos;` for `'`
> * `&quot;` for `"`

# Relations Between Models

## Many2one
Documentation: [Many2one](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#odoo.fields.Many2one)

A `many2one` is a simple link to another object.
For example, in order to define a link to the `res.partner` in our test model, we can write:
```python
from odoo import fields
partner_id = fields.Many2one("res.partner", string="Partner")
```

By convention, `many2one` fields have the `_id` suffix. Accessing the data in the partner can then be easily done with:

```python
# noinspection PyUnresolvedReferences
print(my_test_object.partner_id.name)
```

> **See also** \
> [foreign keys](https://www.postgresql.org/docs/12/tutorial-fk.html)

> **Note** \
> The object `self.env` gives access to request parameters and other useful things:
> * `self.env.cr` or `self._cr` is the database _cursor_ object; it is used for querying the database
> * `self.env.uid` or `self._uid` is the current user’s database id
> * `self.env.user` is the current user’s record
> * `self.env.context` or `self._context` is the context dictionary
> * `self.env.ref(xml_id)` returns the record corresponding to an XML id
> * `self.env[model_name]` returns an instance of the given model

## Many2many
Documentation: [Many2many](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#odoo.fields.Many2many)

A `many2many` is a bidirectional multiple relationship: any record on one side can be related to any number of records
on the other side.
For example, to define a link to the `account.tax` model on our test model:
```python
from odoo import fields
tax_ids = fields.Many2many("account.tax", string="Taxes")
```

By convention, `many2many` fields have the `_ids` suffix. Accessing the data must be done in a loop:

```python
# noinspection PyUnresolvedReferences
for tax in my_test_object.tax_ids:
    print(tax.name)
```

A list of records is known as a _recordset_, i.e. an ordered collection of records.
It supports standard Python operations on collections, such as `len()` and `iter()`,
plus extra set operations like `recs1 | recs2`.

## One2many
Documentation: [One2many](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#odoo.fields.One2many)

`one2many` is the inverse of a `many2one`. For example, we defined on our test model a link to the `res.partner` model
thanks to the field `partner_id`. We can define the inverse relation,
i.e. the list of test models linked to our partner:
```python
from odoo import fields
# The first parameter is called the comodel and the second parameter is the field we want to inverse.
test_ids = fields.One2many("test_model", "partner_id", string="Tests")
```

By convention, `one2many` fields have the `_ids` suffix.
They behave as a list of records, meaning that accessing the data must be done in a loop:

```python
# noinspection PyUnresolvedReferences
for test in partner.test_ids:
    print(test.name)
```

> **Danger** \
> Because a `One2many` is a virtual relationship, there must be a `Many2one` field defined in the comodel.

We don’t need an action or a menu for all models. Some models are intended to be accessed only through another model.

# Computed Fields And Onchanges
Sometimes the value of one field is determined from the values of other fields and other times we want to help
the user with data entry.
These cases are supported by the concepts of computed fields and onchanges.

## Computed Fields
Documentation: [Computed Fields](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#reference-fields-compute)

To create a computed field, create a field and set its attribute `compute` to the name of a method.
The computation method should set the value of the computed field for every record in `self`.

By convention, `compute` methods are private, meaning that they cannot be called from the presentation tier,
only from the business tier. Private methods have a name starting with an underscore `_`.

Computed fields are _read-only_ by default.

### Dependencies
The value of a computed field usually depends on the values of other fields in the computed record.
The ORM expects the developer to specify those dependencies on the compute method with the
decorator [depends()](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#odoo.api.depends).
The given dependencies are used by the ORM to trigger the recomputation of the field whenever some
of its dependencies have been modified:

```python
from odoo import api, fields, models

class TestComputed(models.Model):
    _name = "test.computed"

    total = fields.Float(compute="_compute_total")
    amount = fields.Float()

    @api.depends("amount")
    def _compute_total(self):
        for record in self:
            record.total = 2.0 * record.amount
```

> **Note** \
> `self` is a collection. \
> The object `self` is a _recordset_, i.e. an ordered collection of records.
> It supports the standard Python operations on collections, e.g. `len(self)` and `iter(self)`,
> plus extra set operations such as `recs1 | recs2`. \
> Iterating over `self` gives the records one by one, where each record is itself a collection of size 1.
> You can access/assign fields on single records by using the dot notation, e.g. `record.name`.

Many examples of computed fields [can be found](https://github.com/odoo/odoo/blob/713dd3777ca0ce9d121d5162a3d63de3237509f4/addons/account/models/account_move.py#L3420-L3423) in Odoo.

For relational fields (`many2one`, `many2many`, `one2many`) it’s possible to use paths through a field as a dependency:
```python
from odoo import api, fields

description = fields.Char(compute="_compute_description")
partner_id = fields.Many2one("res.partner")

@api.depends("partner_id.name")
def _compute_description(self):
    for record in self:
        record.description = "Test for partner %s" % record.partner_id.name
```

### Inverse Function
Computed fields are read-only by default.

To allow modification of computed field or dependent field with one impacting the other there is `inverse` function.
For example:
```python
from odoo import api, fields, models

class TestComputed(models.Model):
    _name = "test.computed"

    total = fields.Float(compute="_compute_total", inverse="_inverse_total")
    amount = fields.Float()

    @api.depends("amount")
    def _compute_total(self):
        for record in self:
            record.total = 2.0 * record.amount

    def _inverse_total(self):
        for record in self:
            record.amount = record.total / 2.0
```

[One more example](https://github.com/odoo/odoo/blob/2ccf0bd0dcb2e232ee894f07f24fdc26c51835f7/addons/crm/models/crm_lead.py#L308-L317)

A `compute` method sets the field while an `inverse` method sets the field’s dependencies.

Note that the `inverse` method is called when saving the record, while the `compute` method is called at each change of its dependencies.

Computed fields are not stored in the database by default.
Therefore, it is not possible to search on a computed field unless a search method is defined.
An example can be found [here](https://github.com/odoo/odoo/blob/f011c9aacf3a3010c436d4e4f408cd9ae265de1b/addons/event/models/event_event.py#L188).

Another solution is to store the field with the store=True attribute.
While this is usually convenient, pay attention to the potential computation load added to your model.
```python
from odoo import api, fields

description = fields.Char(compute="_compute_description", store=True)
partner_id = fields.Many2one("res.partner")

@api.depends("partner_id.name")
def _compute_description(self):
    for record in self:
        record.description = "Test for partner %s" % record.partner_id.name
```

Every time the partner name is changed, the description is automatically recomputed for **all the records** referring to it!
This can quickly become prohibitive to recompute when millions of records need recomputation.

It is also worth noting that a computed field can depend on another computed field.
The ORM is smart enough to correctly recompute all the dependencies in the right order…
but sometimes at the cost of degraded performance.

## Onchanges
Documentation: [onchange()](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#odoo.api.onchange)

The _onchange_ mechanism provides a way for the client interface to update a form without saving anything
to the database whenever the user has filled in a field value.
To achieve this, we define a method where self represents the record in the form view and decorate it with
[`@api.onchange()`](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#odoo.api.onchange)
to specify which field it is triggered by.
Any change you make on self will be reflected on the form:
```python
from odoo import api, fields, models


class TestOnchange(models.Model):
    _name = "test.onchange"

    name = fields.Char(string="Name")
    description = fields.Char(string="Description")
    partner_id = fields.Many2one("res.partner", string="Partner")

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        """
        Note: we do not loop on self, this is because the method is only triggered in a form view,
        where self is always a single record.
        """
        self.name = "Document for %s" % self.partner_id.name
        self.description = "Default description for %s" % self.partner_id.name
```
In this example, changing the partner will also change the name and the description values.
It is up to the user whether to change the name and description values afterward.
Also note that we do not loop on self, this is because the method is only triggered in a form view, where self is always a single record.

## Resume about computed fields and onchanges
Always prefer computed fields since they are also triggered outside the context of a form view.
Never ever use an onchange to add business logic to your model.
This is a very **bad idea** since onchanges are not automatically triggered when creating a record programmatically;
they are only triggered in the form view.

Computed fields tend to be easier to debug: such a field is set by a given method, so it’s easy to track when the value is set.
Onchanges, on the other hand, may be confusing: it is very difficult to know the extent of an onchange.
Since several onchange methods may set the same fields, it easily becomes difficult to track where a value is coming from.

> **Note** \
> Prefer _computed fields_ over the _onchanges_

When using stored computed fields, pay close attention to the dependencies.
When computed fields depend on other computed fields, changing a value can trigger a large number of recomputations.
This leads to poor performance.

# Action
Documentation: [Actions](https://www.odoo.com/documentation/16.0/developer/reference/backend/actions.html#reference-actions)
and [Error management](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#reference-exceptions)

For example, to link business logic with a button in common way is:

1> Add a button in the view, e.g. in the `header` of the view:
```xml
<form>
    <header>
        <!--
        By assigning type="object" to our button, the Odoo framework will execute a Python method
        with name="action_do_something" on the given model.
        -->
        <button name="action_do_something" type="object" string="Do Something"/>
    </header>
    <sheet>
        <field name="name"/>
    </sheet>
</form>
```
2> And link this button to business logic:
```python
from odoo import fields, models

class TestAction(models.Model):
    _name = "test.action"

    name = fields.Char()

    def action_do_something(self):
        """
        Note 1: this method isn’t prefixed with an underscore (_), thus it is public and can be called directly from
                the Odoo interface (through an RPC call).
        Note 2: you should always define your methods as private unless they need to be called from the user interface.
        Note 3: we loop on 'self'. Always assume that a method can be called on multiple records; for re-usability.
        Note 4: public method always return something so that it can be called through XML-RPC.
                When in doubt, just return true.
        """
        for record in self:
            record.name = "Something"
        return True
```

Another good example is this [button in a view](https://github.com/odoo/odoo/blob/cd9af815ba591935cda367d33a1d090f248dd18d/addons/crm/views/crm_lead_views.xml#L9-L11)
and its [corresponding Python method](https://github.com/odoo/odoo/blob/cd9af815ba591935cda367d33a1d090f248dd18d/addons/crm/models/crm_lead.py#L746-L760)
