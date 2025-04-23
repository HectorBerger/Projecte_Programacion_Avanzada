from abc import ABC, abstractmethod 

class Item(ABC):
    _id: str

    def __init__(self):
        self._id = str()

    @abstractmethod
    def llegir_dades(self):

        return 


class Movie(Item):

    def

class Book(Item):
    