# 🧠 Console Assistant "Apex"

A modular Python console application that combines an intelligent **Address Book** and **Note-Taking system**

---

## Install & Run
Firstly, clone project from this repository
Then, run next commands:
```
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 src/main.py
```

## 🚀 Features

### 📒 Address Book
- Add, edit, remove contacts
- Manage multiple phone numbers, email addresses, and birthdays
- Search by name, phone, or email
- Display contacts which have coming birthdays in ```n``` given days

### 🗒️ Notes
- Create, tag, and delete notes
- Search notes by keywords or tags
- Display all notes grouped by tag

### 🧾 Command Line Interface
- Type-safe command routing
- Friendly feedback and suggestions on typos
- Simple interface for real-time command interaction

---

## 📖 Command Reference

| Command         | Description                      |
|-----------------|----------------------------------|
| `close`         | Exit the project                 |
| `exit`          | Exit the project                 |
| `add`           | Add a contact                    |
| `all`           | Show all contacts                |
| `show-birthday` | Show a birthday by contact name  |
| `birthdays`     | Show all upcoming birthdays      |
| `delete`        | Delete a contact                 |
| `edit`          | Edit contact fields              |
| `delete-field`  | Delete a specific contact field  |
| `find`          | Find a contact by a specific field |
| `add-address`   | Add an address to a contact      |
| `add-note`      | Add a note                       |
| `delete-note`   | Delete a note                    |
| `show-note`     | Show all notes                   |
| `search-note`   | Search for a note                |
| `edit-note`     | Edit a note                      |
| `sort-note`     | Sort notes                       |

### 💬 Sample Commands
```
> add contact John +380501112233 john@mail.com 01.01.1990
> change phone John +380501112233 +380509998877
> add note "Buy milk" #shopping
> find note milk
> birthdays 7
> exit
```
