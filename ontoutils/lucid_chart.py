import csv
import codecs

class Entity:
    def __init__(self,id,name):
        self.id = id
        self.name = name

class Relation:
    def __init__(self,entity1,relType,entity2):
        self.entity1 = entity1
        self.relType = relType
        self.entity2 = entity2

    def getFullLabelForShortLabel(short_label):
        if short_label == "influences" or short_label == "" or short_label == "+/-" or short_label == 'Bi-directional influence':
            return ("Influences")
        if short_label == "positively influences" or short_label == "+":
            return ("Positively influences")
        if short_label == "negatively influences" or short_label == "-":
            return ("Negatively influences")
        if short_label == "may be influenced by" or short_label == "?" or short_label == "+?":
            return ("May influence")
        if short_label == "is influenced (*) by" or short_label == "*":
            return ("Influences (*)")
        if short_label == "is influenced (sum) by" or short_label == "Sum":
            return ("Influences (sum)")
        if short_label == "correlates with" or short_label == "Correlation" or short_label == "Correlations":
            return ("Correlates with")
        if short_label == "Type of":
            return ("Type of")
        if short_label == "Part of":
            return ("Part of")
        if short_label == "Value of":
            return ("Value of")
        if short_label == "Has attribute":
            return ("Has attribute")
        if short_label == "Has start":
            return ("Has start")
        if short_label == "Has end":
            return ("Has end")
        if short_label == "Transition":
            return ("Transitions to")
        if short_label == "relates through":
            return ("Relates through")
        if short_label == "relates to":
            return ("To")
        print ("Label not recognised: ",short_label)
        return (None)

class ParseLucidChartCsv:
    def parseCsvEntityData(csvFileName):
        entities = {}
        relations = []

        # First parse entities
        with codecs.open(csvFileName, mode='r', encoding="utf-8") as csv_file:

            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                id = row['Id']
                type = row['Name']
                label = str(row['Text Area 1']).strip()
                line_source = row['Line Source']
                line_dest = row['Line Destination']
                source_arrow = row['Source Arrow']
                dest_arrow = row['Destination Arrow']

                if type in ['Process','Connector','Terminator']:
                    entity = Entity(name=label,id=id)
                    entities[id] = entity

        # Then parse relations
        with codecs.open(csvFileName, mode='r', encoding="utf-8") as csv_file:

            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                id = row['Id']
                type = row['Name']
                label = str(row['Text Area 1']).strip()
                line_source = row['Line Source']
                line_dest = row['Line Destination']
                source_arrow = row['Source Arrow']
                dest_arrow = row['Destination Arrow']

                if type == 'Line':
                    relType = label
                    sourceId = line_source
                    destId = line_dest

                    if source_arrow == "Arrow" and dest_arrow == "None":
                        print("Arrow needs reversing: ",relType,entities[sourceId].name,entities[destId].name)
                        sourceId = line_dest
                        destId = line_source

                    if sourceId in entities and destId in entities:
                        entity1 = entities[sourceId]
                        entity2 = entities[destId]
                        relation = Relation(entity1,relType,entity2)
                        relations.append(relation)
                    else:
                        print("Error parsing relation data:  ",id,type,label,line_source,line_dest)
                        continue

        return ( (entities, relations) )







