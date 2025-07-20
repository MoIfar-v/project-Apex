import fields
import re

class Record:
    def __init__(self, name):
        self.name = fields.Name(name)
        self.phones = []
        self.birthday = None
        self.address = None
        self.email = None

    # реалізація класу
    def add(self, args):
        """Додає новий контакт типу Record()

        Args:
            args (phone, birthday, address, email): приймають значення полів нового контакту. 
            Доступні типи: str - змінна має значення
                        None - змінна має значення
                        ____ - довільна кількість символу "_" використовується для пропуску непотрібного поля
                        Наприклад: add Jane 2342342345 12.06.1985 ____ rthrthr@gmail.com, пропущено поле address
        """
        # при створенні контакту замість пропусків "____" встановлює значення None
        pattern = r"^_+$"
        args = [None if re.fullmatch(pattern, arg) else arg for arg in args]
        
        phone, birthday, address, email = args
        if phone:
            self.phones.append(str(fields.Phone(phone)))
        if birthday:
            self.birthday = fields.Birthday(birthday)
        if address:
            self.address = address
        if email:
            self.email = fields.Email(email)
    
    def find_phone(self, phone):
        try:
            phone_index = self.phones.index(phone)
            return self.phones[phone_index]
        except ValueError:
            print(f"Contact {self.name} does not have the number {phone}.")
    
    def edit_contact(self, field, new_value, old_value):
        """Функція змінює поточне значення поля контакту та задає нове якщо значення поля = None

        Args:
            field (str): Поле для зміни
            new_value (str): Нове значення
            old_value (str / None): Старе значення. Для поля phones отримує номер 
                                    який треба замінити. Для всих інших None

        Returns:
            str: Повідмлення користувачу.
        """
        if field == "phones":
            if old_value in self.phones:
                index = self.phones.index(old_value)
                self.phones[index] = str(fields.Phone(new_value))
                massege = "Phone changed."
            else:
                self.phones.append(str(fields.Phone(new_value)))
                massege = "Phone added."
            return massege
        elif field == "birthday":
            if self.birthday:
                massege = "Birthday changed."
            else:
                massege = "Birthday added."
            self.birthday = fields.Birthday(new_value)
            return massege
        
        elif field == "address":
            if self.address:
                massege = "Address changed."
            else:
                massege = "Address added."
            self.address = new_value # fields.Address(new_value)
            return massege
        
        elif field == "email":
            if self.email:
                massege = "Email changed."
            else:
                massege = "Email added."
            self.email = fields.Email(new_value)    
            return massege
            
    def delete_field(self, field, value):
        """Видаляє задані поля контакту шляхом встановлення в них значення None

        Args:
            field (str): поле яке потребує видалення
            value (str): номер телефону який має бути видалений зі списку Person.phones

        Returns:
            str: повідомлення користувачу
        """
        if field == "phones":
            if value in self.phones:
                index = self.phones.index(value)
                self.phones.remove(value)
                massege = "Phone deleted."
            else:
                massege = "This phone does not exist."
            return massege
        
        elif field == "birthday":
            self.birthday = None
            return  "Birthday deleted."
        
        elif field == "address":
            self.address = None
            return "Address deleted."
        
        elif field == "email":
            self.email = None
            return "Email deleted."

    
    def has_birthday_next_days(self, days):
        if self.birthday:
            return self.birthday.has_birthday_next_days(days)
        else:
            return False

    def __repr__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p for p in self.phones)}, birthday: {self.birthday}, address: {self.address}, email: {self.email}\n"
