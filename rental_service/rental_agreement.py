# rental_service/rental_agreement.py
from datetime import date
from typing import List, Tuple, Dict, Any
from rental_service.mixins import LoggingMixin, NotificationMixin
from rental_service.interfaces import Rentable, Reportable
from rental_service.client_base import Tenant
from rental_service.property_base import Property


class RentalAgreement(LoggingMixin, NotificationMixin, Rentable, Reportable):
    """Класс для управления арендой жилья (агрегация + композиция)."""

    def __init__(
        self,
        agreement_id: int,
        tenant: Tenant,
        property_: Property,
        start_date: date,
        end_date: date,
    ):
        self.__agreement_id = agreement_id
        self.__tenant = tenant
        self.__property = property_
        self.__start_date = start_date
        self.__end_date = end_date
        self.__extras: List[Tuple[str, float]] = []
        self.__total_cost = 0.0

        self.log_action(f"Аренда {self.__agreement_id} создана.")
        self.send_notification(
            f"Аренда {self.__property.address} успешно оформлена для {self.__tenant.name}."
        )

    # --- Методы управления ---
    def add_extra(self, service_name: str, price: float):
        self.__extras.append((service_name, price))
        self.log_action(f"Добавлена услуга '{service_name}' стоимостью {price}₽.")

    def remove_extra(self, service_name: str):
        self.__extras = [e for e in self.__extras if e[0] != service_name]
        self.log_action(f"Услуга '{service_name}' удалена.")

    def calculate_total(self, months: int) -> float:
        base = self.__property.calculate_rental_cost(months)
        extras = sum(p for _, p in self.__extras)
        self.__total_cost = base + extras
        self.log_action(f"Общая стоимость аренды: {self.__total_cost}₽.")
        return self.__total_cost

    # --- Интерфейсы ---
    def rent_property(self):
        self.__property.is_available = False
        self.log_action(f"Аренда {self.__agreement_id} активирована.")
        self.send_notification(
            f"Недвижимость {self.__property.address} теперь недоступна для других арендаторов."
        )

    def generate_report(self) -> str:
        return (
            f"Аренда #{self.__agreement_id}\n"
            f"Арендатор: {self.__tenant.name}\n"
            f"Недвижимость: {self.__property.address}\n"
            f"Период: {self.__start_date} — {self.__end_date}\n"
            f"Доп. услуги: {len(self.__extras)}\n"
            f"Итог: {self.__total_cost}₽"
        )

    # --- Сериализация ---
    def to_dict(self) -> Dict[str, Any]:
        return {
            "agreement_id": self.__agreement_id,
            "tenant": self.__tenant.to_dict(),
            "property_id": self.__property.property_id,
            "start_date": str(self.__start_date),
            "end_date": str(self.__end_date),
            "extras": self.__extras,
            "total_cost": self.__total_cost,
        }

    # --- Строковое представление ---
    def __str__(self) -> str:
        return f"Аренда #{self.__agreement_id}: {self.__tenant.name} → {self.__property.address}"
