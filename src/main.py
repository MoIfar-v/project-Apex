import serialization as se
import command_processing as cp
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from colorama import Fore, Style, init 


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
    command_close: "Exit the project",
    command_exit: "Exit the project",
    command_add: "Add a contact",
    command_all: "Show all contacts",
    command_show_birthday: "Show a birthday by contact name",
    command_birthdays: "Show all upcoming birthdays",
    command_delete: "Delete a contact",
    command_edit: "Edit contact fields",
    command_delete_field: "Delete a specific contact field",
    command_find: "Find a contact by a specific field",
    command_add_address: "Add an address to a contact",
    command_add_note: "Add a note",
    command_delete_note: "Delete a note",
    command_show_note: "Show all notes",
    command_search_note: "Search for a note",
    command_edit_note: "Edit a note",      
    command_sort_note: "Sort notes",      

}
completer = WordCompleter(commands.keys(), ignore_case=True)

def main():
    book =  se.load_addressbook()
    notes = se.load_notes()
    print(f"\n 📌 Welcome to the assistant bot!")
    print_all_commands()
    while True:
        user_input = prompt("Enter a command: ", completer=completer)
        command, *args = cp.parse_input(user_input)

        if command in [command_close, command_exit]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == command_add:
            print(cp.add_contact(args, book))

        elif command == command_all:
            cp.print_all(book)

        elif command == command_show_birthday:
            print(cp.show_birth(args, book))
            
        elif command == command_birthdays:
            print(cp.all_birthdays(args, book))

        elif command == command_add_note:
            print(cp.add_note(notes))

        elif command == command_show_note:
            print(cp.show_note(notes))

        elif command == command_search_note:
            print(cp.search_note(notes))

        elif command == command_delete_note:
            print(cp.delete_note(notes))

        elif command == command_edit_note:
            print(cp.edit_note(notes))

        elif command == command_sort_note:
            print(cp.sort_note(notes))
            
        elif command == command_delete:
            print(cp.delete_contact(args, book))
            
        elif command == command_edit:
            print(cp.edit_contact(args, book))

        elif command == command_delete_field:
            print(cp.delete_field(args, book))
            
        elif command == command_find:
            print(cp.find_contact(args, book))

        elif command == command_add_address:
            cp.ask_for_address(args, book)

        else:
            print("Invalid command.")
        
        se.save_addressbook(book)
        se.save_notes(notes)

if __name__ == "__main__":
    main()
