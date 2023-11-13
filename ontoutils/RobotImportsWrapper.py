import logging
import os
import shutil
from multiprocessing import Pool

import openpyxl

from ontoutils.RobotWrapper import RobotWrapper


class OntologyImport:
    prefix: str
    ontology_id: str
    purl: str
    root_id: str
    imported_terms: list[str]
    intermediates: str
    short_name: str

    def __init__(self,
                 ontology_id: str,
                 purl: str,
                 root_id: str,
                 imported_terms: list[str],
                 intermediates: str,
                 short_name: str,
                 prefix: str
                 ):
        self.prefix = prefix
        self.ontology_id = ontology_id
        self.purl = purl
        self.root_id = root_id
        self.imported_terms = imported_terms
        self.intermediates = intermediates
        self.short_name = short_name

    @property
    def slim_file(self):
        return self.ontology_id + '-slim.owl'


class RobotImportsWrapper(RobotWrapper):
    _logger = logging.getLogger(__name__)

    imports: list[OntologyImport]

    def __init__(self, robotcmd, cleanup=False):
        super().__init__(robotcmd, cleanup)
        self.imports = []

    def add_imports_from_excel(self, path):
        """
        Adds imported terms from external ontologies as defined in an excel file

        :param path: Path to excel file
        :return:
        """

        try:
            wb = openpyxl.load_workbook(path)
        except Exception as e:
            print(e)
            raise Exception("Not able to parse input file: " + path + ":" + e)

        sheet = wb.active
        data = sheet.rows

        next(data)

        for row in data:
            rowdata = [i.value for i in row[0:6]]
            onto_id = rowdata[0]
            purl = rowdata[1]
            root_id = rowdata[2]
            ids = rowdata[3]
            intermediates = rowdata[4]
            prefix = rowdata[5]

            if intermediates is None:
                intermediates = 'minimal'

            terms = [term_id[term_id.find("[") + 1:term_id.find("]")] for term_id in ids.split(";")]

            onto_shortname = purl[(purl.rindex('/') + 1):]
            root_id = root_id[root_id.find("[") + 1:root_id.find("]")]  # extract just the ID

            ontology_import = OntologyImport(
                ontology_id=onto_id,
                purl=purl,
                root_id=root_id,
                imported_terms=terms,
                intermediates=intermediates,
                short_name=onto_shortname,
                prefix=prefix
            )

            self.imports.append(ontology_import)

    def download_imported_ontologies(self, download_path="temp") -> None:
        """
        Downloads previously added ontologies

        :param download_path: Path to download the ontologies to
        :return:
        """

        if not os.path.exists(download_path):
            os.mkdir(download_path)

        with Pool(4) as p:
            p.starmap(self._download_ontology, [(x, download_path) for x in self.imports])


    def _download_ontology(self, imp: OntologyImport, download_path: str) -> None:
        # Only download if we don't already have it.
        # Use cleanup=TRUE to clean up afterwards for fresh download next time.
        out = os.path.join(download_path, imp.short_name)
        if not os.path.exists(out):
            get_ontology_cmd = f'curl -L "{imp.purl}" > {out}'
            self._execute_command(get_ontology_cmd, shell_flag=True)

    def extract_slim_ontologies(self, download_path='temp') -> None:
        """
        Extracts the imported terms from the registered imported ontologies. Requires the ontologies to be present in `download_path`
        """
        with Pool(4) as p:
            p.starmap(self._extract_slim_ontology, [(x, download_path) for x in self.imports])

    def _extract_slim_ontology(self, imp: OntologyImport, download_path: str) -> None:
        filename = os.path.join(download_path, imp.slim_file)
        slim_cmd = [self.robotcmd, 'merge',
                    '--input', f'"{os.path.join(download_path, imp.short_name)}"',
                    'extract', '--method', 'MIREOT',
                    '--annotate-with-source', 'true',
                    '--upper-term', imp.root_id,
                    '--intermediates', imp.intermediates,
                    '--output', filename]
        if imp.prefix:
            slim_cmd.append('--prefix')
            slim_cmd.append(imp.prefix)

        for term_id in imp.imported_terms:
            slim_cmd.append('--lower-term')
            slim_cmd.append(term_id)

        slim_cmd = " ".join(slim_cmd)
        self._execute_command(slim_cmd, shell_flag=True)

    def merge_ontologies(self, merged_iri: str, merged_file: str, merged_ontology_name: str):
        """
        Merges previously added, downloaded, and extracted ontology terms into one merged ontology

        :param merged_iri: IRI of the new, merged ontology
        :param merged_file: Output filename
        :param merged_ontology_name: Name of the merged ontology
        :return:
        """
        # Now merge all the imports into a single file
        merge_cmd = [self.robotcmd, 'merge']

        for imp in self.imports:
            merge_cmd.append('--input')
            merge_cmd.append(imp.slim_file)

        merge_cmd.extend(
            ['annotate', '--ontology-iri', merged_iri, '--version-iri', merged_iri, '--annotation rdfs:comment ',
             '"This file contains externally imported content for the ' + merged_ontology_name + '. It was prepared using ROBOT and a custom script from a spreadsheet of imported terms."',
             '--output', merged_file])

        merge_cmd = " ".join(merge_cmd)

        self._execute_command(merge_cmd, shell_flag=True)

        # Now delete the temp directory
        if self.cleanup:
            shutil.rmtree('temp')

    # Handle externally imported content
    def process_imports_from_excel(self, excel_file, merged_iri: str, merged_file: str, merged_ontology_name: str):

        self.add_imports_from_excel(excel_file)
        self.download_imported_ontologies()
        self.extract_slim_ontologies()
        self.merge_ontologies(merged_iri, merged_file, merged_ontology_name)

    def addAdditionalContent(self, extraContentTemplate: str, importsOWLURI: str):
        owlFileName = importsOWLURI[(importsOWLURI.rindex('/') + 1):]
        owlTempFileName = owlFileName.replace(".owl", "-temp.owl")

        robot_cmd = [self.robotcmd, 'template', '--template', extraContentTemplate,
                     '--ontology-iri', importsOWLURI,
                     '--output', owlTempFileName
                     ]

        robot_cmd = " ".join(robot_cmd)

        self._execute_command(command_str=robot_cmd)

        robot_cmd = [self.robotcmd, 'merge', '--input', owlFileName, '--input', owlTempFileName, '--output',
                     owlFileName]

        robot_cmd = " ".join(robot_cmd)

        self._execute_command(command_str=robot_cmd)

    # Remove metadata that causes a problem in Pronto
    # Overwrites original file so be careful
    def removeProblemMetadata(self, importsOWLURI, importsOWLFileName, metadataURIFile):

        robot_cmd = [self.robotcmd, 'remove', '--input', importsOWLFileName,
                     '--term-file', metadataURIFile,
                     '--axioms', 'annotation',
                     '--output', importsOWLFileName
                     ]

        robot_cmd = " ".join(robot_cmd)

        self._execute_command(command_str=robot_cmd)

    # Also save an OBO (For Pronto)
    def createOBOFile(self, importsOWLURI, importsOWLFileName):
        owlFileName = importsOWLURI[(importsOWLURI.rindex('/') + 1):]

        oboFileName = owlFileName.replace(".owl", ".obo")

        robot_cmd = [self.robotcmd, 'merge', '--input', owlFileName, 'convert', '--output', oboFileName, '--check',
                     'false']

        robot_cmd = " ".join(robot_cmd)

        self._execute_command(command_str=robot_cmd)
