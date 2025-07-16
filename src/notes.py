class Note:
    def __init__(self, text, tags=None):
        self.text = text
        self.tags = tags if tags else []

    def __str__(self):
        tags_str = ", ".join(self.tags)
        return f"{self.text} [Tags: {tags_str}]"

class Notes:
    def __init__(self):
        self.notes = []

    def add_note(self, text, tags):
        self.notes.append(Note(text, tags))

    def search_note(self, keyword):
        return [note for note in self.notes if keyword in note.text or keyword in note.tags]

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
