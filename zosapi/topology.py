import sys

import requests

from zosapi import client as C


class TOPOLOGY(C.CLIENT):
    """_z/OSMF Topology Services_

    Args:
        C (_CLIENT_): _Client Instance_

    Returns:
        _type_: _description_
    """

    errors: dict = {}
    rc: int = 0

    def __str__(self) -> str:
        return super().__str__()

    def get_topology_service(
        self,
        service: str = "systems",
        verify: bool = True,
    ):

        TOPOLOGY.rc: int = 0
        TOPOLOGY.errors = {}

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/resttopology/{service}"
        self.log.debug(
            f"TOPOLOGY-000D Method get_defined_systems() uses {url} to access z/OS"
        )

        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            TOPOLOGY.rc = 16
            TOPOLOGY.errors = {"rc": {TOPOLOGY.rc}, "request_error": {e}}
            self.log.critical(
                f"TOPOLOGY-001S Catched an unexpected exception, can not continue {str(TOPOLOGY.errors)}"
            )
            sys.exit(TOPOLOGY.rc)

        if response.status_code != 200:
            self.log.debug(
                f"TOPOLOGY-002E An unexpected statuscode {response.status_code} has been received"
            )
            self.log.debug(f"             {response.text}")
            TOPOLOGY.rc = 8
            TOPOLOGY.errors = {
                "rc": TOPOLOGY.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        return TOPOLOGY.errors, response

    def get_group_systems(
        self,
        group,
        verify: bool = True,
    ):

        TOPOLOGY.rc: int = 0
        TOPOLOGY.errors = {}

        if not verify:
            self.log.warning(
                "Caution Certificate verification is off, this should be turned on in production!"
            )
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/resttopology/systems/groupName/{group}"
        self.log.debug(
            f"TOPOLOGY-000D Method get_defined_systems() uses {url} to access z/OS"
        )

        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            self.log.error(f"An unexpected exception has been caught {e}")
            TOPOLOGY.rc = 16
            TOPOLOGY.errors = {"rc": {TOPOLOGY.rc}, "request_error": {e}}
            self.log.critical(
                f"TOPOLOGY-001S Catched an unexpected exception, can not continue {str(TOPOLOGY.errors)}"
            )
            sys.exit(TOPOLOGY.rc)

        if response.status_code != 200:
            self.log.debug(
                f"TOPOLOGY-002E An unexpected statuscode {response.status_code} has been received"
            )
            self.log.debug(f"             {response.text}")
            TOPOLOGY.rc = 8
            TOPOLOGY.errors = {
                "rc": {TOPOLOGY.rc},
                "status_code": response.status_code,
                "reason": response.reason,
            }

        return TOPOLOGY.errors, response

    def get_sysplex_systems(
        self,
        sysplex,
        verify: bool = True,
    ):

        TOPOLOGY.rc: int = 0
        TOPOLOGY.errors = {}

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/resttopology/systems/sysplexName/{sysplex}"
        self.log.debug(
            f"TOPOLOGY-000D Method get_defined_systems() uses {url} to access z/OS"
        )

        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            TOPOLOGY.rc = 16
            TOPOLOGY.errors = {"rc": {TOPOLOGY.rc}, "request_error": {e}}
            self.log.critical(
                f"TOPOLOGY-001S Catched an unexpected exception, can not continue {str(TOPOLOGY.errors)}"
            )
            sys.exit(TOPOLOGY.rc)

        if response.status_code != 200:
            self.log.debug(
                f"TOPOLOGY-002E An unexpected statuscode {response.status_code} has been received"
            )
            self.log.debug(f"             {response.text}")

            TOPOLOGY.rc = 8
            TOPOLOGY.errors = {
                "rc": {TOPOLOGY.rc},
                "status_code": response.status_code,
                "reason": response.reason,
            }

        return TOPOLOGY.errors, response

    def validate_system(
        self,
        system: str,
        verify: bool = True,
    ):

        TOPOLOGY.rc: int = 0
        TOPOLOGY.errors = {}

        if not verify:
            requests.packages.urllib3.disable_warnings()

        filter: str = ""
        if system != "":
            filter = f"?system={system}"
            self.log.warning(f"Setting filter {filter} for systems query")

        url = f"{self.path_to_api}/services/systems/v1/validation/system{filter}"
        self.log.debug(
            f"TOPOLOGY-000D Method get_defined_systems () uses {url} to access z/OS"
        )

        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            TOPOLOGY.rc = 16
            TOPOLOGY.errors = {"rc": {TOPOLOGY.rc}, "request_error": {e}}
            self.log.critical(
                f"TOPOLOGY-001S Catched an unexpected exception, can not continue {str(TOPOLOGY.errors)}"
            )
            sys.exit(TOPOLOGY.rc)

        if response.status_code != 200:
            self.log.debug(
                f"TOPOLOGY-002E An unexpected statuscode {response.status_code} has been received"
            )
            self.log.debug(f"             {response.text}")
            TOPOLOGY.rc = 8
            TOPOLOGY.errors = {
                "rc": {TOPOLOGY.rc},
                "status_code": response.status_code,
                "reason": response.reason,
            }

        return TOPOLOGY.errors, response

    def validate_plex(
        self,
        verify: bool = True,
    ):

        TOPOLOGY.rc: int = 0
        TOPOLOGY.errors = {}

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/services/systems/v1/validation/plex"
        self.log.debug(
            f"TOPOLOGY-000D Method get_defined_systems () uses {url} to access z/OS"
        )

        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            TOPOLOGY.rc = 16
            TOPOLOGY.errors = {"rc": {TOPOLOGY.rc}, "request_error": {e}}
            self.log.critical(
                f"TOPOLOGY-001S Catched an unexpected exception, can not continue {str(TOPOLOGY.errors)}"
            )
            sys.exit(TOPOLOGY.rc)

        if response.status_code != 200:
            self.log.debug(
                f"TOPOLOGY-002E An unexpected statuscode {response.status_code} has been received"
            )
            self.log.debug(f"             {response.text}")
            TOPOLOGY.rc = 8
            TOPOLOGY.errors = {
                "rc": {TOPOLOGY.rc},
                "status_code": response.status_code,
                "reason": response.reason,
            }

        return TOPOLOGY.errors, response
