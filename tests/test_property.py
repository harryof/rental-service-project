import pytest
from rental_service.property_base import Apartment, House, CommercialSpace
from rental_service.property_factory import PropertyFactory

def test_apartment_creation_and_calc():
    apt = Apartment(1, "ул. Ленина, 10", 45.0, 30000, 2)
    assert apt.number_of_rooms == 2
    assert round(apt.calculate_rental_cost(12)) == 324000  # со скидкой 10%


def test_house_and_garden():
    house = House(2, "ул. Садовая, 5", 120, 50000, True)
    assert house.has_garden
    assert round(house.calculate_rental_cost(2)) == 110000


def test_commercial_cost():
    com = CommercialSpace(3, "ул. Бизнес-центр", 200, 100000, "retail")
    assert round(com.calculate_rental_cost(1)) == 120000


def test_comparisons():
    a = Apartment(1, "A", 40, 30000, 1)
    b = Apartment(2, "B", 40, 40000, 2)
    assert a < b
    assert b > a
    assert not a == b


def test_factory_creates_correct_types():
    apt = PropertyFactory.create_property(
        "apartment",
        property_id=1,
        address="ул. Победы, 1",
        area=50.0,
        monthly_rate=40000,
        number_of_rooms=2,
        is_available=True,
    )
    assert isinstance(apt, Apartment)


def test_serialization_roundtrip():
    apt = Apartment(1, "ул. Казанская, 15", 55.0, 35000, 3)
    data = apt.to_dict()
    assert data["type"] == "Apartment"
    json_str = apt.to_json()
    assert "Казанская" in json_str
