import sys
import json
import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from zosapi import filesystems as fs
from commands.cmd_utils import MutuallyExclusiveOption
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

# ------------------------------------------------------------------------------#
# Define the filessystems create subcommand                                     #
# ------------------------------------------------------------------------------#
@filesystems_cli.command(name="create", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--zfs-dataset-name",
    "-zd",
    required=True,
    type=click.STRING,
    help="The zfs dataset name.",
)
@click.option(
    "--owner",
    "-o",
    default="",
    help="Owner User ID of the new zfs.",
)
@click.option(
    "--group",
    "-g",
    default="",
    type=click.STRING,
    help="The group Owner of the new zfs.",
)
@click.option(
    "--storage-class",
    "-sc",
    default="",
    type=click.STRING,
    help="z/OS DFSMS storage class.",
)
@click.option(
    "--management-class",
    "-mc",
    default="",
    type=click.STRING,
    help="z/OS DFSMS management class.",
)
@click.option(
    "--data-class",
    "-dc",
    default="",
    type=click.STRING,
    help="z/OS DFSMS data class.",
)
@click.option(
    "--primary-cylinders",
    "-pc",
    required=True,
    type=click.INT,
    help="Primary space request in cylinders.",
)
@click.option(
    "--secondary-cylinders",
    "-sc",
    required=True,
    type=click.INT,
    help="Secondary space request in cylinders.",
)
@click.option(
    "--volumes",
    "-vol",
    multiple=True,
    type=click.STRING,
    help="Secondary space request in cylinders.",
)
@click.pass_context
def create_filesystem(
    ctx: click.Context,
    zfs_dataset_name: str,
    owner: str,
    group: str,
    storage_class: str,
    management_class: str,
    data_class: str,
    primary_cylinders: int,
    secondary_cylinders: int,
    volumes: list,
):
    """
    Create a zfs z/UNIX filesystem.

    \b
    The command will create a new zfs filesystem. 
    """
    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-FILES-000D filesystems create entered with:")
    logging.debug(f"              z/Unix file name: {zfs_dataset_name}")
    logging.debug(f"                         Owner: {owner}")
    logging.debug(f"                         Group: {group}")
    logging.debug(f"           Primary Space (CYL): {primary_cylinders}")
    logging.debug(f"         Secondary Space (CYL): {secondary_cylinders}")
    logging.debug(f"              Management Class: {management_class}")
    logging.debug(f"                 Storage Class: {storage_class}")
    logging.debug(f"                    Data Class: {data_class}")
    logging.debug(f"                       Volumes: {volumes}")

    client = fs.FILESYSTEMS(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.zosapi_filessystems_create(
        zfs_dataset_name=zfs_dataset_name,
        owner=owner,
        group=group,
        perms="",
        cyls_pri=primary_cylinders,
        cyls_sec=secondary_cylinders,
        storage_class=storage_class,
        management_class=management_class,
        data_class=data_class,
        volumes=volumes,
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
# Define the filessystems delete subcommand                                     #
# ------------------------------------------------------------------------------#
@filesystems_cli.command(name="delete", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--zfs-dataset-name",
    "-zd",
    required=True,
    type=click.STRING,
    help="The zfs dataset name.",
)
@click.pass_context
def delete_filesystem(
    ctx: click.Context,
    zfs_dataset_name: str,
):
    """
    Delete a zfs z/UNIX filesystem.

    \b
    The command will delete a zfs filesystem. 
    """
    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-FILES-000D filessystems delete entered with:")
    logging.debug(f"              z/Unix file name: {zfs_dataset_name}")

    client = fs.FILESYSTEMS(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.zosapi_filessystems_delete(
        zfs_dataset_name=zfs_dataset_name,
        verify=verify,
    )

    logging.debug("CMD-FILES-000D files delete returned with:")
    logging.debug(f"                errors: {errors}")
    logging.debug(f"              response: {response}")

    if errors:
        response_dict = json.loads(response.text)
        sys.stderr.write(f"{response_dict["message"]}\n")
        for utility_details in response_dict["details"]:
            details = utility_details.split("\n")
            for detail in details:
                sys.stderr.write(f"{detail}\n")
    else:
        sys.stdout.write(f"{response.text}\n")

# ------------------------------------------------------------------------------#
# Define the filessystems mount subcommand                                      #
# ------------------------------------------------------------------------------#
@filesystems_cli.command(name="mount", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--fs-dataset-name",
    "-fn",
    required=True,
    type=click.STRING,
    help="The zfs dataset name.",
)
@click.option(
    "--fs-type",
    "-ft",
    default="zfs",
    show_default=True,
    type=click.STRING,
    help="The file system type.",
)
@click.option(
    "--mount-point",
    "-mp",
    required=True,
    type=click.STRING,
    help="The mount point.",
)
@click.option(
    "--mode",
    "-m",
    default="rdonly",
    show_default=True,
    type=click.STRING,
    help="Mode of mount operation.",
)
@click.option(
    "--setuid/--no-setuid",
    default=False,
    show_default=True,
    type=click.BOOL,
    help="If true uses the setuid option in the mount mode.",
)
@click.pass_context
def file_system_mount(
    ctx: click.Context,
    fs_dataset_name: str,
    fs_type: str,
    mount_point: str,
    mode: str,
    setuid: bool,
):
    """
    Mount a z/UNIX filesystem.

    \b
    You can use this command to mount a z/OS UNIX file system on a specified directory. 
    """
    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-FILES-000D filessystems mount entered with:")
    logging.debug(f"              File system name: {fs_dataset_name}")
    logging.debug(f"                   Mount point: {mount_point}")
    logging.debug(f"                    Mount mode: {mode}")
    logging.debug(f"                        Setuid: {setuid}")

    client = fs.FILESYSTEMS(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.zosapi_filessystems_mount_unmount(
        file_system_name=fs_dataset_name,
        action_unmount=False,
        mount_point=mount_point,
        fs_type=fs_type,
        mode=mode,
        setuid=setuid,
        verify=verify,
    )

    logging.debug("CMD-FILES-000D files mount returned with:")
    logging.debug(f"                errors: {errors}")
    logging.debug(f"              response: {response}")

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
        sys.stdout.write(f"{response.text}\n")
    else:
        sys.stdout.write(f"{response.text}\n")

# ------------------------------------------------------------------------------#
# Define the filessystems unmount subcommand                                    #
# ------------------------------------------------------------------------------#
@filesystems_cli.command(name="unmount", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--fs-dataset-name",
    "-fn",
    required=True,
    type=click.STRING,
    help="The zfs dataset name.",
)
@click.pass_context
def file_system_unmount(
    ctx: click.Context,
    fs_dataset_name: str,
):
    """
    Unmount a z/UNIX filesystem.

    \b
    You can use this command to unmount a z/OS UNIX file system. 
    """
    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-FILES-000D filessystems unmount entered with:")
    logging.debug(f"              File system name: {fs_dataset_name}")

    client = fs.FILESYSTEMS(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.zosapi_filessystems_mount_unmount(
        fs_dataset_name=fs_dataset_name,
        action_unmount=True,
        mount_point=None,
        fs_type=None,
        verify=verify,
    )

    logging.debug("CMD-FILES-000D files unmount returned with:")
    logging.debug(f"                errors: {errors}")
    logging.debug(f"              response: {response}")

    if errors:
        response_dict = json.loads(response.text)
        sys.stderr.write(f"{response_dict["message"]}\n")
        for utility_details in response_dict["details"]:
            details = utility_details.split("\n")
            for detail in details:
                sys.stderr.write(f"{detail}\n")
    else:
        sys.stdout.write(f"{response.text}\n")
        
# ------------------------------------------------------------------------------#
# Define the filessystems list subcommand                                       #
# ------------------------------------------------------------------------------#
@filesystems_cli.command(name="list", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--fs-dataset-name",
    "-fn",
    type=click.STRING,
    default="",
    show_default=True,
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["[path]"],
    help="The zfs dataset name.",
)
@click.option(
    "--path",
    "-p",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["[fs-dataset-name]"],
    default="",
    show_default=True,
    type=click.STRING,
    help="New dataset name for a Dataset rename.",
)
@click.pass_context
def file_system_list(
    ctx: click.Context,
    fs_dataset_name: str,
    path: str,
):
    """
    List z/UNIX filesystem(s).

    \b
    You can use the list z/OS UNIX filesystems command to list all mounted filesystems, or the 
    specific filesystem mounted at a given path, or the filesystem with a given Filesystem name.
    If no options are provided, the command will list all mounted filesystems.
    """
    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-FILES-000D filessystems list entered with:")
    logging.debug(f"              File system name: {fs_dataset_name}")
    logging.debug(f"                          Path: {path}")

    client = fs.FILESYSTEMS(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.zosapi_filessystems_list(
        file_system_name=fs_dataset_name,
        path_name=path,
        verify=verify,
    )

    logging.debug("CMD-FILES-000D files list returned with:")
    logging.debug(f"                errors: {errors}")
    logging.debug(f"              response: {response}")

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
        sys.stdout.write(f"{response.text}\n")
    else:
        sys.stdout.write(f"{response.text}\n")
