"""
Yo me quedaría con el main que ya teniamos hecho

#Projecte
import pickle
import argparse
import os.path
import logging
from recomenador_v2 import Recomenador 
from dataset import DatasetMovies, DatasetBooks, DatasetMusic

def main():
    parser = argparse.ArgumentParser(description="Aplicar un algorisme de recomanació a un dataset per diferents usuaris a escollir.") #Hemos usado argparse para poder mostrar el help más fácilmente
    parser.add_argument("dataset", choices=["MovieLens100k", "Books", "Amazon"], help="Especifiqueu el conjunt de dades a utilitzar: 'MovieLens100k' per a pel·lícules, 'Books' per a recomanacions de llibres, o 'Amazon' per a recomanacions de productes Amazon.") #!#! default? 
    parser.add_argument("method", choices=["Simple", "Col·laboratiu", "Contingut"], help="Especifiqueu el algoritme de recomanació a utilitzar: 'Simple', 'Col·laboratiu' o 'BasatEnContingut'.")
 
    args = parser.parse_args()
    dataset = args.dataset
    method = args.method
    filename = f"recommender_{dataset}_{method}.dat"

    if not os.path.isfile(filename):
        match dataset:
            case "MovieLens100k":
                d = DatasetMovies()
            case "Books":
                d = DatasetBooks()
            case "Amazon":
                d = DatasetMusic() 

        r = Recomenador(d)
        
        #càlculs generals

    else:
        # Per recuperar del fitxer la còpia de l’objecte
        with open(filename, 'rb') as fitxer:
            r = pickle.load(fitxer)
    
    loop = True
    while loop:
        user_id = input("Introdueix un ID de usuari: ") #!#!Habría que comprovar si existe dentro del dataset

        while not r.has_user(user_id): # Comprovar si existeix
            mostra = ", ".join(r.sample_users())
            user_id = input(f"ID no existent (alguns possibles IDs [{mostra}]):")
            
        accio = input("Introdueix una acció (R -> Recomenació / A -> Avaluació / S -> Sortir): ")
        match accio:
            case "R":
                #num_r = input("Entra el número de recomanacions a mostrar: ") 
                if r.recomenar(user_id,method):
                    r.imprimir_recomanacions(user_id)
                else:
                    print("ERROR")
            case "A":
                print()#Mètriques (MAE,RMSE)

            case "S":
                print("Sortint...\n")
                # Per guardar en un fitxer binari una còpia exacta de l’objecte
                with open(filename, 'wb') as fitxer:
                    pickle.dump(r, fitxer)
                loop = False

            case _:
                print("La opció triada no és vàlida.")

if __name__ == '__main__':
    main()
"""