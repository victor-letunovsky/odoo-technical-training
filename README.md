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
