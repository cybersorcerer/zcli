import sys
import requests

from zosapi import client as f


class FILES(f.CLIENT):
    errors: dict = {}
    rc: int = 0

    def zosapi_files_list(self, file_path: str, verify: bool = True):
        """
        Use this operation to list the files and directories in a z/UNIX
        file path on a z/OS system.

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
            self.log.debug(
                f"FILES-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.debug(f"           {response.text}")
            FILES.rc = 8
            FILES.errors = {
                "rc": FILES.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        return FILES.errors, response

    def zosapi_files_retrieve(
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
            self.log.debug(
                f"FILES-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.debug(f"           {response.text}")
            FILES.rc = 8
            FILES.errors = {
                "rc": FILES.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        return FILES.errors, response

    def zosapi_files_write(
        self,
        zunix_file_name: str,
        data: str,
        zunix_file_type: str = "text",
        encoding: str = "IBM-1047",
        charset: str = "ISO8859-1",
        etag: str = "",
        verify: bool = True,
    ):
        """
        Use this operation to write a file from z/UNIX

        Args:
            zunix_file_name (str): Full Path name of the file to write to.
            data (str): Data to write to zunix_file_name.
            zunix_file_type (str): Type of file to retrieve (text or binary).
            encoding (str): Encoding on z/Unix. Default is IBM-1047.
            charset (str): Encoding of local data. Default is ISO8859-1.
            etag (str): Etag returned by retrieve. Default is empty string.
            verify (bool): Verify certificats. Defaults to True.

        Returns:
            error: Dictionalry with return code and error messages if any.
            response: Command response or in case of an error empty list.
        """

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restfiles/fs{zunix_file_name}"

        if etag != "":
            self.headers["If-Match"] = etag

        self.headers["X-IBM-Data-Type"] = f"{zunix_file_type};fileEncoding={encoding}"
        if zunix_file_type == "text":
            self.headers["Content-Type"] = f"text/plain;charset={charset}"
        elif zunix_file_type == "binary":
            self.headers["Content-Type"] = "text/plain"
        else:
            self.log.error(
                f"FILES-003E An unkown file_type of {zunix_file_type} has been specified."
            )
            FILES.rc = 12
            FILES.errors = {
                "rc": 12,
                "status_code": None,
                "reason": f"An unkown file_type {zunix_file_type}, only text/binary allowed",
            }
            return FILES.errors, {}

        try:
            response = requests.put(url, headers=self.headers, data=data, verify=verify)
        except Exception as e:
            FILES.rc = 16
            FILES.errors = {"rc": FILES.rc, "request_error": e}
            self.log.critical(
                f"FILES-001S Catched an unexpected exception, can not continue {str(FILES.errors)}"
            )
            sys.exit(FILES.rc)

        if response.status_code != 201 and response.status_code != 204:
            self.log.debug(
                f"FILES-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.debug(f"           {response.text}")
            FILES.rc = 8
            FILES.errors = {
                "rc": FILES.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        return FILES.errors, response
    

    def zosapi_files_create(
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
            error: Dictionary with return code and error messages if any.
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
            self.log.debug(
                f"FILES-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.debug(f"           {response.text}")
            FILES.rc = 8
            FILES.errors = {
                "rc": FILES.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        return FILES.errors, response
    

    def zosapi_files_delete(
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
            self.log.debug(
                f"FILES-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.debug(f"           {response.text}")
            FILES.rc = 8
            FILES.errors = {
                "rc": FILES.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        return FILES.errors, response
    
    def zosapi_files_util_chmod(
        self,
        zunix_file_path: str,
        permissions: str = "644",
        links: bool = True,
        recursive: bool = False,
        verify: bool = True,
    ):
        """
        Performs chmod on z/Unix files or directories

        Args:
            zunix_file_path (str): The path/file name to create.
            zunix_file_mode (str): The mode of the file, defaults to 644.
            links (bool): Follow links. Defaults to True.
            recursive (bool): Change mode recursively. Defaults to False.
            verify (bool): Verify certificats. Defaults to true

        Returns:
            error: Dictionalry with return code and error messages if any.
            response: Command response or in case of an error empty list.
        """

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restfiles/fs{zunix_file_path}"

        str_link = "follow"
        if not links:
            str_link = "suppress"

        data = {
            "request": "chmod",
            "mode": permissions,
            "links": str_link,
            "recursive": recursive
        }

        try:
            response = requests.put(url, headers=self.headers, json=data, verify=verify)
        except Exception as e:
            FILES.rc = 16
            FILES.errors = {"rc": FILES.rc, "request_error": e}
            self.log.critical(
                f"FILES-001S Catched an unexpected exception, can not continue {str(FILES.errors)}"
            )
            sys.exit(FILES.rc)

        if response.status_code != 200:
            self.log.debug(
                f"FILES-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.debug(f"           {response.text}")
            FILES.rc = 8
            FILES.errors = {
                "rc": FILES.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        return FILES.errors, response
    
    def zosapi_files_util_chown(
        self,
        zunix_file_path: str,
        owner: str,
        group: str,
        links: bool = True,
        recursive: bool = False,
        verify: bool = True,
    ):
        """
        Performs chown on z/Unix files or directories

        Args:
            zunix_file_path (str): The path/file name to create.
            owner (str): The owner of the file.
            group (str): The group of the file.
            links (bool): Follow links. Defaults to True.
            recursive (bool): Change mode recursively. Defaults to False.
            verify (bool): Verify certificats. Defaults to true  

        Returns:
            error: Dictionalry with return code and error messages if any.
            response: Command response or in case of an error empty list.
        """

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restfiles/fs{zunix_file_path}"

        str_link = "follow"
        if not links:
            str_link = "suppress"

        data = {
            "request": "chown",
            "owner": owner,
            "group": group,
            "links": str_link,
            "recursive": recursive
        }

        try:
            response = requests.put(url, headers=self.headers, json=data, verify=verify)
        except Exception as e:
            FILES.rc = 16
            FILES.errors = {"rc": FILES.rc, "request_error": e}
            self.log.critical(
                f"FILES-001S Catched an unexpected exception, can not continue {str(FILES.errors)}"
            )
            sys.exit(FILES.rc)

        if response.status_code != 200:
            self.log.debug(
                f"FILES-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.debug(f"           {response.text}")
            FILES.rc = 8
            FILES.errors = {
                "rc": FILES.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        return FILES.errors, response

    def zosapi_files_util_chtag(
        self,
        zunix_file_path: str,
        action: str,
        codeset: str,
        file_type: str = "mixed",
        links: bool = True,
        recursive: bool = False,
        verify: bool = True,
    ):
        """
        Performs chtag on z/Unix files or directories

        Args:
            zunix_file_path (str): The path/file name to create.
            action (str): The action to perform (set or reset).
            codeset (str): The codeset to use.
            file_type (str): The type of file to set (mixed, text, binary).
            links (bool): Follow links. Defaults to True.
            recursive (bool): Change mode recursively. Defaults to False.
            verify (bool): Verify certificats. Defaults to true

        Returns:
            error: Dictionalry with return code and error messages if any.
            response: Command response or in case of an error empty list.
        """

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restfiles/fs{zunix_file_path}"

        str_link = "change"
        if not links:
            str_link = "suppress"

        data = {
            "request": "chtag",
            "action": action,
            "type": file_type,
            "links": str_link,
            "recursive": recursive
        }

        if action == "set":
            data["codeset"] = codeset

        try:
            response = requests.put(url, headers=self.headers, json=data, verify=verify)
        except Exception as e:
            FILES.rc = 16
            FILES.errors = {"rc": FILES.rc, "request_error": e}
            self.log.critical(
                f"FILES-001S Catched an unexpected exception, can not continue {str(FILES.errors)}"
            )
            sys.exit(FILES.rc)

        if response.status_code != 200:
            self.log.debug(
                f"FILES-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.debug(f"           {response.text}")
            FILES.rc = 8
            FILES.errors = {
                "rc": FILES.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        return FILES.errors, response
    
    def zosapi_files_util_extattr(
        self,
        zunix_file_path: str,
        action: str,
        attributes: str,
        verify: bool = True,
    ):
        """
        Set, reset, and display extended attributes for files

        Args:
            zunix_file_path (str): The path/file name to create.
            action (str): The action to perform (set, reset, or display).
            attributes (str): The attributes to set.
            verify (bool): Verify certificats. Defaults to true

        Returns:
            error: Dictionalry with return code and error messages if any.
            response: Command response or in case of an error empty list.
        """

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restfiles/fs{zunix_file_path}"

        data = {
            "request": "extattr",
        }

        if action != "" and attributes != "":
            data[f"{action}"] = attributes

        try:
            response = requests.put(url, headers=self.headers, json=data, verify=verify)
        except Exception as e:
            FILES.rc = 16
            FILES.errors = {"rc": FILES.rc, "request_error": e}
            self.log.critical(
                f"FILES-001S Catched an unexpected exception, can not continue {str(FILES.errors)}"
            )
            sys.exit(FILES.rc)

        if response.status_code != 200:
            self.log.debug(
                f"FILES-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.debug(f"           {response.text}")
            FILES.rc = 8
            FILES.errors = {
                "rc": FILES.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        return FILES.errors, response

