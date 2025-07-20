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
    """Функція додає до адресної книги типу AddressBook() новий елемент типу Record()
        Поля name, phones - обов'язкові, всі інші можна пропустити ввівши довільну кількість символу "_",
        або повністю проігнорувати останні 3 поля
        
        Приклади команд: add Jane 2342342345 12.06.1985 Київ, Шевченка 10 rthrthr@gmail.com
                         Bob 3454534534 04.12.1993 ____ tgtgt@ggg.com - пропуск одного з полів 
                         add John 9379992222 
                         add Victor 2342342356 ____ ____ wdedw@gmail.com

    Args:
        args (name: Name(), phone: Phone(), birthday: Birhtday(), address: Address, email: Email()): список аргументів в 
        заданому порядку name, phone, birthday, address, email, при ігноруванні останніх полів 
        (одного або декілька) встановлює значення None
        book (AddressBook()): Зберігає нові поля адресної книги

    Returns:
        str: повідомлення користувачу
    """
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
    """Функція виводить у консоль форматовану таблицю всих контактів

    Args:
        book (AddressBook()): Зберігає нові поля адресної книги
    """
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
    """Функція виводить дату народження контакту з ім'ям name

    Args:
        args (name: Name()): ім'я контакту 
        book (AddressBook()): Зберігає нові поля адресної книги

    Returns:
        datatime: дата народження
    """
    name, *_ = args
    return book.show_birthday(name)

@input_error    
def all_birthdays(args, book):
    """Функція виводить у консоль дати народження всих контактів до 
    поточноъ дати + кількість днів встановленої користувачем

    Args:
        args (days_forward: int): кількість днів 
        book (AddressBook()): Зберігає нові поля адресної книги

    Raises:
        BirthdayParamNotValid: просить ввести кількість днів

    Returns:
        Record(): виводить контакти які підпадають під інтервал
    """
    try: 
        days_forward, *_ = args
        days_forward = int(days_forward)
    except:
        raise BirthdayParamNotValid()
    return book.birthdays(int(days_forward))

@input_error 
def delete_contact(args, book):
    """Функція видаляє контакт з ім'ям name з адресної книги AddressBook()

    Args:
        args (name: Name()): ім'я видаляємого контакта
        book (AddressBook()): Зберігає нові поля адресної книги

    Returns:
        str: повідомлення користувачу
    """
    name, *_ = args
    record = book.find(name)
    message = f'Контакт "{name}" видалено'
    if record is None:
        message = f"There is no contact named {name}"
    book.delete(record)
    return message

@input_error 
def edit_contact(args, book):
    """Функція змінює поля контактів та додає нові значення якщо старе значення поля було None
    Приклади команд: edit Bob phones 3423233456 2334565432
                     edit Victor email victor111@gmail.com

    Args:
        args (name: str, field: str, new_value: str, old_value: None): old_value: str якщо змінюється поле phones
        book (AddressBook()): Зберігає нові поля адресної книги

    Returns:
        str: повідомлення користувачу
    """
    
    name, field, new_value, old_value, *_ = args + [None,]
    record = book.find(name)
    
    if record is None:
        message = "There is no contact named {name}"
    message = record.edit_contact(field, new_value, old_value)

    return message

@input_error
def delete_field(args, book):
    """Функція видаляє поле задане користувачем, для полів birthday, address, email - шляхом встановлення 
    значення None у змінну, для phones - видалення елементу списку
    Приклади команд: delete-field Jane phones 4534231295
                     delete-field Bob address

    Args:
        args (name: str, field: str, value: None): ім'я, поле яке треба видалити, value:str якщо треба видалити конкретний номер
        book (AddressBook()): Зберігає нові поля адресної книги

    Returns:
        str: повідомлення користувачу
    """
    
    name, field, value, *_ = args + [None,]
    record = book.find(name)
    
    if record is None:
        message = "There is no contact named {name}"
    message = record.delete_field(field, value)
    
    return message

@input_error
def find_contact(args, book):
    """_summary_

    Args:
        args (_type_): _description_
        book (_type_): _description_

    Returns:
        _type_: _description_
    """
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
    """_summary_

    Args:
        notes_list (_type_): _description_
    """
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
    """_summary_

    Args:
        notes (_type_): _description_

    Returns:
        _type_: _description_
    """
    message = "Note is empty and not added"
    text = input("Enter note text: ")
    tags = input("Enter tags separated by commas: ").split(", ")
    if text:
        notes.add_note(text.strip(), [tag.strip() for tag in tags])     # Додавання нотатки
        message = "Note added"
    return message

@input_error
def delete_note(notes):     # Видалення нотатки за індексом
    """_summary_

    Args:
        notes (_type_): _description_

    Raises:
        NotesIndexNotValid: _description_

    Returns:
        _type_: _description_
    """
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
    """_summary_

    Args:
        notes (_type_): _description_

    Returns:
        _type_: _description_
    """
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
    """_summary_

    Args:
        notes (_type_): _description_

    Returns:
        _type_: _description_
    """
    message = "Nothing found"
    matches = notes.show_all()
    if matches:
        print_notes(matches)
        message = ""    
    return message

@input_error
def edit_note(notes):       # Редагування ноатків за індексом
    """_summary_

    Args:
        notes (_type_): _description_

    Raises:
        NotesIndexNotValid: _description_

    Returns:
        _type_: _description_
    """
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
    """_summary_

    Args:
        notes (_type_): _description_

    Returns:
        _type_: _description_
    """
    message = "No notes with tags"
    tag_map = notes.group_by_tag()
    if tag_map:
        for tag, notes_list in tag_map.items():
            print(f"\n{tag}:")
            for note in notes_list:
                print(f"    - {note}")       
        message = ""    
    return message

