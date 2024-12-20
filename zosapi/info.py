import sys
import requests
from typing import Tuple

from zosapi import client as i


class INFO(i.CLIENT):
    errors: dict = {}
    rc: int = 0

    def zosmf_info(self, verify: bool = True):
        """
        use this operation to retrieve information about z/OSMF on a
        particular z/OS system.

        Args:
            verify (bool): Verify certificats. Defaults to true

        Returns:
            response: Command response or in case of an error empty list.
        """

        url = f"{self.path_to_api}/info"
        if not verify:
            requests.packages.urllib3.disable_warnings()

        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            INFO.rc = 16
            INFO.errors = {"rc": INFO.rc, "request_error": e}
            self.log.critical(f'INFO-001S Catched an unexpected exception, can not continue {str(INFO.errors)}')
            sys.exit(INFO.rc)

        if response.status_code != 200:
            self.log.error(f"INFO-002E An unexpected statuscode {response.status_code} has been received:")
            self.log.error(f"           {response.text}")
            INFO.rc = 8
            INFO.errors = {"rc": INFO.rc, "status_code": response.status_code, "reason": response.reason}

        return INFO.errors, response
