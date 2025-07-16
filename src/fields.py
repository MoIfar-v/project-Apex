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
<<<<<<< HEAD
            self.birthday = dt.strptime(value,"%d.%m.%Y").date()
=======
            self.value =  dt.strptime(value,"%d.%m.%Y").date()
>>>>>>> origin/main
            
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        
    def has_birthday_next_days(self, days):
        birth = self.birthday
        today = dt.today().date()
        next_birthday = self.next_celebration()
        if(next_birthday < today):
              next_birthday = next_birthday.replace(year=next_birthday.year+1)
        difference = next_birthday - today
        return difference.days <= days
        
    def next_celebration(self):
        today = dt.today().date()
        return dt(year=today.year, month=self.birthday.month, day=self.birthday.day).date()
        
class Email(Field):
    def __init__(self, value):
        super().__init__(value)
        pattern = r"^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if re.match(pattern, value):
            self.email = value
        else:
            raise ValueError("Invalid email format.")