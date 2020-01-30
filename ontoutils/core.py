

class OntologyEntity:
    def __init__(self):
        self.id = None
        self.name = None
        self.definition = None
        self.parent = None
        self.synonyms = None
        self.examples = None
        self.comment = None
        self.axioms = None  # May include equivalence axioms
        self.relations = None
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

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


