import sys

import requests

from zosapi import client as C


class SYSVAR(C.CLIENT):
    errors: dict = {}
    rc: int = 0

    def get_system_variables(
        self, sysplex_name: str, system_name: str, verify: bool = True
    ):
        """
        Use this operation to get the z/OSMF variables or system symbols
        from a selected system.

        Args:
            sysplex_name (str): The name of the z/OS SYSPLEX.
            system_name (str): Name of the z/OS system in the z/OS SYSPLEX'.
            verify (bool): Verify certificats. Defaults to true

        Returns:
            dict: Dictionary with errors or empty dict.
            list: Command response or in case of an error empty list.
        """
        variables: list = []
        version: str = "1.0"
        url = (
            f"{self.path_to_api}/variables/rest/{version}/systems/local?source=variable"
        )
        if not verify:
            requests.packages.urllib3.disable_warnings()

        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            SYSVAR.rc = 16
            SYSVAR.errors = {"rc": SYSVAR.rc, "request_error": e}
            self.log.critical(
                f"SYSVAR-001S Catched an unexpected exception, can not continue {str(SYSVAR.errors)}"
            )
            sys.exit(SYSVAR.rc)

        if response.status_code != 200:
            self.log.error(
                f"SYSVAR-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.error(f"           {response.text}")
            SYSVAR.rc = 8
            SYSVAR.errors = {
                "rc": SYSVAR.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        return SYSVAR.errors, response
