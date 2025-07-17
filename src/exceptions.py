class BirthdayParamNotValid(Exception):
    def __init__(self):
        super().__init__("Please enter number of days")