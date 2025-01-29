import sys
import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from zosapi import datasets as d


# ------------------------------------------------------------------------------#
# Define the software group                                                     #
# ------------------------------------------------------------------------------#
@click.group(
    name="datasets",
    cls=HelpColorsGroup,
    help_headers_color="yellow",
    help_options_color="green",
)
def datasets_cli() -> None:
    """
    Interact with z/OS datasets.

    \b
    Module Name.:  commands.cmd_datasets.py
    Alias........: None
    Author.......: Ronny Funk
    Function.....: Work with z/OS Datasets

    Environment: *ix Terminal CLI / Batch Job
    """
    pass


# ------------------------------------------------------------------------------#
# Define the datasets list subcommand                                           #
# ------------------------------------------------------------------------------#
@datasets_cli.command(name="list", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--dsn-level",
    "-dl",
    default="",
    type=click.STRING,
    help="A dataset level to list. DEFAULT <USERID>.**",
)
@click.option(
    "--volser", "-v", default="", type=click.STRING, help="A volume serial number."
)
@click.option(
    "--start", "-s", default="", type=click.STRING, help="A dataset level to list."
)
@click.pass_context
def list(ctx: click.Context, dsn_level: str, volser: str, start: str):
    """
    List z/OS datasets.

    \b
    You can use this command to obtain a list of z/OS datasets.
    You can search the z/OS catalog or a z/OS volume serial for
    matching datasets.
    """

    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-DATASETS-000D datasets list entered with:")
    logging.debug(f"                   DSN Level: {dsn_level}")
    logging.debug(f"                      volser: {volser}")
    logging.debug(f"                       start: {start}")

    if dsn_level == "":
        dsn_level = f"{ctx.obj['USER'].upper()}.**"

    client = d.DATASETS(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.zosapi_datasets_list(
        dsn_level=dsn_level, volser=volser, start=start, verify=verify
    )

    logging.debug("CMD-DATASETS-000D dataset list returned with:")
    logging.debug(f"                errors: {errors}")
    logging.debug(f"              response: {response}")

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        sys.stdout.write(f"{response.text}\n")


# ------------------------------------------------------------------------------#
# Define the datasets members subcommand                                        #
# ------------------------------------------------------------------------------#
@datasets_cli.command(name="members", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--ds-name",
    "-dn",
    required=True,
    type=click.STRING,
    help="The dataset name of a z/OS PDS or PDS/E.",
)
@click.option(
    "--pattern",
    "-p",
    default="",
    type=click.STRING,
    help="A search pattern following the ISPF LMMLIST.",
)
@click.pass_context
def members(ctx: click.Context, ds_name: str, pattern: str):
    """
    List members of z/OS partitioned datasets (PDS and PDS/E).

    \b
    You can use this command to obtain a list of members of z/OS
    partioned datasets.
    """
    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-DATASETS-000D datasets list entered with:")
    logging.debug(f"                Dataset name: {ds_name}")
    logging.debug(f"                     pattern: {pattern}")

    client = d.DATASETS(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.zosapi_datasets_members_list(
        dataset_name=ds_name, pattern=pattern, verify=verify
    )

    logging.debug("CMD-DATASETS-000D dataset list returned with:")
    logging.debug(f"                errors: {errors}")
    logging.debug(f"              response: {response}")

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        sys.stdout.write(f"{response.text}\n")


# ------------------------------------------------------------------------------#
# Define the datasets read subcommand                                           #
# ------------------------------------------------------------------------------#
@datasets_cli.command(name="read", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--ds-name",
    "-dn",
    required=True,
    type=click.STRING,
    help="The dataset name of a z/OS PDS or PDS/E or sequential dataset.",
)
@click.option(
    "--member-name",
    "-mn",
    default="",
    type=click.STRING,
    help="A member name if --ds-name is a PDS or PDS/E.",
)
@click.option(
    "--volser",
    "-v",
    default="",
    type=click.STRING,
    help="A volume serial number if --ds-name is not cataloged.",
)
@click.option(
    "--encoding", "-e", default="", type=click.STRING, help="Encoding of the data."
)
@click.option(
    "--enq-exclusive",
    "-exc",
    is_flag=True,
    default=False,
    type=click.STRING,
    help="If True an exclusive enq will be set, otherwise a share enqueuei.",
)
@click.pass_context
def read(
    ctx: click.Context,
    ds_name: str,
    member_name: str,
    volser: str,
    enq_exclusive: bool,
    encoding: str,
):
    """
    Read a member of a PDS or PDS/E or a sequential dataset.

    \b
    You can use this command to read a member of a dataset or a
    sequental dataset. If the dataset is not cataloged specify a
    volume serial number to read the member or the dataset directly
    from the volume.
    """

    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-DATASETS-000D datasets list entered with:")
    logging.debug(f"                  Dataset name: {ds_name}")
    logging.debug(f"                        member: {member_name}")
    logging.debug(f"                        volser: {volser}")
    logging.debug(f"             exclusive enqueue: {enq_exclusive}")

    client = d.DATASETS(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.zosapi_datasets_read(
        dataset_name=ds_name,
        member=member_name,
        volser=volser,
        encoding=encoding,
        verify=verify,
    )

    logging.debug("CMD-DATASETS-000D dataset list returned with:")
    logging.debug(f"                errors: {errors}")
    logging.debug(f"              response: {response}")

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        sys.stdout.write(f"{response.text}\n")
        sys.stdout.write(f"{response.headers}\n")


# ------------------------------------------------------------------------------#
# Define the datasets create subcommand                                         #
# ------------------------------------------------------------------------------#
@datasets_cli.command(name="create", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--ds-name",
    "-dn",
    required=True,
    type=click.STRING,
    help="The dataset name of a z/OS PDS or PDS/E or sequential dataset.",
)
@click.option(
    "--volser",
    "-v",
    default="",
    type=click.STRING,
    help="A volume serial number.",
)
@click.option(
    "--unit",
    "-u",
    default="",
    type=click.STRING,
    help="z/OS Device type.",
)
@click.option(
    "--dsorg",
    "-do",
    default="PS",
    type=click.STRING,
    show_default=True,
    help="Data set organization (PS/PO).",
)
@click.option(
    "--alcunit",
    "-au",
    default="TRK",
    type=click.STRING,
    show_default=True,
    help="Unit of space allocation (TRK/CYL/M/G).",
)
@click.option(
    "--primary",
    "-p",
    default=10,
    type=click.INT,
    show_default=True,
    help="Primary space allocation.",
)
@click.option(
    "--secondary",
    "-s",
    default=5,
    type=click.INT,
    show_default=True,
    help="Secondary space allocation.",
)
@click.option(
    "--dirblk",
    "-d",
    default=5,
    type=click.INT,
    show_default=True,
    help="Number of directory blocks.",
)
@click.option(
    "--avgblk",
    "-a",
    type=click.INT,
    help="Average block size.",
)
@click.option(
    "--recfm",
    "-r",
    default="FB",
    type=click.STRING,
    show_default=True,
    help="Record format.",
)
@click.option(
    "--blksize",
    "-bs",
    default=0,
    type=click.INT,
    show_default=True,
    help="Block size.",
)
@click.option(
    "--lrecl",
    "-l",
    default=80,
    type=click.INT,
    show_default=True,
    help="Record length.",
)
@click.option(
    "--storclass",
    "-sc",
    default="",
    type=click.STRING,
    help="Storage class.",
)
@click.option(
    "--mgntclass",
    "-mc",
    default="",
    type=click.STRING,
    help="Management class.",
)
@click.option(
    "--dataclass",
    "-dc",
    default="",
    type=click.STRING,
    help="Data class.",
)
@click.option(
    "--dsn-type",
    "-dt",
    default="",
    type=click.STRING,
    help="Data set type.",
)
@click.option(
    "--like",
    "-l",
    default="",
    type=click.STRING,
    help="Model data set name.",
)
@click.pass_context
def create(
    ctx: click.Context,
    ds_name: str,
    volser: str,
    unit: str,
    dsorg: str,
    alcunit: str,
    primary: int,
    secondary: int,
    avgblk: int,
    recfm: str,
    blksize: int,
    lrecl: int,
    storclass: str,
    mgntclass: str,
    dataclass: str,
    dsn_type: str,
    like: str,
):
    """
    Create sequential and partitioned data sets on a z/OS system.

    \b
    You can use this command to create a sequential or partitioned
    dataset.
    """

    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-DATASETS-000D datasets create entered with:")
    logging.debug(f"                 Dataset name: {ds_name}")
    logging.debug(f"                 unit        : {unit}")
    logging.debug(f"                 volser      : {volser}")
    logging.debug(f"                 dsorg       : {dsorg}")
    logging.debug(f"                 alcunit     : {alcunit}")
    logging.debug(f"                 primary     : {primary}")
    logging.debug(f"                 secondary   : {secondary}")
    logging.debug(f"                 avgblock    : {avgblk}")
    logging.debug(f"                 recfm       : {recfm}")
    logging.debug(f"                 blksize     : {blksize}")
    logging.debug(f"                 lrelc       : {lrecl}")
    logging.debug(f"                 storclass   : {storclass}")
    logging.debug(f"                 mgntclass   : {mgntclass}")
    logging.debug(f"                 dataclass   : {dataclass}")
    logging.debug(f"                 dsntype     : {dsn_type}")
    logging.debug(f"                 like        : {like}")

    client = d.DATASETS(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.zosapi_datasets_create(
        ds_name=ds_name,
        volser=volser,
        unit=unit,
        dsorg=dsorg,
        alcunit=alcunit,
        primary=primary,
        secondary=secondary,
        avgblk=avgblk,
        recfm=recfm,
        blksize=blksize,
        lrecl=lrecl,
        storclass=storclass,
        mgntclass=mgntclass,
        dataclass=dataclass,
        dsntype=dsn_type,
        like=like,
        verify=verify,
    )

    logging.debug("CMD-DATASETS-000D dataset list returned with:")
    logging.debug(f"                 errors  : {errors}")
    logging.debug(f"                 response: {response}")

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        sys.stdout.write(f"{response.text}\n")


# ------------------------------------------------------------------------------#
# Define the datasets delete subcommand                                         #
# ------------------------------------------------------------------------------#
@datasets_cli.command(name="delete", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--ds-name",
    "-dn",
    required=True,
    type=click.STRING,
    help="The dataset name of a z/OS PDS or PDS/E or sequential dataset.",
)
@click.option(
    "--member-name",
    "-mn",
    default="",
    type=click.STRING,
    help="Dataset member to delete.",
)
@click.option(
    "--volser",
    "-v",
    default="",
    type=click.STRING,
    help="A volume serial number.",
)
@click.pass_context
def delete(
    ctx: click.Context,
    ds_name: str,
    member_name: str,
    volser: str,
):
    """
    Delete a sequential or partitioned data sets on a z/OS system.

    \b
    You can use this command to delete a sequential or partitioned
    dataset or a member of a partitioned dataset.
    """

    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-DATASETS-000D datasets create entered with:")
    logging.debug(f"                 Dataset name: {ds_name}")
    logging.debug(f"                 Member name : {member_name}")
    logging.debug(f"                 volser      : {volser}")

    client = d.DATASETS(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.zosapi_datasets_delete(
        ds_name=ds_name,
        member_name=member_name,
        volser=volser,
        verify=verify,
    )

    logging.debug("CMD-DATASETS-000D dataset list returned with:")
    logging.debug(f"                 errors  : {errors}")
    logging.debug(f"                 response: {response}")

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        sys.stdout.write(f"{response.text}\n")
