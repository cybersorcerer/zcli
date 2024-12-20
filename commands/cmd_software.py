import sys
import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand

from tui.software import tui_sms_crit_updates
from tui.software import tui_sms_fixc_updates
from tui.software import tui_sms_soft_updates
from tui.software import tui_sms_list

from commands.cmd_utils import MutuallyExclusiveOption
from commands.cmd_defaults import HOST_NAME, GLOBAL_CSI
from zosapi import software as s

#------------------------------------------------------------------------------#
# Define the software group                                                    #
#------------------------------------------------------------------------------#
@click.group(
    name='software',
    cls=HelpColorsGroup,
    help_headers_color='yellow',
    help_options_color='green',
)
def software_cli() -> None:
    """
    Interact with the z/OSMF Software Management task.

    \b
    Module Name.:  commands.cmd_software.py
    Alias........: None
    Author.......: Ronny Funk
    Function.....: Work with the z/OSMF software management task

    Environment: *ix Terminal CLI / Batch Job
    """
    pass

#------------------------------------------------------------------------------#
# Define the query subgroup of the software group                              #
#------------------------------------------------------------------------------#
@software_cli.group(
    name='query',
    cls=HelpColorsGroup,
    help_headers_color='yellow',
    help_options_color='green',
)
def query_cli() -> None:
    """
    Query z/OS SMP/E.

    \b
    The SMP/E CSI Query service allows you to query entries defined
    in SMP/E CSI data sets. You can query SMP/E CSI data sets directly,
    or those associated with software instances. Refer to SMP/E CSI
    application programming interface in z/OS SMP/E Reference
    for more information.
    """
    pass

#------------------------------------------------------------------------------#
# Define the csids subcommand command of the query subgroup                    #
#------------------------------------------------------------------------------#
@query_cli.command(
    name='csids',
    cls=HelpColorsCommand,
    help_options_color='blue'
)
@click.option(
    '--global-csi',
    '-gc',
    type=str,
    required=True,
    default=GLOBAL_CSI,
    help=f'The name of the SMP/E Global CSI. Default is {GLOBAL_CSI}'
)
@click.option(
    '--zones',
    '-z',
    type=str,
    default='GLOBAL',
    help='One or more SMP/E Zone names, separated by comma.'
)
@click.option(
    '--entry',
    '-e',
    type=str,
    default='',
    help='SMP/E entry type (sysmod, dddef etc).'
)
@click.option(
    '--subentries',
    '-se',
    type=str,
    default='',
    help='Blank separated string of subentries.'
)
@click.option(
    '--filter',
    '-fi',
    type=str,
    default='',
    help='Some filter criteria for the query.'
)
@click.pass_context
def csids(ctx: click.Context, global_csi: str, zones: str, entry: str, subentries: str, filter: str):
    """
    Query SMP/E CSI data sets.

    \b
    SMP/E CSI Query action is to be performed on the identified
    global zone CSI data set. Use this Command form to query
    a global zone CSI data set when it is not associated with a
    defined software instance object.
    \b
    Note:
    \b
    If you are uncertain about how to use csids, refer to
    z/OS SMP/E Reference Section GIMAPI!
    \b
    zones:
    \b
    The list of zones to be queried. You may provide one or more
    specific zone names, or any of these values:
    \b
        - GLOBAL
        - ALLTZONES
        - ALLDZONES
        - *
    \b
    entries:
    \b
    The list of entry types to be queried. You may provide one or more
    entry types, or asterisk (“*”) can be used to indicate all entry types
    will be queried.
    \b
    subentries:
    \b
    The list of subentry types to be returned. You may provide one or more
    subentry types, or asterisk (“*”) can be used to indicate all subentry
    types will be returned. This is an optional property. If no subentries
    are provided, then only the entry name and zone will be returned.
    \b
    filter:
    \b
    The list of conditions with which to limit the entries to be returned
    """

    user = ctx.obj['USER']
    password = ctx.obj['PASSWORD']
    verify = ctx.obj['VERIFY']
    logging = ctx.obj['LOGGING']

    client = s.SMS(HOST_NAME, user, password)
    errors, response = client.csiquery(
        global_name=global_csi,
        zones=zones,
        entries=entry,
        subentries=subentries,
        filter=filter,
        verify=verify
    )
    if errors:
        sys.stderr.write(f'{str(errors)}\n')
    else:
        sys.stdout.write(f'{response.text}\n')

#------------------------------------------------------------------------------#
# Define criticalupdates command of the query subgroup of software group       #
#------------------------------------------------------------------------------#
@query_cli.command(
    name='critupdates',
    cls=HelpColorsCommand,
    help_options_color='blue'
)
@click.option(
    '--nick-name',
    '-nn',
    type=str,
    default='',
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["uuid"],
    help='The system nick name of the software instance.'
)
@click.option(
    '--swi-name',
    '-sn',
    type=str,
    default='',
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["uuid"],
    help='The name of the software instance.'
)
@click.option(
    '--uuid',
    '-u',
    type=str,
    default='',
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["swi_name", "nick_name"],
    help='The uuid representing the software instance.'
)
@click.option(
    '--tui/ --no-tui',
    required=False,
    default=False,
    show_default=True,
    help='Display response data in a table.'
)
@click.pass_context
def critical_updates(ctx: click.Context, nick_name: str, swi_name: str, uuid: str, tui: bool):
    """
    Get information about Missing Critical Updates.

    \b
    The Missing Critical Updates command helps you determine if your software
    instances are missing software updates to resolve PE PTFs, HIPER fixes, or
    other exception SYSMODs identified by ERROR HOLDDATA, and helps you identify
    the SYSMODs that resolve those exceptions.
    \b
    To define for which instances you would like to retrieve missing critical updates, specify:
    \b
        - The system nick name AND the software instance name
                        OR
        - The software instance uuid
    \b
    NOTE:
    \b
    This command might take a considerable amount of time to complete, so be patient :-)
    """
    user = ctx.obj['USER']
    password = ctx.obj['PASSWORD']
    verify = ctx.obj['VERIFY']
    logging = ctx.obj['LOGGING']

    client = s.SMS(HOST_NAME, user, password)
    errors, response = client.missing_critical_updates(nickname=nick_name, instance=swi_name, uuid=uuid, verify=verify)
    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        if not tui:
           sys.stdout.write(f'{response.text}\n')
        else:
           tui_sms_crit_updates.show_tui(response.text)

#------------------------------------------------------------------------------#
# Define software updates command of the query subgroup of software group      #
#------------------------------------------------------------------------------#
@query_cli.command(
    name='softupdates',
    cls=HelpColorsCommand,
    help_options_color='blue'
)
@click.option(
    '--nick-name',
    '-nn',
    type=str,
    default='',
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["uuid"],
    help='The system nick name of the software instance.'
)
@click.option(
    '--swi-name',
    '-sn',
    type=str,
    default='',
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["uuid"],
    help='The name of the software instance.'
)
@click.option(
    '--uuid',
    '-u',
    type=str,
    default='',
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["swi_name", "nick_name"],
    help='The uuid representing the software instance.'
)
@click.argument(
    'sysmods',
    nargs=-1,
    required=True
)
@click.option(
    '--tui/ --no-tui',
    required=False,
    default=False,
    show_default=True,
    help='Display response data in a table.'
)
@click.pass_context
def software_updates(ctx: click.Context, nick_name: str, swi_name: str, uuid: str, sysmods: tuple[str, ...], tui: bool):
    """
    Search Software updates.

    \b
    The Software Update Search command allows you to search a software instance
    for one or more software updates. This is helpful when you need to complete
    a task that requires you to determine if a software instance needs to be updated.
    \b
    To define for which instances you would like to search updates for, specify:
    \b
        - The system nick name AND the software instance name
                        OR
        - The software instance uuid
    \b
    ./zcli software query softupdates -nn <nickname> -sn <instance> SYSMODS
                        OR
    ./zcli software query softupdates -u <uuid> SYSMODS
    \b
    NOTE:
    \b
    This command might take a considerable amount of time to complete, so be patient :-)
    """
    user = ctx.obj['USER']
    password = ctx.obj['PASSWORD']
    verify = ctx.obj['VERIFY']
    logging = ctx.obj['LOGGING']

    client = s.SMS(HOST_NAME, user, password)
    errors, response = client.search_software_updates(
        nickname=nick_name,
        instance=swi_name,
        uuid=uuid,
        sysmods=sysmods,
        verify=verify
    )
    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        if not tui:
           sys.stdout.write(f'{response.text}\n')
        else:
           tui_sms_soft_updates.show_tui(response.text)

#------------------------------------------------------------------------------#
# Define fixcatupdates command of the query subgroup of software group         #
#------------------------------------------------------------------------------#
@query_cli.command(
    name='fixcatupdates',
    cls=HelpColorsCommand,
    help_options_color='blue'
)
@click.option(
    '--nick-name',
    '-nn',
    type=str,
    default='',
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["uuid"],
    help='The system nick name of the software instance.'
)
@click.option(
    '--swi-name',
    '-sn',
    type=str,
    default='',
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["uuid"],
    help='The name of the software instance.'
)
@click.option(
    '--uuid',
    '-u',
    type=str,
    default='',
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["swi_name", "nick_name"],
    help='The uuid representing the software instance.'
)
@click.option(
    '--tui/ --no-tui',
    required=False,
    default=False,
    show_default=True,
    help='Display response data in a table.'
)
@click.pass_context
def fixcat_updates(ctx: click.Context, nick_name: str, swi_name: str, uuid: str, tui: bool):
    """
    Get information about missing FIXCAT Updates.

    \b
    The Missing FIXCAT Updates command helps you identify missing updates for fix categories
    that might be applicable to the software instance, and it identifies the SYSMODS that
    can resolve the missing updates.
    \b
    To specifiy for which instances you would like to retrieve missing FIXCAT updates, specify:
    \b
        - The system nick name AND the software instance name
                        OR
        - The software instance uuid
    \b
    NOTE:
    \b
    This command might take a considerable amount of time to complete, so be patient :-)
    """
    user = ctx.obj['USER']
    password = ctx.obj['PASSWORD']
    verify = ctx.obj['VERIFY']
    logging = ctx.obj['LOGGING']

    client = s.SMS(HOST_NAME, user, password)
    errors, response = client.missing_fixcat_updates(nickname=nick_name, instance=swi_name, uuid=uuid, verify=verify)
    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        if not tui:
           sys.stdout.write(f'{response.text}\n')
        else:
           tui_sms_fixc_updates.show_tui(response.text)

#------------------------------------------------------------------------------#
# Define the instances subgroup of the software group                          #
#------------------------------------------------------------------------------#
@software_cli.group(
    name='instances',
    cls=HelpColorsGroup,
    help_headers_color='yellow',
    help_options_color='green',
)
def instances_cli() -> None:
    """
    Work with software instances.

    \b
    Allows you to:
    \b
    - List software instances,
    - Retrieve their properties,
    - List the datasets included in a software instance,
    - Add a new software instance
    - Export a defined software instance
    - Modify the properties of a software instance (not yet implemented)
    - Load products, features and FMIDs for a software instance (not yet implemented)
    - Delete a software instance
    - Delete the temporary catalog alias (not yet implemented)
    - List portable software instances
    - Deploy a software instance (not yet implemented)
    - Delete a deployment (not yet implemented)
    - Retrieve the properties of a protable software instance (not yet implemented)
    - Add a new portable software instance (not yet implemented)
    - Export a defined portable software instance (not yet implemented)
    - Delete a portable software instance (not yet implemented)
    - Retrieve the z/OS system UUID
    """
    pass

#------------------------------------------------------------------------------#
# Define the uuid subcommand of the instances subgroup                         #
#------------------------------------------------------------------------------#
@instances_cli.command(
    name='uuid',
    cls=HelpColorsCommand,
    help_options_color='blue'
)
@click.option(
    '--nick-name',
    '-nn',
    required=True,
    type=click.STRING,
    help='The system nick name'
)
@click.pass_context
def uuid(ctx: click.Context, nick_name: str):
    """
    Retrieve the z/OS system UUID.

    \b
    You can use this command to retrieve the UUID for the software instance that represents
    the installed software for the specified z/OSMF host system.
    \b
    A UUID (Universal Unique Identifier) is a 128-bit value that is used to uniquely identify
    an object. UUIDs are represented with 32 hexadecimal characters, 0 - 9 and A - F, with four hyphens,
    in this form: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.
    For example, “bbc9e8d6-bd61-4f11-af48-ff500fffc178”.
    \b
    The UUID for the z/OS software instance is defined in module IZUSIUI in LPALIB. This module
    is created by z/OSMF during the installation or subsequent deployment of z/OS. The UUID can
    be discovered by this REST API, and then used by other z/OSMF Software Management REST APIs
    to perform actions on the software instance.
    The UUID can also be displayed by using the "D IPLINFO" MVS system command.
    """

    user = ctx.obj['USER']
    password = ctx.obj['PASSWORD']
    verify = ctx.obj['VERIFY']
    logging = ctx.obj['LOGGING']

    client = s.SMS(HOST_NAME, user, password)
    errors, response = client.get_system_uuid(
        nickname=nick_name,
        verify=verify
    )

    if errors:
        sys.stderr.write(f'{str(errors)}\n')
    else:
        sys.stdout.write(f'{response.text}\n')


#------------------------------------------------------------------------------#
# Define the list software instances command of the instances group            #
#------------------------------------------------------------------------------#
@instances_cli.command(
    name='list',
    cls=HelpColorsCommand,
    help_options_color='blue'
)
@click.option(
    '--pswi / --no-pswi',
    default=False,
    show_default=True,
    help='List software or portable software instances.'
)
@click.option(
    '--tui/ --no-tui',
    required=False,
    default=False,
    show_default=True,
    help='Display response data in a table.'
)
@click.pass_context
def list(ctx: click.Context, pswi: bool = False, tui: bool = False):
    """
    Obtain a list of software or portable software instances.

    \b
    You can use the list command to get a list of all software or
    portable software instances defined to z/OSMF.
    \b
    To obtain a list of all software instances issue:
    \b
    ./zcli software instances list
    \b
    To obtain a list of all portable software instances issue:
    ./zcli software instances list --pswi
    """
    user = ctx.obj['USER']
    password = ctx.obj['PASSWORD']
    verify = ctx.obj['VERIFY']
    loggin = ctx.obj['LOGGING']

    client = s.SMS(HOST_NAME, user, password)
    errors, response = client.list_software_instances(pswi=pswi, verify=verify)

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        if not tui:
           sys.stdout.write(f'{response.text}\n')
        else:
           tui_sms_list.show_tui(response.text)

#------------------------------------------------------------------------------#
# Define the add instance subcommand of the instances group                    #
#------------------------------------------------------------------------------#
@instances_cli.command(
    name='add',
    cls=HelpColorsCommand,
    help_options_color='blue'
)
@click.pass_context
def add(ctx: click.Context, file_name: str):
    """
    Add a software instance to z/OSMF.

    \b
    You can use the add command to add a new software instance to z/OSMF. The
    request content must be in a json formatted text file.
    \b
    There is a sample input file in the samples directory (add_instance.json).
    Modify it to suit your needs. When you are done pass it as an input option
    to this command like so:
    \b
    ./zcli software instances add --file-name <full_path_to_your_file_name>
    \b
    For a detailed description refer to:
    \b
    https://www.ibm.com/docs/en/zos/3.1.0?topic=services-add-new-software-instance
    """
    user = ctx.obj['USER']
    password = ctx.obj['PASSWORD']
    verify = ctx.obj['VERIFY']
    loggin = ctx.obj['LOGGING']

    client = s.SMS(HOST_NAME, user, password)
    errors, response = client.add_software_instance(filename=file_name, verify=verify)
    if errors:
        sys.stderr.write(f'{str(errors)}\n')
    else:
        sys.stdout.write(f'{response.text}\n')

#------------------------------------------------------------------------------#
# Define the export instance subcommand of the instances group                 #
#------------------------------------------------------------------------------#
@instances_cli.command(
    name='export',
    cls=HelpColorsCommand,
    help_options_color='blue'
)
@click.option(
    '--file-name',
    '-fn',
    type=str,
    required=True,
    help='File Name of the export input file.'
)
@click.option(
    '--nick-name',
    '-nn',
    type=str,
    default='',
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["uuid"],
    help='The system nick name of the software instance'
)
@click.option(
    '--swi-name',
    '-sn',
    type=str,
    default='',
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["uuid"],
    help='The name of the software instance'
)
@click.option(
    '--uuid',
    '-u',
    type=str,
    default='',
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["swi_name", "nick_name"],
    help='The name of the software instance'
)
@click.pass_context
def export(
    ctx: click.Context,
    file_name: str,
    nick_name: str,
    swi_name: str,
    uuid: str
):
    """
    Export a defined software instance.

    \b
    A portable software instance is a set of portable files that represents the
    content of a z/OSMF software instance. An Export action on a software instance
    is used to create a portable software instance.
    You can use the this command to perform an Export action on a software instance
    that is defined to z/OSMF, which generates a portable software instance
    descriptor file and JCL that when executed creates the archive files for a
    portable software instance, and store those files in a UNIX directory on the
    system where the software instance being exported resides.
    \b
    To define which instance you would like to export, specify:
    \b
        - The system nick name AND the software instance name
                        OR
        - The software instance uuid
    \b
    There is a sample input file in the samples directory (export_instance.json).
    Modify it to suit your needs. When you are done pass it as an input option
    to the command like so:
    \b
    ./zcli software instances export -fn <full_path_to_your_file_name> -nn <nick_name> -sn <instance_name>
                        or
    ./zcli software instances export -fn <full_path_to_your_file_name> -u <instance_uuid>
    \b
    For a detailed description refer to:
    \b
    https://www.ibm.com/docs/en/zos/3.1.0?topic=services-export-defined-software-instance
    """
    user = ctx.obj['USER']
    password = ctx.obj['PASSWORD']
    verify = ctx.obj['VERIFY']
    loggin = ctx.obj['LOGGING']

    client = s.SMS(HOST_NAME, user, password)
    errors, response = client.export_software_instance(
        filename=file_name,
        nick_name=nick_name,
        swi_name=swi_name,
        uuid=uuid,
        verify=verify)

    if errors:
        sys.stderr.write(f'{str(errors)}\n')
    else:
        sys.stdout.write(f'{response.text}\n')

#------------------------------------------------------------------------------#
# Define the delete instance subcommand of the instances group                 #
#------------------------------------------------------------------------------#
@instances_cli.command(
    name='delete',
    cls=HelpColorsCommand,
    help_options_color='blue'
)
@click.option(
    '--nick-name',
    '-nn',
    type=str,
    default='',
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["uuid"],
    help='The system nick name of the software instance'
)
@click.option(
    '--swi-name',
    '-sn',
    type=str,
    default='',
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["uuid"],
    help='The name of the software instance'
)
@click.option(
    '--uuid',
    '-u',
    type=str,
    default='',
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["swi_name", "nick_name"],
    help='The name of the software instance'
)
@click.pass_context
def delete(
    ctx: click.Context,
    nick_name: str,
    swi_name: str,
    uuid: str
):
    """
    Delete a defined software instance.

    \b
    You can use this command to remove a software instance definition from z/OSMF.
    The delete operation removes only the definition of the software instance from z/OSMF.
    The physical data sets that compose the software instance are not affected.
    \b
    To define which instance you would like to delete, specify:
    \b
        - The system nick name AND the software instance name
                        OR
        - The software instance uuid
    \b
    ./zcli software instances delete -nn <nick_name> -sn <instance_name>
                        or
    ./zcli software instances delete -u <instance_uuid>
    \b
    """
    user = ctx.obj['USER']
    password = ctx.obj['PASSWORD']
    verify = ctx.obj['VERIFY']
    loggin = ctx.obj['LOGGING']

    client = s.SMS(HOST_NAME, user, password)
    errors, response = client.delete_software_instance(
        nick_name=nick_name,
        swi_name=swi_name,
        uuid=uuid,
        verify=verify
    )

    if errors:
        sys.stderr.write(f'{str(errors)}\n')
    else:
        sys.stdout.write(f'{response.text}\n')

#------------------------------------------------------------------------------#
# Define the siprops command of the instances subgroup of software group       #
#------------------------------------------------------------------------------#
@instances_cli.command(
    name='siprops',
    cls=HelpColorsCommand,
    help_options_color='blue'
)
@click.option(
    '--nick-name',
    '-nn',
    type=str,
    default='',
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["uuid"],
    help='The system nick name of the software instance'
)
@click.option(
    '--swi-name',
    '-sn',
    type=str,
    default='',
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["uuid"],
    help='The name of the software instance'
)
@click.option(
    '--uuid',
    '-u',
    type=str,
    default='',
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["swi_name", "nick_name"],
    help='The name of the software instance'
)
@click.pass_context
def siprops(ctx: click.Context, nick_name: str, swi_name: str, uuid: str):
    """
    Obtain the properties of a defined software instance.

    \b
    You can use the siprops command to get the properties of a software instance.
    \b
    To define which instance properties you would like to retrieve, specify:
    \b
        - The system nick name AND the software instance name
                        OR
        - The software instance uuid
    """
    user = ctx.obj['USER']
    password = ctx.obj['PASSWORD']
    verify = ctx.obj['VERIFY']
    logging = ctx.obj['LOGGING']

    client = s.SMS(HOST_NAME, user, password)
    errors, response = client.get_software_instance_properties(nick_name=nick_name, sw_name=swi_name, uuid=uuid, verify=verify)
    if errors:
        sys.stderr.write(f'{str(errors)}\n')
    else:
        sys.stdout.write(f'{response.text}\n')

#------------------------------------------------------------------------------#
# Define the silistds command of the instances subgroup of software group      #
#------------------------------------------------------------------------------#
@instances_cli.command(
    name='silistds',
    cls=HelpColorsCommand,
    help_options_color='blue'
)
@click.option(
    '--nick-name',
    '-nn',
    type=str,
    default='',
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["uuid"],
    help='The system nick name of the software instance'
)
@click.option(
    '--swi-name',
    '-sn',
    type=str,
    default='',
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["uuid"],
    help='The name of the software instance'
)
@click.option(
    '--uuid',
    '-u',
    type=str,
    default='',
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["swi_name", "nick_name"],
    help='The uuid representing the software instance.'
)
@click.pass_context
def silistds(ctx: click.Context, nick_name: str, swi_name: str, uuid: str):
    """
    Obtain a list of the data sets that compose a software instance.

    \b
    You can use the silistds command to get the datasets of a software instance.
    \b
    To define which instance datasets you would like to retrieve, specify:
    \b
        - The system nick name AND the software instance name
                        OR
        - The software instance uuid
    """
    user = ctx.obj['USER']
    password = ctx.obj['PASSWORD']
    verify = ctx.obj['VERIFY']
    logging = ctx.obj['LOGGING']

    client = s.SMS(HOST_NAME, user, password)
    errors, response = client.get_software_instance_datasets(nick_name=nick_name, sw_name=swi_name, uuid=uuid, verify=verify)
    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        sys.stdout.write(f'{response.text}\n')
