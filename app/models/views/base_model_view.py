from typing import Any
from flask_login import current_user

from werkzeug.wrappers import Response as BaseResponse
from flask import redirect, request, url_for
from flask_admin.contrib.sqla import ModelView

from app.models.data.role import Role


class BaseModelView(ModelView):
    # Default configurations
    can_create = False
    can_edit = False
    can_delete = False
    can_view_details = False
    column_display_pk = False  # display primary keys
    page_size = 500  # number of entries to display on list view

    def valid_check(self, permission_name: str) -> bool:
        class_as_role: Role = current_user.find_role(self.__class__.__name__)

        has_action_as_permission: bool = (
            permission_name in class_as_role.permissions
        )

        return any(
            [
                current_user.has_role("admin"),
                has_action_as_permission,
            ]
        )

    def is_accessible(self) -> bool:
        # Only allow access to admins and managers
        return any(
            [
                current_user.has_role("admin"),
                all(
                    [
                        current_user.is_authenticated,
                        current_user.has_role(self.__class__.__name__),
                    ]
                ),
            ]
        )

    def inaccessible_callback(self, **kwargs: Any) -> BaseResponse:
        # redirect to login page if user doesn't have access
        return redirect(url_for("security.login", next=request.url))

    def on_model_change(self, form, model, is_created) -> Any:
        if is_created:
            permission_name = "create"
            if self.valid_check(permission_name):
                return super(BaseModelView, self).on_model_change(
                    form, model, is_created
                )

            raise PermissionError(
                f"Current user does not have the: `{permission_name}` permission associated with the Role: `{self.__class__.__name__}`"
            )
        else:
            permission_name = "update"
            if self.valid_check(permission_name):
                return super(BaseModelView, self).on_model_change(
                    form, model, is_created
                )

            raise PermissionError(
                f"Current user does not have the: `{permission_name}` permission associated with the Role: `{self.__class__.__name__}`"
            )

    def delete_model(self, model) -> Any:
        permission_name = "delete"
        if self.valid_check(permission_name):
            return super(BaseModelView, self).delete_model(model)

        raise PermissionError(
            f"Current user does not have the: `{permission_name}` permission associated with the Role: `{self.__class__.__name__}`"
        )

    def get_list(self, *args, **kwargs) -> Any:
        permission_name = "list"
        if self.valid_check(permission_name):
            return super(BaseModelView, self).get_list(*args, **kwargs)

        raise PermissionError(
            f"Current user does not have the: `{permission_name}` permission associated with the Role: `{self.__class__.__name__}`"
        )

    def get_one(self, id) -> Any:
        permission_name = "details"
        if self.valid_check(permission_name):
            return super(BaseModelView, self).get_one(id)

        raise PermissionError(
            f"Current user does not have the: `{permission_name}` permission associated with the Role: `{self.__class__.__name__}`"
        )

    def scaffold_filters(self, name) -> Any:
        permission_name = "filter"
        if self.valid_check(permission_name):
            return super(BaseModelView, self).scaffold_filters(name)

        raise PermissionError(
            f"Current user does not have the: `{permission_name}` permission associated with the Role: `{self.__class__.__name__}`"
        )

    def scaffold_sortable_columns(self) -> Any:
        permission_name = "sort"
        if self.valid_check(permission_name):
            return super(BaseModelView, self).scaffold_sortable_columns()

        raise PermissionError(
            f"Current user does not have the: `{permission_name}` permission associated with the Role: `{self.__class__.__name__}`"
        )

    def scaffold_form(self) -> Any:
        permission_name = "scaffold_form"
        if self.valid_check(permission_name):
            return super(BaseModelView, self).scaffold_form()

        raise PermissionError(
            f"Current user does not have the: `{permission_name}` permission associated with the Role: `{self.__class__.__name__}`"
        )

    def is_action_allowed(self, name: str) -> bool:
        print()
        print("is_action_allowed: name")
        print(name)
        print()
        # Check if user has role
        if name not in [
            "create",
            "edit",
            "delete",
            "view",
        ] or not current_user.has_role(self.__class__.__name__):
            return super(BaseModelView, self).is_action_allowed(name)

        class_as_role: Role = current_user.find_role(self.__class__.__name__)

        has_action_as_permission: bool = name in class_as_role.permissions

        valid_check = any(
            [
                current_user.has_role("admin"),
                has_action_as_permission,
            ]
        )

        return valid_check
