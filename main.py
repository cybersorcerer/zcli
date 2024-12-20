#!/bin/env python
import logging
import sys
import click
from zosmf import jobs as j
from zosmf import sms as s
from zosmf import mvssubs as ss
from zosmf import tso as t
"""
Sample programm to consume the z/OSMF REST API using
the SVA python zosmf package
"""


def main() -> int:
    FORMAT = '%(asctime)s %(filename)s:%(funcName)s:%(lineno)d %(levelname)s - %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(
        format=FORMAT,
        level=logging.DEBUG,
        datefmt=datefmt
    )
    user: str = "svarfun"
    password: str = "Igel0001"
    rc: int = 8
    separator: str = "-"*80
    print(separator)
    client = ss.MVSSUBS("192.168.9.39", user, password)
    errors, response = client.get_subsystems(verify=False)
    if errors:
        print(errors)
    else:
        print(response)

    print(separator)
    client = t.TSO("192.168.9.39", user, password)
    errors, response = client.issue_tso_command(command="LU", verify=False)
    if errors:
        print(errors)
    else:
        print(response)
    return rc


if __name__ == "__main__":
    rc = main()
    sys.exit(rc)
