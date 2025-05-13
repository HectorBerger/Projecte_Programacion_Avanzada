#Projecte
import pickle
import argparse
import os.path
import logging
from recomenador import Simple, Colaboratiu, BasatEnContinguts 
from dataset import DatasetMovies, DatasetBooks

def main():
    parser = argparse.ArgumentParser(description="Aplicar un algorisme de recomanació a un dataset per diferents usuaris a escollir.") #Hemos usado argparse para poder mostrar el help más fácilmente
    parser.add_argument("dataset", choices=["MovieLens100k", "Books", "Amazon"], help="Especifiqueu el conjunt de dades a utilitzar: 'MovieLens100k' per a pel·lícules, 'Books' per a recomanacions de llibres, o 'Amazon' per a recomanacions de productes Amazon.") #!#! default? 
    parser.add_argument("method", choices=["Simple", "Col·laboratiu", "BasatEnContingut"], help="Especifiqueu el algoritme de recomanació a utilitzar: 'Simple', 'Col·laboratiu' o 'BasatEnContingut'.")
 
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
                d = DatasetAmazon()

        match method:
            case "Simple":
                r = Simple(d) #Millor acurtar a Simple?
            case "Col·laboratiu":
                r = Colaboratiu(d)
            case "BasatEnContingut":
                r = BasatEnContinguts(d)
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
            
        accio = input("Introdueix una acció (Recomenació, Avaluació, Sortir): ")
        match accio:
            case "Recomenació":
                #num_r = input("Entra el número de recomanacions a mostrar: ") 
                if r.recomenar(user_id,4):
                    r.imprimir_recomanacions(user_id)
                else:
                    print("")
            case "Avaluació":
                print()#Mètriques (MAE,RMSE)

            case "Sortir":
                print("Sortint...\n")
                # Per guardar en un fitxer binari una còpia exacta de l’objecte
                with open(filename, 'wb') as fitxer:
                    pickle.dump(r, fitxer)
                loop = False

            case _:
                print("La opció triada no és vàlida.")

if __name__ == '__main__':
    main()