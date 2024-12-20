import sys
import requests
from typing import Tuple

from zosapi import client as f


class FILES(f.CLIENT):
    errors: dict = {}
    rc: int = 0

    def zosapi_files_list(self, file_path: str, verify: bool = True):
        """
        Use this operation to list the files and directories in a z/UNIX
        file path on a z/OS system.

        Args:
            file_path (str): Name of file path on z/UNIX
            verify (bool): Verify certificats. Defaults to true

        Returns:
            error: Dictionalry with return code and error messages if any.
            response: Command response or in case of an error empty list.
        """

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restfiles/fs"
        if file_path != '':
            url = url + f'?path={file_path}'

        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            FILES.rc = 16
            FILES.errors = {"rc": FILES.rc, "request_error": e}
            self.log.critical(f'FILES-001S Catched an unexpected exception, can not continue {str(FILES.errors)}')
            sys.exit(FILES.rc)

        if response.status_code != 200:
            self.log.error(f"FILES-002E An unexpected statuscode {response.status_code} has been received:")
            self.log.error(f"           {response.text}")
            FILES.rc = 8
            FILES.errors = {"rc": FILES.rc, "status_code": response.status_code, "reason": response.reason}

        return FILES.errors, response

    def zosapi_files_retrieve(self, file_name: str, verify: bool = True):
        """
        Use this operation to read a file from z/UNIX

        Args:
            file_name (str): Full Path name of the file to read from z/UNIX
            verify (bool): Verify certificats. Defaults to true

        Returns:
            error: Dictionalry with return code and error messages if any.
            response: Command response or in case of an error empty list.
        """

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restfiles/fs{file_name}"

        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            FILES.rc = 16
            FILES.errors = {"rc": FILES.rc, "request_error": e}
            self.log.critical(f'FILES-001S Catched an unexpected exception, can not continue {str(FILES.errors)}')
            sys.exit(FILES.rc)

        if response.status_code != 200:
            self.log.error(f"FILES-002E An unexpected statuscode {response.status_code} has been received:")
            self.log.error(f"           {response.text}")
            FILES.rc = 8
            FILES.errors = {"rc": FILES.rc, "status_code": response.status_code, "reason": response.reason}

        return FILES.errors, response
