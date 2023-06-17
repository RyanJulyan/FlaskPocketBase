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
    column_display_pk = False  # display primary keys
    page_size = 500  # number of entries to display on list view

    def is_accessible(self) -> bool:
        # Only allow access to admins and managers
        return any(
            [
                current_user.has_role("admin"),
                current_user.has_role(self.__class__.__name__),
            ]
        )

    def inaccessible_callback(self, **kwargs: Any) -> BaseResponse:
        # redirect to login page if user doesn't have access
        return redirect(url_for("security.login", next=request.url))

    def is_action_allowed(self, name: str) -> bool:
        # Check if user has role
        if name not in [
            "create",
            "edit",
            "delete",
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
