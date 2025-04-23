from typing import Dict
from items import Item, Book, Movie
from user import User
import csv
import numpy as np

class Dataset:
    _items: Dict[int , Item] # columna : Item
    _users: Dict[int , User] # fila : User
    _pos_items = Dict[str, int] #IdItem : columna
    _pos_users = Dict[str, int] #IdUser : fila

    def __init__(self):
        self._items = dict()
        self._users = dict()
        self.carrega()
    

    def carrega_item(self,nom_fitxer):
        with open(nom_fitxer) as csvfile:
            bookreader = csv.reader(csvfile, delimiter=',')[1:]
            for row in bookreader:

    def carrega_users(self,nom_fitxer):
        pass
    
    def carrega_ratings(self,nom_fitxer):
        pass

