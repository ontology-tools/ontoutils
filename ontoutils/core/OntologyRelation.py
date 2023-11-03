class OntologyRelation:
    def __init__(self,id,name):
        self.id = id
        self.name = name
        self.definition = None
        self.equivalent = None
        self.parent = None
        self.domain = None
        self.range = None

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
