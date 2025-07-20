from datetime import datetime as dt
import re

class Field:
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return str(self.value)


class Name(Field):
    # реалізація класу
    
    def __init__(self, value):
        super().__init__(value)
        self.value = ''.join(self.value.split())
        
        if self.value == "":
            print("You need to enter the name.")
        

class Phone(Field):
    # реалізація класу
    def __init__(self, value):
        super().__init__(value)
        
        if len(self.value) != 10:
            print("You need to enter the correct phone number.")
            
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = dt.strptime(value,"%d.%m.%Y").date()
            
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        
    def has_birthday_next_days(self, days):
        birth = self.value
        today = dt.today().date()
        next_birthday = self.next_celebration()
        if(next_birthday < today):
            next_birthday = next_birthday.replace(year=next_birthday.year+1)
        difference = next_birthday - today
        return difference.days <= days
        
    def next_celebration(self):
        today = dt.today().date()
        return dt(year=today.year, month=self.value.month, day=self.value.day).date()
        
class Email(Field):
    def __init__(self, value):
        super().__init__(value)
        pattern = r"^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if re.match(pattern, value):
            self.email = value
        else:
            raise ValueError("Invalid email format.")

class Address(Field):
    def __init__(self, city, street):  # Нормалізуємо назву міста та вулиці
        self.city = self.normalize_city(city)
        self.street = self.normalize_street(street)

        self.validate()
        
        super().__init__(f"{self.city}, {self.street}")

    def normalize_city(self, city):
        # Обрізаємо зайві пробіли та приводимо місто до правильного формату (перша літера велика)
        return city.strip().title()

    def normalize_street(self, street):
        # Обрізаємо зайві пробіли
        street = street.strip()

        # Якщо вулиця не починається з "вул.", додаємо це
        if not street.lower().startswith("вул."):
            street = "вул. " + street

        return street

    def validate(self):
        # Перевіряємо, що місто є рядком і не порожнє
        if not self.city or not isinstance(self.city, str):
            raise ValueError("Місто має бути непорожнім рядком.")

        # Перевіряємо, що назва вулиці достатньо довга
        if not isinstance(self.street, str) or len(self.street.strip()) < 5:
            raise ValueError("Назва вулиці надто коротка.")

        # Перевіряємо, що у назві вулиці вказаний номер будинку
        if not any(char.isdigit() for char in self.street):
            raise ValueError("У вулиці має бути вказаний номер будинку.")

    def __str__(self):
        # Повертаємо повну адресу у вигляді одного рядка
        return f"{self.city}, {self.street}"

    """@staticmethod
    def print_allowed_cities(): # Show the list of allowed cities to the user
        print("Choose a city from the list:")
        for idx, city in enumerate(Address.allowed_cities, 1):
            print(f"{idx}. {city}")"""
