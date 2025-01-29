# Import necessary libraries
import base64
import ssl
import os
import logging


class CLIENT:
    """
    A class to interact with the z/OSMF server using REST APIs.
    """

    def __init__(
        self,
        protocol: str,
        hostname: str,
        username: str,
        password: str,
        port: str,
        cert_path: str,
    ):
        """
        Initialize the client with the z/OSMF server details.

        Args:
            hostname (str): The hostname of the z/OSMF server.
            username (str): The username for authentication.
            password (str): The password for authentication.
            port     (str): The port of z/OSMF API Server (default None).
            cert_path(str): The path to certificates (default None).
        """
        log = logging.getLogger(__name__)
        log.addHandler(logging.NullHandler())

        authstring = username + ":" + password
        bytestring = authstring.encode("ascii")
        authb64 = base64.b64encode(bytestring)

        verify_path = ssl.get_default_verify_paths()
        log.debug(f"CLIENT-000D Certificate Verification path is {verify_path}")
        os.environ.setdefault("SSL_CERT_FILE", cert_path)
        log.debug(
            f"CLIENT-000D Environment Variable SSL_CERT_FILE has been set to {cert_path}"
        )

        headers = {
            "X-CSRF-ZOSMF-HEADER": "",
            "content-type": "application/json",
            "Authorization": f"Basic {authb64.decode()}",
        }

        self.headers = headers
        self.hostname = hostname
        self.port = ":" + port
        self.path_to_api = f"{protocol}://{self.hostname}{self.port}/zosmf"
        self.cert_path = cert_path
        self.log = log

    def verify_off(self):
        pass
