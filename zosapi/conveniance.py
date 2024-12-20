# Home of some convience methods
from typing import Any, Dict
import json

class Conveniance:
    """
    A class to hold convenience methods for interacting with Z/OSMF.
    """
    @staticmethod
    def get_job_ddnames(response) -> list:
        """Get ddnames of a job

        Args:
            response ([type]): [Response from jobs files]

        Returns:
            list: [DD Names of job]
        """
        ddnames: list = [{}]
        for ddname in json.loads(response.text):
            ddnames.append({
                "ddname": ddname['ddname'], 
                "id": ddname['id'], 
                "recfm": ddname['recfm'],
                "url": ddname['url']
            })
        return ddnames