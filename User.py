class User:
    def __init__(self, User_id: str, Location: str = "Unknown", Age: int = None):
        self._id = User_id
        self.location = Location
        self.age = Age
        self.pos = None

    def set_posicio(self, posicio):
        self.pos = posicio
        return True



        



