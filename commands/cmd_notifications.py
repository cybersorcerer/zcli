import click
import sys
from click_help_colors import HelpColorsGroup, HelpColorsCommand
from zosapi import notifications as n
from commands.cmd_defaults import HOST_NAME
#------------------------------------------------------------------------------#
# Define the issues group                                                      #
#------------------------------------------------------------------------------#
@click.group(
    name='notifications',
    cls=HelpColorsGroup,
    help_headers_color='yellow',
    help_options_color='green',
)
def notifications_cli() -> None:
    """
    Work with z/OSMF notification services.

    \b
    These commands are used to send a notification in the form of a notification
    record or email, to a single or multiple recipients. On a successful request,
    all of the recipients get the notification in their z/OSMF Notification task
    as the default destination.
    """
    pass
#------------------------------------------------------------------------------#
# Define the notifications list subcommand                                     #
#------------------------------------------------------------------------------#
@notifications_cli.command(
    name='list',
    cls=HelpColorsCommand,
    help_options_color='blue'
)
@click.pass_context
def list(ctx: click.Context):
    """
    Get all of the notifications received by the current user.

    \b
    You can use the list command to get all of the notifications that were
    received by the current user. This command supports only the user to get
    notification items in the z/OSMF Notifications task. This does not apply
    to the get mail operation in a user's email account.
    """
    user = ctx.obj['USER']
    password = ctx.obj['PASSWORD']
    verify = ctx.obj['VERIFY']
    logging = ctx.obj['LOGGING']

    logging.debug(f'CMD-NOTIFICATIONS-000D list() entered with:')
    logging.debug(f'                          Verify: {verify}')

    client = n.NOTIFICATIONS(HOST_NAME, user, password)
    errors, response = client.get_notifications(verify=verify)

    logging.debug(f'CMD-NOTIFICATIONS-000D list() returned with:')
    logging.debug(f'                         errors: {errors}')
    logging.debug(f'                       response: {response}')

    if "rc" in errors:
        sys.stderr.write(f'{str(errors)}\n')
    else:
        sys.stdout.write(f'{response.text}\n')

#------------------------------------------------------------------------------#
# Define the notifications send subcommand                                     #
#------------------------------------------------------------------------------#
@notifications_cli.command(
    name='send',
    cls=HelpColorsCommand,
    help_options_color='blue'
)
@click.option(
    '--file-name',
    '-f',
    required=True,
    help='The filename with the notification input data.',
    type=click.STRING
)
@click.pass_context
def send(ctx: click.Context, file_name):
    """
    Send a notification and mail from a z/OSMF user or z/OSMF task.

    \b
    You can use the send subcommand to send a notification AND mail. The
    notification details are in the file specified as input option to this
    command.
    \b
    zcli notifications send --file-name /u/user/notification.json
    \b
    The content of the notification as well as the mail contains the user
    input data. This command does not support application linking.
    A notification with the same subject and content will be sent to all
    recipients. If the "attachment" parameter is specified in the input file,
    the attachment will only appear in the recipients' mail.
    """
    user = ctx.obj['USER']
    password = ctx.obj['PASSWORD']
    verify = ctx.obj['VERIFY']
    logging = ctx.obj['LOGGING']

    logging.debug(f'CMD-NOTIFICATIONS-000D send() entered with:')
    logging.debug(f'                       File Name: {file_name}')
    logging.debug(f'                          Verify: {verify}')

    client = n.NOTIFICATIONS(HOST_NAME, user, password)
    errors, response = client.send_notifications(filename=file_name, verify=verify)

    logging.debug(f'CMD-NOTIFICATIONS-000D send() returned with:')
    logging.debug(f'                         errors: {errors}')
    logging.debug(f'                       response: {response}')

    if "rc" in errors:
        sys.stderr.write(f'{str(errors)}\n')
    else:
        sys.stdout.write(f'{response.text}\n')
