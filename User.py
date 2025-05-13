class User:
    def __init__(self, user_id: str, location: str = "Unknown", age: int = None):
        self._id = user_id
        self._location = location
        self._age = age
        self.pos = None
    
    def __str__(self):
        if (self._age == None) and (self._location == "Unknown"):
            return  f"usuari amb ID {self._id}"
        else:
            return f"usuari amb ID {self._id} (Edat: {self._age} i Localització: {self._location})"
    
    def set_posicio(self, posicio): #No se usa habría que borrar o usar
        self.pos = posicio
        return True



        



