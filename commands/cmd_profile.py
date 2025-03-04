import sys
import click
import json
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from commands.cmd_config import (
    CONFIG,
    DEFAULT_ZOSMF_PROFILE
)

from commands.cmd_utils import (
    get_profile_data,
)

# ------------------------------------------------------------------------------#
# Define the profile group                                                      #
# ------------------------------------------------------------------------------#
@click.group(
    name="profile",
    cls=HelpColorsGroup,
    help_headers_color="yellow",
    help_options_color="green",
)
def profile_cli() -> None:
    """
    Work with zcli profiles.
    \b
    With the profile commands, you can work with zcli profile defintions.

    \b
    Author.......: Ronny Funk
    Function.....: Work with zcli Profiles

    Environment: *ix Terminal CLI / Batch Job
    """
    pass

def get_profile_values(config: dict, name: str) -> dict:
    """_Get profile values_

    Args:
        config (dict): _The configuration object (see command.cmd_utils(read_config)_
        profile_name (str): _Name of profile_

    Returns:
        dict: _Profile values_
    """
    value = False
    if name == DEFAULT_ZOSMF_PROFILE:
        value = True

    description = get_profile_data(
        config=CONFIG,
        profile_name=name,
        profile_type="zosmf",
        key="description",
    )

    user = get_profile_data(
        config=CONFIG,
        profile_name=name,
        profile_type="zosmf",
        key="user",
    )
    protocol = get_profile_data(
        config=CONFIG,
        profile_name=name,
        profile_type="zosmf",
        key="protocol",
    )
    host_name = get_profile_data(
        config=CONFIG,
        profile_name=name,
        profile_type="zosmf",
        key="host",
    )
    port = get_profile_data(
        config=CONFIG,
        profile_name=name,
        profile_type="zosmf",
        key="port",
    )
    reject_unauthorized = get_profile_data(
        config=CONFIG,
        profile_name=name,
        profile_type="zosmf",
        key="rejectUnauthorized",
    )
    user_home = get_profile_data(
        config=CONFIG,
        profile_name=name,
        profile_type="zosmf",
        key="home",
    )
    return {
        "name": name,
        "description": description,
        "user": user,
        "protocol": protocol,
        "host": host_name,
        "port": port,
        "rejectUnauthorized": reject_unauthorized,
        "default": value,
        "home": user_home,
    }

# ------------------------------------------------------------------------------#
# Define the get command subcommand of the profile group                       #
# ------------------------------------------------------------------------------#
@profile_cli.command(name="get", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--name", "-n", required=False, default="", help="Profile name to retrieve, all profiles if empty.", type=click.STRING
)
@click.pass_context
def get(ctx: click.Context, name: str):
    """
    Get zcli profile.
    \b
    You can use this command to get a list of a single or all zcli profile definitions.
    """
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-PROF-000D list() entered with:")
    logging.debug(f"                        name: {name}")

    if name:
        if name not in CONFIG["profiles"]:
            sys.stderr.write(f"ZCLI-PROFILE-001E Profile {name} not found, terminating rc = 12\n")
            sys.exit(12)
        else:
            values: dict = get_profile_values(config=CONFIG, name=name)
            sys.stdout.write(f"{json.dumps(values)}\n")
    else:
        for profile in CONFIG["profiles"]:
            values: dict = get_profile_values(config=CONFIG, name=profile)
            sys.stdout.write(f"{json.dumps(values)}\n")

    logging.debug("CMD-PROF-000D get() returned with:")
    logging.debug(f"                         profile: {json.dumps(values)}")

    sys.exit(0)
