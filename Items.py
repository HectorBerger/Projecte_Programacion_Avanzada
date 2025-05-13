from abc import ABC, abstractmethod 
from typing import List


class Item(ABC):
    _id: str
    _pos_col: int
    _title: str

    @abstractmethod
    def __init__(self,item_id,titol):# -> bool:
        try:
            self._id = str(item_id)
            self._pos_col = int()
            self._title = str(titol)
        except:
            raise ValueError

    def set_columna(self,col):# -> bool: #No se usa
        self._pos_col = int(col)

    def get_id(self):
        return self._id

    @abstractmethod
    def __str__(self):
        raise NotImplementedError
    
    @abstractmethod
    def get_genres(self):
        raise NotImplementedError
        
    
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
    
    def __str__(self):
        return f"{self._title} ({self._any_movie}). Generes: {self._genres} [ID: {self._id}] "
    
    def get_genres(self):
        return self._genres

class Book(Item):
    #isbn = _id
    _author: str
    _any_publicacio: int
    _publisher: str

    def __init__(self,isbn,titol,author,any_pub,publisher): # -> bool:
        try:
            self._author = str(author)
            self._any_publicacio = int(any_pub)
            self._publisher = str(publisher)
            super().__init__(isbn,titol)
        except:
            raise ValueError
        
    def __str__(self):
        return f"{self._title} de {self._author}. Publicat per {self._publisher} a l'any {self._any_publicacio}. [ISBN: {self._id}] "
    
    def get_genres(self):
        raise NotImplemented
