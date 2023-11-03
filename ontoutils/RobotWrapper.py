import logging
import subprocess


class RobotWrapper:
    _logger = logging.getLogger(__name__)

    def __init__(self,robotcmd,cleanup=True):
        self.cleanup = cleanup
        self.robotcmd = robotcmd

    def _execute_command(self, command_str, shell_flag=True):
        self._logger.debug(f"Executing command: {command_str}")
        Output = subprocess.Popen(command_str,
                shell=shell_flag,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
        stdout,stderr = Output.communicate()
        if stdout is not None and len(stdout) > 0:
            print(stdout)
        if stderr is not None:
            print(stderr)
