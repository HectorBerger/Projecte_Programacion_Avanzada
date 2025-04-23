from typing import List
from Items import Item, Book, Movie
from User import User
import csv
import numpy as np

class Recomenador:
    _items: List[Item]

    def __init__(self):
        self._items = []

    

    def carrega(self):
        NOMFITXER = "datasets/books/Books.csv"
        with open(NOMFITXER) as csvfile:
            bookreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in bookreader:
                print(', '.join(row))
