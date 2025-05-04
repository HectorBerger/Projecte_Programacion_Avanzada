from abc import ABC, abstractmethod 
from typing import List


class Item(ABC):
    _id: str
    _pos_col: int
    _title: str

    @abstractmethod
    def __init__(self,item_id,titol):# -> bool:
        self._id = str(item_id)
        self._pos_col = int
        self._title = str(titol)

    def assignar_columna(self,col):# -> bool:
        self._pos_col = int(col)
        
    
class Movie(Item):
    _any_movie: str
    _genres: List[str]
    
    def __init__(self,movie_id,titol,any_mov,generes):# -> bool:
        try:
            self._any_movie= any_mov
            self._genres = generes
            super().__init__(movie_id,titol)
        except:
            raise ValueError
        


class Book(Item):
    #isbn = _id
    _author: str
    _any_publicacio: int
    _publisher: str

    def __init__(self,isbn,author,any_pub,publisher) -> bool:
        try:
            self._author = str
            self._any_publicacio = int
            self._publisher = str
            super().__init__()
        except:
            raise ValueError
        