from typing import Dict
from items import Item, Book, Movie
from abc import ABC, abstractmethod 
from user import User
import csv
import numpy as np


#Provisional hasta decidir que hacer: #Cómo damos las direcciones de los archivos? argumento/atributo/constante/o directamente?
NOM_FITXER_MOVIES = "dataset\\MovieLens100k\\movies.csv"
NOM_FITXER_RATINGS_MOVIES = "dataset\\MovieLens100k\\ratings.csv"

NOM_FITXER_BOOKS = "dataset/Books/Books.csv"
NOM_FITXER_RATING_BOOKS = "dataset/Books/Ratings.csv" 
NOM_FITXER_BOOKS_USERS = "dataset/Books/Users.csv"


class Dataset(ABC):
    _users: Dict[int , User] # fila : User
    _items: Dict[int , Item] # columna : Item
    _pos_users: Dict[str, int] #IdUser : fila
    _pos_items: Dict[str, int] #IdItem : columna
    _ratings: np.array 

    _all_users: set
    _all_items: set

    def __init__(self):
        self._users = dict()
        self._items = dict()
        self._pos_users = dict()
        self._pos_items = dict()
        self._all_users = set()
        self._all_items = set()
        self._ratings = self.carrega_ratings("") 
        print("LOADED") #log
        return None

    @abstractmethod
    def carrega_ratings(self,nom_fitxer):
        raise NotImplemented
                
    @abstractmethod
    def carrega_users(self,nom_fitxer):
        raise NotImplemented    

    @abstractmethod
    def carrega_items(self,nom_fitxer):
        raise NotImplemented    

    def get_users(self):
        return self._all_users     


class DatasetMovies(Dataset):
    def __init__(self):
        super().__init__()

    def carrega_ratings(self,nom_fitxer):
        #Recorrer para saber n i m (el shape de la array)
        #Carregar usuaris i movies
        self._all_items = self.carrega_items("nom_fitxer") #Cómo damos las direcciones de los archivos? argumento/atributo/constante/o directamente?
        self._all_users = self.carrega_users("nom_fitxer") 

        #Crear array y llenarla
        number_of_users = len(self._all_users)
        number_of_items = len(self._all_items)
        ratings = np.empty([number_of_users,number_of_items], dtype=np.float16) #Hemos escogido este tipo ya que necesariamente tiene que ser float porqué tenemos ratings con coma y 16 bits porqué es el más pequeño que entra nuestro máximo
        with open(NOM_FITXER_RATINGS_MOVIES, encoding="utf-8") as csvfile:   
            dict_reader = csv.DictReader(csvfile, delimiter=',')
            for row in dict_reader:
                user_id = row["userId"]
                movie_id = row["movieId"]

                if user_id in self._pos_users.keys() and movie_id in self._pos_items.keys():
                    ratings[self._pos_users[user_id], self._pos_items[movie_id]] = row["rating"]
                else:
                    print(f"User or movie not found: userId={user_id}, movieId={movie_id}") #DEBUG

        return ratings
                

    def carrega_users(self,nom_fitxer):
        users = set()

        with open(NOM_FITXER_RATINGS_MOVIES, encoding="utf-8") as csvfile:   
            user_reader = csv.DictReader(csvfile, delimiter=',')
            for row in user_reader:
                users.add(row["userId"])

        for i,iduser in enumerate(users):
            self._users[i] = User(iduser) # O només iduser? ja que no ens interessa tota la resta
            self._pos_users[iduser] = i

        return users
    
    def carrega_items(self,nom_fitxer):
        movies = set()

        with open(NOM_FITXER_MOVIES, encoding="utf-8") as csvfile:   
            moviesreader = csv.DictReader(csvfile, delimiter=',')
            for i,row in enumerate(moviesreader):
                movieid = row["movieId"]
                titol = " ".join(row["title"].split(" ")[:-1])
                any_movie = str(row["title"].split(" ")[-1].strip("()"))
                generes = row["genres"].split('|')
                self._items[i] = Movie(movieid, titol, any_movie, generes) 
                self._pos_items[movieid] = i

                movies.add(row["movieId"])

        return movies


class DatasetBooks(Dataset):
    def __init__(self):
        super().__init__()

    def carrega_ratings(self,nom_fitxer):
        #!#! Arreglar carrega intentar reducir la apertura de archivos y fijarse que los users creados y libros son los que se usan

        #Recorrer para saber n i m 
        #Carregar els primer 10,000 books i els usuaris més adhients 
        self._all_items = self.carrega_items("nom_fitxer") #Cómo damos las direcciones de los archivos? argumento/atributo/constante/o directamente? 
        self._all_users = self.carrega_users("nom_fitxer")

        #Crear array y llenarla
        number_of_users = len(self._all_users)
        number_of_items = len(self._all_items)
        ratings = np.empty([number_of_users,number_of_items], dtype=np.int8) 
        with open(NOM_FITXER_RATING_BOOKS) as csvfile:
            dict_reader = csv.DictReader(csvfile, delimiter=',')
            for row in dict_reader:
                user_id = row["User-ID"]
                isbn = row["ISBN"]

                if user_id in self._pos_users.keys() and isbn in self._pos_items.keys():
                    ratings[self._pos_users[user_id], self._pos_items[isbn]] = row["Book-Rating"] 
                else:
                    print(f"User or book not found: userId={user_id}, ISBN={isbn}") #DEBUG

        return ratings


    def carrega_users(self,nom_fitxer):
        users = set()
        with open(NOM_FITXER_RATING_BOOKS) as csvfile:   
            bookreader = csv.DictReader(csvfile, delimiter=',')
            for row in bookreader:
                if 
                    users.add(row["User-ID"])

        with open(NOM_FITXER_BOOKS_USERS, 'r') as csvfile:  
            dict_reader = csv.DictReader(csvfile)
            for i,row in enumerate(dict_reader):
                if row["User-ID"] in users:
                    self._users[i] = User(row["User-ID"],row["Location"],row["Age"])
                    self._pos_users[row["User-ID"]] = i

        if len(users) != len(self._users):
            raise ImportError

        return users
    

    def carrega_items(self,nom_fitxer,books):
        books = set()

        with open(NOM_FITXER_BOOKS) as csvfile:   
                bookreader = csv.DictReader(csvfile, delimiter=',') 
                for i,row in enumerate(bookreader):
                    isbn = row["ISBN"]
                    titol = row["Book-Title"]
                    autor = row["Book-Author"]
                    year = row["Year-Of-Publication"]
                    publisher = row["Publisher"]
                    self._items[i] = Book(isbn, titol, autor, year, publisher) 
                    self._pos_items[titol] = i

                    books.add(row["ISBN"])

                    if i==10000:
                        break
        
        return books



