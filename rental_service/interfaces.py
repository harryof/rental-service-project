# rental_service/interfaces.py
from abc import ABC, abstractmethod


class Rentable(ABC):
    """Интерфейс для аренды недвижимости."""

    @abstractmethod
    def rent_property(self):
        """Оформить аренду недвижимости."""
        pass


class Reportable(ABC):
    """Интерфейс для создания отчётов."""

    @abstractmethod
    def generate_report(self) -> str:
        """Сгенерировать отчет об аренде."""
        pass
