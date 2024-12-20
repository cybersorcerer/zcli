
import sys
import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from zosapi import rtd as r
from commands.cmd_defaults import HOST_NAME
#------------------------------------------------------------------------------#
# Define the tso command subcommand                                            #
#------------------------------------------------------------------------------#
@click.command(
    name='rtd',
    cls=HelpColorsCommand,
    help_options_color='blue'
)
@click.option(
    '--address-space-name',
    '-an',
    type=click.STRING,
    default='',
    help='Name of a z/OS address space.'
)
@click.pass_context
def get_rtd(ctx: click.Context, address_space_name: str):
    """
    Use this commmand to retrieve Runtime Diagnostic Data from z/OS.

    \b
    Asname is the name of the address space name or name prefix. DEFAULT: All
    address spaces are analyzed by Runtime Diagnostics in this system.
    """

    user = ctx.obj['USER']
    password = ctx.obj['PASSWORD']
    verify = ctx.obj['VERIFY']

    client = r.RTD(HOST_NAME, user, password)
    errors, response = client.get_rtd(asname=address_space_name, verify=verify)
    if errors:
        sys.stderr.write(f'{str(errors)}\n')
    else:
        sys.stdout.write(f'{response.text}\n')
