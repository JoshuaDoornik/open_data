class place():
    geometry:dict
    id:str
    place:str
    n_people:int

    def __eq__(self, other):
        if(isinstance(other,place)):
            if other.id == self.id:
                return True
            else:
                return False
        else:
            return False

