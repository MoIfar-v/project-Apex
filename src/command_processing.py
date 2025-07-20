from colorama import Fore, Style, init
from fields import Address
from record import Record
from exceptions import BirthdayParamNotValid, NotesIndexNotValid

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
    horizontal_line = "-" * (index_width + max_notes_width + len(delim)*2 + max_tags_width)     # Формування горизонтальної лінії для таблиці
    print(horizontal_line)
    print(f"{title1:<{index_width}}{delim}{title2:<{max_notes_width}}{delim}{title3}")      # Друк шапки таблиці
    print(horizontal_line)
    for note in notes_list:     # Вивід рядків таблиці нотатків
        print(f"{Fore.YELLOW}{note[0]:<{index_width}}{Style.RESET_ALL}{delim}{note[1]:<{max_notes_width}}{delim}{Fore.GREEN}{', '.join(note[2])}{Style.RESET_ALL}")        
    print(horizontal_line)

@input_error
def add_note(notes):        # Додавання нотатки
    message = "Note is empty and not added"
    text = input("Enter note text: ")
    tags = input("Enter tags separated by commas: ").split(", ")
    if text:        # Якщо текст нотатки не порожній, то зберігаємо нотатку
        notes.add_note(text.strip(), [tag.strip() for tag in tags])     # Додавання нотатки
        message = "Note added"
    return message

@input_error
def delete_note(notes):     # Видалення нотатки за індексом
    index_note = input("Index of notes: ")
    try: 
        if index_note.isdigit() and (0 <= int(index_note) < notes.len_notes()):     # якщо введений рядок складається із цифр та число є валідним кількості нотатків в нотатнику, то викликається метод класу для видалення нотатки з введеним індексом
            notes.delete_note(int(index_note))     # Видалення нотатки
            message = "Note deleted"
        else:
            message = "Index invalid"
    except:
        raise NotesIndexNotValid()      # обробка виключення
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
    matches = notes.show_all()      # викликається метод класу для формування списку усіх нотатків
    if matches:
        print_notes(matches)        # викликається функція для виводу нотатків в табличному виді 
        message = ""    
    return message

@input_error
def edit_note(notes):       # Редагування ноатків за індексом
    index_note = input("Index of notes: ")
    try: 
        if index_note.isdigit() and (0 <= int(index_note) < notes.len_notes()):     # якщо введений рядок складається із цифр та число є валідним кількості нотатків в нотатнику, то викликається метод класу для редагування нотатки з введеним індексом
            new_text = input("New text: ")
            notes.edit_note(int(index_note), new_text)      # викликається метод класу для редагування нотатки з введеним індексом та новим текстом
            message = "Note updated"
        else:
            message = "Index invalid"
    except:
        raise NotesIndexNotValid()      # обробка виключення
    return message

@input_error
def sort_note(notes):       # Сортування нотатків за тегами
    message = "No notes with tags"
    tag_map = notes.group_by_tag()      # викликається метод класу для отримання словника з группованими та сортированими нотатками
    if tag_map:     # якщо словник не порожній 
        for tag, notes_list in tag_map.items():     # перебираємо словник 
            print(f"\n{tag}:")      # виводимо тег за яким згрупповані нотатки 
            for note in notes_list:     # перебираємо список нотатків для виводу на екран 
                print(f"    - {note}")       # виводимо нотатку на екран 
        message = ""    
    return message

