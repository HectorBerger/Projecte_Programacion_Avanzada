#Projecte
import pickle
import logging
from Recomenador import Recomenador
from dataset import DatasetMovies, DatasetBooks



#dataset = arg1
#method = arg2

#main prueba
#DatasetBooks()DatasetMovies

if __name__ == "__main__":

    recom = Recomenador(DatasetMovies())
    usuari = "23"
    recomanacio = recom.recomanacio_colaboratiu(usuari, 3)

    if recomanacio:
        print(f"Recomanació per a l'usuari {usuari}: {recom._dataset._items[recom._dataset._pos_items[recomanacio[0][1]]]} amb score {round(recomanacio[0][0], 1)} ")
    else:
        print(f"No hi ha recomanacions disponibles per a l'usuari {usuari}.")



"""
if pickle:
    pickle classes carregar dades
else:
    inicialitzar classes
    carregar dades
    càlculs generals
"""


"""
loop = True
while loop:
    input user id
    input accio
    if Recomenació:
        print 5 primers items 

    elif Avaluació:
        print Mètriques (MAE,RMSE)

    elif Sortir:
        print()
        loop = False

    else:
        print()

"""