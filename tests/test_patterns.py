from rental_service.approval_chain import RentalManager, FinanceDepartment, Director
from rental_service.rental_process import OnlineRentalProcess, OfflineRentalProcess
from rental_service.property_base import Apartment
from rental_service.client_base import Tenant
from rental_service.exceptions import PermissionDeniedError


def test_chain_of_responsibility():
    chain = RentalManager(FinanceDepartment(Director()))
    assert chain.handle_request({"type": "minor"}) == "Изменение одобрено менеджером."
    assert chain.handle_request({"type": "financial"}) == "Изменение одобрено финансовым отделом."
    assert chain.handle_request({"type": "major"}) == "Изменение одобрено директором."


def test_online_rental_process():
    process = OnlineRentalProcess()
    process.user_role = "manager"
    apt = Apartment(1, "ул. Ленина, 10", 50, 30000, 2)
    tenant = Tenant(1 , "Алексей", "+79998887766", "alex@example.com")

    result = process.rent_property(apt, tenant)
    assert result == "Аренда успешно оформлена."
    assert not apt.is_available


def test_offline_rental_process():
    process = OfflineRentalProcess()
    process.user_role = "manager"
    apt = Apartment(2, "ул. Горького, 7", 40, 25000, 1)
    tenant = Tenant(2, "Мария", "+79991112233", "maria@example.com")

    result = process.rent_property(apt, tenant)
    assert result == "Аренда успешно оформлена."
    assert not apt.is_available


def test_permission_denied():
    process = OnlineRentalProcess()
    process.user_role = "guest"
    apt = Apartment(3, "ул. Победы, 5", 60, 28000, 3)
    tenant = Tenant(3, "Иван", "+79997776655", "ivan@example.com")

    try:
        process.rent_property(apt, tenant)
        assert False, "Ожидалось PermissionDeniedError"
    except PermissionDeniedError:
        assert True
