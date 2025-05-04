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

    def __init__(self):
        self._users = dict()
        self._items = dict()
        self._pos_users = dict()
        self._pos_items = dict()
        self._ratings = self.carrega_ratings("") 
        print("LOADED")
        print(self._ratings[:10,:10])

    @abstractmethod
    def carrega_ratings(self,nom_fitxer):
        raise NotImplemented
                
    @abstractmethod
    def carrega_users(self,nom_fitxer):
        raise NotImplemented    

    @abstractmethod
    def carrega_items(self,nom_fitxer):
        raise NotImplemented         


class DatasetMovies(Dataset):
    def __init__(self):
        super().__init__()

    def carrega_ratings(self,nom_fitxer):

        #Recorrer para saber n i m (el shape de la array)
        movies = set()
        with open(NOM_FITXER_MOVIES, encoding="utf-8") as csvfile:   
            moviesreader = csv.DictReader(csvfile, delimiter=',')
            for row in moviesreader:
                movies.add(row["movieId"])

        users = set()
        with open(NOM_FITXER_RATINGS_MOVIES, encoding="utf-8") as csvfile:   
            user_reader = csv.DictReader(csvfile, delimiter=',')
            for row in user_reader:
                users.add(row["userId"])

        #Carregar usuaris i movies
        self.carrega_items("nom_fitxer",movies) #Cómo damos las direcciones de los archivos? argumento/atributo/constante/o directamente?
        self.carrega_users("nom_fitxer",users) 

        #Crear array y llenarla
        number_of_users = len(users)
        number_of_items = len(movies)
        ratings = np.empty([number_of_users,number_of_items], dtype=np.float16) #Hemos escogido este tipo ya que necesariamente tiene que ser float porqué tenemos ratings con coma y 16 bits porqué es el más pequeño que entra nuestro máximo
        with open(NOM_FITXER_RATINGS_MOVIES, encoding="utf-8") as csvfile:   
            dict_reader = csv.DictReader(csvfile, delimiter=',')
            for row in dict_reader:
                user_id = row["userId"]
                movie_id = int(row["movieId"])

                if user_id in self._pos_users.keys() and movie_id in self._pos_items.keys():
                    ratings[self._pos_users[user_id], self._pos_items[movie_id]] = row["rating"]
                else:
                    print(f"User or movie not found: userId={user_id}, movieId={movie_id}")

        return ratings
                

    def carrega_users(self,nom_fitxer,users):
        for i,iduser in enumerate(users):
            self._users[i] = User(iduser) # O només iduser? ja que no ens interessa tota la resta
            self._pos_users[iduser] = i


    def carrega_items(self,nom_fitxer,movies):
        with open(NOM_FITXER_MOVIES, encoding="utf-8") as csvfile:   
            moviesreader = csv.DictReader(csvfile, delimiter=',')
            for i,row in enumerate(moviesreader):
                movieid = int(row["movieId"])
                titol = str(row["title"].split(" "))
                any_movie = str(row["title"].split(" ")[-1].strip("()"))
                generes = row["genres"].split('|')
                self._items[i] = Movie(movieid, titol, any_movie, generes)
                self._pos_items[movieid] = i
 


class DatasetBooks(Dataset):
    def __init__(self):
        super().__init__()

    def carrega_ratings(self,nom_fitxer):
        #Recorrer para saber n i m
        books = set()
        with open(NOM_FITXER_BOOKS) as csvfile:   
            bookreader = csv.reader(csvfile, delimiter=',')
            for row in bookreader[1:]:
                books.add(row[0])
                
        users = set()
        with open(NOM_FITXER_RATING_BOOKS) as csvfile:   
            bookreader = csv.reader(csvfile, delimiter=',')
            for row in bookreader[1:]:
                users.add(row[0])

         #Carregar usuaris i movies
        self.carrega_items("nom_fitxer",books) #Cómo damos las direcciones de los archivos? argumento/atributo/constante/o directamente?
        self.carrega_users("nom_fitxer",users.sorted()) 

        #Crear array y llenarla
        number_of_users = len(users)
        number_of_items = len(books)
        ratings = np.empty([number_of_users,number_of_items], dtype=np.int8) 
        with open(NOM_FITXER_RATING_BOOKS) as csvfile:
            dict_reader = csv.DictReader(csvfile, delimiter=',')
            for row in dict_reader:
                ratings[ self._pos_users[row["User-ID"]], self._pos_items[row["ISBN"]] ] = row["Book-Rating"] 


    def carrega_users(self,nom_fitxer,users):
        with open(NOM_FITXER_BOOKS_USERS, 'r') as csvfile:  
            dict_reader = csv.DictReader(csvfile)
            for i,row in enumerate(dict_reader):
                self._users[i] = User(row["User-ID"],row["Location"],row["Age"])
                self._pos_users[row["User-ID"]] = i

        if len(users) == len(self._users):
            return True
        return False
    

    def carrega_items(self,nom_fitxer,books):
        with open(NOM_FITXER_BOOKS) as csvfile:   
                bookreader = csv.reader(csvfile, delimiter=',') #Va a dar error tiene q ser un dictreader
                for row in bookreader[1:]:
                    ISBN = row[0]
                    titol = row[1]
                    autor = row[2]
                    year = row[3]
                    publisher = row[4]
                    item = Book(ISBN, titol, autor, year, publisher)
                    self._items[ISBN] = item
                    self._pos_items[titol] = ISBN


dts = DatasetMovies()