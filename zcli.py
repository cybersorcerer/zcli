#!/usr/bin/env python
import sys
import click
import logging

from click_help_colors import HelpColorsGroup

from commands.cmd_config import (
    FILES_CACHE_DIR,
    DATASET_CACHE_DIR,
    JOBS_CACHE_DIR,
    DEFAULT_ZOSMF_PROFILE,
    CERT_PATH,
    CONFIG,
)

from commands.cmd_utils import (
    create_directory,
    get_profile_data,
)

from commands.cmd_datasets import datasets_cli
from commands.cmd_files import files_cli
from commands.cmd_filesystems import filesystems_cli
from commands.cmd_info import info
from commands.cmd_jobs import jobs_cli
from commands.cmd_rtd import get_rtd
from commands.cmd_software import software_cli
from commands.cmd_subsystems import subsystems_cli
from commands.cmd_sysvar import sysvar_cli
from commands.cmd_topology import topology_cli
from commands.cmd_tso import tso_cli
from commands.cmd_notifications import notifications_cli
from commands.cmd_console import console_cli

from commands.cmd_globals import (
    TERMINAL,
)

FORMAT = "%(asctime)s %(filename)s:%(funcName)s:%(lineno)d %(levelname)s - %(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(format=FORMAT, level=logging.INFO, datefmt=datefmt)


@click.group(
    cls=HelpColorsGroup, help_headers_color="yellow", help_options_color="green"
)
@click.version_option(
    version="0.0.1a", message="Welcome to z/OS CLI %(prog)s, version %(version)s"
)
@click.option(
    "--verify / --no-verify",
    type=click.BOOL,
    default=True,
    show_default=True,
    help="Turn certificate verification on (--verify) or off (--no-verify).",
)
@click.option(
    "--debug / --no-debug",
    type=click.BOOL,
    default=False,
    show_default=True,
    help="Turn debugging on (--debug) or off (--no-debug).",
)
@click.option(
    "--profile-name",
    "-pn",
    default="",
    type=click.STRING,
    help="z/OSMF Profile to use.",
)
@click.pass_context
def main(
    ctx: click.Context,
    profile_name: str,
    verify: bool,
    debug: bool,
) -> int:
    """
    \b
    Program Name.: z/OS CLI (zcli.py)
    Alias........: zcli
    Author.......: Ronny Funk SVA
    Function.....: z/OS z/OSMF REST API CLI

    Environment: *ix Terminal CLI / Batch Job
    """
    if debug:
        logging.basicConfig(
            format=FORMAT, level=logging.DEBUG, datefmt=datefmt, force=True
        )

    logging.debug("ZCLI-MAIN-000D list() entered with:")
    logging.debug(f"                           verify: {verify}")
    logging.debug(f"                            debug: {debug}")
    logging.debug(f"                     profile name: {profile_name}")

    ctx.ensure_object(dict)

    create_directory(FILES_CACHE_DIR)
    create_directory(DATASET_CACHE_DIR)
    create_directory(JOBS_CACHE_DIR)

    if profile_name == "":
        if DEFAULT_ZOSMF_PROFILE != "":
            profile_name = DEFAULT_ZOSMF_PROFILE
        else:
            raise click.BadParameter(
                "ZCLI-MAIN-001S No default profile in zcli.json and --profile is an empty string, unable to continue.",
                param_hint=["--profile"],
            )

    logging.debug(f"ZCLI-MAIN-000D Profile name is {profile_name}")

    PROTOCOL = get_profile_data(
        config=CONFIG,
        profile_name=profile_name,
        profile_type="zosmf",
        key="protocol",
    )
    logging.debug(
        f'ZCLI-MAIN-000D Value for Property "protocol" from profile {profile_name} is {PROTOCOL}'
    )
    if PROTOCOL == "":
        PROTOCOL = "https"

    HOST_NAME = get_profile_data(
        config=CONFIG,
        profile_name=profile_name,
        profile_type="zosmf",
        key="host",
    )
    logging.debug(
        f'ZCLI-MAIN-000D Value for Property "host" from profile {profile_name} is {HOST_NAME}'
    )
    if HOST_NAME == "":
        raise click.BadParameter(
            f'ZCLI-MAIN-002S Property "host" is missing in profile definition {profile_name}, unable to continue.',
            param_hint=["zcli.json"],
        )

    PORT = get_profile_data(
        config=CONFIG,
        profile_name=profile_name,
        profile_type="zosmf",
        key="port",
    )
    logging.debug(
        f'ZCLI-MAIN-000D Value for Property "port" from profile {profile_name} is {PORT}'
    )
    if PORT == "":
        PORT = "443"

    ENCODING = get_profile_data(
        config=CONFIG,
        profile_name=profile_name,
        profile_type="zosmf",
        key="encoding",
    )
    logging.debug(
        f'ZCLI-MAIN-000D Value for Property "encoding" from profile {profile_name} is {ENCODING}'
    )
    if ENCODING == "":
        ENCODING = "IBM-1047"

    USER = get_profile_data(
        config=CONFIG,
        profile_name=profile_name,
        profile_type="zosmf",
        key="user",
    )
    logging.debug(
        f'ZCLI-MAIN-000D Value for Property "user" from profile {profile_name} is {USER}'
    )
    if USER == "":
        raise click.BadParameter(
            f'ZCLI-MAIN-002S Property "user" is missing in profile definition {profile_name}, unable to continue.',
            param_hint=["zcli.json"],
        )

    PASSWORD = get_profile_data(
        config=CONFIG,
        profile_name=profile_name,
        profile_type="zosmf",
        key="password",
    )
    if PASSWORD == "":
        raise click.BadParameter(
            f'ZCLI-MAIN-002S Property "password" is missing in profile definition {profile_name}, unable to continue.',
            param_hint=["zcli.json"],
        )

    ctx.obj["CERT_PATH"] = CERT_PATH
    ctx.obj["PROFILE_NAME"] = profile_name
    ctx.obj["PROTOCOL"] = PROTOCOL
    ctx.obj["HOST_NAME"] = HOST_NAME
    ctx.obj["PORT"] = PORT
    ctx.obj["ENCODING"] = ENCODING
    ctx.obj["USER"] = USER
    ctx.obj["PASSWORD"] = PASSWORD
    ctx.obj["RC"] = 0
    ctx.obj["DEBUG"] = debug
    ctx.obj["TERMINAL"] = TERMINAL
    ctx.obj["VERIFY"] = verify
    ctx.obj["LOGGING"] = logging

    return ctx.obj["RC"]


if __name__ == "__main__":
    main.add_command(console_cli)
    main.add_command(datasets_cli)
    main.add_command(files_cli)
    main.add_command(filesystems_cli)
    main.add_command(get_rtd)
    main.add_command(info)
    main.add_command(jobs_cli)
    main.add_command(notifications_cli)
    main.add_command(software_cli)
    main.add_command(subsystems_cli)
    main.add_command(sysvar_cli)
    main.add_command(topology_cli)
    main.add_command(tso_cli)

    rc: int = main(obj={}, auto_envvar_prefix="ZCLI")

    sys.exit(rc)
