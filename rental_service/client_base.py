# rental_service/client_base.py
from typing import Dict, Any


class Tenant:
    """Класс, представляющий арендатора (композиция в RentalAgreement)."""

    def __init__(self, tenant_id: int, name: str, email: str, phone: str):
        self.__tenant_id = tenant_id
        self.__name = name
        self.__email = email
        self.__phone = phone

    # --- Геттеры ---
    @property
    def tenant_id(self) -> int:
        return self.__tenant_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def email(self) -> str:
        return self.__email

    @property
    def phone(self) -> str:
        return self.__phone

    def __str__(self) -> str:
        return f"Арендатор: {self.__name} ({self.__email})"

    # --- Сериализация ---
    def to_dict(self) -> Dict[str, Any]:
        return {
            "tenant_id": self.__tenant_id,
            "name": self.__name,
            "email": self.__email,
            "phone": self.__phone,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Tenant":
        return cls(data["tenant_id"], data["name"], data["email"], data["phone"])
