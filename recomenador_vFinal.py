from dataset import Dataset
from avaluador import Avaluador
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import math
import random
from abc import ABC, abstractmethod

#!#!#! Nos quedamos con este no????
class Recomenador(ABC):
    """
    Classe abstracta que defineix la interfície comuna per a diferents
    estratègies de recomanació.
    """

    def __init__(self, dataset: Dataset):
        self._dataset = dataset
        self._recomanacions = dict()
        self._prediccions = dict()
        self._avaluacions = dict()

    def has_user(self, user_id: str):
        return user_id in self._dataset.get_users()
    
    def sample_users(self, k=5):
        return random.sample(list(self._dataset.get_users()), k)

    def recomenar(self, user_id: str, num_r: int = 5):
        if not self.has_user(user_id):
            print(f"Usuari {user_id} no trobat.")
            return False
        
        if user_id in self._recomanacions and user_id in self._prediccions:
            print(f"Prediccions i recomanacions ja fetes per {user_id}.")
            return True
        
        ratings = self._dataset.get_ratings()

        user_pos = self._dataset.get_row_user(user_id)
        user_row = ratings[user_pos]

        llista_prediccions = []
        
        min_vots = int(input("Introdueix el parametre vots mínims: ")) #no deberia ser algo mas generico para todos los algoritmos?
        self.algoritme(ratings, user_row, llista_prediccions, min_vots)

        """
        match algoritme:
            case "Simple":
                min_vots = int(input("Introdueix el parametre vots mínims: "))
                self.algoritme(ratings, user_id, llista_recomenacions, min_vots)
            case "Col·laboratiu":
                k = int(input("Introdueix el nombre d'elements més similars que tindrá en compte l'algoritme:"))
                self.recom_colaborativa(ratings, user_id,llista_recomenacions, k)
            case "Contingut":
                self.recom_basat_en_continguts(ratings, user_id, llista_recomenacions, 0)
        """        

        # Només guardem les tuples prediccio a la llista de recomenacions pertinents
        llista_recomenacions = []
        for prediccio in llista_prediccions.copy():
            if user_row[ self._dataset.get_col_item(prediccio[0]) ] == -1: #prediccio = tuple(id_item, score) per tant mirem que l'item no hagi estat valorat per l'usuari   
                llista_recomenacions.append(prediccio)
                llista_prediccions.remove(prediccio)
                
        
        # Sort the scores and return the top 5 (or num_r) recommendations
        llista_recomenacions = sorted(llista_recomenacions, key=lambda x: x[1], reverse=True )
        self._recomanacions[user_id] = llista_recomenacions[:num_r]
        self._prediccions[user_id] = llista_prediccions

        return True
    
    @abstractmethod
    def algoritme(self, ratings:np.ndarray, user_row:np.ndarray, llista_prediccions:list, arg:int):
        raise NotImplementedError 

    def imprimir_recomanacions(self, user_id: str):
        """Imprimeix les recomanacions per a un usuari donat."""
        if not user_id in self._recomanacions:
            print(f"No hi ha recomanacions disponibles per a l'usuari {user_id}.")
            return False
        else:
            user = self._dataset.get_user_obj(user_id)
            print(f"Recomanació per a l'{user}:")
            for i, tupla in enumerate(self._recomanacions[user_id]): #tupla = item_id, score
                item = self._dataset.get_item_obj(tupla[0])
                print(f" {i+1}: {item} amb predicted score {tupla[1]:.3f}")
            return True
    
    def get_num_vots(self, item_id: str):
        """Retorna el nombre de vots per a un ítem donat."""
        col = self._dataset.get_col_item(item_id)
        column_values = self._dataset.get_ratings()[:, col]
        return np.count_nonzero(column_values != -1)  # Retorna quantes valoracions són no-zero (valoracions reals)
    
    def get_avg(self, item_id: str):
        """Retorna la mitjana de valoracions per a un ítem donat."""
        col = self._dataset.get_col_item(item_id)
        values = self._dataset.get_ratings()[:, col]
        avaluades = values[values != -1]
        return np.mean(avaluades) if len(avaluades) > 0 else 0
    
    def get_avg_global(self):
        all_vals = self._dataset.get_ratings()
        valid = all_vals[all_vals != -1]
        return np.mean(valid) if len(valid) > 0 else 0
    
    def test(self, user_id):
        
        if not user_id in self._avaluacions:
            if self.recomenar(user_id):
                
                pred =  []
                reals = []

                user_pos = self._dataset.get_row_user(user_id)
                user_row = self._dataset.get_ratings()[user_pos]

                for item_id, score_pred in self._prediccions.get(user_id, []):
                    try:
                        col = self._dataset.get_col_item(item_id)
                        valor_real = user_row[col]
                        if valor_real != -1:
                            pred.append(score_pred)
                            reals.append(valor_real)
                    except KeyError:
                        continue
                
                a = Avaluador(user_id)
                a.mae(pred, reals)
                a.rmse(pred, reals)
                self._avaluacions[user_id] = a
            else:
                return "Error al fer les prediccions."

        return self._avaluacions[user_id]
    
class Simple(Recomenador):
    
    def algoritme(self, ratings:np.ndarray, user_row:np.ndarray, llista_prediccions:list, min_vots:int = 10) -> bool:
        """Recomanació simple basada en la mitjana ponderada de les valoracions."""

        avg_global = self.get_avg_global() 

        # Iterem per tots els ítems disponibles
        for item_id in self._dataset.get_items(): #!#!# Respuesta: ya lo he cambiado yo, había aque crear un getter 
            num_vots = self.get_num_vots(item_id)
            if num_vots < min_vots:
            
                continue  # No prou fiable

            # Calculem la mitjana d’aquest ítem 
            avg_item = self.get_avg(item_id)

            # Calculem el score ponderat segons la fórmula
            score = (num_vots / (num_vots + min_vots)) * avg_item + \
                    (min_vots / (num_vots + min_vots)) * avg_global            
            
            llista_prediccions.append( (item_id, score) ) #Guardem predicció

        return True
    
class Colaboratiu(Recomenador):

    def algoritme(self, array_ratings:np.ndarray, user_row:np.ndarray, llista_prediccions:list, k:int):
        """Recomanació col·laborativa basada en la similitud entre usuaris."""
        
        llista_similitud = []

        #1 Calcular similituds
        for i,row in enumerate(array_ratings): #i = numero de fila del veï 
            if not np.array_equal(row, user_row):
                mask = (user_row != -1) & (row != -1)
                if np.any(mask):
                    denominator = (
                        math.sqrt(np.sum(np.power(user_row[mask], 2))) *
                        math.sqrt(np.sum(np.power(row[mask], 2)))
                    )
                    if denominator != 0:
                        similitud = np.dot(user_row[mask], row[mask]) / denominator
                    else:
                        similitud = 0
                else:
                    similitud = 0

                llista_similitud.append((i, similitud))
        
        if not llista_similitud:
            return False

        #2 Seleccionar els k veins més similars
        llista_similitud = sorted(llista_similitud, key=lambda x: x[1], reverse=True)[:k] #Ordenem segons el score de més gran a més petit

        # Step 3: Calculate scores for items not rated by the user
        
        #Pre-càlculs per ser més eficients i l'array dels top-k veins 
        mitja_user = np.mean(user_row[user_row != -1]) #Esto lo podriamos hacer al iniciar en el pickle
        veins_arrays = array_ratings[[sim[0] for sim in llista_similitud], :]
        mitjas_veins = np.column_stack(np.array([np.mean(row[row != -1]) if np.any(row != -1) else 0 for row in veins_arrays]))  # Mean ratings of all neighbors
        columna_similitud = np.column_stack(np.array([sim[1] for sim in llista_similitud])) # Similarities with top-k veins

        for item_id, col in self._dataset._pos_items.items(): #S'ha d'iterar per items no vists per l'user (columnes)
            veins_col = np.column_stack(veins_arrays[:, col])  # Ratings of the current item by all neighbors

            # Mask for neighbors who rated the item
            veins_mask = veins_col != -1

            # Calculate the numerator and denominator
            numerator = np.sum( columna_similitud[veins_mask] * (veins_col[veins_mask] - mitjas_veins[veins_mask]) )
            denominator = np.sum(np.abs(columna_similitud[veins_mask]))

            # Calculate the final score
            if denominator != 0:
                score = mitja_user + numerator / denominator
            else:
                score = mitja_user  # Default to the user's mean if no neighbors rated the item
                
            llista_prediccions.append((item_id, score)) # Guardem predicció

        return True



class BasatEnContinguts(Recomenador):
    
    def algoritme(self, array_ratings:np.ndarray, user_row:np.ndarray, llista_prediccions:list, arg2): 
        #1
        item_features = self._dataset.get_genres()
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(item_features).toarray()

        #2
        denominator = np.sum(user_row)
        if denominator != 0:
            perfil = np.sum(np.reshape(user_row, (-1, 1)) * tfidf_matrix, axis=0) / denominator
        else:
            raise ValueError("L'usuari no ha valorat a ningú")
        
        #3
        S = np.dot(tfidf_matrix, perfil.T)
        
        #4
        PMAX = 5 # La puntuació máxima en el cas de Movies 
        pfinal = S * PMAX #podriamos poner un atributo, si pero como solo es para esto igual esta bien asi

        """mask = user_row == -1
        posicions_no_valorades = np.where(mask)[0]  # índexs reals al dataset

        for idx in posicions_no_valorades:
            score = pfinal[idx] #ERROR
            llista_recomenacions.append( (self._dataset.get_item_id(idx), score))"""

        for idx, item_id in enumerate(self._dataset.get_items()):
            score = pfinal[idx]
            llista_prediccions.append((item_id, score))

        return True

    
    
    
    