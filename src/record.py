import fields

class Record:
    def __init__(self, name):
        self.name = fields.Name(name)
        self.phones = []
        self.birthday = None

    # реалізація класу
    def add_phone(self, phone):
        self.phones.append(str(fields.Phone(phone)))
    
    def find_phone(self, phone):
        try:
            phone_index = self.phones.index(phone)
            return self.phones[phone_index]
        except ValueError:
            print(f"Contact {self.name} does not have the number {phone}.")
    
    def edit_phone(self, old_phone, new_phone):
        self.phones.remove(old_phone)
        self.phones.append(new_phone)
    
    def delete_phone(self):
        self.phones.clear()
        return print(f"All contact phone numbers for {self.name} have been deleted.")
    
    def add_birthday(self, birthday):
        self.birthday = fields.Birthday(birthday)
        return print("Birthday added.")
    
    
    def has_birthday_next_days(self, days):
        if self.birthday:
            return self.birthday.has_birthday_next_days(days)
        else:
            return False
    
    def __repr__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p for p in self.phones)}"
