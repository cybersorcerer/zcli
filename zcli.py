#!/usr/bin/env python
import sys
import click
import logging

from click_help_colors import HelpColorsGroup, HelpColorsCommand

from commands.cmd_defaults import (
    FILES_CACHE_DIR,
    DATASET_CACHE_DIR,
    JOBS_CACHE_DIR,
)

from commands.cmd_datasets import datasets_cli
from commands.cmd_files import files_cli
from commands.cmd_info import info
from commands.cmd_jobs import jobs_cli
from commands.cmd_rtd import get_rtd
from commands.cmd_software import software_cli
from commands.cmd_subsystems import subsystems_cli
from commands.cmd_sysvar import sysvar_cli
from commands.cmd_topology import topology_cli
from commands.cmd_tso import tso_cli
from commands.cmd_notifications import notifications_cli

from commands.cmd_utils import create_directory

from commands.cmd_globals import (
    TERMINAL,
)

FORMAT = '%(asctime)s %(filename)s:%(funcName)s:%(lineno)d %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'

logging.basicConfig(
    format=FORMAT,
    level=logging.INFO,
    datefmt=datefmt
)

@click.group(
    cls=HelpColorsGroup,
    help_headers_color='yellow',
    help_options_color='green'
)
@click.version_option(
    version="0.0.1",
    message="Welcome to z/OS CLI %(prog)s, version %(version)s"
)

@click.option(
    '--verify / --no-verify',
    type=bool,
    default=True,
    help=f'Turn certificate verification on (--verify) or off (--no-verify).'
)
@click.option(
    '--debug / --no-debug',
    type=bool,
    default=False,
    help=f'Turn debugging on (--debug) or off (--no-debug).'
)
@click.option(
    '--user',
    '--u',
    required=True,
    type=str,
    prompt='Enter your RACF User ID > ',
    help=f'The RACF User ID.'
)
@click.option(
    '--password',
    '--p',
    type=str,
    required=True,
    hide_input=True,
    prompt='Enter your RACF Password > ',
    help=f'The RACF Password.'
)
@click.pass_context
def main(ctx: click.Context, user: str, password: str, verify: bool, debug: bool) -> int:
    """
    \b
    Program Name.: z/OS CLI (zcli.py)
    Alias........: zcli
    Author.......: Ronny Funk SVA
    Function.....: z/OS z/OSMF REST API CLI

    Environment: *ix Terminal CLI / Batch Job
    """
    ctx.ensure_object(dict)

    ctx.obj['RC'] = 0

    if user != '':
        ctx.obj['USER'] = user
    else:
        logging.critical(f'ZCLI-MAIN-001S RACF User ID is an empty string, unable to continue')
        ctx.obj['RC'] = 8
    if password != '':
        ctx.obj['PASSWORD'] = password
    else:
        ctx.obj['RC'] = 8
        logging.critical(f'ZCLI-MAIN-002S Password is an empty string, unable to continue')

    ctx.obj['DEBUG'] = debug
    ctx.obj['TERMINAL'] = TERMINAL
    ctx.obj['VERIFY'] = verify
    ctx.obj['LOGGING'] = logging

    if debug:
        logging.basicConfig(
            format=FORMAT,
            level=logging.DEBUG,
            datefmt=datefmt,
            force=True
        )

    return ctx.obj['RC']

if __name__ == '__main__':
    main.add_command(datasets_cli)
    main.add_command(files_cli)
    main.add_command(info)
    main.add_command(jobs_cli)
    main.add_command(get_rtd)
    main.add_command(software_cli)
    main.add_command(subsystems_cli)
    main.add_command(sysvar_cli)
    main.add_command(topology_cli)
    main.add_command(tso_cli)
    main.add_command(notifications_cli)
    create_directory(FILES_CACHE_DIR)
    create_directory(DATASET_CACHE_DIR)
    create_directory(JOBS_CACHE_DIR)
    rc: int = main(obj={}, auto_envvar_prefix='ZCLI')
    sys.exit(rc)
