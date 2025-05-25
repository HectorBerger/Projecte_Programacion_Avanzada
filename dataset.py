from typing import Dict
from items import Item, Book, Movie, VideoGame
from abc import ABC, abstractmethod 
from user import User
import csv, os, logging
import numpy as np
from toolkit import timer, parse, clean_price

#Constants amb els paths pels arxius d'on estreurem la informació
NOM_FITXER_MOVIES = "dataset\\MovieLens100k\\movies.csv"
NOM_FITXER_RATINGS_MOVIES = "dataset\\MovieLens100k\\ratings.csv"

NOM_FITXER_BOOKS = "dataset\\Books\\Books.csv"
NOM_FITXER_BOOKS_USERS = "dataset\\Books\\Users.csv"
NOM_FITXER_RATING_BOOKS = "dataset\\Books\\Ratings.csv" 

NOM_FITXER_VIDEOGAMES_METADATA = "dataset\\VideoGames\\meta_Video_Games.json.gz"
NOM_FITXER_RATINGS_VIDEOGAMES = "dataset\\VideoGames\\Video_Games_5.json.gz"


class Dataset(ABC):
    """
    Classe abstracta que representa un conjunt de dades de recomanació.

    Aquesta classe proporciona la infraestructura comuna per carregar, organitzar i accedir a dades de recomanació.
    Les subclasses concretes com DatasetMovies, DatasetBooks i DatasetVideoGames han d’implementar els mètodes abstractes.

    Attributes
    ----------
    _users : dict[int, User]
        Diccionari que mapeja una fila (índex) a un objecte User.
    _items : dict[int, Item]
        Diccionari que mapeja una columna (índex) a un objecte Item.
    _pos_users : dict[str, int]
        Diccionari que mapeja l'identificador de l'usuari a la seva fila (índex).
    _pos_items : dict[str, int]
        Diccionari que mapeja l'identificador de l'ítem a la seva columna (índex).
    _ratings : np.ndarray
        Matriu de valoracions on files són usuaris i columnes són ítems. Valor -1 indica absència de valoració.
    _pmax : int
        Valor màxim possible d’una valoració.
    _all_users : set
        Conjunt amb tots els identificadors d’usuaris presents al dataset.
    _all_items : set
        Conjunt amb tots els identificadors d’ítems presents al dataset.
    """

    _users: Dict[int , User] # fila : User
    _items: Dict[int , Item] # columna : Item
    _pos_users: Dict[str, int] #id_user : fila
    _pos_items: Dict[str, int] #id_item : columna
    _ratings: np.array 
    _pmax: int
    _all_users: set
    _all_items: set
    
    def __init__(self) -> bool:

        """
        Inicialitza la infraestructura bàsica del dataset, carregant les valoracions i validant la consistència
        entre índexs i identificadors d’usuaris i ítems.

        Returns
        -------
        bool
            True si la inicialització és correcta.

        Raises
        ------
        RuntimeError
            Si hi ha un error en carregar les valoracions o en assignar posicions.
        """

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
            logging.critical("S'ha detectat un comportament inesperat: assignant posicions als items incorrectes")
            raise RuntimeError(f"Error assignant posicions als items: {e}")

        try:
            for i in range(len(self._all_users)):
                user_id = self.get_user_id(i)
                i_retrobat = self.get_row_user(user_id)
                assert i == i_retrobat, f"Error: idx={i}, idx_retrobat={i_retrobat}"
        except Exception as e:
            logging.critical("S'ha detectat un comportament inesperat: assignant posicions als usuaris incorrectes")
            raise RuntimeError(f"Error assignant posicions als usuaris: {e}")
        
        return True

    @abstractmethod
    def carrega_ratings(self):
        """
        Carrega les valoracions del dataset.

        Returns
        -------
        np.ndarray
            Matriu de valoracions.

        Raises
        ------
        NotImplementedError
            Si la subclasse no implementa aquest mètode.
        """
        raise NotImplementedError
                   
    @abstractmethod
    def carrega_users(self):
        """
        Carrega els usuaris del dataset.

        Returns
        -------
        set
            Conjunt d'identificadors d'usuaris.
        Raises
        ------
        NotImplementedError
            Si el mètode no està implementat.
        """
        raise NotImplementedError   

    @abstractmethod
    def carrega_items(self):
        """
        Carrega els ítems del dataset.

        Returns
        -------
        set
            Conjunt d'identificadors d'ítems.
        Raises
        ------
        NotImplementedError
            Si el mètode no està implementat.
        """
        raise NotImplementedError   

    def set_pmax(self, puntuacio_maxima):
        """
        Estableix la puntuació màxima.

        Parameters
        ----------
        puntuacio_maxima : int
            Valor màxim que pot prendre una valoració.

        Raises
        ------
        ValueError
            Si no es pot convertir a enter.
        """
        try:
            self._pmax = abs(int(puntuacio_maxima))
        except:
            logging.warning("Puntuació màxima no assignada, no funcionará l'algoritme basat en continguts")
            raise ValueError

    def get_pmax(self):
        """
        Retorna la puntuació màxima.

        Returns
        -------
        int
            Valor màxim de les valoracions.

        Raises
        ------
        AttributeError
            Si _pmax encara no ha estat establert.
        """
        if self._pmax is not None:
            return self._pmax
        raise AttributeError

    def get_ratings(self):
        """
        Retorna la matriu de valoracions.

        Returns
        -------
        np.ndarray
            Matriu de valoracions.
        """
        return self._ratings
    
    def get_users(self):
        """
        Retorna el conjunt d'usuaris.

        Returns
        -------
        set
            Identificadors d'usuaris.
        """
        return self._all_users   
    
    def get_row_user(self, id_user:str):
        """
        Retorna la fila corresponent a un usuari.

        Parameters
        ----------
        id_user : str
            Identificador de l'usuari.

        Returns
        -------
        int
            Índex de fila.

        Raises
        ------
        ValueError
            Si l'usuari no es troba al dataset.
        """
        if id_user in self._pos_users.keys():
            return self._pos_users[id_user]
        raise ValueError

    def get_user_obj(self, id_user:str):
        """
        Retorna l'objecte User corresponent a l'identificador.

        Parameters
        ----------
        id_user : str
            Identificador de l'usuari.

        Returns
        -------
        User
            Objecte de l'usuari.
        """
        fila = self.get_row_user(id_user)
        return self._users[fila]
    
    def get_user_id(self, pos_user:int):
        """
        Retorna l'identificador d'un usuari a partir de la seva posició.

        Parameters
        ----------
        pos_user : int
            Índex de fila.

        Returns
        -------
        str
            Identificador de l'usuari.

        Raises
        ------
        KeyError
            Si la posició no existeix.
        """
        if pos_user in self._users.keys():
            return self._users[pos_user].get_id()
        raise KeyError
    
    def get_items(self):
        """
        Retorna el conjunt d'ítems.

        Returns
        -------
        set
            Conjunt d'identificadors d'ítems.
        """
        return self._all_items
    
    def get_col_item(self, id_item:str):
        """
        Retorna la columna corresponent a un ítem.

        Parameters
        ----------
        id_item : str
            Identificador de l'ítem.

        Returns
        -------
        int
            Índex de columna.

        Raises
        ------
        KeyError
            Si l'ítem no es troba al dataset.
        """
        if id_item in self._pos_items.keys():
            return self._pos_items[id_item]
        raise KeyError
    
    def get_item_obj(self, item_id:str):
        """
        Retorna l'objecte Item corresponent a l'identificador.

        Parameters
        ----------
        item_id : str
            Identificador de l'ítem.

        Returns
        -------
        Item
            Objecte de l'ítem.
        """
        col = self.get_col_item(item_id)
        return self._items[col]
    
    def get_item_id(self, pos_item:int):
        """
        Retorna l'identificador d'un ítem a partir de la seva posició.

        Parameters
        ----------
        pos_item : int
            Índex de columna.

        Returns
        -------
        str
            Identificador de l'ítem.

        Raises
        ------
        KeyError
            Si la posició no existeix.
        """
        if pos_item in self._items.keys():
            return self._items[pos_item].get_id()
        raise KeyError
    
    def get_genres(self):
        """
        Retorna la llista de gèneres dels ítems.

        Returns
        -------
        list
            Llista de gèneres per a cada ítem.

        Raises
        ------
        NotImplementedError
            Aquest mètode ha de ser implementat per les subclasses.
        """
        raise NotImplementedError


class DatasetMovies(Dataset):
    """
    Dataset que carrega i gestiona les dades de MovieLens (pel·lícules).

    Hereta de Dataset i implementa els mètodes per carregar pel·lícules, usuaris i valoracions.

    Notes
    -----
    Les valoracions es llegeixen d'un fitxer CSV i es guarden en una matriu NumPy de float16.
    Els valors inicials de la matriu són -1 per indicar absència de valoració.
    """

    def __init__(self):
        """
        Inicialitza el dataset de pel·lícules i carrega les dades.

        Raises
        ------
        RuntimeError
            Si hi ha un error en la inicialització del dataset pare.
        """
        if super().__init__():
            print("LOADED")
        else:
            logging.critical("Error crític: no s'ha carregat correctament l'arxiu, no es pot continuar")

    def carrega_ratings(self) -> np.ndarray:
        """
        Carrega les valoracions dels usuaris a les pel·lícules.

        Returns
        -------
        np.ndarray
            Matriu de valoracions (usuaris x pel·lícules).

        Raises
        ------
        FileNotFoundError
            Si els fitxers de dades no existeixen.
        """
        # Comprovar que els arxius existeixen abans de continuar
        if not os.path.exists(NOM_FITXER_MOVIES):
            logging.critical(f"Error crític: no s'ha carregat correctament l'arxiu {NOM_FITXER_MOVIES}, no es pot continuar")
            raise FileNotFoundError(f"No es troba l'arxiu: {NOM_FITXER_MOVIES}")
        if not os.path.exists(NOM_FITXER_RATINGS_MOVIES):
            logging.critical(f"Error crític: no s'ha carregat correctament l'arxiu {NOM_FITXER_RATINGS_MOVIES}, no es pot continuar")
            raise FileNotFoundError(f"No es troba l'arxiu: {NOM_FITXER_RATINGS_MOVIES}")
        
        #Recorrer para saber n i m (el shape de la array)
        #Carregar usuaris i movies
        self._all_items = self.carrega_items()
        logging.debug("Funciona carrega d'items")
        self._all_users = self.carrega_users()
        logging.debug("Funciona carrega d'usuaris")

        #Crear array y llenarla
        number_of_users = len(self._all_users) #n files
        number_of_items = len(self._all_items) #m columnes
        ratings = np.negative( np.ones([number_of_users,number_of_items], dtype=np.float16) )#Hemos escogido este tipo ya que necesariamente tiene que ser float porqué tenemos ratings con coma y 16 bits porqué es el más pequeño que entra nuestro máximo
        logging.debug("Funciona creació d'array")
        with open(NOM_FITXER_RATINGS_MOVIES, 'r', encoding="utf-8") as csvfile:   
            dict_reader = csv.DictReader(csvfile, delimiter=',')
            for row in dict_reader:
                user_id = row["userId"]
                movie_id = row["movieId"]

                if user_id in self._pos_users.keys() and movie_id in self._pos_items.keys():
                    ratings[self._pos_users[user_id], self._pos_items[movie_id]] = row["rating"]
                else:
                    print(f"User or movie not found: userId={user_id}, movieId={movie_id}") #DEBUG
        logging.debug("Funciona carrega de ratings")

        self.set_pmax(np.max(ratings)) # = 5

        logging.debug("Funciona assignació puntuació màxima")

        return ratings
                

    def carrega_users(self) -> set:
        """
        Carrega els usuaris que han valorat pel·lícules.

        Returns
        -------
        set
            Conjunt d'identificadors d'usuaris.
        """
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
        """
        Carrega les pel·lícules del fitxer CSV.

        Returns
        -------
        set
            Conjunt d'identificadors de pel·lícules.
        """
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
        """
        Retorna els gèneres de les pel·lícules.

        Returns
        -------
        list
            Llista amb els gèneres de cada pel·lícula.
        """
        llista_generes = []
        for item in self._items.values(): #insertion order (First in first out) meaning we are doing a for in the order of the columns 
            llista_generes.append(item.get_genres())
        return llista_generes

class DatasetBooks(Dataset):
    """
    Dataset que carrega i gestiona les dades del projecte Book-Crossing.

    Hereta de Dataset i implementa els mètodes per carregar llibres, usuaris i valoracions.

    Notes
    -----
    Es filtren els 10.000 llibres i usuaris amb més activitat per millorar el rendiment.
    """
    def __init__(self):
        """
        Inicialitza el dataset de llibres.

        Raises
        ------
        RuntimeError
            Si hi ha un error en la inicialització del dataset pare.
        """
        if super().__init__():
            print("LOADED") 
        else:
            logging.critical(f"Error crític: no s'ha carregat correctament el dataset Books, no es pot continuar")

    def carrega_ratings(self) -> np.ndarray:
        """
        Carrega les valoracions dels usuaris als llibres.

        Returns
        -------
        np.ndarray
            Matriu de valoracions (usuaris x llibres).

        Raises
        ------
        FileNotFoundError
            Si algun fitxer necessari no es troba.
        """
        # Comprovar que els arxius existeixen abans de continuar
        if not os.path.exists(NOM_FITXER_BOOKS):
            logging.critical(f"Error crític: no s'ha carregat correctament l'arxiu {NOM_FITXER_BOOKS}, no es pot continuar")
            raise FileNotFoundError(f"No es troba l'arxiu: {NOM_FITXER_BOOKS}")
        if not os.path.exists(NOM_FITXER_RATING_BOOKS):
            logging.critical(f"Error crític: no s'ha carregat correctament l'arxiu {NOM_FITXER_RATING_BOOKS}, no es pot continuar")
            raise FileNotFoundError(f"No es troba l'arxiu: {NOM_FITXER_RATING_BOOKS}")
        if not os.path.exists(NOM_FITXER_BOOKS_USERS):
            logging.critical(f"Error crític: no s'ha carregat correctament l'arxiu {NOM_FITXER_BOOKS_USERS}, no es pot continuar")
            raise FileNotFoundError(f"No es troba l'arxiu: {NOM_FITXER_BOOKS_USERS}")
        
        #Recorrer para saber n i m 
        #Carregar els primer 10.000 books i els 10.000 usuaris més adhients 
        self._all_items = self.carrega_items()
        logging.debug("Funciona carrega d'items")
        self._all_users = self.carrega_users()
        logging.debug("Funciona carrega d'usuaris")

        #Crear array y llenarla
        number_of_users = len(self._all_users) #n files
        number_of_items = len(self._all_items) #m columnes
        ratings = np.negative( np.ones([number_of_users,number_of_items], dtype=np.int8) )
        with open(NOM_FITXER_RATING_BOOKS, 'r', encoding="utf-8") as csvfile:
            dict_reader = csv.DictReader(csvfile, delimiter=',')
            for row in dict_reader:
                user_id = row["User-ID"]
                isbn = row["ISBN"]

                if user_id in self._pos_users.keys() and isbn in self._pos_items.keys(): #Hi haurà molts que no hi estàn
                    ratings[self._pos_users[user_id], self._pos_items[isbn]] = np.int8(row["Book-Rating"]) 
        logging.debug("Funciona carrega de ratings")

        return ratings


    def carrega_users(self) -> set:
        """
        Carrega els usuaris que han valorat llibres.

        Returns
        -------
        set
            Conjunt d'identificadors d'usuaris seleccionats.
        
        Raises
        ------
        ImportError
            Si no es poden crear tots els objectes User esperats.
        """
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
        """
        Carrega els llibres del fitxer CSV.

        Returns
        -------
        set
            Conjunt d'identificadors de llibres.
        """
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



class DatasetVideoGames(Dataset):
    """
    Dataset que carrega i gestiona les dades de videojocs d'Amazon.

    Hereta de Dataset i implementa els mètodes per carregar videojocs, usuaris i valoracions.

    Notes
    -----
    Utilitza fitxers JSON compressats (.gz). Limita a 10.000 ítems per rendiment.
    """

    def __init__(self):
        """
        Inicialitza el dataset de videojocs.

        Raises
        ------
        RuntimeError
            Si hi ha un error en la inicialització del dataset pare.
        """
        if super().__init__():
            print("LOADED") 
        else:
            logging.critical(f"Error crític: no s'ha carregat correctament el dataset VideoGames, no es pot continuar")


    def carrega_ratings(self):
        """
        Carrega les valoracions dels usuaris als videojocs.

        Returns
        -------
        np.ndarray
            Matriu de valoracions (usuaris x videojocs).

        Raises
        ------
        FileNotFoundError
            Si els fitxers de valoracions o metadades no es troben.
        """
        # Comprovar que els arxius existeixen abans de continuar
        if not os.path.exists(NOM_FITXER_VIDEOGAMES_METADATA):
            logging.critical(f"Error crític: no s'ha carregat correctament l'arxiu {NOM_FITXER_VIDEOGAMES_METADATA}, no es pot continuar")
            raise FileNotFoundError(f"No es troba l'arxiu: {NOM_FITXER_VIDEOGAMES_METADATA}")
        if not os.path.exists(NOM_FITXER_RATINGS_VIDEOGAMES):
            logging.critical(f"Error crític: no s'ha carregat correctament l'arxiu {NOM_FITXER_RATINGS_VIDEOGAMES}, no es pot continuar")
            raise FileNotFoundError(f"No es troba l'arxiu: {NOM_FITXER_RATINGS_VIDEOGAMES}")
        
        #Recorrer para saber n i m 
        #Carregar els primer 10.000 videogames i els 10.000 usuaris més adhients 
        self._all_items = self.carrega_items() 
        logging.debug("Funciona carrega d'items")
        self._all_users = self.carrega_users()
        logging.debug("Funciona carrega d'usuaris")

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
        logging.debug("Funciona carrega de ratings")
        valid_ratings = ratings[ratings != -1]
        if len(valid_ratings) > 0:
            self.set_pmax(np.max(valid_ratings))
        else:
            self.set_pmax(0)
        logging.debug("Funciona setter de puntuació màxima")

        return ratings
        
            
    
    def carrega_users(self) -> set:
        """
        Carrega els usuaris que han valorat videojocs.

        Returns
        -------
        set
            Conjunt d'identificadors d'usuaris seleccionats.

        Raises
        ------
        ImportError
            Si no es poden crear tots els objectes User esperats.
        """
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
        """
        Carrega els videojocs del fitxer de metadades.

        Returns
        -------
        set
            Conjunt d'identificadors de videojocs.
        """
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
                if i==10000:  #Comentar si es vol complet peró sinó és molt lent
                    break

        return video_games
    
    def get_genres(self):
        """
        Retorna els gèneres dels videojocs.

        Returns
        -------
        list
            Llista amb els gèneres de cada videojoc.
        """
        llista_generes = []
        for item in self._items.values(): 
            llista_generes.append(item.get_genres())
        return llista_generes
