import sys
import requests

from zosapi import client as f


class FILESYSTEMS(f.CLIENT):
    errors: dict = {}
    rc: int = 0

    def zosapi_filessystems_create(
            self, 
            zfs_dataset_name: str, 
            cyls_pri: int, 
            cyls_sec: int, 
            owner: str = "", 
            group: str = "", 
            perms: str = "", 
            storage_class: str = "", 
            management_class: str = "", 
            data_class: str = "", 
            volumes: list = [],
            verify: bool = True
    ):
        """
        Use this operation to create a z/UNIX file system

        Args:
            zfs_dataset_name (str): The name of the z/UNIX file system dataset. 
            owner (str, optional): The owner of the dataset. Defaults to "".
            group (str, optional): The group that owns the dataset. Defaults to "".
            perms (str, optional): The permissions for the dataset. Defaults to "".
            cyls_pri (int): The number of primary cylinders for the dataset.
            cyls_sec (int): The number of secondary cylinders for the dataset.
            storage_class (str): The storage class for the dataset.
            management_class (str): The management class for the dataset.
            data_class (str): The data class for the dataset.
            volumes (list): A list of volume names to be used for the dataset.
            verify (bool, optional): If True, perform SSL verification. Defaults to True.

        Returns:
            error: Dictionalry with return code and error messages if any.
            response: Command response or in case of an error empty list.
        """
        
        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restfiles/mfs/zfs"
        if zfs_dataset_name != "":
            url = url + f"/{zfs_dataset_name}"

        data = {
            "zfsDatasetName": zfs_dataset_name,
            "cylsPri": cyls_pri,
            "cylsSec": cyls_sec,
        }
        if owner != "":
            data["owner"] = owner
        if group != "":
            data["group"] = group
        if perms != "":
            data["perms"] = perms
        if storage_class != "":
            data["storageClass"] = storage_class
        if management_class != "":
            data["managementClass"] = management_class
        if data_class != "":
            data["dataClass"] = data_class
        if volumes != []:
            data["volumes"] = volumes

        try:
            response = requests.post(url, headers=self.headers, json=data, verify=verify)
        except Exception as e:
            FILESYSTEMS.rc = 16
            FILESYSTEMS.errors = {"rc": FILESYSTEMS.rc, "request_error": e}
            self.log.critical(
                f"FILES-001S Catched an unexpected exception, can not continue {str(FILESYSTEMS.errors)}"
            )
            sys.exit(FILESYSTEMS.rc)

        if response.status_code != 201:
            self.log.debug(
                f"FILES-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.debug(f"           {response.text}")
            FILESYSTEMS.rc = 8
            FILESYSTEMS.errors = {
                "rc": FILESYSTEMS.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        return FILESYSTEMS.errors, response

    def zosapi_filessystems_delete(
            self, 
            zfs_dataset_name: str, 
            verify: bool = True
    ):
        """
        Use this operation to delete a z/UNIX file system

        Args:
            zfs_dataset_name (str): The name of the z/UNIX file system dataset. 
            verify (bool, optional): If True, perform SSL verification. Defaults to True.

        Returns:
            error: Dictionalry with return code and error messages if any.
            response: Command response or in case of an error empty list.
        """
        
        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restfiles/mfs/zfs"
        if zfs_dataset_name != "":
            url = url + f"/{zfs_dataset_name}"

        try:
            response = requests.delete(url, headers=self.headers, verify=verify)
        except Exception as e:
            FILESYSTEMS.rc = 16
            FILESYSTEMS.errors = {"rc": FILESYSTEMS.rc, "request_error": e}
            self.log.critical(
                f"FILES-001S Catched an unexpected exception, can not continue {str(FILESYSTEMS.errors)}"
            )
            sys.exit(FILESYSTEMS.rc)

        if response.status_code != 201:
            self.log.debug(
                f"FILES-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.debug(f"           {response.text}")
            FILESYSTEMS.rc = 8
            FILESYSTEMS.errors = {
                "rc": FILESYSTEMS.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        return FILESYSTEMS.errors, response
    
    def zosapi_filessystems_mount_unmount(
            self, 
            file_system_name: str, 
            action_unmount: bool,
            mount_point: str,
            fs_type: str,
            mode: str,
            setuid: bool = False,
            verify: bool = True
    ):
        """
        Use this operation to mount/unmount a file system

        Args:
            file_system_name (str): The name of the file system.
            action_unmount (bool): If True, unmount the file system.
            mount_point (str): The mount point for the file system.
            fs_type (str): The file system type.
            mode (str): The mode for the file system.
            setuid (bool, optional): If True, set the setuid bit. Defaults to False.
            verify (bool, optional): If True, perform SSL verification. Defaults to True.

        Returns:
            error: Dictionalry with return code and error messages if any.
            response: Command response or in case of an error empty list.
        """
        
        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restfiles/mfs/{file_system_name}"

        data: dict = {}
        if action_unmount:
            data["action"] = "unmount"
        else:
            data["action"] = "mount"
            data["mount-point"] = mount_point
            data["fs-type"] = fs_type
            data["mode"] = mode
            if setuid:
                data["mode"] = data["mode"] + " setuid"
            else:
                data["mode"] = data["mode"] + " nosetuid"

        try:
            response = requests.put(url, headers=self.headers, json=data, verify=verify)
        except Exception as e:
            FILESYSTEMS.rc = 16
            FILESYSTEMS.errors = {"rc": FILESYSTEMS.rc, "request_error": e}
            self.log.critical(
                f"FILES-001S Catched an unexpected exception, can not continue {str(FILESYSTEMS.errors)}"
            )
            sys.exit(FILESYSTEMS.rc)

        if response.status_code != 200 and response.status_code != 204:
            self.log.debug(
                f"FILES-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.debug(f"           {response.text}")
            FILESYSTEMS.rc = 8
            FILESYSTEMS.errors = {
                "rc": FILESYSTEMS.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        return FILESYSTEMS.errors, response

    def zosapi_filessystems_list(
            self, 
            file_system_name: str, 
            path_name: str,
            verify: bool = True
    ):
        """
        Use this operation to list z/Unix file systems

        Args:
            file_system_name (str): The name of the file system.
            path_name (str): The path to the file system.
            verify (bool, optional): If True, perform SSL verification. Defaults to True.

        Returns:
            error: Dictionalry with return code and error messages if any.
            response: Command response or in case of an error empty list.
        """
        
        if not verify:
            requests.packages.urllib3.disable_warnings()

        if file_system_name != "":
            url = f"{self.path_to_api}/restfiles/mfs/?fsname={file_system_name}"
        elif path_name != "":
            url = f"{self.path_to_api}/restfiles/mfs/?path={path_name}"
        else:
            url = f"{self.path_to_api}/restfiles/mfs"

        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            FILESYSTEMS.rc = 16
            FILESYSTEMS.errors = {"rc": FILESYSTEMS.rc, "request_error": e}
            self.log.critical(
                f"FILES-001S Catched an unexpected exception, can not continue {str(FILESYSTEMS.errors)}"
            )
            sys.exit(FILESYSTEMS.rc)

        if response.status_code != 200 and response.status_code != 204:
            self.log.debug(
                f"FILES-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.debug(f"           {response.text}")
            FILESYSTEMS.rc = 8
            FILESYSTEMS.errors = {
                "rc": FILESYSTEMS.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        return FILESYSTEMS.errors, response

