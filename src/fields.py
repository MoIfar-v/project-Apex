from datetime import datetime as dt

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
            self.birthday =  dt.strptime(value,"%d.%m.%Y").date()
            
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")