from address_book import AddressBook
from record import Record
from notes import Notes
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
def ask_for_address(args, book): 
    name, *_ = args
    record = book.find(name)
    if not record:
        return f"Контакт із іменем '{name}' не знайдено"

    while True:
        address_input = input("Введи адресу у форматі: Місто, вулиця з номером (наприклад, Київ, Шевченка 10): ").strip()
        try:
            if ',' not in address_input:
                raise ValueError("Адреса має містити місто та вулицю, розділені комою.")
            city, street = map(str.strip, address_input.split(',', 1))
            record.address = Address(city, street)
            return f"Адресу для {name} оновлено: {record.address}"
        except ValueError as e:
            print(f"Помилка: {e}. Спробуй ще раз.")


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

def print_notes(notes_list):        # Табличний вивід нотаток
    delim = " | "
    title1, title2, title3 = 'Index', 'Notes', 'Tags'
    index_width = max(len(notes_list), len(title1))     # Вирахування ширини стовбця Індекс
    max_notes_width = max(max([len(note[1]) for note in notes_list]), len(title2))      # Вирахування ширини стовбця Текст нотатки
    max_tags_width = max(max(len(", ".join(note[2])) for note in notes_list), len(title3))      # Вирахування ширини стовбця Теги до нотатків
    horizontal_line = "-" * (index_width + max_notes_width + len(delim)*2 + max_tags_width)
    print(horizontal_line)
    print(f"{title1:<{index_width}}{delim}{title2:<{max_notes_width}}{delim}{title3}")
    print(horizontal_line)
    for note in notes_list:     # Вивід рядків таблиці нотатків
        print(f"{Fore.YELLOW}{note[0]:<{index_width}}{Style.RESET_ALL}{delim}{note[1]:<{max_notes_width}}{delim}{Fore.GREEN}{', '.join(note[2])}{Style.RESET_ALL}")        
    print(horizontal_line)

@input_error
def add_note(notes):        # Додавання нотатки
    message = "Note is empty and not added"
    text = input("Enter note text: ")
    tags = input("Enter tags separated by commas: ").split(", ")
    if text:
        notes.add_note(text.strip(), [tag.strip() for tag in tags])     # Додавання нотатки
        message = "Note added"
    return message

@input_error
def delete_note(notes):     # Видалення нотатки за індексом
    index_note = input("Index of notes: ")
    try: 
        if index_note.isdigit() and (0 <= int(index_note) < notes.len_notes()):
            notes.delete_note(int(index_note))     # Видалення нотатки
            message = "Note deleted"
        else:
            message = "Index invalid"
    except:
        raise NotesIndexNotValid()
    return message

@input_error
def search_note(notes):     # Пошук нотатків за ключевим словом у тексті нотатки або тегах
    message = ""
    key = input("Keyword or tag: ")
    matches = notes.search_note(key)     # Формування списку нотатків, що відповідають ключевому слову
    if matches:
        print_notes(matches)
    else:
        message = "Nothing found"
    return message

@input_error
def show_note(notes):       # Вивід усіх нотатків
    message = "Nothing found"
    matches = notes.show_all()
    if matches:
        print_notes(matches)
        message = ""    
    return message

@input_error
def edit_note(notes):       # Редагування ноатків за індексом
    index_note = input("Index of notes: ")
    try: 
        if index_note.isdigit() and (0 <= int(index_note) < notes.len_notes()):
            new_text = input("New text: ")
            notes.edit_note(int(index_note), new_text)
            message = "Note updated"
        else:
            message = "Index invalid"
    except:
        raise NotesIndexNotValid()
    return message

@input_error
def sort_note(notes):       # Сортування нотатків за тегами
    message = "No notes with tags"
    tag_map = notes.group_by_tag()
    if tag_map:
        for tag, notes_list in tag_map.items():
            print(f"\n{tag}:")
            for note in notes_list:
                print(f"    - {note}")       
        message = ""    
    return message

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
            print(add_note(notes))

        elif command == command_show_note:
            print(show_note(notes))

        elif command == command_search_note:
            print(search_note(notes))

        elif command == command_delete_note:
            print(delete_note(notes))

        elif command == command_edit_note:
            print(edit_note(notes))

        elif command == command_sort_note:
            print(sort_note(notes))
            
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
