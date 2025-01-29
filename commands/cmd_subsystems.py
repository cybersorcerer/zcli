import click
import sys
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from zosapi import subsystems as ss


# ------------------------------------------------------------------------------#
# Define the issues group                                                      #
# ------------------------------------------------------------------------------#
@click.group(
    name="subsystems",
    cls=HelpColorsGroup,
    help_headers_color="yellow",
    help_options_color="green",
)
def subsystems_cli() -> None:
    """
    This service lists the subsystems on a z/OS system.

    \b
    Module Name.:  commands.cmd_cmd_mvssubs.py
    Alias........: None
    Author.......: Ronny Funk
    Function.....: Get z/OS defined subsystems data

    Environment: *ix Terminal CLI / Batch Job
    """
    pass


# ------------------------------------------------------------------------------#
# Define the subsystem list subcommand                                         #
# ------------------------------------------------------------------------------#
@subsystems_cli.command(name="list", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--name",
    "-n",
    default="",
    help="Name of a subsystem, if empty all subsystems are returned.",
)
@click.pass_context
def list(ctx: click.Context, name: str):
    """
    Get information about z/OS subsystems.
    \b
    You can use the list subcommand to get information about the
    subsystems on a z/OS system. You can filter the returned list
    of subsystems by specifying a subsystem id or wild-card.
    """
    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-SUBSYSTEMS-000D list() entered with:")
    logging.debug(f"                        subsystem name: {name}")

    client = ss.SUBSYSTEMS(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.get_subsystems(filter=name, verify=verify)
    if "rc" in errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        sys.stdout.write(f"{response.text}\n")
