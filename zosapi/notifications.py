
import requests
import sys

from zosapi import client as C

class NOTIFICATIONS(C.CLIENT):
    errors: dict = {}
    rc: int = 0

    def get_notifications(
        self,
        verify: bool = True,
    ):

        NOTIFICATIONS.rc: int = 0
        NOTIFICATIONS.errors = {}

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/notifications/inbox"
        self.log.debug(f"NOTIFICATIONS-000D Method get_notifications uses {url} to access zos")

        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            self.log.critical(f'NOTIFICATIONS-001S Catched and unexpected exception, can not continue {str(NOTIFICATIONS.errors)}')
            NOTIFICATIONS.rc = 16
            NOTIFICATIONS.errors = {"rc": NOTIFICATIONS.rc, "request_error": e}
            sys.exit(NOTIFICATIONS.rc)

        if response.status_code != 200:
            self.log.debug(f"NOTIFICATIONS-002E An unexpected statuscode {response.status_code} has been received")
            self.log.debug(f"           {response.text}")
            NOTIFICATIONS.rc = 8
            NOTIFICATIONS.errors = {"rc": NOTIFICATIONS.rc, "status_code": response.status_code, "reason": response.reason}

        return NOTIFICATIONS.errors, response

    def send_notifications(
        self,
        filename,
        verify: bool = True,
    ):

        NOTIFICATIONS.rc: int = 0
        NOTIFICATIONS.errors = {}

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/notifications/new"
        self.log.debug(f"NOTIFICATIONS-000D Method send_notifications uses {url} to access zos")

        try:
            with open(filename) as notification:
                data = notification.read()
        except Exception as e:
            self.log.error(f"NOTIFICATIONS-003E Error reading input file {filename}")
            self.log.error(f"                  {e}")
            NOTIFICATIONS.rc = 8
            NOTIFICATIONS.errors = {"rc": NOTIFICATIONS.rc, "status_code": f"NOTIFICATIONS-003E Error reading input file {filename}", "reason": "N01"}
            sys.exit(NOTIFICATIONS.rc)

        try:
            response = requests.post(url, headers=self.headers, data=data, verify=verify)
        except Exception as e:
            self.log.critical(f'NOTIFICATIONS-001S Catched and unexpected exception, can not continue {str(NOTIFICATIONS.errors)}')
            NOTIFICATIONS.rc = 16
            NOTIFICATIONS.errors = {"rc": NOTIFICATIONS.rc, "request_error": e}
            sys.exit(NOTIFICATIONS.rc)

        if response.status_code != 200:
            self.log.debug(f"NOTIFICATIONS-002E An unexpected statuscode {response.status_code} has been received")
            self.log.debug(f"                  {response.text}")
            NOTIFICATIONS.rc = 8
            NOTIFICATIONS.errors = {"rc": NOTIFICATIONS.rc, "status_code": response.status_code, "reason": response.reason}

        return NOTIFICATIONS.errors, response
