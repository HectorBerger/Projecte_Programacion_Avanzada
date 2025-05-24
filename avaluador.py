import numpy as np

class Avaluador():
    """
    """
    def __init__(self,user_id):
        self._user_id = user_id
        self._mae = None
        self._rmse = None

    def __str__(self) -> str:
        if self._mae is None and self._rmse is None:
            return "No s'han pogut calcular les mètriques. L'usuari potser no té valoracions reals."
        
        cad=f"Resultats d'avaluació per l'usuari {self._user_id}:\n"
        if self._mae:
            cad+=f"  MAE  (Mean Absolute Error):     {self._mae:.3f}\n"
        if self._rmse:
            cad+=f"  RMSE (Root Mean Squared Error): {self._rmse:.3f}\n"  
        return cad
        
    def mae(self, prediccions:list, valors_reals:list) -> bool:
        if prediccions is None or valors_reals is None:
            raise ValueError("Les prediccions i els valors reals no poden ser None.")
        prediccions = np.array(prediccions)
        valors_reals = np.array(valors_reals)
        if prediccions.shape != valors_reals.shape:
            raise ValueError("Les prediccions i els valors reals han de tenir la mateixa mida.")
        self._mae = np.mean(np.abs(prediccions - valors_reals))
        return True

    def rmse(self, prediccions:list, valors_reals:list) -> bool:
        if prediccions is None or valors_reals is None:
            raise ValueError("Les prediccions i els valors reals no poden ser None.")
        prediccions = np.array(prediccions)
        valors_reals = np.array(valors_reals)
        if prediccions.shape != valors_reals.shape:
            raise ValueError("Les prediccions i els valors reals han de tenir la mateixa mida.")
        self._rmse = np.sqrt(np.mean((prediccions - valors_reals) ** 2))
        return True