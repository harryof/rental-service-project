from abc import ABC, abstractmethod
from rental_service.decorators import check_permissions
from rental_service.mixins import LoggingMixin, NotificationMixin


class RentalProcess(ABC, LoggingMixin, NotificationMixin):
    """Шаблонный метод для процесса аренды."""

    @check_permissions("manager")
    def rent_property(self, property_obj, tenant_obj):
        """Общий алгоритм аренды."""
        if not self.check_availability(property_obj):
            return "Недвижимость недоступна."

        self.create_agreement(property_obj, tenant_obj)
        self.confirm_rental(property_obj, tenant_obj)
        return "Аренда успешно оформлена."

    @abstractmethod
    def check_availability(self, property_obj) -> bool:
        pass

    @abstractmethod
    def create_agreement(self, property_obj, tenant_obj):
        pass

    @abstractmethod
    def confirm_rental(self, property_obj, tenant_obj):
        pass


class OnlineRentalProcess(RentalProcess):
    """Онлайн процесс аренды."""

    def check_availability(self, property_obj) -> bool:
        return property_obj.is_available

    def create_agreement(self, property_obj, tenant_obj):
        self.log_action(f"Аренда онлайн для {tenant_obj.name} оформляется.")
        property_obj.is_available = False

    def confirm_rental(self, property_obj, tenant_obj):
        self.send_notification(f"Аренда {property_obj.address} подтверждена для {tenant_obj.name} (онлайн).")


class OfflineRentalProcess(RentalProcess):
    """Оффлайн процесс аренды."""

    def check_availability(self, property_obj) -> bool:
        return property_obj.is_available

    def create_agreement(self, property_obj, tenant_obj):
        self.log_action(f"Аренда оффлайн для {tenant_obj.name} оформляется.")
        property_obj.is_available = False

    def confirm_rental(self, property_obj, tenant_obj):
        self.send_notification(f"Аренда {property_obj.address} подтверждена для {tenant_obj.name} (в офисе).")
