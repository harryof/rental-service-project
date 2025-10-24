import json
from rental_service.property_factory import PropertyFactory
from rental_service.client_base import Tenant
from rental_service.rental_agreement import RentalAgreement
from rental_service.mixins import LoggingMixin, NotificationMixin


class RentalApp(LoggingMixin, NotificationMixin):
    def __init__(self):
        self.properties = []
        self.tenants = []
        self.agreements = []

    # --- Функции для работы с недвижимостью ---
    def create_property(self):
        print("\n📦 Создание недвижимости")
        property_type = input("Тип (apartment/house/commercialspace): ").strip().lower()
        try:
            kwargs = {
                "property_id": len(self.properties) + 1,
                "address": input("Адрес: "),
                "area": float(input("Площадь (кв.м): ")),
                "monthly_rate": float(input("Месячная ставка: ")),
                "is_available": True
            }

            if property_type == "apartment":
                kwargs["number_of_rooms"] = int(input("Количество комнат: "))
            elif property_type == "house":
                kwargs["has_garden"] = input("Есть сад? (y/n): ").lower() == "y"
            elif property_type == "commercialspace":
                kwargs["business_type"] = input("Тип бизнеса: ")

            prop = PropertyFactory.create_property(property_type, **kwargs)
            self.properties.append(prop)
            self.log_action(f"Добавлена недвижимость: {prop.address}")
            print("✅ Недвижимость успешно создана!\n")

        except Exception as e:
            print(f"❌ Ошибка: {e}")

    def list_properties(self):
        print("\n🏠 Список всей недвижимости:")
        if not self.properties:
            print("Нет объектов.")
        for p in self.properties:
            print(f"- {p}")
        print()

    def search_property(self):
        query = input("\n🔍 Введите адрес для поиска: ").strip().lower()
        found = [p for p in self.properties if query in p.address.lower()]
        if found:
            print("Найдено:")
            for p in found:
                print(f"- {p}")
        else:
            print("❌ Ничего не найдено.")
        print()

    def edit_property(self):
        try:
            pid = int(input("\nВведите ID недвижимости для редактирования: "))
            prop = next((p for p in self.properties if p.property_id == pid), None)
            if not prop:
                print("❌ Недвижимость не найдена.")
                return

            print(f"Редактируем {prop.address}")
            prop.monthly_rate = float(input("Новая ставка (текущее значение {0}): ".format(prop.monthly_rate)))
            prop.area = float(input("Новая площадь (текущее значение {0}): ".format(prop.area)))
            self.log_action(f"Изменена недвижимость ID={pid}")
            print("✅ Изменения сохранены!\n")

        except Exception as e:
            print(f"❌ Ошибка: {e}")

    def delete_property(self):
        try:
            pid = int(input("\nВведите ID недвижимости для удаления: "))
            self.properties = [p for p in self.properties if p.property_id != pid]
            self.log_action(f"Удалена недвижимость ID={pid}")
            print("✅ Недвижимость удалена!\n")
        except Exception as e:
            print(f"❌ Ошибка: {e}")

    def analyze_properties(self):
        print("\n📊 Анализ недвижимости")
        if not self.properties:
            print("Нет данных для анализа.")
            return
        most_expensive = max(self.properties, key=lambda p: p.monthly_rate)
        cheapest = min(self.properties, key=lambda p: p.monthly_rate)
        print(f"💰 Самая дорогая: {most_expensive.address} — {most_expensive.monthly_rate} руб/мес")
        print(f"🪙 Самая дешёвая: {cheapest.address} — {cheapest.monthly_rate} руб/мес\n")

    # --- Работа с арендаторами и арендой ---
    def create_tenant(self):
        print("\n👤 Добавление арендатора")
        try:
            tenant = Tenant(
                tenant_id=len(self.tenants) + 1,
                name=input("Имя: "),
                email=input("Email: "),
                phone=input("Телефон: ")
            )
            self.tenants.append(tenant)
            self.log_action(f"Добавлен арендатор: {tenant.name}")
            print("✅ Арендатор успешно добавлен!\n")
        except Exception as e:
            print(f"❌ Ошибка: {e}")

    def create_agreement(self):
        print("\n🧾 Создание договора аренды")
        if not self.properties or not self.tenants:
            print("❌ Сначала добавьте недвижимость и арендатора.")
            return

        pid = int(input("ID недвижимости: "))
        tid = int(input("ID арендатора: "))
        prop = next((p for p in self.properties if p.property_id == pid), None)
        tenant = next((t for t in self.tenants if t.tenant_id == tid), None)

        if not prop or not tenant:
            print("❌ Неверный ID.")
            return

        agreement = RentalAgreement(
            agreement_id=len(self.agreements) + 1,
            tenant=tenant,
            property_=prop,
            start_date=input("Дата начала (YYYY-MM-DD): "),
            end_date=input("Дата окончания (YYYY-MM-DD): ")
        )
        self.agreements.append(agreement)
        agreement.log_action("Создан новый договор аренды")
        agreement.send_notification("Аренда подтверждена")
        try:
            months = int(input("Введите срок аренды в месяцах: "))
            total = agreement.calculate_total(months)
            print(f"✅ Договор создан. Общая стоимость: {total:.2f} руб.\n")
        except Exception as e:
            print(f"❌ Ошибка при расчете стоимости: {e}")


    # --- Главное меню ---
    def run(self):
        while True:
            print("""
===========================
     СЕРВИС АРЕНДЫ ЖИЛЬЯ
===========================
1. Добавить недвижимость
2. Просмотреть все объекты
3. Поиск недвижимости
4. Редактировать объект
5. Удалить объект
6. Анализ (дорогая/дешёвая)
7. Добавить арендатора
8. Создать договор аренды
0. Выход
""")
            choice = input("Выберите действие: ").strip()

            if choice == "1":
                self.create_property()
            elif choice == "2":
                self.list_properties()
            elif choice == "3":
                self.search_property()
            elif choice == "4":
                self.edit_property()
            elif choice == "5":
                self.delete_property()
            elif choice == "6":
                self.analyze_properties()
            elif choice == "7":
                self.create_tenant()
            elif choice == "8":
                self.create_agreement()
            elif choice == "0":
                print("👋 Завершение работы.")
                break
            else:
                print("❌ Неверный выбор, попробуйте снова.\n")


if __name__ == "__main__":
    app = RentalApp()
    app.run()
