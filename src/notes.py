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
    
    def len_notes(self):
        return len(self.notes)

    def add_note(self, text, tags):
        self.notes.append(Note(text, tags))

    def search_note(self, keyword):
        return [note for note in self.notes if keyword.lower() in note.text.lower().split(" ") or keyword.lower() in note.tags]

    def delete_note(self, index):
        if 0 <= index < len(self.notes):
            print("This note will be deleted: ", str(self.notes[index]))
            del self.notes[index]
            return "Note deleted"
        return "Index invalid"

    def edit_note(self, index, new_text):
        if 0 <= index < len(self.notes):
            g = len(self.notes)
            print(f"Editable note: {self.notes[index].text}")
            self.notes[index].text = new_text
            return "Note updated"
        return "Index invalid"

    def show_all(self):
        return [str(note) for note in self.notes]
    
    def group_by_tag(self):
        tag_map = {}
        list_tags = []        
        for note in self.notes:
            # print(type(note.tags), note.tags)
            list_tags += note.tags
        tags_list = list(set([tag.strip() for tag in list_tags]))
        tags_list.sort()
        # print(tags_list)
        for tag in tags_list:
            for note in self.notes:
                if tag in note.tags:
                    tag_map.setdefault(tag.strip().lower(), []).append(note)
        return tag_map    
