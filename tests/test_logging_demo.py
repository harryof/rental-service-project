from rental_service.property_factory import PropertyFactory

# Создаём квартиру через фабрику
apartment = PropertyFactory.create_property(
    "apartment",
    property_id=1,
    address="ул. Ленина, 5",
    area=45.0,
    monthly_rate=30000,
    number_of_rooms=2
)

# Вызываем метод, который пишет лог
cost = apartment.calculate_rental_cost(6)
print(f"Стоимость аренды: {cost}")