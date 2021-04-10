

class Student(object):
    def __init__(self, name="", surname=""):
        self.__name = name
        self.__surname = surname

    @property
    def name(self):
        return self.__name

    @property
    def surname(self):
        return self.__surname

    @surname.setter
    def surname(self, surname):
        self.__surname = surname

    @name.setter
    def name(self, name):
        self.__name = name

    def hello(self):
        return f"Hello, {self.name}"
