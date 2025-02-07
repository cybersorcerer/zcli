import sys
import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from zosapi import files as f


# ------------------------------------------------------------------------------#
# Define the files group                                                        #
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
    Module Name..: commands.cmd_files.py
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
# Define the files retrieve  subcommand                                         #
# ------------------------------------------------------------------------------#
@files_cli.command(name="retrieve", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--zunix-file-name",
    "-zf",
    required=True,
    type=click.STRING,
    help="Full path to file name to retrieve.",
)
@click.option(
    "--local-file-name",
    "-lf",
    default="",
    type=click.STRING,
    help="Full path to file on local file system to write to.",
)
@click.option(
    "--file-type",
    "-ft",
    default="text",
    show_default=True,
    type=click.Choice(["text", "binary"], case_sensitive=False),
    help="File type, used for convertion.",
)
@click.option(
    "--encoding",
    "-e",
    default="IBM-1047",
    show_default=True,
    help="Codepage on z/Unix, used for conversion.",
)
@click.option(
    "--charset",
    "-c",
    default="ISO8859-1",
    show_default=True,
    help="Codepage of the local file used for conversion.",
)
@click.pass_context
def retrieve_file(
    ctx: click.Context,
    zunix_file_name: str,
    local_file_name: str,
    file_type: str,
    encoding: str,
    charset: str,
):
    """
    Retrieve a file from z/Unix.

    \b
    You can use this command to retrieve a file from z/Unix. To write the
    retrieved data to the local file system also specify --local-file-name.
    """
    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-FILES-000D files retrieve entered with:")
    logging.debug(f"              z/Unix file name: {zunix_file_name}")
    logging.debug(f"               Local file name: {local_file_name}")
    logging.debug(f"                     File Type: {file_type}")
    logging.debug(f"                      Encoding: {encoding}")
    logging.debug(f"                       Charset: {charset}")

    client = f.FILES(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.zosapi_files_retrieve(
        zunix_file_name=zunix_file_name,
        zunix_file_type=file_type,
        encoding=encoding,
        charset=charset,
        verify=verify,
    )

    logging.debug("CMD-FILES-000D files retrieve returned with:")
    logging.debug(f"                errors: {errors}")
    logging.debug(f"              response: {response}")

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        if local_file_name == "":
            sys.stdout.write(f"{response.text}\n")
        else:
            with open(local_file_name, "w") as file:
                file.write(response.text)
        sys.stdout.write(f"ETag: {response.headers['ETag']}\n")


# ------------------------------------------------------------------------------#
# Define the files write subcommand                                             #
# ------------------------------------------------------------------------------#
@files_cli.command(name="write", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--zunix-file-name",
    "-zf",
    required=True,
    type=click.STRING,
    help="Full path to file name of z/Unix file to write to.",
)
@click.option(
    "--local-file-name",
    "-lf",
    required=True,
    type=click.STRING,
    help="Full path to local file name.",
)
@click.option(
    "--etag",
    "-e",
    default="",
    type=click.STRING,
    help="The etag returned from retrieve or empty string.",
)
@click.option(
    "--file-type",
    "-ft",
    default="text",
    show_default=True,
    type=click.Choice(["text", "binary"], case_sensitive=False),
    help="File type, used for convertion.",
)
@click.option(
    "--encoding",
    "-e",
    default="IBM-1047",
    show_default=True,
    help="Codepage on z/Unix, used for conversion.",
)
@click.option(
    "--charset",
    "-c",
    default="ISO8859-1",
    show_default=True,
    help="Codepage of the local, file used for conversion.",
)
@click.pass_context
def write_file(
    ctx: click.Context,
    zunix_file_name: str,
    local_file_name: str,
    etag: str,
    file_type: str,
    encoding: str,
    charset: str,
):
    """
    Write to a file in z/Unix.

    \b
    You can use this command to write to a file in z/Unix. The command will read
    data from --local-file-name and write it to --zunix-file-name. You can specify
    an etag (--etag) formerly returned by the retrieve command. If an etag is specified,
    data will onyl be written to --zunix-file-name if the etag specified here
    matches the etag calculated before data would be written. If the etags do not match
    means that --zunix-file-name has been changed somehow between retrieval and
    this command. If you do not specify --etag data will always be written.
    """
    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-FILES-000D files retrieve entered with:")
    logging.debug(f"              z/Unix file_name: {zunix_file_name}")
    logging.debug(f"               Local file_name: {local_file_name}")
    logging.debug(f"                          Etag: {etag}")
    logging.debug(f"                     File Type: {file_type}")
    logging.debug(f"                      Encoding: {encoding}")
    logging.debug(f"                       Charset: {charset}")

    client = f.FILES(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )

    try:
        with open(local_file_name, "r") as file:
            data = file.read()
    except Exception as e:
        sys.stderr.write(
            f"CMD-FILES-004S Catched an unexpected exception while reading local file {local_file_name}, can not continue {e}"
        )
        sys.exit(1)

    errors, response = client.zosapi_files_write(
        zunix_file_name=zunix_file_name,
        data=data,
        verify=verify,
        etag=etag,
        zunix_file_type=file_type,
        encoding=encoding,
        charset=charset,
    )

    logging.debug("CMD-FILES-000D files write returned with:")
    logging.debug(f"                errors: {errors}")
    logging.debug(f"              response: {response}")

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        sys.stdout.write(f"{response.text}\n")

# ------------------------------------------------------------------------------#
# Define the files create subcommand                                            #
# ------------------------------------------------------------------------------#
@files_cli.command(name="create", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--zunix-file-path",
    "-zp",
    required=True,
    type=click.STRING,
    help="Path to the file to create.",
)
@click.option(
    "--file-type",
    "-ft",
    required=True,
    type=click.Choice(["file", "dir"], case_sensitive=False),
    help="File type, to create.",
)
@click.option(
    "--mode",
    "-m",
    default="rw-rw-rw-",  
    show_default=True,
    help="The file mode to use.",
)
@click.pass_context
def create_file(
    ctx: click.Context,
    zunix_file_path: str,
    file_type: str,
    mode: str,
):
    """
    Create a z/UNIX file or directory.

    \b
    The command will create a file or directory at the specified path. 
    You can specify the file type using --file-type. If you specify file, 
    a file will be created, if you specify dir a directory will be created. 
    You can specify the mode of the file using --mode. The mode should be a 
    string of 9 characters. 
    """
    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-FILES-000D files retrieve entered with:")
    logging.debug(f"              z/Unix file name: {zunix_file_path}")
    logging.debug(f"                     File Type: {file_type}")
    logging.debug(f"                          Mode: {mode}")

    client = f.FILES(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.zosapi_files_create(
        zunix_file_path=zunix_file_path,
        zunix_type=file_type,
        zunix_file_mode=mode,
        verify=verify,
    )

    logging.debug("CMD-FILES-000D files create returned with:")
    logging.debug(f"                errors: {errors}")
    logging.debug(f"              response: {response}")

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        sys.stdout.write(f"{response.text}\n")

# ------------------------------------------------------------------------------#
# Define the files delete subcommand                                            #
# ------------------------------------------------------------------------------#
@files_cli.command(name="delete", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--zunix-file-path",
    "-zp",
    required=True,
    type=click.STRING,
    help="Path to the file or directory to delete.",
)
@click.option(
    "--recursive",
    "-r",
    is_flag=True,
    default=False,
    show_default=True,
    type=click.BOOL,
    help="If True a non empty directory will be deleted, else the directory must be empty.",
)
@click.pass_context
def delete_file(
    ctx: click.Context,
    zunix_file_path: str,
    recursive: bool,
):
    """
    Delete a z/UNIX file or directory.

    \b
    The command will delete a file or directory at the specified path.
    You decide if a non empty directory should be deleted by specifying --recursive.
    """
    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-FILES-000D files retrieve entered with:")
    logging.debug(f"              z/Unix file name: {zunix_file_path}")
    logging.debug(f"                     Recursive: {recursive}")

    client = f.FILES(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.zosapi_files_delete(
        zunix_file_path=zunix_file_path,
        recursive=recursive,
        verify=verify,
    )

    logging.debug("CMD-FILES-000D files delete returned with:")
    logging.debug(f"                errors: {errors}")
    logging.debug(f"              response: {response}")

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        sys.stdout.write(f"{response.text}\n")
        
# ------------------------------------------------------------------------------#
# Define the utilities subgroup of the files group                              #
# ------------------------------------------------------------------------------#
@files_cli.group(
    name="utilities",
    cls=HelpColorsGroup,
    help_headers_color="yellow",
    help_options_color="green",
)
def utilities_cli() -> None:
    """
    z/Unix file utilities.

    \b
    You can use the z/OS UNIX file utilities to operate on a UNIX System Services 
    file or directory. Operations include: chmod, chown, chtag, copy, extattr, 
    getfacl, move, and setfacl.
    """
    pass

