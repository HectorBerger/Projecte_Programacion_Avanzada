from typing import Dict
from items import Item, Book, Movie, VideoGame
from abc import ABC, abstractmethod 
from user import User
import csv, json
import numpy as np
from toolkit import timer

NOM_FITXER_MOVIES = "dataset\\MovieLens100k\\movies.csv"
NOM_FITXER_RATINGS_MOVIES = "dataset\\MovieLens100k\\ratings.csv"

NOM_FITXER_BOOKS = "dataset\\Books\\Books.csv"
NOM_FITXER_BOOKS_USERS = "dataset\\Books\\Users.csv"
NOM_FITXER_RATING_BOOKS = "dataset\\Books\\Ratings.csv" 

NOM_FITXER_VIDEOGAMES_METADATA = "dataset\\VideoGames\\meta_Video_Games.json.gz"
NOM_FITXER_RATINGS_VIDEOGAMES = "dataset\\VideoGames\\Video_Games_5.json.gz"


class Dataset(ABC):
    _users: Dict[int , User] # fila : User
    _items: Dict[int , Item] # columna : Item
    _pos_users: Dict[str, int] #id_user : fila
    _pos_items: Dict[str, int] #id_item : columna
    _ratings: np.array 
    _pmax: int
    _all_users: set
    _all_items: set

    def __init__(self) -> bool:
        self._users = dict()
        self._items = dict()
        self._pos_users = dict() #Cambiar "pos" por "row" i "column" (o "fila" i "columna")
        self._pos_items = dict()
        self._all_users = set()
        self._all_items = set()
        self._pmax = None

        try:
            self._ratings = self.carrega_ratings() 
        except Exception as e:
            raise RuntimeError(f"Error carregant ratings: {e}")

        try:
            for i in range(len(self._all_items)):
                item_id = self.get_item_id(i)
                i_retrobat = self.get_col_item(item_id)
                assert i == i_retrobat, f"Error: idx={i}, idx_retrobat={i_retrobat}"
        except Exception as e:
            raise RuntimeError(f"Error assignant posicions als items: {e}")

        try:
            for i in range(len(self._all_users)):
                user_id = self.get_user_id(i)
                i_retrobat = self.get_row_user(user_id)
                assert i == i_retrobat, f"Error: idx={i}, idx_retrobat={i_retrobat}"
        except Exception as e:
            raise RuntimeError(f"Error assignant posicions als usuaris: {e}")
        
        return True

    @abstractmethod
    def carrega_ratings(self):
        raise NotImplementedError
                
    @abstractmethod
    def carrega_users(self):
        raise NotImplementedError   

    @abstractmethod
    def carrega_items(self):
        raise NotImplementedError   

    def set_pmax(self, puntuacio_maxima):
        try:
            self._pmax = abs(int(puntuacio_maxima))
        except:
            raise ValueError

    def get_pmax(self):
        if self._pmax is not None:
            return self._pmax
        raise AttributeError

    def get_ratings(self):
        return self._ratings
    
    def get_users(self):
        return self._all_users   
    
    def get_row_user(self, id_user:str): 
        if id_user in self._pos_users.keys():
            return self._pos_users[id_user]
        raise ValueError

    def get_user_obj(self, id_user:str):
        fila = self.get_row_user(id_user)
        return self._users[fila]
    
    def get_user_id(self, pos_user:int):
        if pos_user in self._users.keys():
            return self._users[pos_user].get_id()
        raise KeyError
    
    def get_items(self):
        return self._all_items
    
    def get_col_item(self, id_item:str):
        if id_item in self._pos_items.keys():
            return self._pos_items[id_item]
        raise KeyError
    
    def get_item_obj(self, item_id:str):
        col = self.get_col_item(item_id)
        return self._items[col]
    
    def get_item_id(self, pos_item:int):
        if pos_item in self._items.keys():
            return self._items[pos_item].get_id()
        raise KeyError
    
    def get_genres(self):
        raise NotImplementedError


class DatasetMovies(Dataset):
    def __init__(self):
        if super().__init__():
            print("LOADED") #LOG

    def carrega_ratings(self) -> np.ndarray:
        #Recorrer para saber n i m (el shape de la array)
        #Carregar usuaris i movies
        self._all_items = self.carrega_items() 
        self._all_users = self.carrega_users()

        #Crear array y llenarla
        number_of_users = len(self._all_users) #n files
        number_of_items = len(self._all_items) #m columnes
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
        
        self.set_pmax(np.max(ratings)) # = 5

        return ratings
                

    def carrega_users(self) -> set:
        users = set()

        with open(NOM_FITXER_RATINGS_MOVIES, 'r', encoding="utf-8") as csvfile:   
            user_reader = csv.DictReader(csvfile, delimiter=',')
            for row in user_reader:
                users.add(row["userId"])

        for i,iduser in enumerate(users):
            self._users[i] = User(iduser) 
            self._pos_users[iduser] = i

        return users
    
    def carrega_items(self) -> set:
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

import time
class DatasetBooks(Dataset):
    def __init__(self):
        if super().__init__():
            print("LOADED") #LOG

    def carrega_ratings(self) -> np.ndarray:
        #!#! Arreglar carrega intentar reducir la apertura de archivos y fijarse que los users creados y libros son los que se usan

        #Recorrer para saber n i m 
        #Carregar els primer 10.000 books i els 10.000 usuaris més adhients 
        self._all_items = timer(lambda: self.carrega_items()) 
        self._all_users = timer(lambda: self.carrega_users())

        #Crear array y llenarla
        number_of_users = len(self._all_users) #n files
        number_of_items = len(self._all_items) #m columnes
        ratings = np.negative( np.ones([number_of_users,number_of_items], dtype=np.int8) )
        start = time.time()
        with open(NOM_FITXER_RATING_BOOKS, 'r', encoding="utf-8") as csvfile:
            dict_reader = csv.DictReader(csvfile, delimiter=',')
            for row in dict_reader:
                user_id = row["User-ID"]
                isbn = row["ISBN"]

                if user_id in self._pos_users.keys() and isbn in self._pos_items.keys(): #Hi haurà molts que no hi estàn
                    ratings[self._pos_users[user_id], self._pos_items[isbn]] = np.int8(row["Book-Rating"]) 
        print(f"Tiempo: {time.time() - start:.2f}s")
        return ratings


    def carrega_users(self) -> set:
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
    

    def carrega_items(self) -> set:
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


import gzip,re
from scipy.sparse import lil_matrix
def parse(path):
        g = gzip.open(path, 'r')
        for l in g:
            yield json.loads(l)

def clean_price(price):
    if not price or isinstance(price, list):
        return None
    # Si es un string con símbolos de dólar, quítalos y quédate con el número
    if isinstance(price, str):
        # Busca el primer número en el string
        match = re.search(r'(\d+(\.\d+)?)', price.replace(',', ''))
        if match:
            return float(match.group(1))
        else:
            return None
    try:
        return float(price)
    except Exception:
        return None

class DatasetVideoGames(Dataset):
    def __init__(self):
        if super().__init__():
            print("LOADED") #LOG
    def carrega_ratings(self):
        #Recorrer para saber n i m 
        #Carregar els primer 10.000 videogames i els 10.000 usuaris més adhients 
        self._all_items = self.carrega_items() #Cómo damos las direcciones de los archivos? argumento/atributo/constante/o directamente? 
        self._all_users = self.carrega_users()

        #Crear array y llenarla
        number_of_users = len(self._all_users) #n files
        number_of_items = len(self._all_items) #m columnes
        ratings = np.negative( np.ones([number_of_users,number_of_items], dtype=np.float16) )
        for review in parse(NOM_FITXER_RATINGS_VIDEOGAMES): 
            user_id = review.get('reviewerID')
            asin = review.get('asin')

            if user_id in self._pos_users.keys() and asin in self._pos_items.keys(): #Hi haurà molts que no hi estàn
                    score = review.get('overall')
                    try:
                        score_float = float(score)
                        ratings[self._pos_users[user_id], self._pos_items[asin]] = np.float16(score_float)
                    except (TypeError, ValueError):
                        # Si score es None, '', o no convertible, lo ignoras
                        continue
        valid_ratings = ratings[ratings != -1]
        if len(valid_ratings) > 0:
            self.set_pmax(np.max(valid_ratings))
        else:
            self.set_pmax(0)

        return ratings
        
            
    
    def carrega_users(self) -> set:
        temp_users = dict()
        for obj in parse(NOM_FITXER_RATINGS_VIDEOGAMES):
            item_id = obj.get('asin')
            if item_id in self._all_items:
                user_id = obj.get('reviewerID')
                if user_id in temp_users: 
                    temp_users[user_id] += 1
                else:
                    temp_users[user_id] = 1
        
        users = set([user_id for user_id, num_relevancia in sorted(temp_users.items(), key=lambda x: x[1], reverse=True)[:10000]])

        pos = 0
        for obj in parse(NOM_FITXER_RATINGS_VIDEOGAMES):
            user_id = obj.get('reviewerID')
            if user_id in users and not user_id in self._pos_users.keys():
                user_name = obj.get('reviewerName')
                self._users[pos] = User(user_id,name=user_name)
                self._pos_users[user_id] = pos
                pos += 1

        if len(users) != len(self._users):
            raise ImportError
        return users
       

    def carrega_items(self) -> set:
        video_games = set()
        i=0
        for obj in parse(NOM_FITXER_VIDEOGAMES_METADATA):
            categories = obj.get('categories') or obj.get('category') or obj.get('genres')
            if categories:
                try:
                    item_id = obj.get('asin')
                    if item_id in self._pos_items:
                        raise ValueError("Objeto ya creado")
                    titol = obj.get('title')
                    brand = obj.get('brand')
                    price = clean_price(obj.get('price'))
                    description = obj.get('description')
                    if isinstance(description, list):
                        description = " ".join(str(x).strip() for x in description if x)
                    elif description is None:
                        description = ""
                    else:
                        description = str(description)
                    if not item_id or not titol:
                        raise ValueError(f"Missing required field(s) for VideoGame {item_id}")
                    self._items[i] = VideoGame(item_id, titol, categories, price, brand, description)
                    self._pos_items[item_id] = i
                except Exception:
                    continue

                video_games.add(item_id)
                i += 1
                #if i==10000:  #Treure els comentaris si va molt lent
                #    break

        return video_games
    
    def get_genres(self):
        llista_generes = []
        for item in self._items.values(): 
            llista_generes.append(item.get_genres())
        return llista_generes

