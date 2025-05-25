from tqdm import tqdm
import threading
import time
import gzip, json, os, re


def parse(path):
    g = gzip.open(path, 'r')
    for l in g:
        yield json.loads(l)

def clean_price(price):
    if not price or isinstance(price, list):
        return None
    # Si es un string con símbolos de dólar, quítalos y quédate con el número
    if isinstance(price, str):
        # Busca el primer número en el string
        match = re.search(r'(\d+(\.\d+)?)', price.replace(',', ''))
        if match:
            return float(match.group(1))
        else:
            return None
    try:
        return float(price)
    except Exception:
        return None




#A partir de aquí estás funciones se han utilizado para medir y visualizar previamente los datasets
def mostrar_categorias(carpeta, num_lineas=5):
    archivos = [f for f in os.listdir(carpeta) if f.endswith('.gz')]
    for archivo in archivos:
        print(f"\nArchivo: {archivo}")
        ruta = os.path.join(carpeta, archivo)
        for i, obj in enumerate(parse(ruta)):
            print("Objeto:", obj)
            categorias = obj.get('categories') or obj.get('category') or obj.get('genres')
            print("Categorías/Generos:", categorias)
            if i + 1 >= num_lineas:
                break

def categorias_unicas(path):
    categorias_set = set()
    with gzip.open(path, 'rt', encoding='utf-8') as g:
        for l in g:
            obj = json.loads(l)
            categorias = obj.get('categories') or obj.get('category') or obj.get('genres')
            if categorias:
                # Si es una lista de listas (como en Amazon), aplanar
                if isinstance(categorias, list):
                    for cat in categorias:
                        if isinstance(cat, list):
                            categorias_set.update(cat)
                        else:
                            categorias_set.add(cat)
                else:
                    categorias_set.add(categorias)
    print("Categorías únicas encontradas:")
    for cat in sorted(categorias_set):
        print(cat)

if __name__ == "__main__":
    mostrar_categorias('dataset/Amazon',20)
    #categorias_unicas('dataset/Amazon/meta_Video_Games.json.gz')
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

def timer(func):
    start = time.time()
    result = func()
    print(f"Tiempo: {time.time() - start:.2f}s")
    return result

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