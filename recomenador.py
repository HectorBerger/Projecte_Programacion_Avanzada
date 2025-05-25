from dataset import Dataset
from avaluador import Avaluador
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import math, random, l
from abc import ABC, abstractmethod


class Recomenador(ABC):
    """
    Classe abstracta que defineix la interfície comuna per a diferents
    estratègies de recomanació.

    Parameters
    ----------
    dataset : Dataset
        Objecte dataset que conté les dades d'usuaris, ítems i valoracions.

    Attributes
    ----------
    _dataset : Dataset
        Dataset utilitzat per fer recomanacions.
    _recomanacions : dict
        Recomanacions generades per usuari.
    _prediccions : dict
        Totes les prediccions (valoracions esperades) per usuari.
    _avaluacions : dict
        Resultats d'avaluació (objectes Avaluador) per usuari.
    """

    def __init__(self, dataset: Dataset):
        """
        Inicialitza l'objecte Recomenador amb un dataset donat.

        Parameters
        ----------
        dataset : Dataset
            Objecte dataset que conté usuaris, ítems i valoracions.
        """
        self._dataset = dataset
        self._recomanacions = dict()
        self._prediccions = dict()
        self._avaluacions = dict()

    def has_user(self, user_id: str):
        """
        Comprova si l'usuari existeix al dataset.

        Parameters
        ----------
        user_id : str
            Identificador de l'usuari.

        Returns
        -------
        bool
            True si l'usuari existeix.
        """
        return user_id in self._dataset.get_users()

    def sample_users(self, k=5):
        """
        Retorna una mostra aleatòria d'usuaris del dataset.

        Parameters
        ----------
        k : int, optional
            Nombre d'usuaris a retornar (default és 5).

        Returns
        -------
        list
            Llista d'identificadors d'usuaris.
        """
        return random.sample(list(self._dataset.get_users()), k)

    def recomenar(self, user_id: str, num_r: int = 5):
        """
        Genera recomanacions per a un usuari determinat.

        Parameters
        ----------
        user_id : str
            Identificador de l'usuari.
        num_r : int, optional
            Nombre màxim de recomanacions a retornar (default és 5).

        Returns
        -------
        bool
            True si les recomanacions s'han generat correctament.
        """
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

        if not self.algoritme(ratings, user_row, llista_prediccions):
            return False

        # Només guardem les tuples prediccio a la llista de recomenacions pertinents
        llista_recomenacions = []
        for prediccio in llista_prediccions.copy():
            if user_row[self._dataset.get_col_item(prediccio[0])] == -1: #prediccio = tuple(id_item, score) per tant mirem que l'item no hagi estat valorat per l'usuari   
                llista_recomenacions.append(prediccio)
                llista_prediccions.remove(prediccio)

        # Sort the scores and return the top 5 (or num_r) recommendations
        llista_recomenacions = sorted(llista_recomenacions, key=lambda x: x[1], reverse=True )
        llista_prediccions = sorted(llista_prediccions, key=lambda x: x[1], reverse=True )
        self._recomanacions[user_id] = llista_recomenacions[:num_r]
        self._prediccions[user_id] = llista_prediccions

        return True

    @abstractmethod
    def algoritme(self, ratings:np.ndarray, user_row:np.ndarray, llista_prediccions:list, arg:int):
        """
        Algoritme específic de recomanació implementat per subclasses.

        Parameters
        ----------
        ratings : np.ndarray
            Matriu de valoracions del dataset.
        user_row : np.ndarray
            Fila corresponent a l'usuari.
        llista_prediccions : list
            Llista on s'afegeixen tuples (item_id, score).

        Returns
        -------
        bool
            True si s'ha pogut calcular correctament.
        """
        raise NotImplementedError

    def imprimir_recomanacions(self, user_id: str) -> bool:
        """
        Imprimeix les recomanacions per a un usuari donat.

        Parameters
        ----------
        user_id : str
            Identificador de l'usuari.

        Returns
        -------
        bool
            True si hi ha recomanacions per imprimir.
        """
        if user_id not in self._recomanacions:
            print(
                f"No hi ha recomanacions disponibles per a l'usuari {user_id}."
            )
            return False
        else:
            user = self._dataset.get_user_obj(user_id)
            print(f"Recomanació per a l'{user}:")
            for i, tupla in enumerate(self._recomanacions[user_id]):  # tupla = item_id, score
                item = self._dataset.get_item_obj(tupla[0])
                print(f" {i+1}: {item} amb predicted score {tupla[1]:.3f}")
            return True

    def test(self, user_id: str):
        """
        Avalua les prediccions d'un usuari si no s'han avaluat encara.

        Parameters
        ----------
        user_id : str
            Identificador de l'usuari.

        Returns
        -------
        Avaluador or str
            Objecte amb mètriques d'avaluació o missatge d'error.
        """

        if not user_id in self._avaluacions:
            if self.recomenar(user_id):

                pred = []
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
                logging.error("Error al fer les prediccions de l'evaluació")
                return "Error al fer les prediccions."

        return self._avaluacions[user_id]

    def imprimir_prediccions(self, user_id: str) -> bool:
        """
        Imprimeix les millors prediccions per a un usuari.

        Parameters
        ----------
        user_id : str
            Identificador de l'usuari.

        Returns
        -------
        bool
            True si les prediccions existeixen i es poden mostrar.
        """
        try:
            N = int(input("Quantes millors prediccions vols mostrar (per defecte són 5): "))
        except:
            N = 5

        if not user_id in self._prediccions:
            print(f"No hi ha prediccions disponibles per a l'usuari {user_id}.")
            return False
        else:
            user = self._dataset.get_user_obj(user_id)
            print(f"Recomanació per a l'{user}:")
            for i, tupla in enumerate(self._prediccions[user_id][:N]):  # tupla = item_id, score
                item = self._dataset.get_item_obj(tupla[0])
                print(f" {i+1}: {item} amb predicted score {tupla[1]:.3f}")
            return True
    
class Simple(Recomenador):
    """
    Recomanador basat en mitjanes ponderades.

    Aquesta estratègia assigna una puntuació a cada ítem basant-se en la seva mitjana de valoracions i
    el nombre de valoracions rebudes, ponderant respecte a la mitjana global.

    Mètode ideal quan no hi ha informació personalitzada ni similituds disponibles.
    """

    def get_num_vots(self, item_id: str, ratings):
        """
        Retorna el nombre de valoracions que ha rebut un ítem.

        Parameters
        ----------
        item_id : str
            Identificador de l'ítem.
        ratings : np.ndarray
            Matriu de valoracions.

        Returns
        -------
        int
            Nombre de valoracions diferents de -1.
        """
        col = self._dataset.get_col_item(item_id)
        column_values = ratings[:, col]
        return np.count_nonzero(column_values != -1)  # Retorna quantes valoracions són no-zero (valoracions reals)

    def get_avg(self, item_id: str, ratings):
        """
        Retorna la mitjana de valoracions d’un ítem.

        Parameters
        ----------
        item_id : str
            Identificador de l'ítem.
        ratings : np.ndarray
            Matriu de valoracions.

        Returns
        -------
        float
            Mitjana de les valoracions.
        """
        col = self._dataset.get_col_item(item_id)
        values = ratings[:, col]
        avaluades = values[values != -1]
        return np.mean(avaluades) if len(avaluades) > 0 else 0

    def get_avg_global(self):
        """
        Retorna la mitjana global de totes les valoracions del dataset.

        Returns
        -------
        float
            Mitjana global.
        """
        all_vals = self._dataset.get_ratings()
        valid = all_vals[all_vals != -1]
        return np.mean(valid) if len(valid) > 0 else 0

    def algoritme(self, ratings:np.ndarray, user_row: np.ndarray, llista_prediccions: list) -> bool:
        """
        Implementa l'algoritme de recomanació simple basat en mitjanes ponderades.

        Parameters
        ----------
        ratings : np.ndarray
            Matriu de valoracions.
        user_row : np.ndarray
            Vector de valoracions de l'usuari.
        llista_prediccions : list
            Llista on s'afegeixen tuples (item_id, score).

        Returns
        -------
        bool
            True si s'ha pogut calcular correctament.
        """
        try:
            min_vots = int(input("Introdueix el parametre vots mínims (Si no posses res el default serà 10): "))
        except (ValueError, TypeError):
            min_vots = 10

        valid = ratings[ratings != -1]
        avg_global = np.mean(valid) if len(valid) > 0 else 0

        # Iterem per tots els ítems disponibles
        for item_id in self._dataset.get_items(): #!#!# Respuesta: ya lo he cambiado yo, había aque crear un getter 
            num_vots = self.get_num_vots(item_id,ratings)
            if num_vots < min_vots:
                continue  # No prou fiable

            # Calculem la mitjana d’aquest ítem 
            avg_item = self.get_avg(item_id,ratings)

            # Calculem el score ponderat segons la fórmula
            score = (num_vots / (num_vots + min_vots)) * avg_item + \
                    (min_vots / (num_vots + min_vots)) * avg_global            

            llista_prediccions.append( (item_id, score) ) #Guardem predicció

        return True


class Colaboratiu(Recomenador):
    """
    Recomanador col·laboratiu basat en la similitud entre usuaris.

    Aquesta estratègia busca usuaris similars (veïns) i prediu la valoració que faria l'usuari
    observant les valoracions d'aquests veïns.
    """

    def algoritme(self, array_ratings:np.ndarray, user_row:np.ndarray, llista_prediccions:list):
        """
        Implementa l'algoritme col·laboratiu (user-user) basat en similitud cosinus.

        Parameters
        ----------
        array_ratings : np.ndarray
            Matriu de valoracions.
        user_row : np.ndarray
            Vector de valoracions de l'usuari.
        llista_prediccions : list
            Llista on s'afegeixen tuples (item_id, score).

        Returns
        -------
        bool
            True si l'algoritme s'ha executat correctament.
        """
        try:
            k = int(input("Introdueix el nombre de veïns k (Si no introdueixes res, el valor per defecte serà 10): "))
        except (ValueError, TypeError):
            k = 10

        llista_similitud = []

        # 1 Calcular similituds
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

        # 2 Seleccionar els k veins més similars
        llista_similitud = sorted(llista_similitud, key=lambda x: x[1], reverse=True)[:k] #Ordenem segons el score de més gran a més petit

        # Step 3: Calculate scores for items not rated by the user

        # Pre-càlculs per ser més eficients i l'array dels top-k veins 
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
    """
    Recomanador basat en continguts.

    Utilitza les característiques dels ítems (com gèneres) per calcular un perfil de l'usuari
    i recomanar ítems similars als que ja ha valorat positivament.
    """

    def algoritme(self, array_ratings:np.ndarray, user_row:np.ndarray, llista_prediccions:list):
        """
        Implementa el filtratge basat en continguts utilitzant TF-IDF dels gèneres.

        Parameters
        ----------
        array_ratings : np.ndarray
            Matriu de valoracions.
        user_row : np.ndarray
            Vector de valoracions de l'usuari.
        llista_prediccions : list
            Llista on s'afegeixen tuples (item_id, score).

        Returns
        -------
        bool
            True si l'algoritme s'ha executat correctament.
        """
        # 1. Obtenir els gèneres (característiques dels ítems)
        try:
            item_features = self._dataset.get_genres()
        except:
            print("No es pot utilitzar l'algoritme basat en continguts amb el dataset Books ja que els items manquen els generes o categories.")
            return False

        # 1.1 Filtrar ítems que tinguin gèneres vàlids
        idx_valids = [i for i, g in enumerate(item_features) if g.strip().lower() != "(no genres listed)"]
        if not idx_valids:
            raise ValueError("Cap ítem té gèneres vàlids.")

        # 1.2 Filtrar els arrays corresponents
        item_features_filtrats = [item_features[i] for i in idx_valids]
        user_row_filtrat = user_row[idx_valids]

        # 1.3 Crear matriu TF-IDF només amb els ítems vàlids
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(item_features_filtrats).toarray()

        # 1.4 Filtrar les valoracions reals de l’usuari (no -1)
        mask_valorats = user_row_filtrat != -1
        if not np.any(mask_valorats):
            raise ValueError("L'usuari no ha valorat cap ítem vàlid.")

        user_row_valorats = user_row_filtrat[mask_valorats]
        tfidf_valorats = tfidf_matrix[mask_valorats]

        # 2.  Calcular el perfil
        denominator = np.sum(np.abs(user_row_valorats))
        if denominator == 0:
            raise ZeroDivisionError("Valoracions del usuari totes zero.")
        perfil = np.sum(user_row_valorats[:, np.newaxis] * tfidf_valorats, axis=0) / denominator

        # 3. Similitud cosinus
        numerador = np.dot(tfidf_matrix, perfil.T)
        normes_items = np.linalg.norm(tfidf_matrix, axis=1)
        norma_perfil = np.linalg.norm(perfil)

        if norma_perfil == 0 or np.any(normes_items == 0):
            raise ValueError("Perfil buit o hi ha ítems amb vector nul.")

        S = numerador / (normes_items * norma_perfil)

        # 4. Escalar per obtenir puntuació final
        pfinal = S * self._dataset.get_pmax()

        # 5. Afegir les prediccions
        for i, idx in enumerate(idx_valids):
            score = pfinal[i]
            llista_prediccions.append((self._dataset.get_item_id(idx), score))

        return True
