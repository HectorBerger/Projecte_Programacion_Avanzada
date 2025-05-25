from abc import ABC, abstractmethod 
from typing import List


class Item(ABC):
    _id: str
    _title: str

    @abstractmethod
    def __init__(self,item_id:str, titol:str):
        try:
            self._id = str(item_id)
            self._title = str(titol)
        except:
            raise ValueError

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
    
    def __init__(self,movie_id:str,titol:str,any_mov:str,generes:list):
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

    def __init__(self,isbn:str, titol:str, author:str, any_pub:int, publisher:str):
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

class VideoGame(Item):
    #asin = _id
    _categories: list
    _brand: str
    _price: str
    _description: str

    def __init__(self, asin:str, titol:str, categories:list, price:str, brand:str="Unknown", description:str="..."):
        try:
            if isinstance(categories, list):
                flat = [str(x) for cat in categories for x in (cat if isinstance(cat, list) else [cat])]
                self._categories = "|".join(flat)
            else:
                self._categories = str(categories)
            self._brand = brand
            self._price = price
            self._description = description
            super().__init__(asin,titol)
        except:
            raise ValueError(f"Error al inicialitzar les dades del objecte VideoGame {asin}")

    def __str__(self):
        return f"{self._title}, Preu: {'No disponible' if self._price is None else f'${self._price:.2f}'}. Categories: {self._categories} [ID: {self._id}] Descripció: {self._description[:20]}..."

    def get_genres(self):
        return self._categories 
