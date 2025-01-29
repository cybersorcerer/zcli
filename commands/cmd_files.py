import sys
import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from zosapi import files as f


# ------------------------------------------------------------------------------#
# Define the software group                                                    #
# ------------------------------------------------------------------------------#
@click.group(
    name="files",
    cls=HelpColorsGroup,
    help_headers_color="yellow",
    help_options_color="green",
)
def files_cli() -> None:
    """
    Interact with z/OS z/Unix files.

    \b
    Module Name.:  commands.cmd_files.py
    Alias........: None
    Author.......: Ronny Funk
    Function.....: Work with z/Unix files

    Environment: *ix Terminal CLI / Batch Job
    """
    pass


# ------------------------------------------------------------------------------#
# Define the files list subcommand                                             #
# ------------------------------------------------------------------------------#
@files_cli.command(name="list", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--path-name", "-pn", default="", type=click.STRING, help="A path or file name."
)
@click.pass_context
def list(ctx: click.Context, path_name: str):
    """
    List z/Unix files and directories.

    \b
    You can use this command to obtain a list
    of z/Unix files and directories.
    """
    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-FILES-000D files list entered with:")
    logging.debug(f"                   file_name: {path_name}")

    if path_name == "":
        path_name = f"/u/{ctx.obj['USER']}"

    client = f.FILES(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.zosapi_files_list(file_path=path_name, verify=verify)

    logging.debug("CMD-FILES-000D files list returned with:")
    logging.debug(f"                errors: {errors}")
    logging.debug(f"              response: {response}")

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        sys.stdout.write(f"{response.text}\n")


# ------------------------------------------------------------------------------#
# Define the files get  subcommand                                             #
# ------------------------------------------------------------------------------#
@files_cli.command(name="retrieve", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--file-name",
    "-f",
    required=True,
    type=click.STRING,
    help="Full path to file name to retrieve.",
)
@click.pass_context
def zosapi_retrieve_file(ctx: click.Context, file_name: str):
    """
    Retrieve a file from z/Unix.

    \b
    You can use this command to retrieve a file
    from z/Unix.
    """
    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-FILES-000D files retrieve entered with:")
    logging.debug(f"                   file_name: {file_name}")

    client = f.FILES(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.zosapi_files_retrieve(file_name=file_name, verify=verify)

    logging.debug("CMD-FILES-000D files retrieve returned with:")
    logging.debug(f"                errors: {errors}")
    logging.debug(f"              response: {response}")

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        sys.stdout.write(f"{response.text}\n")
        sys.stdout.write(f"ETag: {response.headers['ETag']}\n")
