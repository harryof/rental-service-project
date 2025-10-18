from __future__ import annotations
from abc import ABC, abstractmethod
from abc import ABCMeta
from typing import Dict, Any
import json
from rental_service.mixins import LoggingMixin


class PropertyMeta(ABCMeta):
    """Метакласс для регистрации всех подклассов недвижимости."""

    registry: Dict[str, type] = {}

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        if name != "Property":  # не регистрируем базовый класс
            PropertyMeta.registry[name.lower()] = cls
        return cls


class Property(ABC, metaclass=PropertyMeta):
    """Абстрактный класс недвижимости."""

    def __init__(
        self,
        property_id: int,
        address: str,
        area: float,
        monthly_rate: float,
        is_available: bool = True,
    ):
        self.__property_id = property_id
        self.__address = address
        self.__area = area
        self.__monthly_rate = monthly_rate
        self.__is_available = is_available

    # --- Геттеры и сеттеры ---
    @property
    def property_id(self) -> int:
        return self.__property_id

    @property
    def address(self) -> str:
        return self.__address

    @address.setter
    def address(self, value: str):
        if not value:
            raise ValueError("Адрес не может быть пустым")
        self.__address = value

    @property
    def area(self) -> float:
        return self.__area

    @area.setter
    def area(self, value: float):
        if value <= 0:
            raise ValueError("Площадь должна быть положительным числом")
        self.__area = value

    @property
    def monthly_rate(self) -> float:
        return self.__monthly_rate

    @monthly_rate.setter
    def monthly_rate(self, value: float):
        if value < 0:
            raise ValueError("Ставка не может быть отрицательной")
        self.__monthly_rate = value

    @property
    def is_available(self) -> bool:
        return self.__is_available

    @is_available.setter
    def is_available(self, value: bool):
        self.__is_available = value

    # --- Методы ---
    @abstractmethod
    def calculate_rental_cost(self, months: int) -> float:
        """Абстрактный метод расчета стоимости аренды."""
        pass

    def __str__(self) -> str:
        return f"Недвижимость: {self.address}, Площадь: {self.area} кв.м"

    # --- Методы сравнения ---
    def __lt__(self, other: Property) -> bool:
        return self.monthly_rate < other.monthly_rate

    def __gt__(self, other: Property) -> bool:
        return self.monthly_rate > other.monthly_rate

    def __eq__(self, other: Property) -> bool:
        return self.monthly_rate == other.monthly_rate

    # --- Сериализация ---
    def to_dict(self) -> Dict[str, Any]:
        """Преобразует объект в словарь."""
        return {
            "type": self.__class__.__name__,
            "property_id": self.property_id,
            "address": self.address,
            "area": self.area,
            "monthly_rate": self.monthly_rate,
            "is_available": self.is_available,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Property:
        """Создает объект недвижимости из словаря."""
        property_type = data.get("type", "").lower()
        subclass = PropertyMeta.registry.get(property_type)
        if not subclass:
            raise ValueError(f"Неизвестный тип недвижимости: {property_type}")
        return subclass(
            data["property_id"],
            data["address"],
            data["area"],
            data["monthly_rate"],
            data["is_available"],
            **{k: v for k, v in data.items() if k not in cls().to_dict()},
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


# --- Подклассы недвижимости ---
class Apartment(Property, LoggingMixin):
    def __init__(
        self,
        property_id: int,
        address: str,
        area: float,
        monthly_rate: float,
        number_of_rooms: int,
        is_available: bool = True,
    ):
        super().__init__(property_id, address, area, monthly_rate, is_available)
        self.__number_of_rooms = number_of_rooms

    @property
    def number_of_rooms(self) -> int:
        return self.__number_of_rooms

    def calculate_rental_cost(self, months: int) -> float:
        discount = 0.9 if months >= 12 else 1.0
        cost = self.monthly_rate * months * discount
        self.log_action(f"Расчет френды {cost} руб. за {months} мес.")
        return cost

    def __str__(self):
        return f"Квартира: {self.address}, Комнат: {self.number_of_rooms}"


class House(Property, LoggingMixin):
    def __init__(
        self,
        property_id: int,
        address: str,
        area: float,
        monthly_rate: float,
        has_garden: bool,
        is_available: bool = True,
    ):
        super().__init__(property_id, address, area, monthly_rate, is_available)
        self.__has_garden = has_garden

    @property
    def has_garden(self) -> bool:
        return self.__has_garden

    def calculate_rental_cost(self, months: int) -> float:
        garden_fee = 1.1 if self.has_garden else 1.0
        cost = self.monthly_rate * months * garden_fee
        self.log_action(f"Расчет френды {cost} руб. за {months} мес.")
        return cost

    def __str__(self):
        return f"Дом: {self.address}, Сад: {'Да' if self.has_garden else 'Нет'}"


class CommercialSpace(Property, LoggingMixin):
    def __init__(
        self,
        property_id: int,
        address: str,
        area: float,
        monthly_rate: float,
        business_type: str,
        is_available: bool = True,
    ):
        super().__init__(property_id, address, area, monthly_rate, is_available)
        self.__business_type = business_type

    @property
    def business_type(self) -> str:
        return self.__business_type

    def calculate_rental_cost(self, months: int) -> float:
        business_multiplier = 1.2 if self.business_type.lower() == "retail" else 1.0
        cost = self.monthly_rate * months * business_multiplier
        self.log_action(f"Расчет френды {cost} руб. за {months} мес.")
        return cost

    def __str__(self):
        return f"Коммерческое помещение: {self.address}, Тип бизнеса: {self.business_type}"
