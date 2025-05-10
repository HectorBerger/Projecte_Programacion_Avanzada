import logging


logging.basicConfig(filename='log.txt',level=logging.INFO,
format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')

from tqdm import tqdm
import threading
import time

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