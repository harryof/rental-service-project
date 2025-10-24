# tests/test_rental_agreement.py
from datetime import date
from rental_service.client_base import Tenant
from rental_service.property_base import Apartment
from rental_service.rental_agreement import RentalAgreement


def test_rental_creation_and_total():
    tenant = Tenant(1, "Иван Иванов", "ivan@example.com", "+79991234567")
    apartment = Apartment(1, "ул. Ленина, 10", 50, 30000, 2)
    agreement = RentalAgreement(1, tenant, apartment, date(2025, 1, 1), date(2026, 1, 1))

    agreement.add_extra("Уборка", 2000)
    total = agreement.calculate_total(12)

    assert total > 0
    assert isinstance(total, float)
    assert "Аренда" in str(agreement)

    report = agreement.generate_report()
    assert "Арендатор" in report
    assert "Недвижимость" in report


def test_rent_property_and_remove_extra():
    tenant = Tenant(2, "Мария Смирнова", "maria@example.com", "+79997654321")
    apartment = Apartment(2, "ул. Советская, 5", 40, 25000, 1)
    agreement = RentalAgreement(2, tenant, apartment, date(2025, 3, 1), date(2025, 9, 1))

    agreement.add_extra("Интернет", 1500)
    agreement.remove_extra("Интернет")
    agreement.rent_property()

    assert apartment.is_available is False
