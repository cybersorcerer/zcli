# ------------------------------------------------------------------------------#
# Define the filesystems group                                                  #
# ------------------------------------------------------------------------------#
@click.group(
    name="filesystems",
    cls=HelpColorsGroup,
    help_headers_color="yellow",
    help_options_color="green",
)
def filesystems_cli() -> None:
    """
    Interact with z/OS z/Unix filesystems.

    \b
    Module Name..: commands.cmd_filesystems.py
    Author.......: Ronny Funk
    Function.....: Work with z/Unix filesystems

    Environment: *ix Terminal CLI / Batch Job
    """
    pass