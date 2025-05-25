import numpy as np

class Avaluador():
    """
    Classe per avaluar la qualitat de les prediccions d'un sistema de recomanació per a un usuari concret.

    Parameters
    ----------
    user_id : str o int
        Identificador de l'usuari a avaluar.

    Attributes
    ----------
    _user_id : str o int
        Identificador de l'usuari.
    _mae : float o None
        Valor de l'error absolut mitjà (MAE) calculat.
    _rmse : float o None
        Valor de l'arrel quadrada de l'error quadràtic mitjà (RMSE) calculat.
    """

    def __init__(self, user_id):
        """
        Inicialitza l'avaluador per a un usuari concret.

        Parameters
        ----------
        user_id : str o int
            Identificador de l'usuari.
        """
        self._user_id = user_id
        self._mae = None
        self._rmse = None

    def __str__(self) -> str:
        """
        Retorna una cadena amb els resultats de l'avaluació.

        Returns
        -------
        str
            Resultats de les mètriques calculades per l'usuari.
        """
        if self._mae is None and self._rmse is None:
            return "No s'han pogut calcular les mètriques. L'usuari potser no té valoracions reals."
        
        cad = f"Resultats d'avaluació per l'usuari {self._user_id}:\n"
        if self._mae:
            cad += f"  MAE  (Mean Absolute Error):     {self._mae:.3f}\n"
        if self._rmse:
            cad += f"  RMSE (Root Mean Squared Error): {self._rmse:.3f}\n"  
        return cad
        
    def mae(self, prediccions: list, valors_reals: list) -> bool:
        """
        Calcula el Mean Absolute Error (MAE) entre les prediccions i els valors reals.

        Parameters
        ----------
        prediccions : list o np.ndarray
            Llista o array de valors predits.
        valors_reals : list o np.ndarray
            Llista o array de valors reals.

        Returns
        -------
        bool
            True si el càlcul s'ha realitzat correctament.

        Raises
        ------
        ValueError
            Si les llistes són None o no tenen la mateixa mida.
        """
        if prediccions is None or valors_reals is None:
            raise ValueError("Les prediccions i els valors reals no poden ser None.")
        prediccions = np.array(prediccions)
        valors_reals = np.array(valors_reals)
        if prediccions.shape != valors_reals.shape:
            raise ValueError("Les prediccions i els valors reals han de tenir la mateixa mida.")
        self._mae = np.mean(np.abs(prediccions - valors_reals))
        return True

    def rmse(self, prediccions: list, valors_reals: list) -> bool:
        """
        Calcula el Root Mean Squared Error (RMSE) entre les prediccions i els valors reals.

        Parameters
        ----------
        prediccions : list o np.ndarray
            Llista o array de valors predits.
        valors_reals : list o np.ndarray
            Llista o array de valors reals.

        Returns
        -------
        bool
            True si el càlcul s'ha realitzat correctament.

        Raises
        ------
        ValueError
            Si les llistes són None o no tenen la mateixa mida.
        """
        if prediccions is None or valors_reals is None:
            raise ValueError("Les prediccions i els valors reals no poden ser None.")
        prediccions = np.array(prediccions)
        valors_reals = np.array(valors_reals)
        if prediccions.shape != valors_reals.shape:
            raise ValueError("Les prediccions i els valors reals han de tenir la mateixa mida.")
        self._rmse = np.sqrt(np.mean((prediccions - valors_reals) ** 2))
        return True
