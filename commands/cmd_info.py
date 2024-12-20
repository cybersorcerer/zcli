
import sys
import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from zosapi import info as i
from commands.cmd_defaults import HOST_NAME
#------------------------------------------------------------------------------#
# Define the tso command subcommand                                            #
#------------------------------------------------------------------------------#
@click.command(
    name='info',
    cls=HelpColorsCommand,
    help_options_color='blue'
)
@click.pass_context
def info(ctx: click.Context):
    """
    Use this commmand to retrieve information about z/OSMF.

    \b
    This service allows the caller to query the version and other details
    about the instance of z/OSMF running on a particular system.
    """

    user = ctx.obj['USER']
    password = ctx.obj['PASSWORD']
    verify = ctx.obj['VERIFY']

    client = i.INFO(HOST_NAME, user, password)
    errors, response = client.zosmf_info(verify=verify)
    if errors:
        sys.stderr.write(f'{str(errors)}\n')
    else:
        sys.stdout.write(f'{response.text}\n')

