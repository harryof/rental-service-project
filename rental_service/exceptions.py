class InvalidPropertyError(Exception):
    """Ошибка: некорректные данные о недвижимости."""
    pass


class PermissionDeniedError(Exception):
    """Ошибка: у пользователя нет прав доступа."""
    pass


class RentalNotFoundError(Exception):
    """Ошибка: аренда не найдена."""
    pass
