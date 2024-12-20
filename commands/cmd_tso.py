
import sys
import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from zosapi import tso as t
from commands.cmd_defaults import HOST_NAME

#------------------------------------------------------------------------------#
# Define the issues group                                                      #
#------------------------------------------------------------------------------#
@click.group(
    name='tso',
    cls=HelpColorsGroup,
    help_headers_color='yellow',
    help_options_color='green',
)
def tso_cli() -> None:
    """
    Work with TSO/E address space services on a z/OS system.
    \b
    Module Name.:  commands.cmd_tso.py
    Alias........: None
    Author.......: Ronny Funk
    Function.....: Query z/OS z/OSMF Toplogy Services

    Environment: *ix Terminal CLI / Batch Job
    """
    pass
#------------------------------------------------------------------------------#
# Define the tso command subcommand                                            #
#------------------------------------------------------------------------------#
@tso_cli.command(
    name='command',
    cls=HelpColorsCommand,
    help_options_color='blue'
)
@click.option(
    '--command',
    '-c',
    required=True,
    help='The TSO/E command to issue.',
    type=str
)
@click.pass_context
def command(ctx: click.Context,command: str):
    """
    Issue TSO/E command.
    \b
    You can use this operation to issue a TSO/E command and
    get a corresponding response.
    """

    user = ctx.obj['USER']
    password = ctx.obj['PASSWORD']
    verify = ctx.obj['VERIFY']

    client = t.TSO(HOST_NAME, user, password)
    errors, response = client.issue_tso_command(command, verify=verify)
    if errors:
        sys.stderr.write(f'{str(errors)}\n')
    else:
        sys.stdout.write(f'{response.text}\n')

