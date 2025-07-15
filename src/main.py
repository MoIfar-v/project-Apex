from colorama import Fore, Style, init
from address_book import AddressBook
from record import Record
import pickle


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "There is no contact with that name."
        except IndexError:
            return "Я не знаю нашо, і де це виключення буде викликатися але хай буде)."
    return inner

@input_error
def parse_input(user_input):
    
    cmd, *args, = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book):
    name, phone = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_ph(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record != None:
        record.edit_phone(old_phone, new_phone)
        return "The phone has been replaced"
    else:    
        return "Contact does not exist"

@input_error
def user_phone(args, book):
    name, *_ = args
    record = book.find(name)
    if record != None:
        return record.phones
    else:    
        return "Contact does not exist"

@input_error
def print_all(book):
    return book

@input_error
def add_birth(args, book):
    name, birthday, *_ = args
    record = book.find(name)
    if record != None:
        record.add_birthday(birthday)
    else:    
        return "Contact does not exist"

@input_error
def show_birth(args, book):
    name, *_ = args
    return book.show_birthday(name)

@input_error    
def all_birthdays(book):
    return book.birthdays()

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_ph(args, book))

        elif command == "phone":
            print(user_phone(args, book))

        elif command == "all":
            print(print_all(book))

        elif command == "add-birthday":
            print(add_birth(args, book))

        elif command == "show-birthday":
            print(show_birth(args, book))

        elif command == "birthdays":
            print(all_birthdays(book))

        else:
            print("Invalid command.")
        
        save_data(book)

if __name__ == "__main__":
    main()
