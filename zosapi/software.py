import requests
import time
import sys

from zosapi import client as C

class SMS(C.CLIENT):

    """_summary_

    Args:
        C (_type_): _description_

    Returns:
        _type_: _description_
    """
    errors: dict = {}
    rc: int = 0

    def __str__(self) -> str:
        return super().__str__()

    def build_table_string(self, string: str) -> str:
        string_str: str = "["
        for word in string.split(','):
            string_str = string_str + f"'{word}',"
        string_str = string_str + "],"
        return string_str

    def sysmod_report(self, response):
        for entry in response['entries']:
            line: str = entry['entryname'] + ',' + \
            entry['entrytype'] + ',' + entry['zonename']
            for subentry in entry['subentries']:
                for key in subentry:
                    if key != 'VER':
                        line = line + ',' + key + ','
                        for value in subentry[key]:
                            line = line + value + ','
                    else:
                        if subentry[key]:
                            line = line + key + ',' + subentry[key] + ','

            print(line)

    def csv_report(self, response):
        for entry in response['entries']:
            line: str = entry['entryname'] + ';' + \
            entry['entrytype'] + ';' + entry['zonename']
            for subentry in entry['subentries']:
                for key in subentry:
                    if key != 'VER':
                        line = line + ';' + key + ';'
                        for value in subentry[key]:
                            line = line + value + ';'
                    else:
                        if subentry[key]:
                            line = line + key + ';' + subentry[key] + ';'

            print(line)

    def friendly_report(self, response):
        for entry in response['entries']:
            line: str = entry['entryname'] + ' ' + \
            entry['entrytype'] + ' ' + entry['zonename'].ljust(8)
            for subentry in entry['subentries']:
                for key in subentry:
                    if key == 'DATASET':
                        line = line + ' ' + key.ljust(8) + ' '
                        for value in subentry[key]:
                            line = line + value + ';'
                    else:
                        if subentry[key]:
                            line = line + key + '0' + subentry[key] + ';'

            print(line)

    def add_software_instance(self, filename: str = '', verify: bool = True):
        SMS.rc: int = 0
        SMS.errors = {}
        st: str = 'running'

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/swmgmt/swi"

        if filename != '':
            with open(filename, "r") as add_instance:
                data = add_instance.read()
        else:
            SMS.rc = 16
            self.log.error(f"SMS-007E File name is required, can not continue")
            response = None
            SMS.errors = {"rc": SMS.rc, "status_code": "File name is required, can not continue", "reason": "S07"}
            return SMS.errors,response

        try:
            response = requests.post(url, headers=self.headers, data=data, verify=verify)
        except Exception as e:
            SMS.rc = 16
            SMS.errors = {"rc": SMS.rc, "request_error": e}
            self.log.critical(f'SMS-001S Catched an unexpected exception, can not continue {str(SMS.errors)}')
            sys.exit(SMS.rc)

        if response.status_code != 202:
            self.log.error(f"SMS-002E An unexpected statuscode {response.status_code} has been received")
            self.log.error(f"        {response.text}")
            SMS.rc = 8
            SMS.errors = {"rc": SMS.rc, "status_code": response.status_code, "reason": response.reason}
        else:
            statusurl: str = response.json()['statusurl']
            response = requests.get(statusurl, headers=self.headers)
            if response.status_code == 200:
                while st == "running":
                    try:
                        st = response.json()['status']
                    except Exception as e:
                        SMS.rc = 16
                        SMS.errors = {"rc": SMS.rc, "request_error": e}
                        self.log.critical(f'SMS-001S Catched an unexpected exception, can not continue {str(SMS.errors)}')
                        sys.exit(SMS.rc)

                    if st == "running":
                        self.log.debug(f'SMS-000D Collecting query response, please wait, status is {st}')
                        self.log.debug(f'        {response.text}')
                        time.sleep(0.5)
                        response = requests.get(statusurl, headers=self.headers)
            else:
                self.log.error(f"SMS-003E An unexpected statuscode {response.status_code} has been received:")
                self.log.error(f"        {response.text}")
                SMS.errors = {"rc": SMS.rc, "status_code": response.status_code, "reason": response.reason}
                SMS.rc = 8

        return SMS.errors, response

    def export_software_instance(
        self,
        filename: str = '',
        nick_name: str = '',
        swi_name: str = '',
        uuid: str = '',
        verify: bool = True
    ):
        SMS.rc: int = 0
        SMS.errors = {}
        st: str = 'running'

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/swmgmt/swi"

        if uuid != '':
            url = url + f'/{uuid}'
        elif nick_name != '' and swi_name != '':
            url = url + f'/{nick_name}' + f'/{swi_name}'
        else:
            SMS.rc = 16
            response = None
            SMS.errors = {"rc": {SMS.rc}, "status_code": "Either uuid or nick name and instance name must be specified", "reason": "S05"}
            return SMS.errors, response

        url = url + '/export'

        if filename != '':
            with open(filename, "r") as export_instance:
                data = export_instance.read()
        else:
            SMS.rc = 16
            self.log.error(f"SMS-007E File name is required, can not continue")
            response = None
            SMS.errors = {"rc": SMS.rc, "status_code": "File name is required, can not continue", "reason": "S07"}
            return SMS.errors,response

        try:
            response = requests.post(url, headers=self.headers, data=data, verify=verify)
        except Exception as e:
            SMS.rc = 16
            SMS.errors = {"rc": SMS.rc, "request_error": e}
            self.log.critical(f'SMS-001S Catched an unexpected exception, can not continue {str(SMS.errors)}')
            sys.exit(SMS.rc)

        if response.status_code != 202:
            self.log.error(f"SMS-002E An unexpected statuscode {response.status_code} has been received")
            self.log.error(f"        {response.text}")
            SMS.rc = 8
            SMS.errors = {"rc": SMS.rc, "status_code": response.status_code, "reason": response.reason}
        else:
            statusurl: str = response.json()['statusurl']
            response = requests.get(statusurl, headers=self.headers)
            if response.status_code == 200:
                while st == "running":
                    try:
                        st = response.json()['status']
                    except Exception as e:
                        SMS.rc = 16
                        SMS.errors = {"rc": SMS.rc, "request_error": e}
                        self.log.critical(f'SMS-001S Catched an unexpected exception, can not continue {str(SMS.errors)}')
                        sys.exit(SMS.rc)

                    if st == "running":
                        self.log.debug(f'SMS-000D Collecting query response, please wait, status is {st}')
                        self.log.debug(f'        {response.text}')
                        time.sleep(0.5)
                        response = requests.get(statusurl, headers=self.headers)
            else:
                self.log.error(f"SMS-003E An unexpected statuscode {response.status_code} has been received:")
                self.log.error(f"        {response.text}")
                SMS.errors = {"rc": SMS.rc, "status_code": response.status_code, "reason": response.reason}
                SMS.rc = 8

        return SMS.errors, response

    def delete_software_instance(
        self,
        nick_name: str = '',
        swi_name: str = '',
        uuid: str = '',
        verify: bool = True
    ):
        SMS.rc: int = 0
        SMS.errors = {}
        st: str = 'running'

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/swmgmt/swi"

        if uuid != '':
            url = url + f'/{uuid}'
        elif nick_name != '' and swi_name != '':
            url = url + f'/{nick_name}' + f'/{swi_name}'
        else:
            SMS.rc = 16
            response = None
            SMS.errors = {"rc": {SMS.rc}, "status_code": "Either uuid or nick name and instance name must be specified", "reason": "S05"}
            return SMS.errors, response

        try:
            response = requests.delete(url, headers=self.headers, verify=verify)
        except Exception as e:
            SMS.rc = 16
            SMS.errors = {"rc": SMS.rc, "request_error": e}
            self.log.critical(f'SMS-001S Catched an unexpected exception, can not continue {str(SMS.errors)}')
            sys.exit(SMS.rc)

        if response.status_code != 200:
            self.log.error(f"SMS-002E An unexpected statuscode {response.status_code} has been received")
            self.log.error(f"        {response.text}")
            SMS.rc = 8
            SMS.errors = {"rc": SMS.rc, "status_code": response.status_code, "reason": response.reason}

        return SMS.errors, response

    def list_software_instances(self, pswi: bool = False, verify: bool = True):
        SMS.rc: int = 0
        SMS.errors = {}

        if not verify:
            requests.packages.urllib3.disable_warnings()

        if not pswi:
            url = f"{self.path_to_api}/swmgmt/swi"
        else:
            url = f"{self.path_to_api}/swmgmt/pswi"

        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            SMS.rc = 16
            SMS.errors = {"rc": SMS.rc, "request_error": e}
            self.log.critical(f'SMS-001S Catched an unexpected exception, can not continue {str(SMS.errors)}')
            sys.exit(SMS.rc)

        if response.status_code != 200:
            self.log.error(f"SMS-002E An unexpected statuscode {response.status_code} has been received")
            self.log.error(f"        {response.text}")
            SMS.rc = 8
            SMS.errors = {"rc": SMS.rc, "status_code": response.status_code, "reason": response.reason}

        return SMS.errors, response

    def get_software_instance_properties(
        self,
        nick_name: str = '',
        sw_name: str = '',
        uuid: str= '',
        verify: bool = True
    ):
        SMS.rc: int = 0
        SMS.errors = {}

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/swmgmt/swi"

        if uuid != '':
            url = url + f'/{uuid}'
        elif nick_name != '' and sw_name != '':
            url = url + f'/{nick_name}' + f'/{sw_name}'
        else:
            SMS.rc = 16
            SMS.errors = {"rc": {SMS.rc}, "status_code": "Either uuid or nick name and instance name must be specified", "reason": "S05"}
            return SMS.errors, {}

        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            SMS.rc = 16
            SMS.errors = {"rc": {SMS.rc}, "request_error": {e}}
            self.log.critical(f'SMS-001S Catched an unexpected exception, can not continue {str(SMS.errors)}')
            sys.exit(SMS.rc)

        if response.status_code != 200:
            self.log.error(f"SMS-002E An unexpected statuscode {response.status_code} has been received:")
            self.log.error(f"        {response.text}")
            SMS.rc = 8
            SMS.errors = {"rc": SMS.rc, "status_code": response.status_code, "reason": response.reason}

        return SMS.errors, response

    def get_software_instance_datasets(
        self,
        nick_name: str = '',
        sw_name: str = '',
        uuid: str= '',
        verify: bool = True
    ):
        SMS.rc: int = 0
        SMS.errors = {}

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/swmgmt/swi"

        if uuid != '':
            url = url + f'/{uuid}/datasets'
        elif nick_name != '' and sw_name != '':
            url = url + f'/{nick_name}' + f'/{sw_name}/datasets'
        else:
            SMS.rc = 16
            SMS.errors = {"rc": SMS.rc, "status_code": "Either uuid or nick name and instance name must be specified", "reason": "S05"}
            return SMS.errors, {}

        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            SMS.rc = 16
            SMS.errors = {"rc": SMS.rc, "request_error": e}
            self.log.critical(f'SMS-001S Catched an unexpected exception, can not continue {str(SMS.errors)}')
            sys.exit(SMS.rc)

        if response.status_code != 200:
            self.log.error(f"SMS-002E An unexpected statuscode {response.status_code} has been received:")
            self.log.error(f"        {response.text}")
            SMS.rc = 8
            SMS.errors = {"rc": SMS.rc, "status_code": response.status_code, "reason": response.reason}

        return SMS.errors, response

    def get_system_uuid(self, nickname: str = '', verify: bool = True):
        SMS.rc: int = 0
        SMS.errors: dict = {}

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/swmgmt/system/uuid"

        if nickname != '':
            url = url + f'/{nickname}'
        else:
            SMS.rc = 8
            self.log.error("SMS-004E Nickname required.")
            response = None
            SMS.errors = {"rc": SMS.rc, "status_code": "Nickname required.", "reason": "S01"}
            return SMS.errors, response

        try:
            response = requests.post(url, headers=self.headers, verify=verify)
        except Exception as e:
            SMS.rc = 16
            SMS.errors = {"rc": SMS.rc, "request_error": e}
            self.log.critical(f'SMS-001S Catched an unexpected exception, can not continue {str(SMS.errors)}')
            sys.exit(SMS.rc)

        if response.status_code != 200:
            self.log.error(f"SMS-002E An unexpected statuscode {response.status_code} has been received")
            self.log.error(f"        {response.text}")
            SMS.rc = 8
            SMS.errors = {"rc": SMS.rc, "status_code": response.status_code, "reason": response.reason}

        return SMS.errors, response

    def missing_critical_updates(self, nickname: str = '', instance: str = '', uuid: str = '', verify: bool = True):
        SMS.rc: int = 0
        SMS.errors: dict = {}
        st: str = "running"

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/swmgmt/swi"

        if uuid == '':
            if nickname == '' or instance == '':
                SMS.rc = 8
                self.log.error("SMS-004E Nickname and Software Instance Name or UUID are required.")
                response = None
                SMS.errors = {"rc": SMS.rc, "status_code": "Nickname and Software Instance Name or UUID are required.", "reason": "S02"}
                return SMS.errors, response
            else:
                url = url + f"/{nickname}/{instance}"
        else:
                url = url + f"/{uuid}"

        url = url + '/missingcriticalupdates'

        try:
            response = requests.post(url, headers=self.headers, verify=verify)
        except Exception as e:
            SMS.rc = 16
            SMS.errors = {"rc": SMS.rc, "request_error": e}
            self.log.critical(f'SMS-001S Catched an unexpected exception, can not continue {str(SMS.errors)}')
            sys.exit(SMS.rc)

        if response.status_code != 202:
            self.log.error(f"SMS-002E An unexpected statuscode {response.status_code} has been received")
            self.log.error(f"        {response.text}")
            SMS.rc = 8
            SMS.errors = {"rc": SMS.rc, "status_code": response.status_code, "reason": response.reason}
        else:
            statusurl: str = response.json()['statusurl']
            response = requests.get(statusurl, headers=self.headers)
            if response.status_code == 200:
                while st == "running":
                    try:
                        st = response.json()['status']
                    except Exception as e:
                        SMS.rc = 16
                        SMS.errors = {"rc": SMS.rc, "request_error": e}
                        self.log.critical(f'SMS-001S Catched an unexpected exception, can not continue {str(SMS.errors)}')
                        sys.exit(SMS.rc)

                    if st == "running":
                        self.log.debug(f'SMS-000D Collecting query response, please wait, status is {st}')
                        self.log.debug(f'        {response.text}')
                        time.sleep(0.5)
                        response = requests.get(statusurl, headers=self.headers)
            else:
                self.log.error(f"SMS-003E An unexpected statuscode {response.status_code} has been received:")
                self.log.error(f"        {response.text}")
                SMS.errors = {"rc": SMS.rc, "status_code": response.status_code, "reason": response.reason}
                SMS.rc = 8

        return SMS.errors, response

    def missing_fixcat_updates(self, nickname: str = '', instance: str = '', uuid: str = '', verify: bool = True):
        SMS.rc: int = 0
        SMS.errors: dict = {}
        st: str = "running"

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/swmgmt/swi"

        if uuid == '':
            if nickname == '' or instance == '':
                SMS.rc = 8
                self.log.error("SMS-004E Nickname and Software Instance Name or UUID are required.")
                response = None
                SMS.errors = {"rc": SMS.rc, "status_code": "Nickname and Software Instance Name or UUID are required.", "reason": "S02"}
                return SMS.errors, response
            else:
                url = url + f"/{nickname}/{instance}"
        else:
                url = url + f"/{uuid}"

        url = url + '/missingfixcatupdates'

        try:
            response = requests.post(url, headers=self.headers, verify=verify)
        except Exception as e:
            SMS.rc = 16
            SMS.errors = {"rc": SMS.rc, "request_error": e}
            self.log.critical(f'SMS-001S Catched an unexpected exception, can not continue {str(SMS.errors)}')
            sys.exit(SMS.rc)

        if response.status_code != 202:
            self.log.error(f"SMS-002E An unexpected statuscode {response.status_code} has been received")
            self.log.error(f"        {response.text}")
            SMS.rc = 8
            SMS.errors = {"rc": SMS.rc, "status_code": response.status_code, "reason": response.reason}
        else:
            statusurl: str = response.json()['statusurl']
            response = requests.get(statusurl, headers=self.headers)
            if response.status_code == 200:
                while st == "running":
                    try:
                        st = response.json()['status']
                    except Exception as e:
                        SMS.rc = 16
                        SMS.errors = {"rc": SMS.rc, "request_error": e}
                        self.log.critical(f'SMS-001S Catched an unexpected exception, can not continue {str(SMS.errors)}')
                        sys.exit(SMS.rc)

                    if st == "running":
                        self.log.debug(f'SMS-000D Collecting query response, please wait, status is {st}')
                        self.log.debug(f'        {response.text}')
                        time.sleep(0.5)
                        response = requests.get(statusurl, headers=self.headers)
            else:
                self.log.error(f"SMS-003E An unexpected statuscode {response.status_code} has been received:")
                self.log.error(f"        {response.text}")
                SMS.errors = {"rc": SMS.rc, "status_code": response.status_code, "reason": response.reason}
                SMS.rc = 8

        return SMS.errors, response

    def search_software_updates(self, nickname: str = '', instance: str = '', uuid: str = '', sysmods: tuple[str, ...] = [], verify: bool = True):
        SMS.rc: int = 0
        SMS.errors: dict = {}
        st: str = "running"

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/swmgmt/swi"

        if uuid == '':
            if nickname == '' or instance == '':
                SMS.rc = 8
                self.log.error("SMS-004E Nickname and Software Instance Name or UUID are required.")
                response = None
                SMS.errors = {"rc": SMS.rc, "status_code": "Nickname and Software Instance Name or UUID are required.", "reason": "S02"}
                return SMS.errors, response
            else:
                url = url + f"/{nickname}/{instance}"
        else:
                url = url + f"/{uuid}"

        url = url + '/softwareupdatesearch'

        data = '{ "updates": ['
        for sysmod in sysmods:
            data = data + f'"{sysmod}", '
        data = data + ']}'

        self.log.debug(f"SMS-000D Request content is {data}")

        try:
            response = requests.post(url, headers=self.headers, data=data, verify=verify)
        except Exception as e:
            SMS.rc = 16
            SMS.errors = {"rc": SMS.rc, "request_error": e}
            self.log.critical(f'SMS-001S Catched an unexpected exception, can not continue {str(SMS.errors)}')
            sys.exit(SMS.rc)

        if response.status_code != 202:
            self.log.error(f"SMS-002E An unexpected statuscode {response.status_code} has been received")
            self.log.error(f"        {response.text}")
            SMS.rc = 8
            SMS.errors = {"rc": SMS.rc, "status_code": response.status_code, "reason": response.reason}
        else:
            statusurl: str = response.json()['statusurl']
            response = requests.get(statusurl, headers=self.headers)
            if response.status_code == 200:
                while st == "running":
                    try:
                        st = response.json()['status']
                    except Exception as e:
                        SMS.rc = 16
                        SMS.errors = {"rc": SMS.rc, "request_error": e}
                        self.log.critical(f'SMS-001S Catched an unexpected exception, can not continue {str(SMS.errors)}')
                        sys.exit(SMS.rc)

                    if st == "running":
                        self.log.debug(f'SMS-000D Collecting query response, please wait, status is {st}')
                        self.log.debug(f'        {response.text}')
                        time.sleep(0.5)
                        response = requests.get(statusurl, headers=self.headers)
            else:
                self.log.error(f"SMS-003E An unexpected statuscode {response.status_code} has been received:")
                self.log.error(f"        {response.text}")
                SMS.errors = {"rc": SMS.rc, "status_code": response.status_code, "reason": response.reason}
                SMS.rc = 8

        return SMS.errors, response

    def csiquery(
        self,
        global_name: str,
        zones: str,
        entries: str = '',
        subentries: str = '',
        filter: str = '',
        verify: bool = False
    ):
        """_Querying an SMP/E CSI data set.
        This is an asynchronous operation. Therefore, on completion of the initial POST request,
        the z/OSMF Software Management REST interface returns an HTTP response code of 202
        Accepted and a JSON document containing a URL for the status monitor for the request.
        This function performs GET requests to the supplied URL to monitor the status of the operation
        and to obtain and subsequently return the result set._

        Args:
            global_name (str, optional): _Name of a SMP/E global CSI. Defaults to 'SMPE.GLOBAL.CSI'._
            zones (str, optional): _One or more zones names separated by comma_. Defaults to 'GLOBAL'.
            entries (str, optional): __. Defaults to ''.
            subentries (str, optional): _List of subentries_. Defaults to '*'.
            filter (str, optional): _Some filter criteria for the query_. Defaults to ''.
            verify (bool, optional): _certificate verification on/off_. Defaults to False.

        Returns:
            dict | list: _errors and query response_
        """

        SMS.rc: int = 0
        SMS.errors: dict = {}
        st: str = "running"

        zone_str: str = self.build_table_string(zones)

        subentry_str: str = "["
        for subentry in subentries.split(','):
            subentry_str = subentry_str + f"'{subentry}', "
        subentry_str = subentry_str + "],"

        data = "{'zones': " + zone_str + f"'entries': ['{
            entries}'],'subentries': " + subentry_str + "'filter': " + '"' + filter + '"}'

        self.log.debug(f'SMS-000D Request Bodey Data is {data}')

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/swmgmt/csi/csiquery/{global_name}"

        try:
            response = requests.post(
            url, headers=self.headers, data=data, verify=verify)
        except Exception as e:
            SMS.rc = 16
            SMS.errors = {"rc": SMS.rc, "request_error": e}
            self.log.critical(f'SMS-001S Catched an unexpected exception, can not continue {str(SMS.errors)}')
            sys.exit(SMS.rc)

        if response.status_code == 202:
            statusurl: str = response.json()['statusurl']
            response = requests.get(statusurl, headers=self.headers)
            if response.status_code == 200:
                while st == "running":
                    try:
                        st = response.json()['status']
                    except Exception as e:
                        SMS.rc = 16
                        SMS.errors = {"rc": SMS.rc, "request_error": e}
                        self.log.critical(f'SMS-001S Catched an unexpected exception, can not continue {str(SMS.errors)}')
                        sys.exit(SMS.rc)

                    if st == "running":
                        self.log.debug(f'SMS-000D Collecting query response, please wait, status is {st}')
                        self.log.debug(f'        {response.text}')
                        time.sleep(0.5)
                        response = requests.get(statusurl, headers=self.headers)
            else:
                self.log.error(f"SMS-003E An unexpected statuscode {response.status_code} has been received:")
                self.log.error(f"        {response.text}")
                SMS.errors = {"rc": SMS.rc, "status_code": response.status_code, "reason": response.reason}
                SMS.rc = 8

        else:
            self.log.error(f"SMS-002E An unexpected statuscode {response.status_code} has been received:")
            self.log.error(f"        {response.text}")
            SMS.errors = {"rc": SMS.rc, "status_code": response.status_code, "reason": response.reason}
            SMS.rc = 8

        return SMS.errors, response
