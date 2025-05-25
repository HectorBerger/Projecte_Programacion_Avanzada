# Projecte Programació Avançada 
# Repositori públic: https://github.com/HectorBerger/Projecte_Programacion_Avanzada

import argparse, os.path, pickle, logging, datetime
from recomenador import Simple, Colaboratiu, BasatEnContinguts 
from dataset import DatasetMovies, DatasetBooks, DatasetVideoGames

"""
Script principal per executar el sistema de recomanació.

Aquest script permet seleccionar el dataset i l'algorisme de recomanació, carregar o desar l'estat, i interactuar amb l'usuari per obtenir recomanacions o avaluar el sistema.

Usage
-----
python main.py {MovieLens100k, Books, VideoGames} {Simple, Col·laboratiu, Contingut}
"""


def main():
    """
    Executa el flux principal de l'aplicació de recomanació.

    El procés inclou:
      - Anàlisi d'arguments per seleccionar dataset i mètode.
      - Càrrega o creació del recomanador.
      - Bucle d'interacció amb l'usuari per obtenir recomanacions, avaluar o sortir.

    Parameters
    ----------
    Cap

    Returns
    -------
    None

    Side Effects
    ------------
    - Llegeix i escriu fitxers binaris per persistència.
    - Mostra informació per consola.
    - Escriu logs a 'log.txt'.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_filename = f"log_{timestamp}.txt"

    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format='%(asctime)s | %(name)s | %(levelname)s | %(message)s'
    )

    logging.info(f"Execució inicialitzada")

    parser = argparse.ArgumentParser(description="Aplicar un algorisme de recomanació a un dataset per diferents usuaris a escollir.") #Hemos usado argparse para poder mostrar el help más fácilmente
    parser.add_argument("dataset", choices=["MovieLens100k", "Books", "VideoGames"], help="Especifiqueu el conjunt de dades a utilitzar: 'MovieLens100k' per a pel·lícules, 'Books' per a recomanacions de llibres, o 'VideoGames' per a recomanacions de Videojocs que són productes a Amazon.") 
    parser.add_argument("method", choices=["Simple", "Col·laboratiu", "Contingut"], help="Especifiqueu el algoritme de recomanació a utilitzar: 'Simple', 'Col·laboratiu' o 'BasatEnContingut'.")

    args = parser.parse_args()
    dataset = args.dataset
    method = args.method
    filename = f"recommender_{dataset}_{method}.dat"

    logging.info("Argumentos analizados. Inicio del proceso de carga de datos")
    if not os.path.isfile(filename):
        match dataset:
            case "MovieLens100k":
                d = DatasetMovies()
            case "Books":
                d = DatasetBooks()
            case "VideoGames":
                d = DatasetVideoGames() 
        logging.info(f"Dataset {dataset} cargado desde zero")

        match method:
            case "Simple":
                r = Simple(d) 
            case "Col·laboratiu":
                r = Colaboratiu(d)
            case "Contingut":
                r = BasatEnContinguts(d)
        #càlculs generals
        logging.info(f"Clase Recomendador {method} creada correctamente")

    else:
        # Per recuperar del fitxer la còpia de l’objecte
        with open(filename, 'rb') as fitxer:
            r = pickle.load(fitxer)
        logging.info(f"Pickle cargado correctamente con Clase Recomendador {method} junto al dataset {dataset}")


    loop = True
    while loop:
        user_id = input("Introdueix un ID de usuari: ")

        while not r.has_user(user_id):  # Comprovar si existeix
            mostra = ", ".join(r.sample_users())
            user_id = input(f"ID no existent (alguns possibles IDs [{mostra}]): ")

        accio = input("Introdueix una acció (R -> Recomenació / A -> Avaluació / S -> Sortir): ")
        logging.info(
            f"Acció inicialitzada { 'Recomenació' if accio == 'R' else 'Avaluació' if accio == 'A' else 'Sortir' if accio == 'S' else 'NO VÀLIDA' }, amb ID d'usuari escollit: {user_id}"
        )
        match accio:
            case "R":
                num_r = 5  # num_r = input("Entra el número de recomanacions a mostrar: ") 
                if r.recomenar(user_id,num_r):
                    r.imprimir_recomanacions(user_id)
                    logging.info(f"Recomenació finalitzada")
                else:
                    logging.error(f"Error al fer les preddiccions a l'usuari: {user_id}")
                    print("Error al fer les prediccions")

            case "A":
                print(r.test(user_id))
                r.imprimir_prediccions(user_id)
                logging.info(f"Evaluació finalitzada")
            case "S":
                print("Sortint...\n")
                # Per guardar en un fitxer binari una còpia exacta de l’objecte
                if not os.path.isfile(filename):
                    with open(filename, 'wb') as fitxer:
                        pickle.dump(r, fitxer)
                    logging.info(f"Pickle guardat correctament amb recomenadaro {method} juntament amb el dataset {dataset}")

                loop = False

            case _:
                print("La opció triada no és vàlida.")

    logging.info(f"Execució finalitzada\n\n")

if __name__ == '__main__':
    main()
