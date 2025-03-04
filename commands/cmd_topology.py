import click
import sys
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from zosapi import topology as tp


# ------------------------------------------------------------------------------#
# Define the topology group                                                      #
# ------------------------------------------------------------------------------#
@click.group(
    name="topology",
    cls=HelpColorsGroup,
    help_headers_color="yellow",
    help_options_color="green",
)
def topology_cli() -> None:
    """
    Provides commands for working with the groups, sysplexes,
    central processor complexes (CPCs), and systems that are
    defined to z/OSMF

    \b
    Author.......: Ronny Funk
    Function.....: Query z/OS z/OSMF Toplogy Services

    Environment: z/Unix Terminal CLI / Batch Job
    """
    pass


# ------------------------------------------------------------------------------#
# Define the topology list groups command                                      #
# ------------------------------------------------------------------------------#
@topology_cli.command(name="groups", cls=HelpColorsCommand, help_options_color="blue")
@click.pass_context
def groups(ctx: click.Context):
    """
    List z/OSMF defined groups.
    \b
    You can use this operation to obtain a list
    of the groups that are defined to a z/OSMF
    instance.
    """
    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-TOPOLOGY-000D groups() entered with (None):")

    client = tp.TOPOLOGY(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )

    errors, response = client.get_topology_service(service="groups", verify=verify)

    logging.debug("CMD-TOPOLOGY-000D groups() returned with:")
    logging.debug(f"                    response: {response}")
    logging.debug(f"                      errors: {errors}")

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        sys.stdout.write(f"{response.text}\n")

# ------------------------------------------------------------------------------#
# Define the topology list sysplex command                                      #
# ------------------------------------------------------------------------------#
@topology_cli.command(name="sysplex", cls=HelpColorsCommand, help_options_color="blue")
@click.pass_context
def sysplex(ctx: click.Context):
    """
    List z/OSMF defined sysplexes.
    \b
    You can use this operation to obtain a list
    of the sysplexes that are defined to a
    z/OSMF instance.
    """

    verify = ctx.obj["VERIFY"]

    client = tp.TOPOLOGY(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.get_topology_service(service="sysplexes", verify=verify)
    if errors:
        sys.stderr.write(str(errors))
    else:
        sys.stdout.write(f"{response.text}\n")


# ------------------------------------------------------------------------------#
# Define the topology systems group                                            #
# ------------------------------------------------------------------------------#
@topology_cli.group(
    name="systems",
    cls=HelpColorsGroup,
    help_headers_color="yellow",
    help_options_color="green",
)
def systems_cli() -> None:
    """
    You can use this operations to obtain a list of the systems
    that are defined to a z/OSMF instance, systems by z/OSMF group
    or by z/OSMF defined sysplexes.

    \b
    Module Name.:  commands.cmd_topology.py
    Alias........: None
    Author.......: Ronny Funk
    Function.....: Query z/OS z/OSMF Toplogy Services

    Environment: z/Unix Terminal CLI / Batch Job
    """


# ------------------------------------------------------------------------------#
# Define the topology list subcommand of the topology systems group            #
# ------------------------------------------------------------------------------#
@systems_cli.command(name="list", cls=HelpColorsCommand, help_options_color="blue")
@click.pass_context
def list(ctx: click.Context):
    """
    List all z/OSMF defined systems.
    \b
    You can use this operation to obtain a list
    of the systems that are defined to a z/OSMF
    instance.
    """

    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    client = tp.TOPOLOGY(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.get_topology_service(service="systems", verify=verify)

    logging.debug("CMD-TOPOLOGY-000D list() returned with:")
    logging.debug(f"                    response: {response}")
    logging.debug(f"                      errors: {errors}")

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        sys.stdout.write(f"{response.text}\n")
    pass


# ------------------------------------------------------------------------------#
# Define the topology list systems contained in a group                        #
# ------------------------------------------------------------------------------#
@systems_cli.command(name="in-group", cls=HelpColorsCommand, help_options_color="blue")
@click.option("--name", "-n", type=click.STRING, required=True, help="The z/OSMF group name.")
@click.pass_context
def systems_in_group(ctx: click.Context, name: str, verify: bool = True):
    """
    List systems defined in a z/OSMF group.
    \b
    You can use this operation to obtain a list of the systems that
    are included in a group.
    """

    verify = ctx.obj["VERIFY"]

    client = tp.TOPOLOGY(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
    )
    errors, response = client.get_group_systems(group=name, verify=verify)
    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        sys.stdout.write(response.text)


@systems_cli.command(
    name="in-sysplex", cls=HelpColorsCommand, help_options_color="blue"
)
@click.option("--name", "-n", type=click.STRING, required=True, help="The z/OS sysplex name.")
@click.pass_context
def systems_in_sysplex(ctx: click.Context, name: str, verify: bool = True):
    """
    List systems defined in a z/OS parallel sysplex.
    \b
    You can use this operation to obtain a list of the systems that
    are included in a z/OS parallel sysplex.
    """

    verify = ctx.obj["VERIFY"]

    client = tp.TOPOLOGY(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.get_group_systems(group=name, verify=verify)
    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        sys.stdout.write(f"{response.text}\n")


@topology_cli.group(
    name="validate",
    cls=HelpColorsGroup,
    help_headers_color="yellow",
    help_options_color="green",
)
def validate_cli() -> None:
    """
    Validate Connection status of z/OS system(s)/plexes
    \b
    Author.......: Ronny Funk
    Function.....: Query z/OS z/OSMF Toplogy Services

    Environment: z/Unix Terminal CLI / Batch Job
    """
    pass


@validate_cli.command(name="system", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--name", "-n", type=click.STRING, default="", help="Name of z/OS system to validate."
)
@click.pass_context
def system(ctx: click.Context, name: str, verify: bool = True):
    """
    Check z/OS system connection status.

    \b
    You can use this operation to check the connection status of a
    specified system which is managed through the z/OSMF Systems task.
    If no system is provided, then validate LocalSystemDefinition.
    """

    verify = ctx.obj["VERIFY"]

    client = tp.TOPOLOGY(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )

    errors, response = client.validate_system(system=name, verify=verify)

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        sys.stdout.write(f"{response.text}\n")


@validate_cli.command(name="plex", cls=HelpColorsCommand, help_options_color="blue")
@click.pass_context
def plex(ctx: click.Context, verify: bool = True):
    """
    Check z/OS plex systems connection status.

    \b
    You can use this operation to obtain a list of the systems
    that are defined to a z/OSMF instance and validate them.
    """

    verify = ctx.obj["VERIFY"]

    client = tp.TOPOLOGY(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )

    errors, response = client.validate_plex(verify=verify)

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        sys.stdout.write(f"{response.text}\n")
