from address_book import AddressBook
from record import Record
from notes import Notes
from fields import Address #щоб можна було умови
from colorama import Fore, Style, init 
import pickle
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from exceptions import BirthdayParamNotValid, NotesIndexNotValid

def save_addressbook(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_addressbook(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
    
def save_notes(notes, filename="notes.pkl"):
    with open(filename, "wb") as f:
        pickle.dump((notes), f)

def load_notes(filename="notes.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return Notes()

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return paint_error("Give me name and phone please.")
        except KeyError:
            return paint_error("There is no contact with that name.")
        except IndexError:
            return paint_error("Index invalid")
        except Exception as e:
            return paint_error(str(e))
    return inner

def paint_error(error):
    return f"{Fore.RED}{error}{Style.RESET_ALL}"

@input_error
def parse_input(user_input):
    
    cmd, *args, = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def ask_for_address(args, book): # Функція, яка запитує місто і вулицю, перевіряє їх, і повертає коректну адресу
    name, *_ = args
    record = book.find(name)
    while True:
        print("Вибери місто з дозволених:")
        Address.print_allowed_cities()  # Виводимо список дозволених міст
        city = input("Місто: ").strip()
        street = input("Вулиця з номером (наприклад, Шевченка 10): ").strip()
        try:
            record.address = Address(city, street)
            break
            #return str(Address(city, street))  # Якщо все валідно — повертаємо адресу
        except ValueError as e:
            print(f"Помилка: {e}. Спробуй ще раз.")  # Інакше просимо ввести ще раз

@input_error
def add_contact(args, book):
    #не перезаписувати контакт при повторному додаванні
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

@input_error
def print_all(book):
    head_color = "\33[1;97;100m"
    end_color = "\33[0m"
    spacer = f"{head_color}{"":^20}|{"":^25}|{"":^25}|{"":^35}|{"":^25}{end_color}"
    head = f"{head_color}{"Name":^20}|{"Phones":^25}|{"Birthday":^25}|{"Address":^35}|{"Email":^25}{end_color}"
    
    print(spacer)
    print(head)
    print(spacer)
    
    for record in book.data:
        body_color = "\33[1;97;42m"
        if book.index(record) % 2 == 0:
            body_color = "\33[1;97;43m"
        body = f"{body_color}{str(record.name):^20}|{'; '.join(p for p in record.phones):^25}|{str(record.birthday):^25}|{str(record.address):^35}|{str(record.email):^25}{end_color}"
        print(body)
    print("Done")
        
@input_error
def show_birth(args, book):
    name, *_ = args
    return book.show_birthday(name)

@input_error    
def all_birthdays(args, book):
    try: 
        days_forward, *_ = args
        days_forward = int(days_forward)
    except:
        raise BirthdayParamNotValid()
    return book.birthdays(int(days_forward))

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

@input_error
def find_contact(args, book):
    field, value, *_ = args
    result = []

    for record in book:
        if field == "name" and record.name.value == value:
            result.append(record)
        elif field == "phone" and any(ph.value == value for ph in record.phones):
            result.append(record)
        elif field == "birthday" and record.birthday and record.birthday.value.strftime("%d.%m.%Y") == value:
            result.append(record)
        elif field == "email" and record.email and record.email.value == value:
            result.append(record)
        elif field == "address" and record.address and value.lower() in str(record.address).lower():
            result.append(record)

    if not result:
        return "Контактів не знайдено"
    
    return "\n".join(str(r) for r in result)


command_close = "close"
command_exit = "exit"
command_add = "add"
command_all = "all"
command_show_birthday = "show-birthday"
command_birthdays = "birthdays"
command_add_note = "add-note"
command_delete_note = "delete-note"
command_show_note = "show-note"
command_search_note = "search-note"
command_edit_note = "edit-note"
command_sort_note = "sort-note"
command_delete = "delete"
command_edit = "edit"
command_delete_field = "delete-field"
command_find = "find"
command_add_address = "add-address"

commands = {
    command_close: "Вийти з проекту",
    command_exit: "Вийти з проекту",
    command_add: "Додати контакт",
    command_all: "Показати всі контакти",
    command_show_birthday: "Показати день народження",
    command_birthdays: "Показати всі дні народження",
    command_add_note: "Додати нотатку",
    command_delete_note: "Видалити нотатку",
    command_show_note: "Показати усі нотатки",
    command_search_note: "Знайти нотатку",
    command_edit_note: "Редагувати нотатку",      
    command_sort_note: "Сортувати нотатки",      
    command_delete: "Видалити контакт",
    command_edit: "Змінити поля контакту",
    command_delete_field: "Видалення поля контакту",
    command_find: "Знайти контакт за полем",
    command_add_address: "Додати адресу"
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
    book =  load_addressbook()
    notes = load_notes()
    print(f"\n 📌 Welcome to the assistant bot!")
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

        elif command == command_all:
            print_all(book)

        elif command == command_show_birthday:
            print(show_birth(args, book))
            
        elif command == command_birthdays:
            print(all_birthdays(args, book))

        elif command == command_add_note:
            text = input("Enter note text: ")
            tags = input("Enter tags separated by commas: ").split(", ")
            notes.add_note(text.strip(), [tag.strip() for tag in tags])
            print("Note added")

        elif command == command_delete_note:
            index_note = input("Індекс нотатки: ")
            if index_note.isdigit():
                print(notes.delete_note(int(index_note)))

        elif command == command_show_note:
            for i, note in enumerate(notes.show_all()):
                print(f"{i}: {note}")

        elif command == command_search_note:
            key = input("Keyword or tag: ")
            matches = notes.search_note(key)
            if matches:
                for i, note in enumerate(matches):
                    print(f"{i}: {note}")
            else:
                print("Nothing found")

        elif command == command_delete_note:
            index_note = input("Index of notes: ")
            try: 
                if index_note.isdigit() and (0 <= int(index_note) < notes.len_notes()):
                    print(notes.delete_note(int(index_note)))
                else:
                    print("Index invalid")
            except:
                raise NotesIndexNotValid()

        elif command == command_edit_note:
            index_note = input("Index of notes: ")
            try: 
                if index_note.isdigit() and (0 <= int(index_note) < notes.len_notes()):
                    new_text = input("New text: ")
                    print(notes.edit_note(int(index_note), new_text)) 
                else:
                    print("Index invalid")
            except:
                raise NotesIndexNotValid()

        elif command == command_sort_note:
            tag_map = notes.group_by_tag()
            if not tag_map:
                print("No notes with tags")
            else:
                for tag, notes_list in tag_map.items():
                    print(f"\n#{tag}:")
                    for note in notes_list:
                        print(f"    - {note}")                                             
            
        elif command == command_delete:
            print(delete_contact(args, book))
            
        elif command == command_edit:
            print(edit_contact(args, book))

        elif command == command_delete_field:
            print(delete_field(args, book))
            
        elif command == command_find:
            print(find_contact(args, book))
        elif command == command_add_address:
            ask_for_address(args, book)
        else:
            print("Invalid command.")
        
        save_addressbook(book)
        save_notes(notes)

if __name__ == "__main__":
    main()
