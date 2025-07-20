class Note:     # Класс для нотатки
    def __init__(self, text, tags=None):
        self.text = text
        self.tags = tags if tags else []

    def __str__(self):
        tags_str = ", ".join(self.tags)
        return f"{self.text} [Tags: {tags_str}]"        # формуємо вигляд для нотатки друку 

class Notes:        # Класс для зберігання нотатків
    def __init__(self):
        self.notes = []
    
    def len_notes(self):        # функція для підрахувння кількості нотатків
        return len(self.notes)

    def add_note(self, text, tags):     # функція для додаванння нотатки
        self.notes.append(Note(text, tags))     # додаємо нотатку до нотатника

    def search_note(self, keyword):     # функція для пошуку нотатків за ключевим словом у тексті нотатка або у тегах до нотатки
        list = [[note.text, note.tags] for note in self.notes]      # формуєм список усіх нотатків, де кожна нотатка є списком з тексту та списку тегів
        for idx, note in enumerate(list):       # додаємо індекси до кожної нотатки
            note.insert(0,idx)    
        return [note for note in list if keyword.lower() in note[1].lower().split(" ") or keyword.lower() in note[2]]       # формуєм список нотатків, в яких клучево слово зустрічається в тексті нотатків або в тегах до нотатки
    
    def delete_note(self, index):     # функція для видалення нотатки за індексом
        print("This note will be deleted: ", str(self.notes[index]))        # виводимо текст нотатки що видаляється
        del self.notes[index]       # видаляємо нотатку
 
    def edit_note(self, index, new_text):     # функція для редагування нотатки за індексом
        print(f"Editable note: {self.notes[index].text}")       # виводимо текст нотатки що редагується
        self.notes[index].text = new_text       # записуємо новий текст нотатки

    def show_all(self):     # функція для виводу усіх нотатків
        list = [[note.text, note.tags] for note in self.notes]      # формуєм список усіх нотатків, де кожна нотатка є списком з тексту та списку тегів
        for idx, note in enumerate(list):       # додаємо індекси до кожної нотатки
            note.insert(0,idx)
        return list     #  повертаємо список усіх нотатків для виводу
       
    def group_by_tag(self):     # функція для сортування нотатків за тегами
        tag_map = {}        # створюємо словник для групування та сортування нотатків
        list_tags = []       # створюємо пустий список для формування списку усіх тегів до усіх нотатків 
        for note in self.notes:          # формування списку усіх тегів
            list_tags += note.tags
        tags_list = list(set([tag.strip() for tag in list_tags]))       # формування списку унікальних тегів для всіх нотатків
        tags_list.sort()        # сортування усіх тегів у списку
        for tag in tags_list:       # перебираємо кожен тег зі списку усіх унікальних тегів
            for note in self.notes:     # перебираємо усі нотатки
                if tag in note.tags:        # перевіряємо чи є тег в списку тегів до нотатки та якщо є додаємо нотатку до списку нотатків до цього тега
                    tag_map.setdefault(tag.strip().lower(), []).append(note)
        return tag_map      #  повертаємо словник усіх сгруппованих нотатків для виводу
