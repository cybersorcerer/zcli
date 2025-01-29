import sys
import click
from click_help_colors import HelpColorsCommand
from zosapi import info as i
from tui.info import tui_info_list


# ------------------------------------------------------------------------------#
# Define the info command subcommand                                            #
# ------------------------------------------------------------------------------#
@click.command(name="info", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--tui/ --no-tui",
    required=False,
    default=False,
    show_default=True,
    help="Display response data in a table.",
)
@click.pass_context
def info(ctx: click.Context, tui: bool):
    """
    Use this commmand to retrieve information about z/OSMF.

    \b
    This service allows the caller to query the version and other details
    about the instance of z/OSMF running on a particular system.
    """

    verify = ctx.obj["VERIFY"]

    client = i.INFO(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.zosmf_info(verify=verify)

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        if not tui:
            sys.stdout.write(f"{response.text}\n")
        else:
            tui_info_list.show_tui(response.text)
