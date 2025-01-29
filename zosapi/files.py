import sys
import requests

from zosapi import client as f

class FILES(f.CLIENT):
    errors: dict = {}
    rc: int = 0

    def zosapi_files_list(
            self, 
            file_path: str = '', 
            filter: str = '', 
            group_owner: str = '', 
            mtime: int = 0,
            size: str = '',
            permissions: str = '',
            user: str = '',
            typ: str = '', 
            lstat: bool = False, 
            max_items: int = 0, 
            depth: int = 1, 
            verify: bool = True
    ):
        """
        Use this operation to list the files and directories in a z/UNIX
        file path on a z/OS system.

        Args:
            file_path (str)   : Name of file path on z/UNIX or empty string
            filter (str)      : Select entries that match pattern according to the rules of fnmatch(). 
                              : The supplied pattern is matched against the absolute path of the entry, 
                              : with behavior similar to the find -name option.
            group_owner (str) : Select entries that have a group owner of name. If name is an integer value, 
                              : select entries that have a group owner of GID.
            mtime (int)       : Select entries that were modified with a value of number days ago. If a 
                              : number is given without a minus sign or plus sign, files that are modified 
                              : exactly number of days ago are selected. If number is preceded with a plus sign, 
                              : files modified more than number of days ago are selected. If number is preceded 
                              : with a minus sign, files modified less than number of days ago are selected.
            size (str)        : Select files that are number long. If number does not include a suffix, the number 
                              : of the file size in bytes. If number includes a suffix of K, the number size is 
                              : in 1024-byte blocks; if M, the number size is 1048578-byte blocks, and if G 
                              : the number size is 1073741824-byte blocks. If number is specified without a plus 
                              : sign or minus sign, files of the size matching number exactly are selected. 
                              : If number is preceded with a plus sign, files larger than number are selected. 
                              : If number is preceded with a minus sign, files smaller than number are selected.
                              : If this parameter is specified, only regular files are checked; see the type parameter.
            permissions (str) : Select entries whose permissions match the value octal_mask. If octal_mask is prefixed
                              : by a minus sign, entries that have all of the bits set are present in octal_mask. 
                              : Otherwise, only select entries whose permission bits match octal_mask exactly.
                              : Only the rightmost 12 bits (07777) of octal_mask are used.
            user (str)        : Select entries that have a user owner of name. If name is an integer value,
                              : select entries that have a user owner of UID.
            depth (int)       : When depth is greater than 1, subdirectories up to the specified depth are listed. 
                              : When depth is 1, only the files in the path are listed.
            lstat (bool)      : If the value of this header is "true", a lstat() is performed on the path rather than stat()
                              : and a list containing one item is returned with the lstat results.
            max_items (int)   : Maximum number of items to return, if 0 all items will be returned.
            verify (bool)     : Verify certificats. Defaults to true

        Returns:
            error: Dictionary with return code and error messages or empty.
            response: Command response or empty.
        """

        if not verify:
            requests.packages.urllib3.disable_warnings()

        strt: str = '?'

        url = f"{self.path_to_api}/restfiles/fs"
        if file_path != '':
            url = url + f'{strt}path={file_path}'
            strt = '&'
        if filter != '':
            url = url + f'{strt}name={filter}'
            strt = '&'
        if group_owner != '':
            url = url + f'{strt}group={group_owner}'
            strt = '&'
        if mtime != 0:
            url = url + f'{strt}mtime={mtime}'
            strt = '&'
        if size != '':
            url = url + f'{strt}size={size}'
            strt = '&'
        if permissions != '':
            url = url + f'{strt}perm={permissions}'
            strt = '&'
        if user != '':
            url = url + f'{strt}user={user}'
            strt = '&'
        if depth != 0:
            url = url + f'{strt}depth={depth}'
            strt = '&'
        if typ != '':
            url = url + f'{strt}type={typ}'
            strt = '&'
        if filter != '':
            url = url + f'{strt}name={filter}'

        self.headers['X-IBM-Max-Items'] = str(max_items)
        self.headers['X-IBM-Lstat'] = str(lstat).lower()

        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            FILES.rc = 16
            FILES.errors = {"rc": FILES.rc, "request_error": e}
            self.log.critical(f'FILES-001S Catched an unexpected exception, can not continue {str(FILES.errors)}')
            sys.exit(FILES.rc)

        if response.status_code != 200:
            self.log.error(f"FILES-002E An unexpected statuscode {response.status_code} has been received:")
            self.log.error(f"           {response.text}")
            FILES.rc = 8
            FILES.errors = {"rc": FILES.rc, "status_code": response.status_code, "reason": response.reason}

        return FILES.errors, response

    def zosapi_files_retrieve(self, file_name: str, verify: bool = True):
        """
        Use this operation to read a file from z/UNIX

        Args:
            file_name (str): Full Path name of the file to read from z/UNIX
            verify (bool): Verify certificats. Defaults to true

        Returns:
            error: Dictionalry with return code and error messages if any.
            response: Command response or in case of an error empty list.
        """

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restfiles/fs{file_name}"

        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            FILES.rc = 16
            FILES.errors = {"rc": FILES.rc, "request_error": e}
            self.log.critical(f'FILES-001S Catched an unexpected exception, can not continue {str(FILES.errors)}')
            sys.exit(FILES.rc)

        if response.status_code != 200:
            self.log.error(f"FILES-002E An unexpected statuscode {response.status_code} has been received:")
            self.log.error(f"           {response.text}")
            FILES.rc = 8
            FILES.errors = {"rc": FILES.rc, "status_code": response.status_code, "reason": response.reason}

        return FILES.errors, response

    def zosapi_file_systems_list(self, verify: bool = True):
        pass
