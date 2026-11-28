# Django admin for data models

Whenever you add a custom Django model that stores data, register the model in
its owning app's `admin.py` as part of the same change. Create the module if
needed and include the model's migration in the same change.

- Start with Django's default registration using `admin.site.register(Model)`.
  Add a `ModelAdmin` when list columns, filters, search, or read-only fields
  help staff inspect the integrated data or support existing access rules.
- Keep Django admin access under the project's existing staff and model
  permissions.
- After applying migrations in the development or test environment, confirm
  that an authorized staff user can find the model in Django admin and view
  a representative record. For an integration, use a record created through
  the integration path.
- Run a read-only query directly against the same database. Compare the
  record's identifier, representative values, and relevant relationships
  with what appears in admin. Record both checks in the change record.
