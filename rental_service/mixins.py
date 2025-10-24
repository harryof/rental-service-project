import logging


# Настройка логгера — он будет писать в файл и в консоль
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("rental_service.log", encoding="utf-8"),  # лог в файл
        logging.StreamHandler()  # лог в консоль
    ]
)


class LoggingMixin:
    """Миксин для логирования действий с объектами недвижимости."""

    def log_action(self, action: str):
        """Логирует указанное действие."""
        class_name = self.__class__.__name__
        logging.info(f"{class_name} - {action}")
        return f"{class_name} - {action}"


class NotificationMixin:
    """Миксин для отправки уведомлений пользователям."""

    def send_notification(self, message: str):
        """Имитация отправки уведомления пользователю."""
        notification = f"[Уведомление] {message}"
        print(notification)  # выводим в консоль (для демонстрации)
        logging.info(notification)  # и записываем в лог
        return notification
