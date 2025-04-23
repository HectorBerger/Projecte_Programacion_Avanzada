from abc import ABC, abstractmethod 
from typing import List


class Item(ABC):
    _id: str
    _pos_col: int
    _title: str

    @abstractmethod
    def __init__(self,item_id,titol) -> bool:
        self._id = str(item_id)
        self._pos_col = int
        self._title = str(titol)

    def assignar_columna(self,col) -> bool:
        self._pos_col = int(col)
        return True
    
class Movie(Item):
    _genres: List[str]
    
    def __init__(self) -> bool:
        try:
            self._genres = []
            super().__init__()
        except:
            raise 
        else:
            return True


class Book(Item):
    #isbn = _id
    _author: str
    _any_publicacio: int
    _publisher: str

    def __init__(self) -> bool:
        try:
            self._author = str
            self._any_publicacio = int
            self._publisher = str
            super().__init__()
        except:
            raise 
        else:
            return True