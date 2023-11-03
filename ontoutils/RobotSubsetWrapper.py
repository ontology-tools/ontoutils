import logging
from typing import Optional

from ontoutils.RobotWrapper import RobotWrapper


class RobotSubsetWrapper(RobotWrapper):
    _logger = logging.getLogger(__name__)

    def __init__(self, robotcmd):
        super().__init__(robotcmd)

    def create_subset_from(self, input_ontology_file_name: str, output_file_name: str, root_id: str, id_prefix: str, export_csv_headers: str=None,
                           export_sort: Optional[str]=None):
        robot_cmd = [self.robotcmd, 'merge',
                     '--input', input_ontology_file_name,
                     'extract',
                     '--method', 'MIREOT',
                     '--prefix', id_prefix,
                     '--annotate-with-source', 'true',
                     '--branch-from-term', root_id,
                     '--intermediates', 'all']

        if export_csv_headers:
            robot_cmd.extend(['export', '--header', '"' + export_csv_headers + '"',
                              '--prefix', id_prefix,
                              '--split', '"; "',
                              '--export', output_file_name])
            if export_sort:
                robot_cmd.extend(['--sort', '"' + export_sort + '"'])
        else:
            robot_cmd.extend(['--output', output_file_name])

        robot_cmd = " ".join(robot_cmd)

        self._logger.debug(f"Executing Robot command: {robot_cmd}")

        self._execute_command(command_str=robot_cmd)
