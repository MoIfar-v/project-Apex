from collections import UserList

class AddressBook(UserList):
    # реалізація класу
    def add_record(self, contact):
        self.append(contact)
    
    def find(self, args):
        name, *_ = args
        try:
            for record in self.data:
                if record.name.value == name:
                    return record
        except KeyError:
            print("No such contact exists")

    def delete(self, record):
        self.remove(record)

    def birthdays(self, days_forward):
        upcoming_birthdays = [record for record in self.data if record.has_birthday_next_days(days_forward)]
        return sorted(upcoming_birthdays, key=lambda record: record.birthday.value)
    
    def show_birthday(self, name):
        try:
            for record in self.data:
                if record.name.value == name:
                    return record.birthday.birthday
        except KeyError:
            print("No such contact exists")