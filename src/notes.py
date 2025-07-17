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
            print("Ця нотатка буде видалена: ",str(self.notes[index]))
            del self.notes[index]
            return "Note deleted"
        return "Index invalid"

    def edit_note(self, index, new_text):
        g = len(self.notes)
        if 0 <= index < len(self.notes):
            print(f"Editable note: {self.notes[index].text}")
            self.notes[index].text = new_text
            return "Note updated"
        return "Index invalid"
    
    def len_notes(self):
        k = len(self.notes)
        return k

    def show_all(self):
        return [str(note) for note in self.notes]
