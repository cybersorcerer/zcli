import sys
import requests

from zosapi import client as f


class FILESYSTEMS(f.CLIENT):
    errors: dict = {}
    rc: int = 0

    def zosapi_filessystems_create(self, file_path: str, verify: bool = True):
        """
        Use this operation to create a z/UNIX file system

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
        if file_path != "":
            url = url + f"?path={file_path}"

        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            FILES.rc = 16
            FILES.errors = {"rc": FILES.rc, "request_error": e}
            self.log.critical(
                f"FILES-001S Catched an unexpected exception, can not continue {str(FILES.errors)}"
            )
            sys.exit(FILES.rc)

        if response.status_code != 200:
            self.log.error(
                f"FILES-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.error(f"           {response.text}")
            FILES.rc = 8
            FILES.errors = {
                "rc": FILES.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        return FILES.errors, response

    def zosapi_filesystem_delete(
        self,
        zunix_file_name: str,
        zunix_file_type: str = "text",
        encoding: str = "IBM-1047",
        charset: str = "ISO8859-1",
        verify: bool = True,
    ):
        """
        Use this operation to read a file from z/UNIX

        Args:
            zunix_file_name (str): Full Path name of the file to write to.
            zunix_file_type (str): Type of file to retrieve (text or binary).
            encoding (str): Encoding on z/Unix. Default is IBM-1047.
            charset (str): Encoding of local data. Default is ISO8859-1.
            verify (bool): Verify certificats. Defaults to true

        Returns:
            error: Dictionalry with return code and error messages if any.
            response: Command response or in case of an error empty list.
        """

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restfiles/fs{zunix_file_name}"

        self.headers["X-IBM-Data-Type"] = f"{zunix_file_type};fileEncoding={encoding}"

        if zunix_file_type == "text":
            self.headers["Content-Type"] = f"text/plain;charset={charset}"
        elif zunix_file_type == "binary":
            self.headers["Content-Type"] = "text/plain"
        else:
            self.headers["Content-Type"] = "text/plain"

        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            FILES.rc = 16
            FILES.errors = {"rc": FILES.rc, "request_error": e}
            self.log.critical(
                f"FILES-001S Catched an unexpected exception, can not continue {str(FILES.errors)}"
            )
            sys.exit(FILES.rc)

        if response.status_code != 200:
            self.log.error(
                f"FILES-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.error(f"           {response.text}")
            FILES.rc = 8
            FILES.errors = {
                "rc": FILES.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        return FILES.errors, response


    def zosapi_filesystems_mount(
        self,
        zunix_file_path: str,
        zunix_type: str,
        zunix_file_mode: str = "rw-r--r--",
        verify: bool = True,
    ):
        """
        Use this operation to create a z/Unix file or directory

        Args:
            zunix_file_path (str): The path/file name to create.
            zunix_type (str): The tpe to create dir or file, defaults to dir.
            zunix_file_mode (str): The mode of the file, defaults to rw-r--r--.
            verify (bool): Verify certificats. Defaults to true

        Returns:
            error: Dictionalry with return code and error messages if any.
            response: Command response or in case of an error empty list.
        """

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restfiles/fs{zunix_file_path}"
        print(url)

        data = {"type": zunix_type, "mode": zunix_file_mode.upper()}

        try:
            response = requests.post(url, headers=self.headers, json=data, verify=verify)
        except Exception as e:
            FILES.rc = 16
            FILES.errors = {"rc": FILES.rc, "request_error": e}
            self.log.critical(
                f"FILES-001S Catched an unexpected exception, can not continue {str(FILES.errors)}"
            )
            sys.exit(FILES.rc)

        if response.status_code != 201:
            self.log.error(
                f"FILES-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.error(f"           {response.text}")
            FILES.rc = 8
            FILES.errors = {
                "rc": FILES.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        return FILES.errors, response
    

    def zosapi_filesystems_unmount(
        self,
        zunix_file_path: str,
        recursive: bool = False,
        verify: bool = True,
    ):
        """
        Use this operation to delete a z/Unix file or directory

        Args:
            zunix_file_path (str): The path/file name to create.
            recursive (bool): Delete recursively. Defaults to False.
            verify (bool): Verify certificats. Defaults to true

        Returns:
            error: Dictionalry with return code and error messages if any.
            response: Command response or in case of an error empty list.
        """

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restfiles/fs{zunix_file_path}"

        if recursive:
            self.headers["X-IBM-Option"] = "recursive"  
        
        try:
            response = requests.delete(url, headers=self.headers, verify=verify)
        except Exception as e:
            FILES.rc = 16
            FILES.errors = {"rc": FILES.rc, "request_error": e}
            self.log.critical(
                f"FILES-001S Catched an unexpected exception, can not continue {str(FILES.errors)}"
            )
            sys.exit(FILES.rc)

        if response.status_code != 204:
            self.log.error(
                f"FILES-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.error(f"           {response.text}")
            FILES.rc = 8
            FILES.errors = {
                "rc": FILES.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        return FILES.errors, response

