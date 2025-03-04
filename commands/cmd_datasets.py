import sys
import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from zosapi import datasets as d
from commands.cmd_utils import MutuallyExclusiveOption


# ------------------------------------------------------------------------------#
# Define the datasets group                                                     #
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
    Read a member of a PDS or PDS/E or a sequential datasets.

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
    Delete sequential/partitioned z/OS datasets or members.

    \b
    You can use this command to delete a sequential or partitioned
    dataset or delete members on a partitioned dataset. If you would
    like to delete non cataloged datasets or member, you can specify
    a z/OS volume serial.

    \b
    """

    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-DATASETS-000D datasets delete entered with:")
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


# ------------------------------------------------------------------------------#
# Define the instances subgroup of the software group                          #
# ------------------------------------------------------------------------------#
@datasets_cli.group(
    name="utilities",
    cls=HelpColorsGroup,
    help_headers_color="yellow",
    help_options_color="green",
)
def utilities_cli() -> None:
    """
    Copy, rename, hmigrate, hrecall or hdelete z/OS dataset.

    \b
    You can use the z/OS data set and member utilities to work with data sets and members.
    The available commands allow you to, rename members or datasets, copy data set,
    copy member, migrate data set, recall a migrated data set, and delete a backup version
    of a data set.
    """
    pass


# ------------------------------------------------------------------------------#
# Define the datasets utils hrecall                                             #
# ------------------------------------------------------------------------------#
@utilities_cli.command(name="hrecall", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--ds-name",
    "-dn",
    required=True,
    type=click.STRING,
    help="The dataset name of a z/OS PDS or PDS/E or sequential dataset.",
)
@click.option(
    "--wait/--no-wait",
    required=False,
    default=False,
    show_default=True,
    help="If true, the function waits for completion of the request.",
)
@click.pass_context
def hrecall(
    ctx: click.Context,
    ds_name: str,
    wait: bool,
):
    """
    Recall a migrated z/OS Dataset.

    \b
    You can use this command to recall a previously migrated sequential
    or partitioned dataset.
    """

    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-DATASETS-000D datasets hrecall entered with:")
    logging.debug(f"                 Dataset name: {ds_name}")
    logging.debug(f"                 Wait        : {wait}")

    client = d.DATASETS(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.zosapi_datasets_utils(
        ds_name=ds_name,
        to_ds_name="",
        to_member_name="",
        member_name="",
        wait=wait,
        utility_name="hrecall",
        volser="",
        excl=False,
        purge=False,
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
# Define the datasets utils hmigrate                                            #
# ------------------------------------------------------------------------------#
@utilities_cli.command(
    name="hmigrate", cls=HelpColorsCommand, help_options_color="blue"
)
@click.option(
    "--ds-name",
    "-dn",
    required=True,
    type=click.STRING,
    help="The dataset name of a z/OS PDS or PDS/E or sequential dataset.",
)
@click.option(
    "--wait/--no-wait",
    required=False,
    default=False,
    show_default=True,
    help="If true, the function waits for completion of the request.",
)
@click.pass_context
def hmigrate(
    ctx: click.Context,
    ds_name: str,
    wait: bool,
):
    """
    Migrates a z/OS dataset.

    \b
    Migrates a data set to a DFSMShsm level 1 or level 2 volume.
    Performed in the foreground by DFSMShsm.
    """

    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-DATASETS-000D datasets hmigrate entered with:")
    logging.debug(f"                 Dataset name: {ds_name}")
    logging.debug(f"                 Wait        : {wait}")

    client = d.DATASETS(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.zosapi_datasets_utils(
        ds_name=ds_name,
        to_ds_name="",
        to_member_name="",
        utility_name="hmigrate",
        member_name="",
        wait=wait,
        volser="",
        purge=False,
        excl=False,
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
# Define the datasets utils hdelete                                             #
# ------------------------------------------------------------------------------#
@utilities_cli.command(name="hdelete", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--ds-name",
    "-dn",
    required=True,
    type=click.STRING,
    help="The dataset name of a z/OS PDS or PDS/E or sequential dataset.",
)
@click.option(
    "--wait/--no-wait",
    required=False,
    default=False,
    show_default=True,
    help="If true, the function waits for completion of the request.",
)
@click.option(
    "--purge/--no-purge",
    required=False,
    default=False,
    show_default=True,
    help="If False the function uses PURGE=NO on ARCHDEL request.",
)
@click.pass_context
def hdelete(
    ctx: click.Context,
    ds_name: str,
    wait: bool,
    purge: bool,
):
    """
    Delete a migrated z/OS Dataset.

    \b
    Scratches a data set on a DASD migration volume without recalling the data set
    or marks the data set not valid in the TTOC for any tape ML2 volumes that contain
    the data set. DFSMShsm then uncatalogs the data set. DFSMShsm deletes all control data
    set records related to the migration copy. If the data set is migrated to an SDSP, the MCD
    is updated to indicate that the migration copy needs to be scratched. If a discrete RACF
    data set profile exists, DFSMShsm deletes it.
    """

    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-DATASETS-000D datasets hdelete entered with:")
    logging.debug(f"                 Dataset name: {ds_name}")
    logging.debug(f"                 Wait        : {wait}")

    client = d.DATASETS(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.zosapi_datasets_utils(
        ds_name=ds_name,
        to_ds_name="",
        to_member_name="",
        utility_name="hdelete",
        member_name="",
        wait=wait,
        purge=purge,
        volser="",
        excl=False,
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
# Define the datasets read subcommand                                           #
# ------------------------------------------------------------------------------#
@utilities_cli.command(name="rename", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--ds-name",
    "-dn",
    required=True,
    type=click.STRING,
    help="Dataset name.",
)
@click.option(
    "--to-ds-name",
    "-tdn",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["[to_member_name]"],
    default="",
    type=click.STRING,
    help="New dataset name for a Dataset rename.",
)
@click.option(
    "--member-name",
    "-fmn",
    default="",
    type=click.STRING,
    help="Member name on --ds-name.",
)
@click.option(
    "--to-member-name",
    "-tmn",
    default="",
    type=click.STRING,
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["to_ds_name"],
    help="New member name on --ds-name.",
)
@click.option(
    "--enq-exclusive/--no-enq-exclusive",
    default=False,
    show_default=True,
    help="If False a shared enq will be set.",
)
@click.pass_context
def rename(
    ctx: click.Context,
    ds_name: str,
    to_ds_name: str,
    member_name: str,
    to_member_name: str,
    enq_exclusive: bool,
):
    """
    Rename z/OS Datasets or members in a z/OS PDS(E).

    \b
    You can use this command to rename a member of a dataset or a
    sequental dataset.
    """

    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-DATASETS-000D datasets list entered with:")
    logging.debug(f"                  Dataset name: {ds_name}")
    logging.debug(f"                        member: {member_name}")
    logging.debug(f"             exclusive enqueue: {enq_exclusive}")

    client = d.DATASETS(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.zosapi_datasets_utils(
        ds_name=ds_name,
        to_ds_name=to_ds_name,
        member=member_name,
        to_member_name=to_member_name,
        excl=enq_exclusive,
        volser="",
        purge=False,
        wait=False,
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
