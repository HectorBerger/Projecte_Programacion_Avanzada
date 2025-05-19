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
    _pos_users: Dict[str, int] #id_user : fila
    _pos_items: Dict[str, int] #id_item : columna
    _ratings: np.array 
    _pmax: int
    _all_users: set
    _all_items: set

    def __init__(self):
        self._users = dict()
        self._items = dict()
        self._pos_users = dict() #Cambiar "pos" por "row" i "column" (o "fila" i "columna")
        self._pos_items = dict()
        self._all_users = set()
        self._all_items = set()
        self._pmax = int()
        self._ratings = self.carrega_ratings("") 
        print("LOADED") #log
        return True

    @abstractmethod
    def carrega_ratings(self,nom_fitxer):
        raise NotImplementedError
                
    @abstractmethod
    def carrega_users(self,nom_fitxer):
        raise NotImplementedError   

    @abstractmethod
    def carrega_items(self,nom_fitxer):
        raise NotImplementedError   

    def print_recomenacions(llista_recomenacions,k=5):
        for i in range(k):
            print(f"")#Recomanació per a l'usuari {usuari}: {recom._dataset._items[recom._dataset._pos_items[recomanacio[0][1]]]} amb score {round(recomanacio[0][0], 1)} "))

    def set_pmax(self, puntuacio_maxima):
        self._pmax = abs(int(puntuacio_maxima))

    def get_pmax(self):
        return self._pmax

    def get_ratings(self):
        return self._ratings
    
    def get_users(self):
        return self._all_users   

    def get_user_obj(self, id_user):
        fila = self.get_row_user(id_user)
        return self._users[fila]
    
    def get_row_user(self, id_user:str): #O "pos"?
        if id_user in self._pos_users.keys():
            return self._pos_users[id_user]
        raise ValueError
    
    def get_col_item(self, id_item:str):
        if id_item in self._pos_items.keys():
            return self._pos_items[id_item]
        raise KeyError
    
    def get_item_obj(self, item_id: str):
        col = self.get_col_item(item_id)
        return self._items[col]
    
    def get_item_id(self, pos_item):
        if pos_item in self._items.keys():
            return self._items[pos_item].get_id()
        raise KeyError
    
    def get_items():
        return self._all_items

    @abstractmethod
    def get_genres(self):
        return NotImplementedError


class DatasetMovies(Dataset):
    def __init__(self):
        super().__init__()
        self.set_pmax(5)

    def carrega_ratings(self,nom_fitxer):
        #Recorrer para saber n i m (el shape de la array)
        #Carregar usuaris i movies
        self._all_items = self.carrega_items("nom_fitxer") #Cómo damos las direcciones de los archivos? argumento/atributo/constante/o directamente?
        self._all_users = self.carrega_users("nom_fitxer") 

        #Crear array y llenarla
        number_of_users = len(self._all_users)
        number_of_items = len(self._all_items)
        ratings = np.negative( np.ones([number_of_users,number_of_items], dtype=np.float16) )#Hemos escogido este tipo ya que necesariamente tiene que ser float porqué tenemos ratings con coma y 16 bits porqué es el más pequeño que entra nuestro máximo
        with open(NOM_FITXER_RATINGS_MOVIES, 'r', encoding="utf-8") as csvfile:   
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

        with open(NOM_FITXER_RATINGS_MOVIES, 'r', encoding="utf-8") as csvfile:   
            user_reader = csv.DictReader(csvfile, delimiter=',')
            for row in user_reader:
                users.add(row["userId"])

        for i,iduser in enumerate(users):
            self._users[i] = User(iduser) # O només iduser? ja que no ens interessa tota la resta
            self._pos_users[iduser] = i

        return users
    
    def carrega_items(self,nom_fitxer):
        movies = set()

        with open(NOM_FITXER_MOVIES, 'r', encoding="utf-8") as csvfile:   
            moviesreader = csv.DictReader(csvfile, delimiter=',')
            for i,row in enumerate(moviesreader):
                movieid = row["movieId"]
                titol = " ".join(row["title"].split(" ")[:-1])
                any_movie = str(row["title"].split(" ")[-1].strip("()"))
                generes = row["genres"]#.split('|')
                self._items[i] = Movie(movieid, titol, any_movie, generes) 
                self._pos_items[movieid] = i

                movies.add(row["movieId"])

        return movies

    def get_genres(self):
        llista_generes = []
        for item in self._items.values(): #insertion order (First in first out) meaning we are doing a for in the order of the columns 
            llista_generes.append(item.get_genres())
        return llista_generes


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
        ratings = np.negative( np.ones([number_of_users,number_of_items], dtype=np.int8) )
        with open(NOM_FITXER_RATING_BOOKS, 'r', encoding="utf-8") as csvfile:
            dict_reader = csv.DictReader(csvfile, delimiter=',')
            for row in dict_reader:
                user_id = row["User-ID"]
                isbn = row["ISBN"]

                if user_id in self._pos_users.keys() and isbn in self._pos_items.keys(): #Hi haurà molts que no hi estàn
                    ratings[self._pos_users[user_id], self._pos_items[isbn]] = np.int8(row["Book-Rating"]) 

        return ratings


    def carrega_users(self,nom_fitxer):
        temp_users = dict()
        with open(NOM_FITXER_RATING_BOOKS, 'r', encoding="utf-8") as csvfile:   
            bookreader = csv.DictReader(csvfile, delimiter=',')
            for row in bookreader:
                if row["ISBN"] in self._all_items:
                    if row["User-ID"] in temp_users: # and int(row["Book-Rating"]) > 0:
                        temp_users[row["User-ID"]] += 1
                    else:
                        temp_users[row["User-ID"]] = 1

        users = set([user_id for user_id, num_relevancia in sorted(temp_users.items(), key=lambda x: x[1], reverse=True)[:10000]])

        with open(NOM_FITXER_BOOKS_USERS, 'r', encoding="utf-8") as csvfile:  
            dict_reader = csv.DictReader(csvfile)
            pos = 0
            for row in dict_reader:
                if row["User-ID"] in users:
                    self._users[pos] = User(row["User-ID"],row["Location"],row["Age"])
                    self._pos_users[row["User-ID"]] = pos
                    pos += 1

        if len(users) != len(self._users):
            raise ImportError

        return users
    

    def carrega_items(self,nom_fitxer):
        books = set()

        with open(NOM_FITXER_BOOKS, 'r', encoding="utf-8") as csvfile:   
                bookreader = csv.DictReader(csvfile, delimiter=',') 
                for i,row in enumerate(bookreader):
                    isbn = row["ISBN"]
                    titol = row["Book-Title"]
                    autor = row["Book-Author"]
                    year = row["Year-Of-Publication"]
                    publisher = row["Publisher"]
                    self._items[i] = Book(isbn, titol, autor, year, publisher) 
                    self._pos_items[isbn] = i

                    books.add(row["ISBN"])

                    if i==10000:
                        break
        
        return books

    def get_genres(self):
        raise NotImplemented

