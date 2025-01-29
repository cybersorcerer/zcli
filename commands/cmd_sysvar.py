import sys
import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from zosapi import sysvar as s


# ------------------------------------------------------------------------------#
# Define the software group                                                    #
# ------------------------------------------------------------------------------#
@click.group(
    name="sysvar",
    cls=HelpColorsGroup,
    help_headers_color="yellow",
    help_options_color="green",
)
def sysvar_cli() -> None:
    """
    Interact with the z/OSMF and System variables.

    \b
    Module Name.:  commands.cmd_sysvar.py
    Alias........: None
    Author.......: Ronny Funk
    Function.....: Work with z/OS and z/OSMF variables

    Environment: *ix Terminal CLI / Batch Job
    """
    pass


# ------------------------------------------------------------------------------#
# Define the tso command subcommand                                            #
# ------------------------------------------------------------------------------#
@sysvar_cli.command(name="get", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--plex-name",
    "-pn",
    type=click.STRING,
    required=True,
    default="",
    help="The name of a z/OS sysplex.",
)
@click.option(
    "--system-name",
    "-sn",
    type=click.STRING,
    default="",
    help="The name of a z/OS system.",
)
@click.pass_context
def get(ctx: click.Context, plex_name: str, system_name: str):
    """
    Use this command to retrieve z/OSMF and system variables.

    \b
    You can specify one or more of the following optional command parameters:
    \b
        - sysplex-name (identifies the sysplex. For system symbols, only the local sysplex-name is supprted.)
        - system-name (identifies the system in the sysplex.)
    \b
    """

    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-SYSVAR-000D list() entered with:")
    logging.debug(f"                      sysplex name: {plex_name}")
    logging.debug(f"                       system name: {system_name}")

    client = s.SYSVAR(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.get_system_variables(
        sysplex_name=plex_name, system_name=system_name, verify=verify
    )

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        sys.stdout.write(f"{response.text}\n")
