from abc import ABC, abstractmethod


class Handler(ABC):
    """Базовый класс для звеньев цепочки."""
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    @abstractmethod
    def handle_request(self, request: dict):
        pass


class RentalManager(Handler):
    def handle_request(self, request: dict):
        if request.get("type") == "minor":
            return "Изменение одобрено менеджером."
        elif self.next_handler:
            return self.next_handler.handle_request(request)
        return "Запрос не обработан."


class FinanceDepartment(Handler):
    def handle_request(self, request: dict):
        if request.get("type") == "financial":
            return "Изменение одобрено финансовым отделом."
        elif self.next_handler:
            return self.next_handler.handle_request(request)
        return "Запрос не обработан."


class Director(Handler):
    def handle_request(self, request: dict):
        return "Изменение одобрено директором."
