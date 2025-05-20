import numpy as np

class Avaluador():
    """
    """
    def __init__(self):
        self._mae = None
        self._rmse = None

    def __str__(self):
        return f"MAE: {self._mae:.3f}, RMSE: {self._rmse:.3f}"
        
    def mae(self,prediccions,valors_reals):
        self._mae=np.mean(np.abs(prediccions-valors_reals))
        return self._mae

    def rmse(self, prediccions,valors_reals):
        self._rmse= np.sqrt(np.mean((prediccions-valors_reals)**2))
        return self._rmse