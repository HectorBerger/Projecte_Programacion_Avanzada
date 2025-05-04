from dataset import Dataset
import numpy as np

class Recomenador:
    _dataset: Dataset

    def __init__(self, dataset) -> True:
        self._dataset = dataset
        return True
        
    def recomanacio_simple(self, user_id, min_vots=3):
        # Comprova si l’usuari existeix al dataset
        if user_id not in self._dataset._pos_users:
            print(f"Usuari {user_id} no trobat.")
            return None

        # Obté la fila de la matriu que correspon a aquest usuari i les seves valoracions
        user_row = self._dataset._pos_users[user_id]
        ratings = self._dataset._ratings[user_row]

        millor_item = None # Aquí guardarem l’ítem recomanat
        millor_score = -1  # Inicialitzem el millor score

        # Iterem per tots els ítems disponibles
        for item_id, col in self._dataset._pos_items.items():
            # Si l’usuari ja ha valorat aquest ítem, el saltem
            if ratings[col] > 0:
                continue  # Ja l'ha valorat

            # Comptem quants vots té aquest ítem i mirem que sigui fiable
            num_vots = self.get_num_vots(item_id)
            if num_vots < min_vots:
                continue  # No prou fiable

            # Calculem la mitjana d’aquest ítem i la mitjana global
            avg_item = self.get_avg(item_id)
            avg_global = self.get_avg_global()

            # Calculem el score ponderat segons la fórmula
            score = (num_vots / (num_vots + min_vots)) * avg_item + \
                    (min_vots / (num_vots + min_vots)) * avg_global

            # Si aquest score és millor que l’anterior, l’actualitzem
            if score > millor_score:
                millor_score = score
                millor_item = item_id

        return millor_item

    def recomanacio_colaboratiu(self, user, item):
        pass

    def get_num_vots(self, item_id):
        col = self._dataset._pos_items[item_id]  # Obté la columna corresponent
        column_values = self._dataset._ratings[:, col]  # Obté els valors de la columna
        return np.count_nonzero(column_values)  # Retorna quantes valoracions són no-zero (valoracions reals)

    def get_avg(self, item_id):
        col = self._dataset._pos_items[item_id]   # Obté la columna corresponent a l'ítem
        values = self._dataset._ratings[:, col]   # Obté els valors de la columna
        non_zero = values[values > 0] # Filtra només les valoracions que són més grans que 0
        return np.mean(non_zero) if len(non_zero) > 0 else 0  # Retorna la mitjana si n’hi ha
    
    def get_avg_global(self):
        all_ratings = self._dataset._ratings # Obté tota la matriu de valoracions del dataset
        non_zero = all_ratings[all_ratings > 0]  # Filtra només les valoracions positives
        return np.mean(non_zero) if len(non_zero) > 0 else 0 # Retorna la mitjana global