from functools import wraps


def has_role(user, roles):
    if roles == "any":
        return True
    return any(role in user.roles for role in roles)


def has_permission(user, permissions):
    if permissions == "any":
        return True
    return any(
        permission in role.permissions
        for role in user.roles
        for permission in permissions
    )


def requires(roles=None, permissions=None, use_function_name_as_role=False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_user()  # You'll need to define this function

            if use_function_name_as_role and not roles:
                roles = [f.__name__]

            if roles is not None and not isinstance(roles, (list, tuple)):
                roles = [roles]
            if permissions is not None and not isinstance(
                permissions, (list, tuple)
            ):
                permissions = [permissions]

            if roles and not has_role(user, roles):
                return "Role Required", 403
            if permissions and not has_permission(user, permissions):
                return "Permission Denied", 403

            return f(*args, **kwargs)

        return decorated_function

    return decorator
