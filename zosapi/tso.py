import sys

import requests

from zosapi import client as C


class TSO(C.CLIENT):
    errors: dict = {}
    rc: int = 0

    def issue_tso_command(self, command: str, verify: bool = True):
        """
        Issue a TSO command

        Args:
            command (str): The TSO command to issue.

        Returns:
            dict: A dictionary containing the response from the server.
        """
        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/tsoApp/v1/tso"
        data = '{"tsoCmd": "' + command + '"}'

        self.log.debug(f"TSO-000D URL is {url}")
        self.log.debug(f"TSO-000D Request body is {data}")

        try:
            response = requests.put(url, headers=self.headers, data=data, verify=verify)
        except Exception as e:
            TSO.rc = 16
            TSO.errors = {"rc": {TSO.rc}, "request_error": {e}}
            self.log.critical(
                f"TSO-001S Catched an unexpected exception, can not continue {str(TSO.errors)}"
            )
            sys.exit(TSO.rc)

        if response.status_code != 200:
            self.log.error(
                f"TSO-002E An unexpected statuscode {response.status_code} has been received"
            )
            self.log.error(f"           {response.text}")
            TSO.rc = 8
            TSO.errors = {
                "rc": {TSO.rc},
                "status_code": response.status_code,
                "reason": response.reason,
            }

        return TSO.errors, response
