import sys
import requests
from typing import Tuple

from zosapi import client as r


class RTD(r.CLIENT):
    errors: dict = {}
    rc: int = 0

    def get_rtd(self, asname: str, verify: bool = True):
        """
        Use this command to obtain the Runtime Diagnostic Data (RTD) for a
        specified addresse space on a defined system.

        Args:
            asname (str): Name of address space.
            verify (bool): Verify certificats. Defaults to true

        Returns:
            dict: Return Code and error related data if any.
            response: Command response or in case of an error empty list.
        """

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/resthub/hzr/v1/analyze/anomaly"
        if asname != '':
            url = url + f'?asname={asname}'
        try:
            response = requests.get(url, headers=self.headers, verify=verify)

        except Exception as e:
            RTD.rc = 16
            RTD.errors = {"rc": RTD.rc, "request_error": e}
            self.log.critical(f'RTD-001S Catched an unexpected exception, can not continue {str(RTD.errors)}')
            sys.exit(RTD.rc)

        if response.status_code != 200:
            self.log.error(f"RTD-002E An unexpected statuscode {response.status_code} has been received:")
            self.log.error(f"           {response.text}")
            RTD.rc = 8
            RTD.errors = {"rc": RTD.rc, "status_code": response.status_code, "reason": response.reason}

        return RTD.errors, response
