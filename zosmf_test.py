#!/bin/env python3
import sys  
import zosmf.api as api
from zosmf.api import zosmf as z
"""
A python package to consume the z/OSMF 1.0 REST APIs
"""

if __name__ == "__main__":
    rc: int = 0
    print('======================================================================================================================')
    try:
        client = z.CLIENT("192.168.9.39", "svarfun", "Igel0001")
        print(client.get_info())
    except Exception as e:
        rc = 1
        print("ERROR: ", str(e))
    
    print('======================================================================================================================')
    
    try:
        client = z.CLIENT("192.168.9.39", "svarfun", "Igel0001")
        print(client.get_mvssubs(ssid='JES2'))
    except Exception as e:
        rc = 1
        print("ERROR: ", str(e))
    
    #print('======================================================================================================================')
    #try:
    #    client = z.CLIENT("192.168.9.39", "svarfun", "Igel0001")
    #    print(client.issue_zos_command(command='D A,L'))
    #except Exception as e:
    #    rc = 1
    #    print("ERROR: ", str(e))
    
    print('======================================================================================================================')
    #try:
    client = z.CLIENT("192.168.9.39", "svarfun", "Igel0001")
    print(client.issue_tso_command(command='lu'))
    #except Exception as e:
    #    rc = 1
    #    print("ERROR: ", str(e))
    #
    sys.exit(rc)
