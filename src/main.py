from address_book import AddressBook
from record import Record
from notes import Notes
from colorama import Fore, Style, init 
import pickle
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

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
    name, phone, birthday, address, email, *_ = args + [None, None, None]
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    data = [phone, birthday, address, email]
    record.add(data)
    return message

"""@input_error
def change_ph(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record != None:
        record.edit_phone(old_phone, new_phone)
        return "The phone has been replaced"
    else:    
        return "Contact does not exist"""

"""@input_error
def user_phone(args, book):
    name, *_ = args
    record = book.find(name)
    if record != None:
        return record.phones
    else:    
        return "Contact does not exist"""

@input_error
def print_all(book):
    return book

"""@input_error
def add_birth(args, book):
    name, birthday, *_ = args
    record = book.find(name)
    if record != None:
        record.add_birthday(birthday)
    else:    
        return "Contact does not exist"
"""
@input_error
def show_birth(args, book):
    name, *_ = args
    return book.show_birthday(name)

@input_error    
def all_birthdays(args, book):
    return book.birthdays()

@input_error 
def delete_contact(args, book):
    name, *_ = args
    record = book.find(name)
    message = f'Контакт "{name}" видалено'
    if record is None:
        message = f"There is no contact named {name}"
    book.delete(record)
    return message

@input_error 
def edit_contact(args, book):
    #Приклад синтаксису 1: edit Bob phones 3423233456 2334565432
    #Приклад синтаксису 2: edit Victor email victor111@gmail.com
    
    name, field, new_value, old_value, *_ = args + [None,]
    record = book.find(name)
    
    if record is None:
        message = "There is no contact named {name}"
    message = record.edit_contact(field, new_value, old_value)
    
    return message

@input_error
def delete_field(args, book):
    #Приклад синтаксису 1: delete-field Jane phones 4534231295
    #Приклад синтаксису 1: delete-field Bob address
    
    name, field, value, *_ = args + [None,]
    record = book.find(name)
    
    if record is None:
        message = "There is no contact named {name}"
    message = record.delete_field(field, value)
    
    return message

command_close = "close"
command_exit = "exit"
command_add = "add"
#command_change = "change"
#command_phone = "phone"
command_all = "all"
#command_add_birthday = "add-birthday"
command_show_birthday = "show-birthday"
command_birthdays = "birthdays"
command_add_note = "add-note"
command_delete_note = "delete-note"
command_show_note = "show-note"
command_search_note = "search-note"
command_edit_note = "edit-note"
command_delete = "delete"
command_edit = "edit"
command_delete_field = "delete-field"

commands = {
    command_close: "Вийти з проекту",
    command_exit: "Вийти з проекту",
    command_add: "Додати контакт",
    #command_change: "Змінити контакт",
    #command_phone: "Змінити номер телефону",
    command_all: "Показати всі контакти",
    #command_add_birthday: "Додати день народження",
    command_show_birthday: "Показати день народження",
    command_birthdays: "Показати всі дні народження",
    command_add_note: "Додати нотатку",
    command_delete_note: "Видалити нотатку",
    command_show_note: "Показати усі нотатки",
    command_search_note: "Знайти нотатку",
    command_edit_note: "Редагувати нотатку",      
    command_delete: "Видалити контакт",
    command_edit: "Змінити поля контакту",
    command_delete_field: "Видалення поля контакту"
}
completer = WordCompleter(commands.keys(), ignore_case=True)

def print_all_commands():
    delim = " | "
    max_key_width = max(len(cmd) for cmd in commands.keys())
    max_value_width = max(len(cmd) for cmd in commands.values())
    horizontal_line = "-" * (max_key_width + max_value_width + len(delim))
    print(horizontal_line)
    print(f"{'Command':<{max_key_width}}{delim}Description")
    print(horizontal_line)
    for cmd, desc in commands.items():
        print(f"{Fore.YELLOW}{cmd:<{max_key_width}}{Style.RESET_ALL}{delim}{desc}")
    print(horizontal_line)

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    print_all_commands()
    while True:
        user_input = prompt("Enter a command: ", completer=completer)
        command, *args = parse_input(user_input)

        if command in [command_close, command_exit]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == command_add:
            print(add_contact(args, book))

        #elif command == command_change:
        #    print(change_ph(args, book))

        #elif command == command_phone:
        #    print(user_phone(args, book))

        elif command == command_all:
            print(print_all(book))

        #elif command == command_add_birthday:
        #    print(add_birth(args, book))

        elif command == command_show_birthday:
            print(show_birth(args, book))
            
        elif command == command_birthdays:
            print(all_birthdays(book))

        elif command == command_add_note:
            text = input("Введи текст нотатки: ")
            notes.add_note(text.strip())
            print("Нотатку додано.")

        elif command == command_delete_note:
            index_note = input("Індекс нотатки: ")
            if index_note.isdigit():
                print(notes.delete_note(int(index_note)))

        elif command == command_show_note:
            for i, note in enumerate(notes.show_all()):
                print(f"{i}: {note}")

        elif command == command_search_note:
            key = input("Ключове слово або тег: ")
            matches = notes.search_note(key)
            if matches:
                for i, note in enumerate(matches):
                    print(f"{i}: {note}")
            else:
                print("Нічого не знайдено.")

        elif command == command_edit_note:
            index_note = input("Індекс нотатки: ")
            if index_note.isdigit():
                new_text = input("Новий текст: ")
                print(notes.edit_note(int(index_note), new_text))  
            else:
                print("Індекс недійсний")                 
            
        elif command == command_delete:
            print(delete_contact(args, book))
            
        elif command == command_edit:
            print(edit_contact(args, book))
        elif command == command_delete_field:
            print(delete_field(args, book))
        else:
            print("Invalid command.")

        save_data(book)

if __name__ == "__main__":
    main()
