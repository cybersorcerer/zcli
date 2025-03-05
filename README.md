# Python z/OSMF Command Line Interface (zcli)

- [Python z/OSMF Command Line Interface (zcli)](#python-zosmf-command-line-interface-zcli)
  - [Overview](#overview)
  - [Installation](#installation)
    - [Clone this repository to a directory of your choosing](#clone-this-repository-to-a-directory-of-your-choosing)
    - [Create a virtual environment and upgrade pip](#create-a-virtual-environment-and-upgrade-pip)
    - [Install requirements](#install-requirements)
    - [Copy shell script zcli from the repository root to $HOME/.local/bin or any other directory in your PATH](#copy-shell-script-zcli-from-the-repository-root-to-homelocalbin-or-any-other-directory-in-your-path)
    - [Edit $HOME/.local/bin/zcli](#edit-homelocalbinzcli)
    - [Create the zcli configuration file](#create-the-zcli-configuration-file)
    - [Edit zcli configuration file to suit your needs](#edit-zcli-configuration-file-to-suit-your-needs)
  - [How to use zcli.py](#how-to-use-zclipy)

## Overview

`zcli` is a Python command-line interface (CLI) client designed to interact with IBM z/OS Mainframe Management Facility (z/OSMF). This client provides a user-friendly way to manage various aspects of z/OS environments, such as job management, file and dataset access, and system information retrieval. It is tested on MacOS and z/UNIX. Windows Environments are untested as of now. This is an early alpha version, some z/OSMF REST API functions are still missing, others might not work as expected. I am a z/OS systems programmer and have little experience with Python so please bear with me.

## Installation

To install `zcli`, you need Python 3.10 or higher installed on your system. Most of the steps below will be automated in the future, but for now you need to follow the steps below.

### Clone this repository to a directory of your choosing
  
```bash
git clone git@github.com:cybersorcerer/zcli.git
```

### Create a virtual environment and upgrade pip

Change directory to the directory you cloned the zcli repo to and create a virtual environment, activate the environment and upgrade pip.
  
```bash
cd <PATH_TO_ZCLI_DIR>
python -m venv venv
. venv/bin/activate
python -m pip install --upgrade pip
```

### Install requirements

With activated virtual environment install zcli requirements.

```bash
pip install -r requirements.txt
```

### Copy shell script zcli from the repository root to $HOME/.local/bin or any other directory in your PATH

```bash
cp <PATH_TO_ZCLI_DIR>/zcli $HOME/.local/bin
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
./zcli.py "$@"
```

### Create the zcli configuration file

Create the zcli configuration directory and copy samples/zcli.json

```bash
mkdir -p $HOME/.config/zcli
cp <PATH_TO_ZCLI_DIR>/samples/zcli.json $HOME/.config/zcli.json
```

zcli.json will contain your credentials, please make sure it can only be accessed by your user id

```bash
chmod 600 zcli.json
```

### Edit zcli configuration file to suit your needs

1. Change ```<profile_name>```to a meaningful name
2. Change ```<hostname/ip-address>``` to the host name / ip address of your z/OSMF host
3. Change any of the other properties if required
4. Add additional ```<profile_name>``` objects as required
5. Review ```defaults:``` and make any required changes.
6. It is a good idea to add one of your ```<profile_names>```as the default profile for **zosmf**

## How to use zcli.py

```bash
zcli --no-verify --help
Usage: zcli.py [OPTIONS] COMMAND [ARGS]...

  Program Name.: z/OS CLI (zcli.py)
  Alias........: zcli
  Author.......: Ronny Funk SVA
  Function.....: z/OS z/OSMF REST API CLI

  Environment: *ix Terminal CLI / Batch Job

Options:
  --version                 Show the version and exit.
  --verify / --no-verify    Turn certificate verification on (--verify) or off
                            (--no-verify).  [default: verify]
  --debug / --no-debug      Turn debugging on (--debug) or off (--no-debug).
                            [default: no-debug]
  -pn, --profile-name TEXT  z/OSMF Profile to use.
  --help                    Show this message and exit.

Commands:
  console        Issue z/OS console commands.
  datasets       Interact with z/OS datasets.
  files          Interact with z/OS z/Unix files.
  filesystems    Interact with z/OS z/Unix filesystems.
  info           Use this commmand to retrieve information about z/OSMF.
  jobs           Work with batch jobs on a z/OS system.
  notifications  Work with z/OSMF notification services.
  profile        Work with zcli profiles.
  rtd            Use this commmand to retrieve Runtime Diagnostic Data...
  software       Interact with the z/OSMF Software Management task.
  subsystems     This service lists the subsystems on a z/OS system.
  sysvar         Interact with the z/OSMF and System variables.
  topology       Provides commands for working with the groups,...
  tso            Work with TSO/E address space services on a z/OS system.
```
