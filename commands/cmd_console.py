import sys
import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from zosapi import console as c


# ------------------------------------------------------------------------------#
# Define the issues group                                                      #
# ------------------------------------------------------------------------------#
@click.group(
    name="console",
    cls=HelpColorsGroup,
    help_headers_color="yellow",
    help_options_color="green",
)
def console_cli() -> None:
    """
    Issue z/OS console commands.
    \b
    With the z/OS console commands, you can issue system commands and work with both
    solicited messages (messages that were issued in response to the command)
    and unsolicited messages (other messages that might or might not have been issued
    in response to the command). z/OS console services establish an extended MCS (EMCS)
    console, which is then used to issue commands and receive messages..

    \b
    Module Name.:  commands.cmd_console.py
    Alias........: None
    Author.......: Ronny Funk
    Function.....: Work with z/OS Console services

    Environment: *ix Terminal CLI / Batch Job
    """
    pass


# ------------------------------------------------------------------------------#
# Define the tso command subcommand                                            #
# ------------------------------------------------------------------------------#
@console_cli.command(name="command", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--command", "-c", required=True, help="The z/OS command to issue.", type=str
)
@click.pass_context
def command(ctx: click.Context, command: str):
    """
    Issue z/OS command.
    \b
    You can use this command to issue a z/OS command and
    get a corresponding response.
    """

    client = c.CONSOLE(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.issue_zos_command(command, verify=ctx.obj["VERIFY"])
    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        sys.stdout.write(f"{response.text}\n")
