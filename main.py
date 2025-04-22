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