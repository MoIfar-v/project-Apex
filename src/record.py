import fields

class Record:
    def __init__(self, name):
        self.name = fields.Name(name)
        self.phones = []
        self.birthday = None
        self.address = None
        self.email = None

    # реалізація класу
    def add(self, args):
        phone, birthday, address, email = args
        if phone:
            self.phones.append(str(fields.Phone(phone)))
        if birthday:
            self.birthday = fields.Birthday(birthday)
        if address:
            pass
        if email:
            self.email = str(fields.Email(email))
    
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
    
    def add_email(self, email):
        self.birthday = fields.Email(email)
        return print("Email додано.")
    
    def edit(self, field, new_value, old_value):
        if field == "email":
            self.email = new_value
            
    
    
    def has_birthday_next_days(self, days):
        if self.birthday:
            return self.birthday.has_birthday_next_days(days)
        else:
            return False
    
    def __repr__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p for p in self.phones)}, birthday: {self.birthday}, address: {self.address}, email: {self.email}\n"
