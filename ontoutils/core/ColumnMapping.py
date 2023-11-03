import re
from enum import Enum
from typing import Optional

from ontoutils.utils import quoteIfNeeded


class RobotType(Enum):
    ROBOT_TYPE_ID = 1
    ROBOT_TYPE_LABEL = 2
    ROBOT_TYPE_PARENT = 3
    ROBOT_TYPE_RELATION = 4
    ROBOT_TYPE_ANNOTATION = 5
    ROBOT_TYPE_DISJOINT = 6
    ROBOT_TYPE_EQUIVALENCE = 7


class ColumnMapping:
    def __init__(self, excel_col_name: str, robot_type: RobotType, mapping_id: Optional[str] = None):
        self.excelColName = excel_col_name
        self.robotType = robot_type
        self.mappingId = mapping_id  # relationship or annotation ID
        self.quoteNeeded = robot_type in [
            RobotType.ROBOT_TYPE_DISJOINT]

    def get_robot_code_string(self) -> str:
        if self.robotType == RobotType.ROBOT_TYPE_ID:
            return "ID"
        elif self.robotType == RobotType.ROBOT_TYPE_LABEL:
            return "LABEL"
        elif self.robotType == RobotType.ROBOT_TYPE_PARENT:
            return "SC % SPLIT=;"
        elif self.robotType == RobotType.ROBOT_TYPE_RELATION:
            return "SC " + self.mappingId + " some % SPLIT=;"
        elif self.robotType == RobotType.ROBOT_TYPE_ANNOTATION:
            return "A " + self.mappingId + " SPLIT=;"
        elif self.robotType == RobotType.ROBOT_TYPE_DISJOINT:
            return "DC % SPLIT=;"
        elif self.robotType == RobotType.ROBOT_TYPE_EQUIVALENCE:
            return "EC %"

    def parse_value(self, value: str) -> str:
        if value is None:
            return ''
        else:
            value_a = value.encode("ascii", "ignore").decode("utf-8")
            value_a = re.sub('\(.*?\)', '', value_a)
            value_a = re.sub('\[.*?\]', '', value_a)
            value_a = value_a.strip()
            if self.quoteNeeded:
                values = value_a.split(';')
                values = [v.strip() for v in values]
                values = [quoteIfNeeded(v) for v in values]
                value_a = ";".join(values)

            return value_a


def get_id_mapping(column_name: str) -> ColumnMapping:
    return ColumnMapping(column_name, RobotType.ROBOT_TYPE_ID)


def get_label_mapping(column_name: str) -> ColumnMapping:
    return ColumnMapping(column_name, RobotType.ROBOT_TYPE_LABEL)


def get_parent_mapping(column_name: str) -> ColumnMapping:
    return ColumnMapping(column_name, RobotType.ROBOT_TYPE_PARENT)


def get_relationship_mapping(column_name: str, rel_id: Optional[str] = None) -> ColumnMapping:
    if rel_id is None:
        rel_id = column_name
    return ColumnMapping(column_name, RobotType.ROBOT_TYPE_RELATION, rel_id)


def get_annotation_mapping(column_name: str, anno_id: str) -> ColumnMapping:
    return ColumnMapping(column_name, RobotType.ROBOT_TYPE_ANNOTATION, anno_id)


def get_disjoint_mapping(column_name: str) -> ColumnMapping:
    return ColumnMapping(column_name, RobotType.ROBOT_TYPE_DISJOINT)


def get_equivalence_mapping(column_name: str) -> ColumnMapping:
    return ColumnMapping(column_name, RobotType.ROBOT_TYPE_EQUIVALENCE)


DEFAULT_HEADER_MAPPINGS = {"BCIO_ID": get_id_mapping("BCIO_ID"),
                           "ID": get_id_mapping("ID"),
                           "Name": get_label_mapping("Name"),
                           "Label": get_label_mapping("Label"),
                           "Label (synonym)": get_label_mapping("Label"),
                           "Parent": get_parent_mapping("Parent"),
                           "Parent class/ BFO class": get_parent_mapping("Parent"),
                           "Logical definition": get_equivalence_mapping("Logical definition"),
                           "Disjoint classes": get_disjoint_mapping("Disjoint classes"),
                           "Definition": get_annotation_mapping("Definition", "IAO:0000115"),
                           "Definition_ID": get_annotation_mapping("Definition_ID", "rdfs:isDefinedBy"),
                           "Definition_Source": get_annotation_mapping("Definition_source", "IAO:0000119"),
                           "Definition source": get_annotation_mapping("Definition source", "IAO:0000119"),
                           "Examples": get_annotation_mapping("Examples", "IAO:0000112"),
                           "Examples of usage": get_annotation_mapping("Examples", "IAO:0000112"),
                           "Elaboration": get_annotation_mapping("Elaboration", "IAO:0000112"),
                           "Curator note": get_annotation_mapping("Curator note", "IAO:0000232"),
                           "Synonyms": get_annotation_mapping("Synonyms", "IAO:0000118"),
                           "Comment": get_annotation_mapping("Comment", "rdfs:comment"),
                           "Curation status": get_annotation_mapping("Curation status", "IAO:0000078")
                           }
DEFAULT_HEADERS_TO_IGNORE = ["Structure", "BFO entity", "Sub-ontology", "Informal definition"]
