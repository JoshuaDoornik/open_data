class place():
    geometry:dict
    id:str
    properties:dict

    def __eq__(self, other):
        if(isinstance(other,place)):
            if other.id == self.id:
                return True
            else:
                return False
        else:
            return False

