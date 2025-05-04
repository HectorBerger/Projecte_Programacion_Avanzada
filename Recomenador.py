from dataset import Dataset
import numpy as np

class Recomenador:
    _dataset: Dataset

    def __init__(self, dataset) -> True:
        self._dataset = dataset
        return True
        
    def recomanacio_simple(self, user_id, min_vots=3):
        if user_id not in self._dataset._pos_users:
            print(f"Usuari {user_id} no trobat.")
            return None

        user_row = self._dataset._pos_users[user_id]
        ratings = self._dataset._ratings[user_row]

        millor_item = None
        millor_score = -1

        for item_id, col in self._dataset._pos_items.items():
            if ratings[col] > 0:
                continue  # Ja l'ha valorat

            num_vots = self.get_num_vots(item_id)
            if num_vots < min_vots:
                continue  # No prou fiable

            avg_item = self.get_avg(item_id)
            avg_global = self.get_avg_global()

            score = (num_vots / (num_vots + min_vots)) * avg_item + \
                    (min_vots / (num_vots + min_vots)) * avg_global

            if score > millor_score:
                millor_score = score
                millor_item = item_id

        return millor_item

    def recomanacio_colaboratiu(self, user, item):
        pass

    def get_num_vots(self, item_id):
        col = self._dataset._pos_items[item_id]
        column_values = self._dataset._ratings[:, col]
        return np.count_nonzero(column_values)

    def get_avg(self, item_id):
        col = self._dataset._pos_items[item_id]
        values = self._dataset._ratings[:, col]
        non_zero = values[values > 0]
        return np.mean(non_zero) if len(non_zero) > 0 else 0

    def get_avg_global(self):
        all_ratings = self._dataset._ratings
        non_zero = all_ratings[all_ratings > 0]
        return np.mean(non_zero) if len(non_zero) > 0 else 0