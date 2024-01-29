# Odoo 16.0 - Technical Training

The Technical Training of Odoo 16.0 is available on the
[Tutorial](https://www.odoo.com/documentation/master/developer/howtos/rdtraining.html) or [Getting started](https://www.odoo.com/documentation/master/developer/tutorials/getting_started.html)

[Developer Mode](https://www.odoo.com/documentation/16.0/applications/general/developer_mode.html)

[Solutions](https://github.com/odoo/technical-training-solutions/tree/16.0-core) to this training

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

To link an action to a button use `type="action"` and refer to the external identifier of acton in the name.
```xml
<button type="action" name="%(test.test_model_action)d" string="My Action"/>
```

# Constraints
One of purposes of constraints is to prevent users from entering incorrect data.
For example prevent users from setting negative price.

Odoo provides two ways to set up automatically verified invariants:
1. [Python constraints](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#odoo.api.constrains) and 
2. SQL constraints.

## SQL
Documentation: [Models](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#reference-orm-models)
and [PostgreSQL’s documentation](https://www.postgresql.org/docs/12/ddl-constraints.html)

SQL constraints are defined through the model attribute `_sql_constraints`.
This attribute is assigned a list of triples containing strings `(name, sql_definition, message)`, where:
1. `name` is a valid SQL constraint name
2. `sql_definition` is a [table_constraint](https://www.postgresql.org/docs/12/ddl-constraints.html) expression
3. `message` is the error message

You can find a simple example [here](https://github.com/odoo/odoo/blob/24b0b6f07f65b6151d1d06150e376320a44fd20a/addons/analytic/models/analytic_account.py#L20-L23).

## Python
Documentation: [constrains()](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#odoo.api.constrains)

Python constraints are necessary to make more complex checks which require Python code.

A Python constraint is defined as a method decorated with [`@api.constrains`](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#odoo.api.constrains)
and is invoked on a recordset.
The decorator specifies which fields are involved in the constraint.
The constraint is automatically evaluated when any of these fields are modified.
The method should raise an exception (usually `ValidationError`) if its invariant is not satisfied:
```python
from odoo import api, fields
from odoo.exceptions import ValidationError

@api.constrains('date_end')
def _check_date_end(self):
    for record in self:
        if record.date_end < fields.Date.today():
            raise ValidationError("The end date cannot be set in the past")
    # all records passed the test, don't return anything
```

A simple example can be found [here](https://github.com/odoo/odoo/blob/274dd3bf503e1b612179db92e410b336bfaecfb4/addons/stock/models/stock_quant.py#L239-L244).

SQL constraints are usually more efficient than Python constraints.
When performance matters, always prefer SQL to Python constraints.

# Add The Sprinkles
Documentation: [Views](https://www.odoo.com/documentation/16.0/developer/reference/backend/views.html#reference-views)

## Inline Views
In some cases we want to define a specific list view which is only used in the context of a form view.
For example, we would like to display the list of properties linked to a property type.
However, we only want to display 3 fields for clarity: `name`, `expected price` and `state`.

To do this, we can define _inline_ list views. An inline list view is defined directly inside a form view.
For example:
```python
from odoo import fields, models

class TestModel(models.Model):
    _name = "test_model"
    _description = "Test Model"

    description = fields.Char()
    line_ids = fields.One2many("test_model_line", "model_id")


class TestModelLine(models.Model):
    _name = "test_model_line"
    _description = "Test Model Line"

    model_id = fields.Many2one("test_model")
    field_1 = fields.Char()
    field_2 = fields.Char()
    field_3 = fields.Char()
```

```xml
<form>
    <field name="description"/>
    <field name="line_ids">
        <tree>
            <field name="field_1"/>
            <field name="field_2"/>
        </tree>
    </field>
</form>
```

In the form view of the `test_model`, we define a specific list view for `test_model_line` with fields `field_1` and `field_2`.

An example can be found [here](https://github.com/odoo/odoo/blob/0e12fa135882cd5095dbf15fe2f64231c6a84336/addons/event/views/event_tag_views.xml#L27-L33).

## Widgets
Documentation: [Field Widgets](https://www.odoo.com/documentation/16.0/developer/reference/frontend/javascript_reference.html#reference-js-widgets)

Widget is about how fields would look in UI.
Odoo chooses the right ‘widget’ depending on the field type.

However, in some cases, we want a specific representation of a field which can be done thanks to the `widget` attribute.
(Search for `"widget"` within estate module views for some examples).

Each field type has a set of widgets which can be used to fine tune its display.
Some widgets also take extra options.
An exhaustive list can be found in [Field Widgets](https://www.odoo.com/documentation/16.0/developer/reference/frontend/javascript_reference.html#reference-js-widgets).

[Another good example](https://github.com/odoo/odoo/blob/0e12fa135882cd5095dbf15fe2f64231c6a84336/addons/account/views/account_bank_statement_views.xml#L136) of `statusbar` widget.

> **Warning** \
> Add a field only **once** to a list or a form view. Adding it multiple times is not supported.

## List Order
Documentation: [Models](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#reference-orm-models)

By default, the records are retrieved in a non-deterministic order depending on PostgreSQL.

Odoo provides several ways to set a default order.

### `_order` field of model

The most common way is to define the `_order` attribute directly in the model.

The `_order` attribute takes a string containing a list of fields which will be used for sorting.
It will be converted to an [order_by](https://www.postgresql.org/docs/12/queries-order.html) clause in SQL.
For example:
```python
from odoo import fields, models

class TestModel(models.Model):
    _name = "test_model"
    _description = "Test Model"
    _order = "id desc"

    description = fields.Char()
```

`_order` field way of ordering has the advantage of a consistent order everywhere a list of records is retrieved.

### `_default_order` attribute of `<tree>` view
It is also possible to define a specific order directly in a view thanks to the `default_order` attribute
([Example](https://github.com/odoo/odoo/blob/892dd6860733c46caf379fd36f57219082331b66/addons/crm/report/crm_activity_report_views.xml#L30))
```xml
<tree default_order="date desc">...</tree>
```

### Manual
Manual order by drag the record up and down in the list.

To do so, a `sequence` field is used in combination with the `handle` widget.
Obviously the `sequence` field must be the first field in the `_order` attribute.

For example:
```python
from odoo import fields
...
_order = 'sequence, name'
sequence = fields.Integer('Sequence', default=1, help="Used to order property types.")
```
```xml
<tree string="Property Types">
    <field name="sequence" widget="handle"/>
    <field name="name"/>
</tree>
```

## Attributes and options

### Prevent inline `Many2one` item creation and editing
Documentation: [widget `many2one (FieldMany2One)`](https://www.odoo.com/documentation/16.0/developer/reference/frontend/javascript_reference.html#relational-fields)
```xml
<field name="property_type_id" options="{'no_create': True}"/>
```

### Tags color
Documentation: [widget `many2many_tags (FieldMany2ManyTags)`](https://www.odoo.com/documentation/16.0/developer/reference/frontend/javascript_reference.html#relational-fields)

To give tags a color:\
1> Add `color` field to model.
```python
from odoo import fields
color = fields.Integer()
```
2> Add `color_field` option to `Many2many` field:
```xml
<field name="tag_ids" widget="many2many_tags" string="Tags" options="{'color_field': 'color'}"/>
```

### Show buttons for specific states
Documentation: [`states` attr of `<button>`](https://www.odoo.com/documentation/16.0/developer/reference/backend/views.html#list)

A `state` field is used in combination with a `states` attribute in the view to display buttons conditionally.
For example:
```xml
<button name="action_sold_property" type="object" string="Sold" states="new,received,accepted"/>
```

### `invisible` option and attribute
It is possible to make a field `invisible`, `readonly` or `required` based on the value of other fields thanks
to the `attrs` attribute.

Note that `invisible` can also be applied to other elements of the view such as `button` or `group`.

The `attrs` is a dictionary with the property as a key and a domain as a value:
```xml
<form>
    <!--
        The `description` field is invisible when `is_partner` is `False`.
        It is important to note that a field used in an `attrs` **must** be present in the view.
        If it should not be displayed to the user, we can use the `invisible` attribute to hide it.
    -->
    <field name="description" attrs="{'invisible': [('is_partner', '=', False)]}"/>
    <field name="is_partner" invisible="1"/>
</form>
```

> **Warning**\
> Using a (conditional) readonly attribute in the view can be useful to prevent data entry errors,
> but keep in mind that it doesn't provide any level of security!
> There is no check done server-side, therefore it’s always possible to write on the field through an RPC call.

### Attributes and Options :: List
When the model only has a few fields, it can be useful to edit records directly through the list view and not have
to open the form view.
This can be achieved thanks to the `editable` attribute:
```xml
<tree editable="bottom">...</tree>
```

When a model has a lot of fields some of them can be optionally hidden to fit into the list using `optional` attribute
([documentation](https://www.odoo.com/documentation/16.0/developer/reference/backend/views.html#list)):
```xml
<field name="date_availability" optional="hide"/>
```

Color codes are useful to visually emphasize records:
[Decorations](https://www.odoo.com/documentation/16.0/developer/reference/frontend/javascript_reference.html#decorations)
```xml
<field name="state" decoration-danger="amount &lt; 10000"/>
```
```xml
<!-- The records where `is_partner` is `True` will be displayed in green. -->
<tree decoration-success="is_partner==True">
    <field name="name"/>
    <field name="is_partner" invisible="1"/>
</tree>
```

> **Warning**\
> Keep in mind that **all** fields used in attributes must be in the view!

### Attributes and Options :: Search
Documentation:
[Search](https://www.odoo.com/documentation/16.0/developer/reference/backend/views.html#reference-views-search) and
[Search defaults](https://www.odoo.com/documentation/16.0/developer/reference/backend/views.html#reference-views-search-defaults)

To have filter applied by default it's necessary to use `search_default_{$name}` action context,
where `{$name}` is the filter name.

Here is an example of an
[action](https://github.com/odoo/odoo/blob/6decc32a889b46947db6dd4d42ef995935894a2a/addons/crm/report/crm_opportunity_report_views.xml#L115)
with its
[corresponding filter](https://github.com/odoo/odoo/blob/6decc32a889b46947db6dd4d42ef995935894a2a/addons/crm/report/crm_opportunity_report_views.xml#L68).

For example:
```xml
<!-- Make filter 'filter_available' default -->
<field name="context">{'search_default_filter_available': True}</field>
```

Search view `<field>` elements can have a `filter_domain` that overrides the domain generated for searching
on the given field.
In the given domain, `self` represents the value entered by the user.
In the example below, it is used to search on both `name` and `description` fields.
```xml
<search string="Test">
    <field name="description" string="Name and description"
           filter_domain="['|', ('name', 'ilike', self), ('description', 'ilike', self)]"/>
</search>
```

## Stat Buttons
_Stat Buttons_ are displayed on the top right of a form view and give quick access to linked documents.

Search for some examples in the Odoo codebase for `oe_stat_button`.

Documentation about the concept of [Related fields](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#reference-fields-related).

To understand concept of _Related fields_ consider following example of definition of the `description` field:
```python
from odoo import fields

partner_id = fields.Many2one("res.partner", string="Partner")
description = fields.Char(related="partner_id.name")
```
is equivalent to:
```python
from odoo import fields, api

partner_id = fields.Many2one("res.partner", string="Partner")
description = fields.Char(compute="_compute_description")

@api.depends("partner_id.name")
def _compute_description(self):
    for record in self:
        record.description = record.partner_id.name
```
Every time the partner name is changed, the description is modified.

# Inheritance
It's about extending functionality of an existing module.

## Python Inheritance
CRUD actions are already included in our model thanks to classical Python inheritance:
```python
from odoo import models

class TestModel(models.Model):
    _name = "test_model"
    _description = "Test Model"

    ...
```
Our class TestModel inherits from [Model](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#odoo.models.Model)
which provides
[create()](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#odoo.models.Model.create),
[read()](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#odoo.models.Model.read),
[write()](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#odoo.models.Model.write) and
[unlink()](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#odoo.models.Model.unlink).

These methods (and any other method defined on
[Model](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#odoo.models.Model))
can be extended to add specific business logic:
```python
from odoo import models, api

class TestModel(models.Model):
    _name = "test_model"
    _description = "Test Model"

    ...

    @api.model
    def create(self, vals):
        # Do some business logic, modify vals...
        ...
        # Then call super to execute the parent method
        return super().create(vals)
```
The decorator [model()](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#odoo.api.model)
is necessary for the [create()](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#odoo.models.Model.create)
method because the content of the recordset `self` is not relevant in the context of creation, but it is not necessary for the other CRUD methods.

> **Warning** \
> Instead of directly override
> [unlink()](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#odoo.models.Model.unlink)
> method, it's better to write a new method decorated with
> [ondelete()](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#odoo.api.ondelete) instead.
> Methods decorated with `ondelete()` are called during `unlink()` and avoid some issues that can occur during
> uninstalling the model's module when `unlink()` is directly overriden.

> **Danger**
> * It is very important to **always** call `super()` to avoid breaking the flow.
>   There are only a few very specific cases where you don’t want to call it.
> * Make sure to **always** return data consistent with the parent method.
>   For example, if the parent method returns a `dict()`, your override must also return a `dict()`.

## Model Inheritance
Documentation: [Inheritance and extension](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#reference-orm-inheritance)

A practical example where two fields are added to a model can be found
[here](https://github.com/odoo/odoo/blob/60e9410e9aa3be4a9db50f6f7534ba31fea3bc29/addons/account_fleet/models/account_move.py#L39-L47).

## View Inheritance
Documentation: [Inheritance](https://www.odoo.com/documentation/16.0/developer/reference/backend/views.html#reference-views-inheritance)

An extension view references its parent using the inherit_id field. Instead of a single view, its arch field contains
a number of xpath elements that select and alter the content of their parent view:
```xml
<record id="inherited_model_view_form" model="ir.ui.view">
    <field name="name">inherited.model.form.inherit.test</field>
    <field name="model">inherited.model</field>
    <field name="inherit_id" ref="inherited.inherited_model_view_form"/>
    <field name="arch" type="xml">
        <!-- find field description and add the field
             new_field after it -->
        <xpath expr="//field[@name='description']" position="after">
          <field name="new_field"/>
        </xpath>
    </field>
</record>
```

* `expr`\
  An XPath expression selecting a single element in the parent view. Raises an error if it matches no element or more than one
* `position`\
  Operation to apply to the matched element:
  * `inside`\
    appends xpath’s body to the end of the matched element
  * `replace`\
    replaces the matched element with the xpath’s body, replacing any $0 node occurrence in the new body with the original element
  * `before`\
    inserts the xpath’s body as a sibling before the matched element
  * `after`\
    inserts the xpaths’s body as a sibling after the matched element
  * `attributes`\
    alters the attributes of the matched element using the special attribute elements in the xpath’s body

An example of a view inheritance extension can be found
[here](https://github.com/odoo/odoo/blob/691d1f087040f1ec7066e485d19ce3662dfc6501/addons/account_fleet/views/account_move_views.xml#L3-L17).

An example of inheritance of the users’ view can be found [here](https://github.com/odoo/odoo/blob/691d1f087040f1ec7066e485d19ce3662dfc6501/addons/gamification/views/res_users_views.xml#L5-L14).

# Interact With Other Modules
Any time we interact with another module, we need to keep in mind the modularity.
If we intend to sell our application to real estate agencies, some may want the invoicing feature but others may not want it.

The common approach for such use cases is to create a _‘link’_ module.
In our case, the module would depend on `estate` and `account` and would include the invoice creation logic
of the estate property.
This way the real estate and the accounting modules can be installed independently.
When both are installed, the link module provides the new feature.

# A Brief History Of QWeb
Documentation: [QWeb Templates](https://www.odoo.com/documentation/16.0/developer/reference/frontend/qweb.html#reference-qweb)

QWeb is the primary templating engine used by Odoo.
It is an XML templating engine and used mostly to generate HTML fragments and pages.

## A Kanban View
Documentation: [Kanban](https://www.odoo.com/documentation/16.0/developer/reference/backend/views.html#reference-views-kanban)

Kanban board is when the records are displayed in a card-like structure.

The definition of a Kanban view is similar to the definition of the list and form views,
except that their root element is `<kanban>`.

In its simplest form, a Kanban view looks like:
```xml
<kanban>
    <templates>
        <t t-name="kanban-box">
            <div class="oe_kanban_global_click">
                <field name="name"/>
            </div>
        </t>
    </templates>
</kanban>
```
Breaking down this example:
* `<templates>`: defines a list of [QWeb Templates](https://www.odoo.com/documentation/16.0/developer/reference/frontend/qweb.html#reference-qweb).
  Kanban views _must_ define at least one root template `kanban-box`, which will be rendered once for each record.
* `<t t-name="kanban-box">`: `<t>` is a placeholder element for QWeb directives. 
  In this case, it is used to set the `name` of the template to `kanban-box`
* `<div class="oe_kanban_global_click">`: the `oe_kanban_global_click` makes the `<div>` clickable to open the record.
* `<field name="name"/>`: this will add the `name` field to the view.

If we want to display an element conditionally, we can use the `t-if` directive
(see [Conditionals](https://www.odoo.com/documentation/16.0/developer/reference/frontend/qweb.html#reference-qweb-conditionals)):
```xml
<kanban>
    <!-- 'state' field is outside '<templates>' element - if we need the value of a field but don't want to display
         it in the view. -->
    <field name="state"/>
    <templates>
        <t t-name="kanban-box">
            <div class="oe_kanban_global_click">
                <field name="name"/>
                <!-- the '<div>' element is rendered if the condition is true -->
                <div t-if="record.state.raw_value == 'new'">
                    This is new!
                </div>
            </div>
        </t>
    </templates>
</kanban>
```
`record` is an object with all the requested fields as its attributes.
Each field has two attributes `value` and `raw_value`.
The former is formatted according to current user parameters and the latter is the direct value from a
[read()](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#odoo.models.Model.read).

# Module Data

## Data Types
There are two:
1. Master Data
2. Demo Data

### Master Data
Master data is usually part of the technical or business requirements for the module.
In other words, such data is often necessary for the module to work properly.
This data will always be installed when installing the module.

Example of technical data are
[views](https://www.odoo.com/documentation/16.0/developer/reference/backend/views.html#reference-views) and
[actions](https://www.odoo.com/documentation/16.0/developer/reference/backend/actions.html#reference-actions).
Those are one kind of master data.

On top of technical data, business data can be defined, e.g. _countries_, _currencies_, _units of measure_,
as well as complete country localization (legal reports, tax definitions, chart of account), and much more...

### Demo Data
In additional to master data, which are requirements for a module to work properly,
we also like having data for demonstration purposes:
* Help the sales representatives make their demos quickly.
* Have a set of working data for developers to test new features and see how these new features look with
  data they might not have added themselves.
* Test that the data is loaded correctly, without raising an error.
* Setup most of the features to be used quickly when creating a new database.

Demo data is automatically loaded when you start the server if you don’t explicitly say you don’t want it.
This can be done in the database manager or with the command line:
```bash
$  ./odoo-bin --addons-path=... -d db -i account --without-demo=all
```

## Data Declaration

### Manifest
Documentation: [Module Manifests](https://www.odoo.com/documentation/16.0/developer/reference/backend/module.html#reference-module-manifest)

Data is declared either in CSV or in XML. Each file containing data must be added in the manifest for them to be loaded.

The keys to use in the manifest to add new data are:
1. `data` for the master data; includes list of files in following folders:
   * `views` folder for views and actions
   * `security` folder for security related data
   * `data` folder for other data
2. `demo` for the demo data; includes list of files only in one folder:
   * `demo` folder for demo data

Folder tree looks like:
```
estate
├── data
│   └── master_data.xml
├── demo
│   └── demo_data.xml
├── models
│   ├── *.py
│   └── __init__.py
├── security
│   └── ir.model.access.csv
├── views
│   └── estate_property_offer_views.xml
├── __init__.py
└── __manifest__.py
```

Manifest looks like:

```python
# -*- coding: utf-8 -*-
# noinspection PyStatementEffect
{
  "name": "Real Estate",
  "depends": [
    ...
  ],
  "data": [
    "security/ir.model.access.csv",  # CSV and XML files are loaded at the same place
    "views/estate_property_offer_views.xml",  # Views are data too
    "data/master_data.xml",  # Split the data in multiple files depending on the model
  ],
  "demo": [
    "demo/demo_data.xml",
  ],
  "application": True,
}
```

### CSV
Documentation: [CSV data files](https://www.odoo.com/documentation/16.0/developer/reference/backend/data.html#reference-data-csvdatafiles)

The easiest way to declare simple data is by using the CSV format.
This is however limited in terms of features: use it for long lists of simple models, but prefer XML otherwise.
```csv
id,field_a,field_b,related_id:id
id1,valueA1,valueB1,module.relatedid
id2,valueA2,valueB2,module.relatedid
```

### XML
Documentation: [Data Files](https://www.odoo.com/documentation/16.0/developer/reference/backend/data.html#reference-data)

When data is more complex than XML should be used rather than CSV:
```xml
<!-- `odoo` is the root element of the data file -->
<odoo>
  <record id="id1" model="tutorial.example">
    <field name="field_a">valueA1</field>
    <field name="field_b">valueB1</field>
  </record>

  <record id="id2" model="tutorial.example">
    <field name="field_a">valueA2</field>
    <field name="field_b">valueB2</field>
  </record>
</odoo>
```

#### Data Extension
`eval` is used if you need to compute the value. For example:
```xml
<odoo>
  <record id="id1" model="tutorial.example">
    <field name="year" eval="datetime.now().year+1"/>
  </record>
</odoo>
```

`search` is used if you need the ORM to do a _search_:
```xml
<odoo>
  <record id="id1" model="account.move.line">
    <field name="account_id" search="[
      ('user_type_id', '=', ref('account.data_account_type_direct_costs')),
      ('company_id', '=', obj().env.company.id)]
    "/>
  </record>
</odoo>
```

`function` is needed to execute python code when loading data:
```xml
<function model="tutorial.example" name="action_validate">
    <value eval="[ref('demo_invoice_1')]"/>
</function>
```

### Add X2many fields
Documentation: [Command](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#odoo.fields.Command)

[Command](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#odoo.fields.Command) is used
to add related data in One2many or Many2many field:
```xml
<odoo>
  <record id="id1" model="tutorial.example">
    <field name="related_ids" eval="[
        Command.create({
            'name': 'My name',
        }),
        Command.create({
            'name': 'Your name',
        }),
        Command.link(ref('model.xml_id')),
    ]"/>
  </record>
</odoo>
```
For example offers in _Trailer home_ property: [estate.property.xml](./estate/data/estate.property.xml)

## Accessing the data
> **Warning**\
> You should **never** access demo data outside the demo data declaration, not even in tests.

### In python
In python code, you can use the `env.ref(self, xml_id, raise_if_not_found=True)` method.
It returns the recordset linked to the `xml_id` you specify.

### In XML
In XML, you can use the `ref` key like this:
```xml
<odoo>
  <record id="id1" model="tutorial.example">
    <field name="related_id" ref="module.relatedid"/>
  </record>
</odoo>
```

### In CSV
The title of the column must be suffixed with `:id` or `/id` :
```csv
id,parent_id:id,name
"child1","module.parent","Name1"
"child2","module.parent","Name2"
"child3","module.parent","Name3"
```
For example: [list of country states](https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/res.country.state.csv)

## Advanced

### External id or XML id
Because we don’t want a column `xml_id` in every single SQL table of the database, we need a mechanism to store it.
This is done with the `ir.model.data` model.

To get list of external id (xml_id) from DB:
```sql
SELECT * FROM public.ir_model_data where model like 'estate%';
```

### No update
The records created with the `noupdate` flag won’t be updated when upgrading the module that created them,
but it will be created if it didn't exist yet:
```xml
<odoo noupdate="1">
  <record id="id1" model="model">
    <field name="fieldA" eval="True"/>
  </record>
</odoo>
```
> **Note**\
> `odoo-bin -i module` will bypass this setting and always load the data.
> But normally one shouldn’t do this on a production database.

### Import as SQL
In some cases, it makes sense to do the import directly in SQL.
This is however discouraged as it bypasses all the features of the ORM,
computed fields (including metadata) and python constraints.

* It can help to speed the import time by a lot
   [with huge files](https://github.com/odoo/enterprise/blob/d46cceef8c594b9056d0115edb7169e207a5986f/product_unspsc/hooks.py#L19).
* For more complex imports like for the
   [translations](https://github.com/odoo/odoo/blob/e1f8d549895cd9c459e6350430f30d541d02838a/odoo/addons/base/models/ir_translation.py#L24).
* It can be necessary to
   [initialize the database](https://github.com/odoo/odoo/blob/e1f8d549895cd9c459e6350430f30d541d02838a/odoo/addons/base/data/base_data.sql).

> **Note**\
> Generally using raw SQL also bypasses ACLs and increases the risks of injections.
> Reference: [Security in Odoo](https://www.odoo.com/documentation/16.0/developer/reference/backend/security.html#reference-security)

# Restrict access to data

## Groups
Documentation: [the security reference](https://www.odoo.com/documentation/16.0/developer/reference/backend/security.html#reference-security)

In keeping with Odoo’s data-driven nature, a group is no more than a record of the `res.groups` model.
They are normally part of a module’s [master data](https://www.odoo.com/documentation/16.0/developer/tutorials/define_module_data.html),
defined in one of the module’s data files.

As simple example [can be found here](https://github.com/odoo/odoo/blob/532c083cbbe0ee6e7a940e2bdc9c677bd56b62fa/addons/hr/security/hr_security.xml#L9-L14).

## Access Rights
Documentation: [Access Rights](https://www.odoo.com/documentation/16.0/developer/reference/backend/security.html#reference-security-acl)

Access rights are a way to give users access to models via groups: associate an access right to a group,
then all users with that group will have the access.

> **Note**
> * The group of an access right can be omitted, this means the ACL applies to every user,
>    this is a useful but risky fallback as depending on the applications installed
>    it can grant even non-users access to the model.
> * If no access right applies to a user, they are not granted access (default-deny).
> * If a menu item points to a model to which a user doesn't have access and has no submenus which the user can see,
>    the menu will not be displayed.

## Record Rules
Documentation: [Record Rules](https://www.odoo.com/documentation/16.0/developer/reference/backend/security.html#reference-security-rules)

Record _rules_ can grant or reject access to individual records:
```xml
<record id="rule_id" model="ir.rule">
    <field name="name">A description of the rule's role</field>
    <field name="model_id" ref="model_to_manage"/>
    <field name="perm_read" eval="False"/>
    <field name="groups" eval="[Command.link(ref('base.group_user'))]"/>
    <field name="domain_force">[
        '|', ('user_id', '=', user.id),
             ('user_id', '=', False)
    ]</field>
</record>
```
The [Search domains](https://www.odoo.com/documentation/16.0/developer/reference/backend/orm.html#reference-orm-domains)
is how access is managed: if the record passes then access is granted, otherwise access is rejected.

## Security Override
### Bypassing Security
There are two main ways to bypass existing security checks in Odoo, either wilfully or as a side effect:
* The `sudo()` method will create a new recordset in _“sudo mode”_, this ignores all access rights and record rules
   (although hard-coded group and user checks may still apply).
* Performing raw SQL queries will bypass access rights and record rules as a side effect of bypassing the ORM itself.

> **Danger**\
> These features should generally be avoided, and only used with extreme care, after having checked that
> the current user and operation should be able to bypass normal access rights validation.
> Operations performed in such modes should also rely on user input as little as possible,
> and should validate it to the maximum extent they can.

### Programmatically checking security
Therefore, when performing non-CRUD operations, or legitimately bypassing the ORM or security, or when triggering other
side effects, it is extremely important to perform explicit security checks.

Explicit security checks can be performed by:
* Checking who the current user is (`self.env.user`) and match them against specific models or records.
* Checking that the current user has specific groups hard-coded to allow or deny an operation (`self.env.user.has_group`).
* Calling the `check_access_rights(operation)` method on a recordset, this verifies whether the current user
   has access to the model itself.
* Calling `check_access_rule(operations)` on a non-empty recordset, this verifies that the current user
   is allowed to perform the operation on _every_ record of the set.

> **Warning**\
> Checking access rights and checking record rules are separate operations,
> if you’re checking record rules you usually want to also check access rights beforehand.

## Multi-company security

> **See also**\
> [Multi-company Guidelines](https://www.odoo.com/documentation/16.0/developer/howtos/company.html#reference-howtos-company)
> for an overview of multi-company facilities in general, and
> [multi-company security rules](https://www.odoo.com/documentation/16.0/developer/howtos/company.html#howto-company-security) in particular.

Multi-company rules are simply record rules based on the `company_ids` or `company_id` fields:
* `company_ids` is all the companies to which the current user has access
* `company_id` is the currently active company (the one the user is currently working in / for).
Multi-company rules will _usually_ use the former i.e. check if the record is associated with _one_ of the companies the user has access to:
```xml
<record model="ir.rule" id="hr_appraisal_plan_comp_rule">
    <field name="name">Appraisal Plan multi-company</field>
    <field name="model_id" ref="model_hr_appraisal_plan"/>
    <field name="domain_force">[
        '|', ('company_id', '=', False),
             ('company_id', 'in', company_ids)
    ]</field>
</record>
```

> **Danger**\
> Multi-company rules are usually [global](https://www.odoo.com/documentation/16.0/developer/reference/backend/security.html#reference-security-rules-global),
> otherwise there is a high risk that additional rules would allow bypassing the multi-company rules.

## Visibility != Security

* _Visibility_ features mean a user can still access the model or record otherwise, either through another part
   of the interface or by [performing operations remotely using RPC](https://www.odoo.com/documentation/16.0/developer/reference/external_api.html),
   things might just not be visible in the web interface in some contexts.
* _Security_ features mean a user can not access records, fields or operations.

Examples:
* In server actions [only system users can see or update Python code.](https://github.com/odoo/odoo/blob/7058e338a980268df1c502b8b2860bdd8be9f727/odoo/addons/base/models/ir_actions.py#L414-L417)
* [only managers have an immediate filter to see their teams’ leaves.](https://github.com/odoo/odoo/blob/8e19904bcaff8300803a7b596c02ec45fcf36ae6/addons/hr_holidays/report/hr_leave_reports.xml#L16)
* [only system administrators can see the elearning settings menu.](https://github.com/odoo/odoo/blob/ff828a3e0c5386dc54e6a46fd71de9272ef3b691/addons/website_slides/views/website_slides_menu_views.xml#L64-L69)

# Unit Tests
Documentation: [Odoo’s Test Framework: Learn Best Practices](https://www.youtube.com/watch?v=JEIscps0OOQ) (Odoo Experience 2020) on YouTube.

Writing tests is a necessity for multiple reasons. Here is a non-exhaustive list:
* Ensure code will not be broken in the future
* Define the scope of your code
* Give examples of use cases
* It is one way to technically document the code
* Help your coding by defining your goal before working towards it

## Running Tests
Run all the tests of account, and modules installed by account the dependencies already installed are not tested
this takes some time because you need to install the modules, but `at_install` and `post_install` are respected:
```bash
$ odoo-bin -i account --test-enable
```

Run all the tests in this file:
```bash
$ odoo-bin --test-file=addons/account/tests/test_account_move_entry.py
```

Test tags can help you filter quite easily:
```bash
$ odoo-bin --test-tags=/account:TestAccountMove.test_custom_currency_on_account_1
```

## CI: Integration Bots

### Runbot
Documentation: [Runbot FAQ](https://runbot.odoo.com/doc)

### Robodoo

### Mergebot
Documentation: [Mergebot](https://mergebot.odoo.com/)

## Modules
Because Odoo is modular, the tests need to be also modular.
This means tests are defined in the module that adds the functionality you are adding in,
and tests cannot depend on functionality coming from modules your module doesn't depend on.

Documentation: [Special Tags](https://www.odoo.com/documentation/16.0/developer/reference/backend/testing.html#reference-testing-tags)
```python
from odoo.tests.common import TransactionCase
from odoo.tests import tagged

# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
@tagged('post_install', '-at_install')  # add `post_install` and remove `at_install`
class PostInstallTestCase(TransactionCase):
    def test_01(self):
        ...

@tagged('at_install')  # this is the default
class AtInstallTestCase(TransactionCase):
    def test_01(self):
        ...
```
If the behavior you want to test can be changed by the installation of another module,
you need to ensure that the tag `at_install` is set; otherwise, you can use the tag `post_install`
to speed up the CI and ensure it is not changed if it shouldn’t.

## Writing a test
Documentation: [Python unittest](https://docs.python.org/3/library/unittest.html) and
[Testing Odoo](https://www.odoo.com/documentation/16.0/developer/reference/backend/testing.html#reference-testing)

Here are a few things to take into consideration before writing a test:
* The tests should be independent of the data currently in the database (including demo data)
* Tests should not impact the database by leaving/changing residual data.
   This is usually done by the test framework by doing a rollback.
   Therefore, you must never call `cr.commit` in a test (nor anywhere else in the business code).
* For a bug fix, the test should fail before applying the fix and pass after.
* Don’t test something that is already tested elsewhere; you can trust the ORM.
   Most of the tests in business modules should only test the business flows.
* You shouldn’t need to flush data into the database.

> **Note**\
> Remember that `onchange` only applies in the Form views, not by changing the attributes in python.
> This also applies in the tests. If you want to emulate a Form view, you can use `odoo.tests.common.Form`.

The tests should be in a `tests` folder at the root of your module.
Each test file name should start with `test_` and be imported in the `__init__.py` of the test folder.
You shouldn’t import the test folder/module in the `__init__.py` of the module.

```
estate
├── models
│   ├── *.py
│   └── __init__.py
├── tests
│   ├── test_*.py
│   └── __init__.py
├── __init__.py
└── __manifest__.py
```
All the tests should extend `odoo.tests.common.TransactionCase`. You usually define a `setUpClass` and the tests.
After writing the `setUpClass`, you have an `env` available in the class and can start interacting with the ORM.

These test classes are built on top of the `unittest` python module.
```python
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged

# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.
@tagged('post_install', '-at_install')
class EstateTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super(EstateTestCase, cls).setUpClass()

        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.
        cls.properties = cls.env['estate.property'].create([...])

    def test_creation_area(self):
        """Test that the total_area is computed like it should."""
        self.properties.living_area = 20
        self.assertRecordValues(self.properties, [
           {'name': ..., 'total_area': ...},
           {'name': ..., 'total_area': ...},
        ])


    def test_action_sell(self):
        """Test that everything behaves like it should when selling a property."""
        self.properties.action_sold()
        self.assertRecordValues(self.properties, [
           {'name': ..., 'state': ...},
           {'name': ..., 'state': ...},
        ])

        with self.assertRaises(UserError):
            self.properties.forbidden_action_on_sold_property()
```
> **Note**\
> For better readability, split your tests into multiple files depending on the scope of the tests.
> You can also have a Common class that most of the tests should inherit from;
> this common class can define the whole setup for the module.
> For instance, in [account](https://github.com/odoo/odoo/blob/16.0/addons/account/tests/common.py).