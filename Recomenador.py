from typing import List
from Items import Item, Book, Movie
from User import User
import csv
import numpy as np

class Recomenador:
    _items: List[Item]

    def __init__(self):
        self._items = []
        
    def recomanacio_simple(self, user, item):
        if min_vots < minim:
            return 0

        # Calcular la puntuación de la película
        num_vots = item.get_num_vots()
        avg_item = item.get_avg()
        avg_global = self.get_avg_global()
        score = (num_vots/(num_vots + min_vots))*avg_item + (min_vots/(num_vots + min_vots))*avg_global

        return score

    def recomanacio_colaboratiu(self, user, item):

    def get_num_vots(self):
        # Implementar la lógica para obtener el número de votos
        pass

    def get_avg(self):
        # Implementar la lógica para obtener el promedio
        pass

    def get_avg_global(self):
        # Implementar la lógica para obtener el promedio global
        pass

    

    

    def carrega(self):
        NOMFITXER = "datasets/books/Books.csv"
        with open(NOMFITXER) as csvfile:
            bookreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in bookreader:
                print(', '.join(row))
