import json
import sys
import requests
from typing import Tuple

from zosapi import client as C


class CONSOLE(C.CLIENT):
    errors: dict = {}
    rc: int = 0

    def issue_zos_command(self,
                          command: str,
                          console_name: str = 'defcn',
                          verify: bool = True
                          ):
        """
        This operation issues a command, based on the properties that
        are specified in the request body. On successful completion,
        HTTP status code 200 is returned.
        A JSON object typically contains the command response.

        Args:
            command (str): The z/OS command to issue.
            console_name (str): The name of the console to use; defaults to 'defcn'.
            verify (bool): Verify certificats. Defaults to true

        Returns:
            dict: Dictionary with errors or empty dict.
            list: Command response or in case of an error empty list.
        """
        url = f"{self.path_to_api}/restconsoles/consoles/{console_name}"
        data = {
            "cmd": command,
            "routcode": "ALL",
        }
        # Convert Python to JSON
        json_object = json.dumps(data)
        if not verify:
            requests.packages.urllib3.disable_warnings()
        try:
            response = requests.put(url, headers=self.headers, data=json_object, verify=verify)
        except Exception as e:
            CONSOLE.rc = 16
            CONSOLE.errors = {"rc": CONSOLE.rc, "request_error": e}
            self.log.critical(f'CONSOLE-001S Catched and unexpected exception, can not continue {str(CONSOLE.errors)}')
            sys.exit(CONSOLE.rc )

        if response.status_code != 200:
            self.log.error(f"CONSOLE-002E An unexpected statuscode {response.status_code} has been received:")
            self.log.error(f"            {response.text}")
            CONSOLE.rc = 8
            CONSOLE.errors = {"rc": CONSOLE.rc, "status_code": response.status_code, "reason": response.reason}

        return CONSOLE.errors, response
