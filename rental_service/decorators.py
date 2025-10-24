from functools import wraps
from rental_service.exceptions import PermissionDeniedError


def check_permissions(required_role: str):
    """
    Декоратор для проверки прав пользователя перед выполнением метода.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            user_role = getattr(self, "user_role", "guest")
            if user_role != required_role:
                raise PermissionDeniedError(
                    f"Недостаточно прав: требуется '{required_role}', а у пользователя '{user_role}'."
                )
            return func(self, *args, **kwargs)
        return wrapper
    return decorator
