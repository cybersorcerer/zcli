import sys
import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from commands.cmd_utils import MutuallyExclusiveOption
from zosapi import datasets as d
from commands.cmd_defaults import HOST_NAME
#------------------------------------------------------------------------------#
# Define the software group                                                    #
#------------------------------------------------------------------------------#
@click.group(
    name='datasets',
    cls=HelpColorsGroup,
    help_headers_color='yellow',
    help_options_color='green',
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

#------------------------------------------------------------------------------#
# Define the datasets list subcommand                                          #
#------------------------------------------------------------------------------#
@datasets_cli.command(
    name='list',
    cls=HelpColorsCommand,
    help_options_color='blue'
)
@click.option(
    '--dsn-level',
    '-dl',
    default='',
    type=click.STRING,
    help='A dataset level to list. DEFAULT <USERID>.**'
)
@click.option(
    '--volser',
    '-v',
    default='',
    type=click.STRING,
    help='A volume serial number.'
)
@click.option(
    '--start',
    '-s',
    default='',
    type=click.STRING,
    help='A dataset level to list.'
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
    user = ctx.obj['USER']
    password = ctx.obj['PASSWORD']
    verify = ctx.obj['VERIFY']
    logging = ctx.obj['LOGGING']


    logging.debug(f'CMD-DATASETS-000D datasets list entered with:')
    logging.debug(f'                   DSN Level: {dsn_level}')
    logging.debug(f'                      volser: {volser}')
    logging.debug(f'                       start: {start}')

    if dsn_level == '':
        dsn_level = f'{user.upper()}.**'


    client = d.DATASETS(HOST_NAME, user, password)
    errors, response = client.zosapi_datasets_list(dsn_level=dsn_level, volser=volser, start=start, verify=verify)

    logging.debug(f'CMD-DATASETS-000D dataset list returned with:')
    logging.debug(f'                errors: {errors}')
    logging.debug(f'              response: {response}')

    if errors:
        sys.stderr.write(f'{str(errors)}\n')
    else:
        sys.stdout.write(f'{response.text}\n')

#------------------------------------------------------------------------------#
# Define the datasets members subcommand                                       #
#------------------------------------------------------------------------------#
@datasets_cli.command(
    name='members',
    cls=HelpColorsCommand,
    help_options_color='blue'
)
@click.option(
    '--ds-name',
    '-dn',
    required=True,
    type=click.STRING,
    help='The dataset name of a z/OS PDS or PDS/E.'
)
@click.option(
    '--pattern',
    '-p',
    default='',
    type=click.STRING,
    help='A search pattern following the ISPF LMMLIST.'
)
@click.pass_context
def members(ctx: click.Context, ds_name: str, pattern: str):
    """
    List members of z/OS partitioned datasets (PDS and PDS/E).

    \b
    You can use this command to obtain a list of members of z/OS
    partioned datasets.
    """
    user = ctx.obj['USER']
    password = ctx.obj['PASSWORD']
    verify = ctx.obj['VERIFY']
    logging = ctx.obj['LOGGING']


    logging.debug(f'CMD-DATASETS-000D datasets list entered with:')
    logging.debug(f'                Dataset name: {ds_name}')
    logging.debug(f'                     pattern: {pattern}')

    client = d.DATASETS(HOST_NAME, user, password)
    errors, response = client.zosapi_datasets_members_list(dataset_name=ds_name, pattern=pattern, verify=verify)

    logging.debug(f'CMD-DATASETS-000D dataset list returned with:')
    logging.debug(f'                errors: {errors}')
    logging.debug(f'              response: {response}')

    if errors:
        sys.stderr.write(f'{str(errors)}\n')
    else:
        sys.stdout.write(f'{response.text}\n')

#------------------------------------------------------------------------------#
# Define the datasets read subcommand                                          #
#------------------------------------------------------------------------------#
@datasets_cli.command(
    name='read',
    cls=HelpColorsCommand,
    help_options_color='blue'
)
@click.option(
    '--ds-name',
    '-dn',
    required=True,
    type=click.STRING,
    help='The dataset name of a z/OS PDS or PDS/E or sequential dataset.'
)
@click.option(
    '--member-name',
    '-mn',
    default='',
    type=click.STRING,
    help='A member name if --ds-name is a PDS or PDS/E.'
)
@click.option(
    '--volser',
    '-v',
    default='',
    type=click.STRING,
    help='A volume serial number if --ds-name is not cataloged.'
)
@click.option(
    '--encoding',
    '-e',
    default='',
    type=click.STRING,
    help='Encoding of the data.'
)
@click.option(
    '--enq-exclusive',
    '-exc',
    is_flag=True,
    default=False,
    type=click.STRING,
    help='If True an exclusive enq will be set, otherwise a share enqueuei.'
)
@click.pass_context
def read(
        ctx: click.Context, 
        ds_name: str, 
        member_name: str, 
        volser: str, 
        enq_exclusive: bool, 
        encoding: str
):
    """
    Read a member of a PDS or PDS/E or a sequential dataset.  

    \b
    You can use this command to read a member of a dataset or a
    sequental dataset. If the dataset is not cataloged specify a 
    volume serial number to read the member or the dataset directly 
    from the volume.
    """
    user = ctx.obj['USER']
    password = ctx.obj['PASSWORD']
    verify = ctx.obj['VERIFY']
    logging = ctx.obj['LOGGING']


    logging.debug(f'CMD-DATASETS-000D datasets list entered with:')
    logging.debug(f'                  Dataset name: {ds_name}')
    logging.debug(f'                        member: {member_name}')
    logging.debug(f'                        volser: {volser}')
    logging.debug(f'             exclusive enqueue: {enq_exclusive}')

    client = d.DATASETS(HOST_NAME, user, password)
    errors, response = client.zosapi_datasets_read(
        dataset_name=ds_name, 
        member=member_name, 
        volser=volser, 
        encoding=encoding, 
        verify=verify
    )

    logging.debug(f'CMD-DATASETS-000D dataset list returned with:')
    logging.debug(f'                errors: {errors}')
    logging.debug(f'              response: {response}')

    if errors:
        sys.stderr.write(f'{str(errors)}\n')
    else:
        sys.stdout.write(f'{response.text}\n')
        sys.stdout.write(f'{response.headers}\n')


