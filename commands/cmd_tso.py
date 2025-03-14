import sys
import json
import json
import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from zosapi import tso as t


# ------------------------------------------------------------------------------#
# Define the issues group                                                      #
# ------------------------------------------------------------------------------#
@click.group(
    name="tso",
    cls=HelpColorsGroup,
    help_headers_color="yellow",
    help_options_color="green",
)
def tso_cli() -> None:
    """
    Work with TSO/E address space services on a z/OS system.
    \b
    Module Name.:  commands.cmd_tso.py
    Alias........: None
    Author.......: Ronny Funk
    Function.....: Work with z/OS TSO/E services

    Environment: *ix Terminal CLI / Batch Job
    """
    pass


# ------------------------------------------------------------------------------#
# Define the tso command subcommand                                            #
# ------------------------------------------------------------------------------#
@tso_cli.command(name="command", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--text/--no-text",
    default=False,
    help="Display the response as text.",
)
@click.option(
    "--command", "-c", required=True, help="The TSO/E command to issue.", type=click.STRING
)
@click.pass_context
def command(ctx: click.Context, text: bool, command: str):
    """
    Issue TSO/E command.
    \b
    You can use this operation to issue a TSO/E command and
    get a corresponding response.
    """

    verify = ctx.obj["VERIFY"]

    client = t.TSO(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.issue_tso_command(command, verify=verify)
    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        if text:
            response_dict = json.loads(response.text)
            for line in response_dict["cmdResponse"]:
                sys.stdout.write(f"{line["message"]}\n")
        else:
            sys.stdout.write(f"{response.text}\n")
