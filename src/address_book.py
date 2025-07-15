from collections import UserList
from datetime import datetime as dt

class AddressBook(UserList):
    # реалізація класу
    def add_record(self, contact):
        self.append(contact)
    
    def find(self, name):
        try:
            for record in self.data:
                if record.name.value == name:
                    return record
        except KeyError:
            print("No such contact exists")

    def delete(self, name):
        try:
            for record in self.data:
                if record.name.value == name:
                    del record
                    print("Contact successfully deleted")
        except KeyError:
            print("No such contact exists")

    def birthdays(self):
        self.date_now = dt.today().date()                                              
        self.birthdays_list = []
        for u_birth in self.data:
            if u_birth.birthday == None:
                continue
            
            celeb_year = self.date_now.year
        
            if u_birth.birthday.birthday.month < self.date_now.month and u_birth.birthday.birthday.day < self.date_now.day:
                celeb_year = celeb_year + 1
                continue
        
            u_birth_tmp = u_birth.birthday.birthday.replace(year=celeb_year)
            delta_days = u_birth_tmp - self.date_now
        
            if delta_days.days > 0 and (13 - self.date_now.weekday()) > delta_days.days:
                self.birthdays_list.append(u_birth)
        return self.birthdays_list
    
    def show_birthday(self, name):
        try:
            for record in self.data:
                if record.name.value == name:
                    return record.birthday.birthday
        except KeyError:
            print("No such contact exists")