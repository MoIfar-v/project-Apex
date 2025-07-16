# Треба додати в main.py імпорт цих класів з notes.py
# а також в команди треба додати: add-note, search-note, delete-note, edit-note, show-note

class Note:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return f"{self.text}"

class Notes:
    def __init__(self):
        self.notes = []

    def add_note(self, text):
        self.notes.append(Note(text))

    def search_note(self, keyword):
        return [note for note in self.notes if keyword in note.text]

    def delete_note(self, index):
        if 0 <= index < len(self.notes):
            del self.notes[index]
            return "Нотатку видалено"
        return "Індекс недійсний"

    def edit_note(self, index, new_text):
        if 0 <= index < len(self.notes):
            print(f"Нотатка, що редагується: {self.notes[index].text}")
            self.notes[index].text = new_text
            return "Нотатку оновлено"
        return "Індекс недійсний"

    def show_all(self):
        return [str(note) for note in self.notes]
