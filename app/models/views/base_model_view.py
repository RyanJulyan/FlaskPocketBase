from flask_admin.contrib.sqla import ModelView


class BaseModelView(ModelView):
    # Default configurations
    can_create = True
    can_edit = True
    can_delete = True
    column_display_pk = False  # display primary keys
    page_size = 100  # number of entries to display on list view
