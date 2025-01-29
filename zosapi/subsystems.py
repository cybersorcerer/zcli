import requests
import sys
from typing import Tuple

from zosapi import client as C

class SUBSYSTEMS(C.CLIENT):
    errors: dict = {}
    rc: int = 0

    def get_subsystems(
        self,
        filter: str = "",
        verify: bool = True,
    ):

        SUBSYSTEMS.rc: int = 0
        SUBSYSTEMS.errors = {}

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/rest/mvssubs"
        self.log.debug(f"SUBSYS-000D Method get_subsystems uses {url} to access zos")

        if filter != '':
            url = url + f'?ssid={filter}'
            self.log.debug(f"SUBSYS-000D Method get_subsystems ?ssid={filter} has been added to url")

        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            self.log.critical(f'SUBSYS-001S Catched and unexpected exception, can not continue {str(SUBSYSTEMS.errors)}')
            SUBSYSTEMS.rc = 16
            SUBSYSTEMS.errors = {"rc": SUBSYSTEMS.rc, "request_error": e}
            sys.exit(SUBSYSTEMS.rc)

        if response.status_code != 200:
            self.log.error(f"SUBSYS-002E An unexpected statuscode {response.status_code} has been received")
            self.log.error(f"           {response.text}")
            SUBSYSTEMS.rc = 8
            SUBSYSTEMS.errors = {"rc": SUBSYSTEMS.rc, "status_code": response.status_code, "reason": response.reason}

        return SUBSYSTEMS.errors, response
