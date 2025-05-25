class User:
    """
    Representa un usuari dins del sistema de recomanació.

    Aquesta classe encapsula informació bàsica sobre l'usuari com l'identificador,
    la localització, l'edat i el nom.

    Attributes
    ----------
    _id : str
        Identificador únic de l'usuari.
    _location : str
        Localització de l'usuari (pot ser 'Unknown').
    _age : int or None
        Edat de l'usuari (pot ser None si no se sap).
    _name : str
        Nom de l'usuari (pot ser 'Unknown').
    """

    _id:str
    _location:str
    _age: int
    _name:str

    def __init__(self, user_id: str, location: str = "Unknown", age: int = None, name: str = "Unknown"):
        """
        Inicialitza un nou objecte User.

        Parameters
        ----------
        user_id : str
            Identificador únic de l'usuari.
        location : str, optional
            Localització de l'usuari (per defecte és 'Unknown').
        age : int, optional
            Edat de l'usuari (per defecte és None).
        name : str, optional
            Nom de l'usuari (per defecte és 'Unknown').
        """
        self._id = user_id
        self._location = location
        self._age = age
        self._name = name
    
    def __str__(self):
        """
        Retorna una representació en cadena de l'usuari.

        Returns
        -------
        str
            Descripció amb ID, edat i localització si estan disponibles.
        """
        if (self._age == None) and (self._location == "Unknown"):
            return  f"usuari amb ID {self._id}"
        else:
            return f"usuari amb ID {self._id} (Edat: {self._age}, Localització: {self._location} i Nom: {self._name})"

    def get_id(self):
        """
        Retorna l'identificador de l'usuari.

        Returns
        -------
        str
            ID de l'usuari.
        """
        return self._id
