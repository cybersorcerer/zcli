import sys
import requests

from zosapi import client as d


class DATASETS(d.CLIENT):
    errors: dict = {}
    rc: int = 0

    def zosapi_datasets_list(
        self, dsn_level: str, volser: str = "", start: str = "", verify: bool = True
    ):
        """
        Use this operation to list the z/OS Datasets.

        Args:
            dsn_level (str): DS Name Level
            volser (str): a z/OS volume serial number
            start (str): Starting point for listing
            verify (bool): Verify certificates. Defaults to true

        Returns:
            error: Dictionary with return code and error messages if any.
            response: Command response or in case of an error empty list.
        """

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restfiles/ds"
        if dsn_level != "":
            url = url + f"?dslevel={dsn_level}"
        if volser != "":
            url = url + f"&volser={volser}"
        if start != "":
            url = url + f"&start={start}"

        self.headers["X-IBM-Attributes"] = "base,total"
        self.headers["X-IBM-Max-Items"] = "0"

        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            DATASETS.rc = 16
            DATASETS.errors = {"rc": DATASETS.rc, "request_error": e}
            self.log.critical(
                f"DATASETS-001S Catched an unexpected exception, can not continue {str(DATASETS.errors)}"
            )
            sys.exit(DATASETS.rc)

        if response.status_code != 200:
            self.log.error(
                f"DATASETS-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.error(f"             {response.text}")
            DATASETS.rc = 8
            DATASETS.errors = {
                "rc": DATASETS.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        return DATASETS.errors, response

    def zosapi_datasets_members_list(
        self, dataset_name: str, pattern: str = "", verify: bool = True
    ):
        """
        Use this operation to list the members of a z/OS PDS or PDS/E.

        Args:
            dataset_name (str): Name of z/OS PDS or PDS/E
            pattern (str): Pattern to filter members
            verify (bool): Verify certificates. Defaults to true

        Returns:
            error: Dictionary with return code and error messages if any.
            response: Command response or in case of an error empty list.
        """

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restfiles/ds/{dataset_name}/member"

        if pattern != "":
            url = url + f"&pattern={pattern}"

        self.headers["X-IBM-Attributes"] = "base,total"
        self.headers["X-IBM-Max-Items"] = "0"

        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            DATASETS.rc = 16
            DATASETS.errors = {"rc": DATASETS.rc, "request_error": e}
            self.log.critical(
                f"DATASETS-001S Catched an unexpected exception, can not continue {str(DATASETS.errors)}"
            )
            sys.exit(DATASETS.rc)

        if response.status_code != 200:
            self.log.error(
                f"DATASETS-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.error(f"             {response.text}")
            DATASETS.rc = 8
            DATASETS.errors = {
                "rc": DATASETS.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        return DATASETS.errors, response

    def zosapi_datasets_read(
        self,
        dataset_name: str,
        volser: str = "",
        member: str = "",
        encoding: str = "",
        enq_exclusive: bool = False,
        verify: bool = True,
    ):
        """
        Use this operation to read a member of a PDS or PDS/E or a sequential dataset.

        Args:
            dataset_name (str): Name of z/OS PDS or PDS/E or sequential dataset
            member (str): Member name of a PDS or PDS/E
            volser (str): Volume serial
            encoding (str): The encoding to be used
            enq_exclusive (bool): If true X-IBM-Obtain-ENQ will be set to EXCL
            verify (bool): Verify certificates. Defaults to true

        Returns:
            error: Dictionary with return code and error messages if any.
            response: Command response or in case of an error empty list.
        """

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restfiles/ds"

        if volser != "":
            url = url + f"/-({volser})"
        if dataset_name != "":
            url = url + f"/{dataset_name}"
        if member != "":
            url = url + f"({member})"

        self.headers["X-IBM-Data-Type"] = "text"
        self.headers["X-IBM-Obtain-ENQ"] = "SHRW"
        self.headers["X-IBM-Return-Etag"] = "true"
        if enq_exclusive:
            self.headers["X-IBM-Obtain-ENQ"] = "EXCLU"
        if encoding != "":
            self.headers["X-IBM-Dsname-Encoding"] = f"{encoding}"

        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            DATASETS.rc = 16
            DATASETS.errors = {"rc": DATASETS.rc, "request_error": e}
            self.log.critical(
                f"DATASETS-001S Catched an unexpected exception, can not continue {str(DATASETS.errors)}"
            )
            sys.exit(DATASETS.rc)

        if response.status_code != 200:
            self.log.error(
                f"DATASETS-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.error(f"             {response.text}")
            DATASETS.rc = 8
            DATASETS.errors = {
                "rc": DATASETS.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        return DATASETS.errors, response

    def zosapi_datasets_create(
        self,
        ds_name: str,
        volser: str,
        unit: str,
        dsorg: str,
        alcunit: str,
        primary: int,
        secondary: int,
        dirblk: int,
        avgblk: int,
        recfm: str,
        blksize: int,
        lrecl: int,
        storclass: str,
        mgntclass: str,
        dataclass: str,
        dsntype: str,
        like: str,
        verify: bool = True,
    ):
        """
        Use this operation to create a new z/OS dataset.

        Args:
            ds_name (str): Dataset name
            volser (str): Volume serial
            unit (str): Unit
            dsorg (str): Dataset organization
            alcunit (str): Allocation unit
            primary (int): Primary space
            secondary (int): Secondary space
            dirblk (int): Directory blocks
            avgblk (int): Average block size
            recfm (str): Record format
            blksize (int): Block size
            lrecl (int): Logical record length
            storclass (str): Storage class
            mgntclass (str): Management class
            dataclass (str): Data class
            dsntype (str): Dataset type
            like (str): Like dataset
            verify (bool): Verify certificates. Defaults to true

        Returns:
            error: Dictionary with return code and error messages if any.
            response: Command response or in case of an error empty list.
        """

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restfiles/ds/{ds_name}"
        payload = {
            "volser": volser,
            "unit": unit,
            "dsorg": dsorg,
            "alcunit": alcunit,
            "primary": primary,
            "secondary": secondary,
            "dirblk": dirblk,
            "avgblk": avgblk,
            "recfm": recfm,
            "blksize": blksize,
            "lrecl": lrecl,
            "storclass": storclass,
            "mgntclass": mgntclass,
            "dataclass": dataclass,
            "dsntype": dsntype,
            "like": like,
        }

        self.headers["Content-Type"] = "application/json"

        try:
            response = requests.post(
                url, headers=self.headers, json=payload, verify=verify
            )
        except Exception as e:
            DATASETS.rc = 16
            DATASETS.errors = {"rc": DATASETS.rc, "request_error": e}
            self.log.critical(
                f"DATASETS-001S Catched an unexpected exception, can not continue {str(DATASETS.errors)}"
            )
            sys.exit(DATASETS.rc)

        if response.status_code != 201:
            self.log.error(
                f"DATASETS-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.error(f"             {response.text}")
            DATASETS.rc = 8
            DATASETS.errors = {
                "rc": DATASETS.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        return DATASETS.errors, response


def zosapi_datasets_delete(
    self,
    ds_name: str,
    member_name: str,
    volser: str,
    verify: bool = True,
):
    url = f"{self.path_to_api}/restfiles/ds/{ds_name}"
    
    if not verify:
        requests.packages.urllib3.disable_warnings()
        
    self.headers["Content-Type"] = "application/json"

    try:
        response = requests.delete(
            url, headers=self.headers, json=payload, verify=verify
        )
    except Exception as e:
        DATASETS.rc = 16
        DATASETS.errors = {"rc": DATASETS.rc, "request_error": e}
        self.log.critical(
            f"DATASETS-001S Catched an unexpected exception, can not continue {str(DATASETS.errors)}"
        )
        sys.exit(DATASETS.rc)
    if response.status_code != 201:
        self.log.error(
            f"DATASETS-002E An unexpected statuscode {response.status_code} has been received:"
        )
        self.log.error(f"             {response.text}")
        DATASETS.rc = 8
        DATASETS.errors = {
            "rc": DATASETS.rc,
            "status_code": response.status_code,
            "reason": response.reason,
        }
