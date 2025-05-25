from abc import ABC, abstractmethod 
from typing import List


class Item(ABC):
    """
    Classe abstracta base per representar un element (item) genèric.

    Attributes
    ----------
    _id : str
        Identificador únic de l'ítem.
    _title : str
        Títol de l'ítem.
    """
    _id: str
    _title: str

    @abstractmethod
    def __init__(self,item_id:str, titol:str):
        """
        Inicialitza un ítem genèric.

        Parameters
        ----------
        item_id : str
            Identificador únic de l'ítem.
        titol : str
            Títol de l'ítem.

        Raises
        ------
        ValueError
            Si hi ha un error durant la conversió dels paràmetres.
        """
        try:
            self._id = str(item_id)
            self._title = str(titol)
        except:
            raise ValueError

    def get_id(self):
        """
        Retorna l'identificador de l'ítem.

        Returns
        -------
        str
            Identificador de l'ítem.
        """
        return self._id

    @abstractmethod
    def __str__(self):
        """
        Representació en cadena de l'ítem.

        Returns
        -------
        str
            Cadena representativa de l'ítem.

        Raises
        ------
        NotImplementedError
            Si la subclasse no implementa aquest mètode.
        """
        raise NotImplementedError
    
    @abstractmethod
    def get_genres(self):
        """
        Retorna els gèneres o categories associades a l'ítem.

        Returns
        -------
        list or str
            Llista o cadena de gèneres/categories.

        Raises
        ------
        NotImplementedError
            Si la subclasse no implementa aquest mètode.
        """
        raise NotImplementedError
        
    
class Movie(Item):
    """
    Classe per representar una pel·lícula.

    Attributes
    ----------
    _any_movie : str
        Any de llançament de la pel·lícula.
    _genres : list of str
        Gèneres associats a la pel·lícula.
    """
    _any_movie: str
    _genres: List[str]
    
    def __init__(self,movie_id:str,titol:str,any_mov:str,generes:list):
        """
        Inicialitza una pel·lícula.

        Parameters
        ----------
        movie_id : str
            Identificador de la pel·lícula.
        titol : str
            Títol de la pel·lícula.
        any_mov : str
            Any de llançament.
        generes : list
            Gèneres de la pel·lícula.

        Raises
        ------
        ValueError
            Si hi ha un error durant la inicialització.
        """
        try:
            self._any_movie= any_mov
            self._genres = generes
            super().__init__(movie_id,titol)
        except:
            raise ValueError
    
    def __str__(self):
        """
        Retorna una descripció textual de la pel·lícula.

        Returns
        -------
        str
            Descripció de la pel·lícula.
        """
        return f"{self._title} ({self._any_movie}). Generes: {self._genres} [ID: {self._id}] "
    
    def get_genres(self):
        """
        Retorna els gèneres de la pel·lícula.

        Returns
        -------
        list
            Llista de gèneres.
        """
        return self._genres

class Book(Item):
    """
    Classe per representar un llibre.

    Attributes
    ----------
    _author : str
        Autor del llibre.
    _any_publicacio : int
        Any de publicació.
    _publisher : str
        Editorial del llibre.
    """

    #isbn = _id
    _author: str
    _any_publicacio: int
    _publisher: str

    def __init__(self,isbn:str, titol:str, author:str, any_pub:int, publisher:str):
        """
        Inicialitza un llibre.

        Parameters
        ----------
        isbn : str
            Codi ISBN del llibre.
        titol : str
            Títol del llibre.
        author : str
            Autor del llibre.
        any_pub : int
            Any de publicació.
        publisher : str
            Editorial.

        Raises
        ------
        ValueError
            Si hi ha un error durant la inicialització.
        """
        try:
            self._author = str(author)
            self._any_publicacio = int(any_pub)
            self._publisher = str(publisher)
            super().__init__(isbn,titol)
        except:
            raise ValueError
        
    def __str__(self):
        """
        Retorna una descripció textual del llibre.

        Returns
        -------
        str
            Descripció del llibre.
        """
        return f"{self._title} de {self._author}. Publicat per {self._publisher} a l'any {self._any_publicacio}. [ISBN: {self._id}] "
    
    def get_genres(self):
        """
        No implementat per llibres.

        Raises
        ------
        NotImplementedError
        """
        raise NotImplementedError

class VideoGame(Item):
    """
    Classe per representar un videojoc.

    Attributes
    ----------
    _categories : str
        Categories del videojoc (separades per "|").
    _brand : str
        Marca del videojoc.
    _price : str
        Preu del videojoc.
    _description : str
        Descripció del videojoc.
    """

    #asin = _id
    _categories: list
    _brand: str
    _price: str
    _description: str

    def __init__(self, asin:str, titol:str, categories:list, price:str, brand:str="Unknown", description:str="..."):
        """
        Inicialitza un videojoc.

        Parameters
        ----------
        asin : str
            Codi ASIN del videojoc.
        titol : str
            Títol del videojoc.
        categories : list
            Llista de categories (pot contenir subllistes).
        price : str
            Preu del videojoc.
        brand : str, optional
            Marca del videojoc (default és "Unknown").
        description : str, optional
            Descripció (default és "...").

        Raises
        ------
        ValueError
            Si hi ha un error durant la inicialització.
        """
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
        """
        Retorna una descripció textual del videojoc.

        Returns
        -------
        str
            Descripció del videojoc amb preu i categories.
        """
        return f"{self._title}, Preu: {'No disponible' if self._price is None else f'${self._price:.2f}'}. Categories: {self._categories} [ID: {self._id}] Descripció: {self._description[:20]}..."

    def get_genres(self):
        """
        Retorna les categories del videojoc.

        Returns
        -------
        str
            Categories separades per "|".
        """
        return self._categories 
