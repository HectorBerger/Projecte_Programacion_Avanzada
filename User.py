class User:
    _id:str
    _location:str
    _age: int
    _name:str
    
    def __init__(self, user_id: str, location: str = "Unknown", age: int = None, name: str = "Unknown"):
        self._id = user_id
        self._location = location
        self._age = age
        self._name = name
    
    def __str__(self):
        if (self._age == None) and (self._location == "Unknown"):
            return  f"usuari amb ID {self._id}"
        else:
            return f"usuari amb ID {self._id} (Edat: {self._age}, Localització: {self._location} i Nom: {self._name})"
    
    def get_id(self):
        return self._id



        



