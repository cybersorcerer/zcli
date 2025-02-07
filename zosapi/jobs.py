import sys

import requests

from zosapi import client as C


class JOBS(C.CLIENT):
    errors: dict = {}
    rc: int = 0

    def traverse_job_list(
        self, prefix: str, job_list: list, filter: str = "all"
    ) -> list:
        """_Traverse the returned list of jobs and apply filter criteria_

        Args:
            _prefix (str)_: _Prefix of jobid (JOB, STC or TSU)_.
            _job_list (list)_: _The list of job returned by z/OSMF_.
            _filter (str, optional)_: _Filter to aplly to job status. Defaults to all_.

        Returns:
            list: Filtered list of jobs.
        """
        filtered_list: list = []
        for job in job_list:
            if job["jobid"][0:3].upper() == prefix.upper():
                filtered_list.append(job)
        return filtered_list

    def get_job_list(
        self,
        owner: str = "*",
        prefix: str = "*",
        max_jobs: int = 1000,
        exec_data: str = "Y",
        active_only: bool = False,
        verify: bool = True,
    ):
        """Get a list of jobs from z/OS.

        Args:
            owner (str)....: User ID of the job owner whose jobs are being queried; the default is the z/OS user ID.
                             Folded to uppercase; cannot exceed 8 characters.]. Defaults to '*'.
            prefix (str)...: Job name prefix; default is *. Folded to uppercase; cannot exceed 8 characters._
            jobid (str)....: Job ID. Folded to uppercase; cannot exceed 8 characters. This query parameter is mutually
                             exclusive with user-correlator.
            exec_data (str): This optional parameter specifies whether to return execution data about the job,
                             if execution data is available. This parameter is a string value and is case-insensitive.
                             Valid values are:
                                  - Y (or y)
                                  - N (or n) Defaults to 'Y'.
            type (str).....: Type of jobs to include in the search; default is all types. Valid values are: A (all),
                             ojob (only Jobs), ostc (onyl started tasks), otsu (Only TSO/E users).
            filter(str)....: Filter jobs based on their status.
                                  - 'all'      : All Jobs/STCs/TSO
                                  - 'active'   : Active Jobs/STCs/TSO Users only
                             Defaults to 'all'.
            verify (bool)..: Whether or not to verify SSL certificates; default is True.

        Returns:
            dict: _Return Code and some details about the error_
            response: _Response object returned by z/OSMF._
        """
        JOBS.rc: int = 0
        JOBS.errors = {}

        self.log.debug("JOBS-000D get_job_list() entered with:")
        self.log.debug(f"                owner: {owner}")
        self.log.debug(f"               prefix: {prefix}")
        self.log.debug(f"            exec_data: {exec_data}")
        self.log.debug(f"          active_only: {active_only}")
        self.log.debug(f"               verify: {verify}")

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restjobs/jobs?owner={owner}&prefix={prefix}&exec-data={exec_data}&max-jobs={max_jobs}"

        if active_only:
            url = url + "&status=active"
        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            JOBS.rc = 16
            JOBS.errors = {"rc": JOBS.rc, "request_error": e}
            self.log.critical(
                f"JOBS-001S Catched and unexpected error, can not continue {str(JOBS.errors)}"
            )
            sys.exit(JOBS.rc)

        if response.status_code != 200:
            self.log.debug(
                f"JOBS-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.debug(f"         {response.text}")
            JOBS.errors = {
                "rc": JOBS.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }
            JOBS.rc = 8

        self.log.debug("JOBS-000D get_job_list() returned with:")
        self.log.debug(f"            errors: {JOBS.errors}")
        self.log.debug(f"          response: {response}")

        return JOBS.errors, response

    def get_job_by_jobname_jobid(
        self,
        jobname: str,
        jobid: str,
        stepdata: str = "Y",
        files: bool = False,
        verify: bool = True,
    ):
        """_Get a single job by its ID_

        Args:
            _self (object)....:_ _The z/OSMF Client object._
            _jobname (str)....:_ _The z/OS job name; cannot exceed 8 characters._
            _jobid (str)......:_ _The z/OS jobid of job name; cannot exceed 8._
                                 _characters._
            _verify (bool)....:_ _Whether or not to verify SSL certificates; default is True._

        Returns:
            dict: _Return Code and some details about the error_
            response: _Response object returned by z/OSMF._
        """
        JOBS.rc: int = 0
        JOBS.errors = {}

        self.log.debug("JOBS-000D get_job_by_jobname_jobid() entered with:")
        self.log.debug(f"           Job Name: {jobname}")
        self.log.debug(f"             Job ID: {jobid}")
        self.log.debug(f"          Step Data: {stepdata}")
        self.log.debug(f"              Files: {files}")
        self.log.debug(f"             Verify: {verify}")

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restjobs/jobs/{jobname}/{jobid}?step-data={stepdata}"
        if files:
            url = f"{self.path_to_api}/restjobs/jobs/{jobname}/{jobid}/files"

        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            JOBS.rc = 16
            JOBS.errors = {"rc": JOBS.rc, "request_error": e}
            self.log.critical(
                f"JOBS-001S Catched and unexpected error, can not continue {str(JOBS.errors)}"
            )
            sys.exit(JOBS.rc)

        if response.status_code != 200:
            self.log.debug(
                f"JOBS-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.debug(f"         {response.text}")
            JOBS.rc = 8
            JOBS.errors = {
                "rc": JOBS.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        self.log.debug("JOBS-000D get_job_by_jobname_jobid() returned with:")
        self.log.debug(f"            errors: {JOBS.errors}")
        self.log.debug(f"          response: {response.json()}")

        return JOBS.errors, response

    def get_job_by_job_correlator(
        self,
        correlator: str,
        stepdata: str = "Y",
        files: bool = False,
        verify: bool = True,
    ):
        """_Get a single job by its job correlator._

        Args:
            self (object).......: _The z/OSMF Client object_
            correlator (str)....: _The z/OS jobs job correlator._
            verify (bool).......: _Whether or not to verify SSL certificates; default is True._


        Returns:
            dict: _Return Code and some details about the error_
            response: _Response object returned by z/OSMF._
        """
        JOBS.rc: int = 0
        JOBS.errors = {}

        self.log.debug("JOBS-000D get_job_by_job_correlator() entered with:")
        self.log.debug(f"          correlator: {correlator}")
        self.log.debug(f"           Step Data: {stepdata}")
        self.log.debug(f"               Files: {files}")
        self.log.debug(f"              Verify: {verify}")

        url = f"{self.path_to_api}/restjobs/jobs/{correlator}?step-date={stepdata}"
        if files:
            url = f"{self.path_to_api}/restjobs/jobs/{correlator}/files"

        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            JOBS.rc = 16
            JOBS.errors = {"rc": JOBS.rc, "request_error": e}
            self.log.critical(
                f"JOBS-001S Catched and unexpected error, can not continue {str(JOBS.errors)}"
            )
            sys.exit(JOBS.rc)

        if response.status_code != 200:
            JOBS.rc = 8
            self.log.debug(
                f"JOBS-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.debug(f"         {response.text}")
            JOBS.errors = {
                "rc": JOBS.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        self.log.debug("JOBS-000D get_job_by_job_correlator() returned with:")
        self.log.debug(f"            errors: {JOBS.errors}")
        self.log.debug(f"          response: {response.json()}")

        return JOBS.errors, response

    def get_files_by_jobname_jobid(self, jobname: str, jobid: str, verify: bool = True):
        """_Get the spool files of a job by its jobname and jobid_

        Args:
            self (object)....: _The z/OSMF Client object._
            jobname (str)....: _The z/OS job name; cannot exceed 8 characters._
            jobid (str)......: _The z/OS jobid of job name; cannot exceed 8_
                                characters._
            verify (bool)....: _Whether or not to verify SSL certificates; default is True._

        Returns:
            dict: _Return Code and some details about the error_
            response: _Response object returned by z/OSMF._
        """
        JOBS.rc: int = 0
        JOBS.errors = {}

        self.log.debug("JOBS-000D get_files_by_jobname_jobid() entered with:")
        self.log.debug(f"          Job Name: {jobname}")
        self.log.debug(f"            Job ID: {jobid}")
        self.log.debug(f"            Verify: {verify}")

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restjobs/jobs/{jobname}/{jobid}/files"

        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            JOBS.rc = 16
            JOBS.errors = {"rc": JOBS.rc, "request_error": e}
            self.log.critical(
                f"JOBS-001S Catched and unexpected error, can not continue {str(JOBS.errors)}"
            )
            sys.exit(JOBS.rc)

        if response.status_code != 200:
            JOBS.rc = 8
            self.log.debug(
                f"JOBS-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.debug(f"         {response.text}")
            JOBS.errors = {
                "rc": JOBS.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        self.log.debug("JOBS-000D get_files_by_jobname_jobid() returned with:")
        self.log.debug(f"            errors: {JOBS.errors}")
        self.log.debug(f"          response: {response.json()}")

        return JOBS.errors, response

    def get_files_by_job_correlator(self, correlator: str, verify: bool = True):
        """_Get the spool files of a jobs correlator_

        Args:
            self (object).......: _The z/OSMF Client object_
            correlator (str)....: _The job correlator._
            verify (bool).......: _Whether or not to verify SSL certificates; default is True._

        Returns:
            dict: _Return Code and some details about the error_
            response: _Response object returned by z/OSMF._
        """
        JOBS.rc: int = 0
        JOBS.errors = {}

        self.log.debug("JOBS-000D get_files_by_job_correlator() entered with:")
        self.log.debug(f"          correlator: {correlator}")
        self.log.debug(f"              Verify: {verify}")

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restjobs/jobs/{correlator}/files"

        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            JOBS.rc = 16
            JOBS.errors = {"rc": JOBS.rc, "request_error": e}
            self.log.critical(
                f"JOBS-001S Catched and unexpected error, can not continue {str(JOBS.errors)}"
            )
            sys.exit(JOBS.rc)

        if response.status_code == 200:
            JOBS.rc = 8
            self.log.debug(
                f"JOBS-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.debug(f"         {response.text}")
            JOBS.errors = {
                "rc": JOBS.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        self.log.debug("JOBS-000D get_files_by_job_correlator() returned with:")
        self.log.debug(f"            errors: {JOBS.errors}")
        self.log.debug(f"          response: {response.json()}")

        return JOBS.errors, response

    def get_job_file_by_url(self, url: str, verify: bool = True):
        pass

    def get_job_file_by_id(
        self,
        fileid: str = "",
        jobname: str = "",
        jobid: str = "",
        correlator: str = "",
        verify: bool = True,
    ):
        """Get a JES Spool File by its file ID._

        Args:
            jobname (str)..........: _The z/OS job name; cannot exceed 8 characters._
            jobid (str)............: _The z/OS jobid of job name; cannot exceed 8_
                                     _characters._
            correlator (str).......: _The job correlator._
                      id (str).....: _The id of the spool file to retrieve._
            verify (bool)..........: _Turn certificate verification on/off_. Defaults to True (on)._

        Returns:
            dict: _Return Code and some details about the error_
            response: _Response object returned by z/OSMF._
        """
        JOBS.rc: int = 0
        JOBS.errors = {}

        self.log.debug("JOBS-000D get_job_file_by_id() entered with:")
        self.log.debug(f"                    name: {jobname}")
        self.log.debug(f"                   jobid: {jobid}")
        self.log.debug(f"          job-correlator: {correlator}")
        self.log.debug(f"                      id: {fileid}")
        self.log.debug(f"                  Verify: {verify}")

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restjobs/jobs"

        if jobname != "":
            url = url + f"/{jobname}"
            if jobid != "":
                url = url + f"/{jobid}/files"
            else:
                JOBS.rc = 8
                self.log.error("JOBS-004E Job Name and Job ID required.")
                response = None
                JOBS.errors = {
                    "rc": JOBS.rc,
                    "status_code": "Job Name and Job ID required.",
                    "reason": "J01",
                }
                return JOBS.errors, response
        else:
            if correlator != "":
                url = url + f"/{correlator}/files"
            else:
                JOBS.rc = 8
                self.log.error(
                    "JOBS-005E One of Job Name and Job ID or Correlator required."
                )
                response = None
                JOBS.errors = {
                    "rc": JOBS.rc,
                    "status_code": "One of Job Name and Job ID or Correlator required.",
                    "reason": "J02",
                }
                return JOBS.errors, response

        if fileid != "":
            url = url + f"/{fileid}/records"
        else:
            JOBS.rc = 8
            self.log.error("JOBS-007E A spool file id is required.")
            response = None
            JOBS.errors = {
                "rc": JOBS.rc,
                "status_code": "A spool file id is required.",
                "reason": "J03",
            }
            return JOBS.errors, response

        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            JOBS.rc = 16
            JOBS.errors = {"rc": JOBS.rc, "request_error": e}
            self.log.critical(
                f"JOBS-001S Catched and unexpected error, can not continue {str(JOBS.errors)}"
            )
            sys.exit(JOBS.rc)

        if response.status_code != 200:
            JOBS.rc = 8
            self.log.debug(
                f"JOBS-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.debug(f"         {response.text}")
            JOBS.errors = {
                "rc": JOBS.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        self.log.debug("JOBS-000D get_job_file_by_id() returned with:")
        self.log.debug(f"            errors: {JOBS.errors}")
        self.log.debug(f"          response: {response}")

        return JOBS.errors, response

    def get_job_jcl(
        self,
        jobname: str = "",
        jobid: str = "",
        correlator: str = "",
        verify: bool = True,
    ):
        """Get the jobs JCL.

        Args:
            jobname (str)..........: The z/OS job name; cannot exceed 8 characters.
            jobid (str)............: The z/OS jobid of job name; cannot exceed 8
                                     characters.
            correlator (str).......: The job correlator.
                      id (str).....: The id of the spool file to retrieve.
            verify (bool)..........: Turn certificate verification on/off_. Defaults to True (on).

        Returns:
            dict: Return Code and some details about the error
            response: Response object returned by z/OSMF.
        """
        JOBS.rc: int = 0
        JOBS.errors = {}

        self.log.debug("JOBS-000D get_job_jcl() entered with:")
        self.log.debug(f"                    name: {jobname}")
        self.log.debug(f"                   jobid: {jobid}")
        self.log.debug(f"          job-correlator: {correlator}")
        self.log.debug(f"                  Verify: {verify}")

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restjobs/jobs"

        if jobname != "":
            url = url + f"/{jobname}"
            if jobid != "":
                url = url + f"/{jobid}/files"
            else:
                JOBS.rc = 8
                self.log.error("JOBS-004E Job Name and Job ID required.")
                response = None
                JOBS.errors = {
                    "rc": JOBS.rc,
                    "status_code": "Job Name and Job ID required.",
                    "reason": "J01",
                }
                return JOBS.errors, response
        else:
            if correlator != "":
                url = url + f"/{correlator}/files"
            else:
                JOBS.rc = 8
                self.log.error(
                    "JOBS-005E One of Job Name and Job ID or Correlator required."
                )
                response = None
                JOBS.errors = {
                    "rc": JOBS.rc,
                    "status_code": "One of Job Name and Job ID or Correlator required.",
                    "reason": "J02",
                }
                return JOBS.errors, response

        url = url + "/JCL/records"

        try:
            response = requests.get(url, headers=self.headers, verify=verify)
        except Exception as e:
            JOBS.rc = 16
            JOBS.errors = {"rc": JOBS.rc, "request_error": e}
            self.log.critical(
                f"JOBS-001S Catched and unexpected error, can not continue {str(JOBS.errors)}"
            )
            sys.exit(JOBS.rc)

        if response.status_code != 200:
            JOBS.rc = 8
            self.log.debug(
                f"JOBS-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.debug(f"         {response.text}")
            JOBS.errors = {
                "rc": JOBS.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        self.log.debug("JOBS-000D get_job_jcl() returned with:")
        self.log.debug(f"            errors: {JOBS.errors}")
        self.log.debug(f"          response: {response}")

        return JOBS.errors, response

    def submit_job(self, file_name: str, jes_name: str = "", verify: bool = True):
        """_Submit job to z/OS_

        Args:
            file_name (str).........: _Name of the z/Unix file with z/OS JCL to submit_
            jes_name (str)..........: _Secondary JES name_. Defaults to ''.
            verify (bool)...........: _Turn certificate verification on/off_. Defaults to True (on).

        Returns:
            dict: _Return Code and some details about the error_
            response: _Response object returned by z/OSMF._
        """
        JOBS.rc: int = 0
        JOBS.errors = {}

        self.log.debug("JOBS-000D submit_job() entered with:")
        self.log.debug(f"                   File Name: {file_name}")
        self.log.debug(f"          Secondary JES Name: {jes_name}")
        self.log.debug(f"                      Verify: {verify}")

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restjobs/jobs/"

        if jes_name != "":
            url = url + f"-{jes_name}"

        if file_name != "":
            data = "{ " + '"file": ' + '"' + f"{file_name}" + '" }'

        self.headers["X-IBM-Notification-URL"] = "http://localhost:8080"

        try:
            response = requests.put(url, headers=self.headers, data=data, verify=verify)
        except Exception as e:
            JOBS.rc = 16
            JOBS.errors = {"rc": JOBS.rc, "request_error": e}
            self.log.critical(
                f"JOBS-001S Catched and unexpected error, can not continue {str(JOBS.errors)}"
            )
            sys.exit(JOBS.rc)

        if response.status_code != 201:
            JOBS.rc = 8
            self.log.debug(
                f"JOBS-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.debug(f"         {response.text}")
            JOBS.errors = {
                "rc": JOBS.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        self.log.debug("JOBS-000D submit_job() returned with:")
        self.log.debug(f"            errors: {JOBS.errors}")
        self.log.debug(f"          response: {response}")

        return JOBS.errors, response

    def hold_job(
        self,
        jobname: str,
        jobid: str,
        jesname: str = "",
        correlator: str = "",
        synchronous: bool = True,
        verify: bool = True,
    ):
        """_Hold a JES Job either as synchronous or asynchronous operation._

        Args:
            jobname (str)..........: _The z/OS job name; cannot exceed 8 characters._
            jobid (str)............: _The z/OS jobid of job name; cannot exceed 8_
                                     _characters._
            correlator (str).......: _The job correlator._
            synchronous (bool).....: _Specify the type of operation, True synchronous, False asynchronous._
            verify (bool)..........: _Turn certificate verification on/off_. Defaults to True (on)._

        Returns:
            dict: _Return Code and some details about the error_
            response: _Response object returned by z/OSMF._
        """
        JOBS.rc: int = 0
        JOBS.errors = {}

        self.log.debug("JOBS-000D hold_job() entered with:")
        self.log.debug(f"          Job Name: {jobname}")
        self.log.debug(f"            Job ID: {jobid}")
        self.log.debug(f"          JES Name: {jesname}")
        self.log.debug(f"        correlator: {correlator}")
        self.log.debug(f"            Verify: {verify}")

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restjobs/jobs/"

        data = "{ " + '"request": "hold", '

        if not synchronous:
            data = data + '"version": ' + '"1.0"}'
        else:
            data = data + '"version": ' + '"2.0"}'

        if jesname != "":
            url = url + f"-{jesname}"

        if jobname != "":
            url = url + f"{jobname}/"
            if jobid != "":
                url = url + f"{jobid}"
            else:
                JOBS.rc = 8
                self.log.error("JOBS-004E Job Name and Job ID required.")
                response = None
                JOBS.errors = {
                    "rc": JOBS.rc,
                    "status_code": "Job Name and Job ID required.",
                    "reason": "J01",
                }
                return JOBS.errors, response
        else:
            if correlator != "":
                url = url + f"{correlator}"
            else:
                JOBS.rc = 8
                self.log.error(
                    "JOBS-005E One of Job Name and Job ID or Correlator required."
                )
                response = None
                JOBS.errors = {
                    "rc": JOBS.rc,
                    "status_code": "One of Job Name and Job ID or Correlator required.",
                    "reason": "J02",
                }
                return JOBS.errors, response

        try:
            response = requests.put(url, headers=self.headers, data=data, verify=verify)
        except Exception as e:
            JOBS.rc = 16
            JOBS.errors = {"rc": JOBS.rc, "request_error": e}
            self.log.critical(
                f"JOBS-001S Catched and unexpected error, can not continue {str(JOBS.errors)}"
            )
            sys.exit(JOBS.rc)

        if response.status_code != 200 or response.status_code != 202:
            JOBS.rc = 8
            self.log.debug(
                f"JOBS-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.debug(f"         {response.text}")
            JOBS.errors = {
                "rc": JOBS.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        self.log.debug("JOBS-000D hold_job() returned with:")
        self.log.debug(f"            errors: {JOBS.errors}")
        self.log.debug(f"          response: {response}")

        return JOBS.errors, response

    def release_job(
        self,
        jobname: str,
        jobid: str,
        jesname: str = "",
        correlator: str = "",
        synchronous: bool = True,
        verify: bool = True,
    ):
        """Release a JES Job either as synchronous or asynchronous operation._

        Args:
            jobname (str)..........: _The z/OS job name; cannot exceed 8 characters._
            jobid (str)............: _The z/OS jobid of job name; cannot exceed 8_
                                     _characters._
            correlator (str).......: _The job correlator._
            synchronous (bool).....: _Specify the type of operation, True synchronous, False asynchronous._
            verify (bool)..........: _Turn certificate verification on/off_. Defaults to True (on)._

        Returns:
            dict: _Return Code and some details about the error_
            response: _Response object returned by z/OSMF._
        """
        JOBS.rc: int = 0
        JOBS.errors = {}

        self.log.debug("JOBS-000D release_job() entered with:")
        self.log.debug(f"          Job Name: {jobname}")
        self.log.debug(f"            Job ID: {jobid}")
        self.log.debug(f"          JES Name: {jesname}")
        self.log.debug(f"        correlator: {correlator}")
        self.log.debug(f"            Verify: {verify}")

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restjobs/jobs/"

        data = "{ " + '"request": "release", '

        if not synchronous:
            data = data + '"version": ' + '"1.0"}'
        else:
            data = data + '"version": ' + '"2.0"}'

        if jesname != "":
            url = url + f"-{jesname}"

        if jobname != "":
            url = url + f"{jobname}/"
            if jobid != "":
                url = url + f"{jobid}"
            else:
                JOBS.rc = 8
                self.log.error("JOBS-004E Job Name and Job ID required.")
                response = None
                JOBS.errors = {
                    "rc": JOBS.rc,
                    "status_code": "Job Name and Job ID required.",
                    "reason": "J01",
                }
                return JOBS.errors, response
        else:
            if correlator != "":
                url = url + f"{correlator}"
            else:
                JOBS.rc = 8
                self.log.error(
                    "JOBS-005E One of Job Name and Job ID or Correlator required."
                )
                response = None
                JOBS.errors = {
                    "rc": JOBS.rc,
                    "status_code": "One of Job Name and Job ID or Correlator required.",
                    "reason": "J02",
                }
                return JOBS.errors, response

        try:
            response = requests.put(url, headers=self.headers, data=data, verify=verify)
        except Exception as e:
            JOBS.rc = 16
            JOBS.errors = {"rc": JOBS.rc, "request_error": e}
            self.log.critical(
                f"JOBS-001S Catched and unexpected error, can not continue {str(JOBS.errors)}"
            )
            sys.exit(JOBS.rc)

        if response.status_code != 200 or response.status_code != 202:
            JOBS.rc = 8
            self.log.debug(
                f"JOBS-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.debug(f"         {response.text}")
            JOBS.errors = {
                "rc": JOBS.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        self.log.debug("JOBS-000D release_job() returned with:")
        self.log.debug(f"            errors: {JOBS.errors}")
        self.log.debug(f"          response: {response}")

        return JOBS.errors, response

    def change_job_class(
        self,
        jobname: str,
        jobid: str,
        jobclass: str,
        jesname: str = "",
        correlator: str = "",
        synchronous: bool = True,
        verify: bool = True,
    ):
        """Change the job class of a JES Job either as synchronous or asynchronous operation._

        Args:
            jobname (str)..........: _The z/OS job name; cannot exceed 8 characters._
            jobid (str)............: _The z/OS jobid of job name; cannot exceed 8_
                                     _characters._
            jobclass (str).........: _New jobclass to._
            correlator (str).......: _The job correlator._
            synchronous (bool).....: _Specify the type of operation, True synchronous, False asynchronous._
            verify (bool)..........: _Turn certificate verification on/off_. Defaults to True (on)._

        Returns:
            dict: _Return Code and some details about the error_
            response: _Response object returned by z/OSMF._
        """
        JOBS.rc: int = 0
        JOBS.errors = {}

        self.log.debug("JOBS-000D change_job_class() entered with:")
        self.log.debug(f"          Job Name: {jobname}")
        self.log.debug(f"            Job ID: {jobid}")
        self.log.debug(f"          jobclass: {jobclass}")
        self.log.debug(f"          JES Name: {jesname}")
        self.log.debug(f"        correlator: {correlator}")
        self.log.debug(f"            Verify: {verify}")

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restjobs/jobs/"

        if jobclass != "":
            data = "{ " + '"class": ' + f'"{jobclass}", '
            if not synchronous:
                data = data + '"version": ' + '"1.0"}'
            else:
                data = data + '"version": ' + '"2.0"}'
        else:
            JOBS.rc = 8
            self.log.error("JOBS-007E A new class name is required.")
            response = None
            JOBS.errors = {
                "rc": JOBS.rc,
                "status_code": "A new class name is required.",
                "reason": "J03",
            }
            return JOBS.errors, response

        if jesname != "":
            url = url + f"-{jesname}"

        if jobname != "":
            url = url + f"{jobname}/"
            if jobid != "":
                url = url + f"{jobid}"
            else:
                JOBS.rc = 8
                self.log.error("JOBS-004E Job Name and Job ID required.")
                response = None
                JOBS.errors = {
                    "rc": JOBS.rc,
                    "status_code": "Job Name and Job ID required.",
                    "reason": "J01",
                }
                return JOBS.errors, response
        else:
            if correlator != "":
                url = url + f"{correlator}"
            else:
                JOBS.rc = 8
                self.log.error(
                    "JOBS-005E One of Job Name and Job ID or Correlator required."
                )
                response = None
                JOBS.errors = {
                    "rc": JOBS.rc,
                    "status_code": "One of Job Name and Job ID or Correlator required.",
                    "reason": "J02",
                }
                return JOBS.errors, response

        try:
            response = requests.put(url, headers=self.headers, data=data, verify=verify)
        except Exception as e:
            JOBS.rc = 16
            JOBS.errors = {"rc": JOBS.rc, "request_error": e}
            self.log.critical(
                f"JOBS-001S Catched and unexpected error, can not continue {str(JOBS.errors)}"
            )
            sys.exit(JOBS.rc)

        if response.status_code != 200 or response.status_code != 202:
            JOBS.rc = 8
            self.log.debug(
                f"JOBS-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.debug(f"         {response.text}")
            JOBS.errors = {
                "rc": JOBS.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        self.log.debug("JOBS-000D change_job_class() returned with:")
        self.log.debug(f"            errors: {JOBS.errors}")
        self.log.debug(f"          response: {response}")

        return JOBS.errors, response

    def cancel_job(
        self,
        jobname: str,
        jobid: str,
        jesname: str = "",
        correlator: str = "",
        synchronous: bool = True,
        verify: bool = True,
    ):
        """Cancel a JES Job either as synchronous or asynchronous operation._

        Args:
            jobname (str)..........: _The z/OS job name; cannot exceed 8 characters._
            jobid (str)............: _The z/OS jobid of job name; cannot exceed 8_
                                     _characters._
            correlator (str).......: _The job correlator._
            synchronous (bool).....: _Specify the type of operation, True synchronous, False asynchronous._
            verify (bool)..........: _Turn certificate verification on/off_. Defaults to True (on)._

        Returns:
            dict: _Return Code and some details about the error_
            response: _Response object returned by z/OSMF._
        """
        JOBS.rc: int = 0
        JOBS.errors = {}

        self.log.debug("JOBS-000D cancel_job() entered with:")
        self.log.debug(f"          Job Name: {jobname}")
        self.log.debug(f"            Job ID: {jobid}")
        self.log.debug(f"          JES Name: {jesname}")
        self.log.debug(f"        correlator: {correlator}")
        self.log.debug(f"            Verify: {verify}")

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restjobs/jobs/"

        data = "{ " + '"request": "cancel", '
        if not synchronous:
            data = data + '"version": ' + '"1.0"}'
        else:
            data = data + '"version": ' + '"2.0"}'

        if jesname != "":
            url = url + f"-{jesname}"

        if jobname != "":
            url = url + f"{jobname}/"
            if jobid != "":
                url = url + f"{jobid}"
            else:
                JOBS.rc = 8
                self.log.error("JOBS-004E Job Name and Job ID required.")
                response = None
                JOBS.errors = {
                    "rc": JOBS.rc,
                    "status_code": "Job Name and Job ID required.",
                    "reason": "J01",
                }
                return JOBS.errors, response
        else:
            if correlator != "":
                url = url + f"{correlator}"
            else:
                JOBS.rc = 8
                self.log.error(
                    "JOBS-005E One of Job Name and Job ID or Correlator required."
                )
                response = None
                JOBS.errors = {
                    "rc": JOBS.rc,
                    "status_code": "One of Job Name and Job ID or Correlator required.",
                    "reason": "J02",
                }
                return JOBS.errors, response

        try:
            response = requests.put(url, headers=self.headers, data=data, verify=verify)
        except Exception as e:
            JOBS.rc = 16
            JOBS.errors = {"rc": JOBS.rc, "request_error": e}
            self.log.critical(
                f"JOBS-001S Catched and unexpected error, can not continue {str(JOBS.errors)}"
            )
            sys.exit(JOBS.rc)

        if response.status_code != 200 or response.status_code != 202:
            JOBS.rc = 8
            self.log.debug(
                f"JOBS-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.debug(f"         {response.text}")
            JOBS.errors = {
                "rc": JOBS.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        self.log.debug("JOBS-000D cancel_job() returned with:")
        self.log.debug(f"            errors: {JOBS.errors}")
        self.log.debug(f"          response: {response}")

        return JOBS.errors, response

    def cancel_and_purge_job(
        self,
        jobname: str,
        jobid: str,
        jesname: str = "",
        correlator: str = "",
        synchronous: bool = True,
        verify: bool = True,
    ):
        """Cancel a JES and purges its output Job either as synchronous or asynchronous operation._

        Args:
            jobname (str)..........: _The z/OS job name; cannot exceed 8 characters._
            jobid (str)............: _The z/OS jobid of job name; cannot exceed 8_
                                     _characters._
            correlator (str).......: _The job correlator._
            synchronous (bool).....: _Specify the type of operation, True synchronous, False asynchronous._
            verify (bool)..........: _Turn certificate verification on/off_. Defaults to True (on)._

        Returns:
            dict: _Return Code and some details about the error_
            response: _Response object returned by z/OSMF._
        """
        JOBS.rc: int = 0
        JOBS.errors = {}

        self.log.debug("JOBS-000D cancel_and_purge_job() entered with:")
        self.log.debug(f"          Job Name: {jobname}")
        self.log.debug(f"            Job ID: {jobid}")
        self.log.debug(f"          JES Name: {jesname}")
        self.log.debug(f"        correlator: {correlator}")
        self.log.debug(f"            Verify: {verify}")

        if not verify:
            requests.packages.urllib3.disable_warnings()

        url = f"{self.path_to_api}/restjobs/jobs/"

        if not synchronous:
            self.headers["X-IBM-Job-Modify-Version"] = "1.0"
        else:
            self.headers["X-IBM-Job-Modify-Version"] = "2.0"

        if jesname != "":
            url = url + f"-{jesname}"

        if jobname != "":
            url = url + f"{jobname}/"
            if jobid != "":
                url = url + f"{jobid}"
            else:
                JOBS.rc = 8
                self.log.error("JOBS-004E Job Name and Job ID required.")
                response = None
                JOBS.errors = {
                    "rc": JOBS.rc,
                    "status_code": "Job Name and Job ID required.",
                    "reason": "J01",
                }
                return JOBS.errors, response
        else:
            if correlator != "":
                url = url + f"{correlator}"
            else:
                JOBS.rc = 8
                self.log.error(
                    "JOBS-005E One of Job Name and Job ID or Correlator required."
                )
                response = None
                JOBS.errors = {
                    "rc": JOBS.rc,
                    "status_code": "One of Job Name and Job ID or Correlator required.",
                    "reason": "J02",
                }
                return JOBS.errors, response

        try:
            response = requests.delete(url, headers=self.headers, verify=verify)
        except Exception as e:
            JOBS.rc = 16
            JOBS.errors = {"rc": JOBS.rc, "request_error": e}
            self.log.critical(
                f"JOBS-001S Catched and unexpected error, can not continue {str(JOBS.errors)}"
            )
            sys.exit(JOBS.rc)

        if response.status_code != 200 or response.status_code != 202:
            JOBS.rc = 8
            self.log.debug(
                f"JOBS-002E An unexpected statuscode {response.status_code} has been received:"
            )
            self.log.debug(f"         {response.text}")
            JOBS.errors = {
                "rc": JOBS.rc,
                "status_code": response.status_code,
                "reason": response.reason,
            }

        self.log.debug("JOBS-000D cancel_and_purge_job() returned with:")
        self.log.debug("            errors: {JOBS.errors}")
        self.log.debug("          response: {response}")

        return JOBS.errors, response
