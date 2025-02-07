# Python z/OSMF Command Line Interface (zcli)

## Overview

`zcli` is a Python command-line interface (CLI) client designed to interact with IBM z/OS Mainframe Management Facility (z/OSMF). This client provides a user-friendly way to manage various aspects of z/OS environments, such as job management, file and dataset access, and system information retrieval. It is tested on MacOS and z/UNIX. Windows Environments are untested as of now. This is an early alpha version, some z/OSMF REST API functions are still missing, others might not work as expected. I am a z/OS systems programmer and have little experience with Python so please bear with me.

## Installation

To install `zcli`, you need Python 3.10 or higher installed on your system.

### Clone this repository to a directory of your choosing
  
```bash
git clone git@github.com:cybersorcerer/zcli.git
```

### Create a virtual environment and upgrade pip
  
```bash
python -m venv venv
. venv/bin/activate
python -m pip install --upgrade pip
```

### Install requirements

```bash
pip install -r requirements.txt
```

### Copy zcli from the root of this repository to $HOME/.local/bin or any other directory in your PATH

```bash
cp <PATH_TO_ZCLI_INSTALL_DIR>/zcli $HOME/.local/bin
chmod 755 $HOME/.local/bin/zcli
```

### Edit $HOME/.local/bin/zcli

Change <PATH_TO_ZCLI_DIR> to the path you cloned this repository to.

```bash
#!/usr/bin/env bash
cd "<PATH_TO_ZCLI_DIR>"
[[ "$VIRTUAL_ENV" == "" ]]; INVENV=$?
if [ "$INVENV" -eq "0" ]; then
  source venv/bin/activate
fi
./zcli "$@"
```
