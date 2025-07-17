class BirthdayParamNotValid(Exception):
    def __init__(self):
        super().__init__("Please enter number of days")

class NotesIndexNotValid(Exception):
    def __init__(self):
        super().__init__("Please enter correct Index of notes")