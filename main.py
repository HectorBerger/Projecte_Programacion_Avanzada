#Projecte

import csv
import numpy as np

#Leer bases de datos
NOMFITXER = "datasets/books/Books.csv"
with open(NOMFITXER) as csvfile:
    bookreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in bookreader:
        print(', '.join(row))

class Recomenador:
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

    

        

class User:
    def __init__(self):
        self._id = str()

from abc import ABC, abstractmethod 
class Item(ABC):
    def __init__(self):
        self._id = str()


class Movie(Item):
    def __init__(self):
        self._id = str()

class Book(Item):
    def __init__(self):
        self._id = str()