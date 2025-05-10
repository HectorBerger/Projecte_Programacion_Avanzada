#Projecte
import pickle
import argparse
import logging
from Recomenador import Recomenador
from dataset import DatasetMovies, DatasetBooks



#DatasetBooks()DatasetMovies
def main():

    parser = argparse.ArgumentParser(description="Aplicar un algoritmo de recomendación a un dataset.") #Hemos usado argparse para poder mostrar el help más fácilmente
    parser.add_argument("dataset", choices=["","",""], help="") #default?  type=str?=>not necessary
    parser.add_argument("method", choices=[""], help="")

    args = parser.parse_args()
    dataset = args.dataset
    method = args.method
    recom = Recomenador(DatasetMovies())
    usuari = "23"
    recomanacio = recom.recomanacio_colaboratiu(usuari, 3)

    if recomanacio:
        print(f"Recomanació per a l'usuari {usuari}: {recom._dataset._items[recom._dataset._pos_items[recomanacio[0][1]]]} amb score {round(recomanacio[0][0], 1)} ")
    else:
        print(f"No hi ha recomanacions disponibles per a l'usuari {usuari}.")


if __name__ == '__main__':
    main()




"""
r = Recommender()
...
# Per guardar en un fitxer binari una còpia exacta de l’objecte
with open(“recommender.dat", 'wb') as fitxer:
    pickle.dump(r, fitxer)

# Per recuperar del fitxer la còpia de l’objecte
with open(“recommender.dat", 'rb') as fitxer:
    r = pickle.load(fitxer)

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