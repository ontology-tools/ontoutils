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
        self.curation_status = None
        self.logical_definition = None
        self.definition_source = None
        self.curator_note = None

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
