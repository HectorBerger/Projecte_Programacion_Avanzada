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

    def __init__(self, dataset_name):
        self.dataset_name = int(dataset_name) #str o int?
        self._items = dict()
        self._users = dict()
        self.carrega()
    

    def carrega_items(self,nom_fitxer):
        if self.dataset_name == 1: #!#!#! He pensado que podemos hacer que sea una clase abstracta y que haya un dataset hijo por cada tipo, así nos ahorramos estos ifs raros
            with open(nom_fitxer) as csvfile:   
                bookreader = csv.reader(csvfile, delimiter=',')
                for row in bookreader[1:]:
                    id = int(row[0])
                    titol = row[1:-1]
                    generes = row[2].split('|')
                    any = row[1].split(" ")[-1].strip("()")
                    item = Movie(id, titol, generes, any)
                    self._items[id] = item
                    self._pos_items[titol] = id

        elif self.dataset_name == 2:
            with open(nom_fitxer) as csvfile:   
                bookreader = csv.reader(csvfile, delimiter=',')
                for row in bookreader[1:]:
                    ISBN = row[0]
                    titol = row[1]
                    autor = row[2]
                    year = row[3]
                    publisher = row[4]
                    item = Book(ISBN, titol, autor, year, publisher)
                    self._items[ISBN] = item
                    self._pos_items[titol] = ISBN
            

    def carrega_users(self,nom_fitxer):
        pass
    

    def carrega_ratings(self,nom_fitxer):
        if self.dataset_name == 1:
            movies = set()
            with open(nom_fitxer) as csvfile:   #fitxer movies
                bookreader = csv.reader(csvfile, delimiter=',')
                for row in bookreader[1:]:
                    movies.add(row[0])
            users = set()
            with open(nom_fitxer) as csvfile:   #fitxer ratings
                bookreader = csv.reader(csvfile, delimiter=',')
                for row in bookreader[1:]:
                    users.add(row[0])
        #Recorrer para saber n i m
            number_of_users = len(users)
            number_of_items = len(movies)
            np.empty([number_of_users,number_of_items], dtype=np.float16) #Hemos escogido este tipo ya que necesariamente tiene que ser float porqué tenemos ratings con coma y 16 bits porqué es el más pequeño que entra nuestro máximo
            with open(nom_fitxer) as csvfile:   #fitxer ratings
                bookreader = csv.reader(csvfile, delimiter=',')
                for row in bookreader[1:]:
                    #csv.Dictreader con los headers
                    pass

        elif self.dataset_name == 2:
            books = set()
            with open(nom_fitxer) as csvfile:   #fitxer books
                bookreader = csv.reader(csvfile, delimiter=',')
                for row in bookreader[1:]:
                    books.add(row[0])
            users = set()
            with open(nom_fitxer) as csvfile:   #fitxer users/ratings
                bookreader = csv.reader(csvfile, delimiter=',')
                for row in bookreader[1:]:
                    users.add(row[0])
        #Recorrer para saber n i m
            number_of_users = len(users)
            number_of_items = len(books)
            np.empty([number_of_users,number_of_items], dtype=np.int8) 
            with open(nom_fitxer) as csvfile:   #fitxer ratings
                bookreader = csv.reader(csvfile, delimiter=',')
                for row in bookreader[1:]:
                    #csv.Dictreader con los headers
