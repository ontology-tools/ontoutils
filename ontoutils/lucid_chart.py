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


class ParseLucidChartCsv:
    def parseCsvEntityData(self,csvFileName):
        entities = {}
        relations = []

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

                if type in ['Process','Connector']:
                    entity = Entity(name=label,id=id)
                    entities[id] = entity

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







