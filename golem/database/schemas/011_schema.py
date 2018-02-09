# pylint: disable=no-member
# pylint: disable=too-few-public-methods
"""Peewee migrations -- 011_schema.py.

Some examples (model - class or model name)::

    # Return model in current state by name
    > Model = migrator.orm['model_name']

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.python(func, *args, **kwargs)        # Run python code
    > migrator.create_model(Model)                  # Create a model
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.drop_index(model, *col_names)
    > migrator.add_not_null(model, *field_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)

"""

import peewee as pw

from golem.model import PaymentStatus


SCHEMA_VERSION = 11


def migrate(migrator, _database, **_kwargs):
    """Write your migrations here."""

    migrator.drop_index('hardwarepreset', 'name')

    migrator.add_index('hardwarepreset', 'name', unique=True)

    migrator.change_fields('networkmessage',
                           local_role=pw.ActorField(),
                           remote_role=pw.ActorField())

    migrator.change_fields('payment', status=pw.PaymentStatusField(
        default=PaymentStatus.awaiting, index=True
    ))

    migrator.drop_index('performance', 'environment_id')

    migrator.add_index('performance', 'environment_id', unique=True)


def rollback(migrator, _database, **_kwargs):
    """Write your rollback migrations here."""

    migrator.drop_index('performance', 'environment_id')

    migrator.add_index('performance', 'environment_id', unique=True)

    migrator.change_fields('payment', status=pw.EnumField(
        default=PaymentStatus.awaiting, index=True
    ))

    migrator.change_fields('networkmessage',
                           local_role=pw.EnumField(),
                           remote_role=pw.EnumField())

    migrator.drop_index('hardwarepreset', 'name')

    migrator.add_index('hardwarepreset', 'name', unique=True)
