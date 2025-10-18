from rental_service.property_base import PropertyMeta, Property


class PropertyFactory:
    """Фабрика для создания объектов недвижимости по типу."""

    @staticmethod
    def create_property(property_type: str, **kwargs) -> Property:
        property_type = property_type.lower()
        cls = PropertyMeta.registry.get(property_type)
        if not cls:
            raise ValueError(f"Неизвестный тип недвижимости: {property_type}")
        return cls(**kwargs)
