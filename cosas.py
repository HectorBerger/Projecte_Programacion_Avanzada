import logging


#logging.basicConfig(filename='log.txt',level=logging.INFO,
#format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')

from tqdm import tqdm
import threading
import time

import gzip, json
import os

def parse(path):
    with gzip.open(path, 'rt', encoding='utf-8') as g:
        for l in g:
            yield json.loads(l)

def mostrar_categorias(carpeta, num_lineas=5):
    archivos = [f for f in os.listdir(carpeta) if f.endswith('.gz')]
    for archivo in archivos:
        print(f"\nArchivo: {archivo}")
        ruta = os.path.join(carpeta, archivo)
        for i, obj in enumerate(parse(ruta)):
            #print("Objeto:", obj)
            categorias = obj.get('categories') or obj.get('category') or obj.get('genres')
            print("Categorías/Generos:", categorias)
            if i + 1 >= num_lineas:
                break

if __name__ == "__main__":
    mostrar_categorias('dataset/Digital_Music_5',20)
    # Ejemplo de uso:
    # mostrar_categorias('Digital_musica_5')
    
def executar_amb_barra(func, *args, **kwargs):
    resultat = [None]

    def target():
        resultat[0] = func(*args, **kwargs)

    fil = threading.Thread(target=target)
    fil.start()

    with tqdm(desc=f"Executant '{func.__name__}'", bar_format='{l_bar}{bar}| {elapsed} s') as barra:
        while fil.is_alive():
            time.sleep(0.1)
            barra.update(1)

    fil.join()
    return resultat[0]


def func(a, b):
    """
    Short summary of the function.

    Extended description of the function.

    Parameters
    ----------
    a : int
        Description of parameter `a`.
    b : str
        Description of parameter `b`.

    Returns
    -------
    int
        Description of the return value.

    Raises
    ------
    ValueError
        If `a` is less than zero.
    """