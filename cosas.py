import logging


logging.basicConfig(filename='log.txt',level=logging.INFO,
format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')

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