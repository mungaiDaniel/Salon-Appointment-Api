"""Authorization decorators. Both **fail closed**: no valid token means no access."""

import functools

from flask_jwt_extended import current_user, jwt_required

from app.auth.model import ROLE_LEVEL
from app.errors import forbidden


def role_required(minimum_role: str):
    """Require a valid JWT whose user holds ``minimum_role`` or higher.

    The role is read from the database on every request (see ``user_lookup_loader``), so
    promotions/demotions take effect immediately and deleted users are locked out.
    """
    required_level = ROLE_LEVEL[minimum_role]

    def decorator(view):
        @functools.wraps(view)
        @jwt_required()
        def wrapper(*args, **kwargs):
            if current_user.role_level < required_level:
                raise forbidden(
                    f"This action requires the '{minimum_role}' role or higher.",
                    code="insufficient_role",
                )
            return view(*args, **kwargs)

        return wrapper

    return decorator
