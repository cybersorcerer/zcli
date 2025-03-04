import sys
import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand

from tui.jobs import tui_jobs_list
from zosapi import jobs as j
from commands.cmd_utils import MutuallyExclusiveOption


# ------------------------------------------------------------------------------#
# Define the issues group                                                      #
# ------------------------------------------------------------------------------#
@click.group(
    name="jobs",
    cls=HelpColorsGroup,
    help_headers_color="yellow",
    help_options_color="green",
)
def jobs_cli() -> None:
    """
    Work with batch jobs on a z/OS system.

    \b
    Author.......: Ronny Funk
    Function.....: Work with JES jobs and spool files

    Environment: *ix Terminal CLI / Batch Job
    """
    pass


# ------------------------------------------------------------------------------#
# Define the jobs list subcommand                                              #
# ------------------------------------------------------------------------------#
@jobs_cli.command(name="list", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--owner",
    "-o",
    required=False,
    help="Owner of the jobs to list",
    default="",
    type=click.STRING,
)
@click.option(
    "--prefix",
    "-p",
    required=False,
    help="Job name prefix; default is *",
    default="*",
    type=click.STRING,
)
@click.option(
    "--max-jobs",
    "-mj",
    required=False,
    help="Maximum number of jobs returned..",
    default=1000,
    show_default=True,
    type=click.INT,
)
@click.option(
    "--exec-data / --no-exec-data",
    required=False,
    default=True,
    show_default=True,
    help="Also get execution data. Usually you want this!",
)
@click.option(
    "--tui/ --no-tui",
    required=False,
    default=False,
    show_default=True,
    help="Display response data in a table.",
)
@click.option(
    "--active / --all",
    required=False,
    default=False,
    show_default=True,
    help="Include only active jobs in list.",
)
@click.pass_context
def list(
    ctx: click.Context,
    owner: str,
    prefix: str,
    max_jobs: int,
    exec_data: bool,
    tui: bool,
    active: bool,
):
    """
    Use this command to list jobs by owner, prefix, or job ID.

    \b
    You can specify one or more of the following optional query parameters:
    \b
        - owner
        - prefix
        - max-jobs
        - exec-data
        - acive / all
    \b
    """
    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-JOBS-000D list() entered with:")
    logging.debug(f"                       owner: {owner}")
    logging.debug(f"                      prefix: {prefix}")
    logging.debug(f"                    max-jobs: {max_jobs}")
    logging.debug(f"                   exec-data: {exec_data}")
    logging.debug(f"                 active-only: {active}")

    exec: str = "N"
    if exec_data:
        exec = "Y"

    if owner == "":
        owner = ctx.obj["USER"]

    client = j.JOBS(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.get_job_list(
        owner=owner,
        prefix=prefix,
        max_jobs=max_jobs,
        exec_data=exec,
        active_only=active,
        verify=verify,
    )
    logging.debug("CMD-JOBS-000D list() returned with:")
    logging.debug(f"                errors: {errors}")
    logging.debug(f"              response: {response}")
    logging.debug(f"                header: {response.headers}")

    if errors:
        sys.stderr.write(str(errors))
    else:
        if not tui:
            sys.stdout.write(f"{response.text}\n")
        else:
            tui_jobs_list.show_tui(response.text)


# ------------------------------------------------------------------------------#
# Define the jobs ddnames subcommand                                           #
# ------------------------------------------------------------------------------#
@jobs_cli.command(name="ddnames", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--job-id",
    "-ji",
    required=False,
    help="A Job ID.",
    default="*",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["job_correlator"],
    type=click.STRING,
)
@click.option(
    "--job-name",
    "-jn",
    required=False,
    help="The job name.",
    default="*",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["job_correlator"],
    type=click.STRING,
)
@click.option(
    "--job-correlator",
    "-jc",
    required=False,
    help="The user portion of the job correlator.",
    default="",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["jobid", "name"],
    type=click.STRING,
)
@click.option(
    "--files / --no-files",
    required=False,
    help="Get the jobs spool file DD names.",
    default=False,
    type=click.BOOL,
)
@click.pass_context
def ddnames(
    ctx: click.Context, job_id: str, job_name: str, job_correlator: str, files: bool
):
    """
    Use this command to retrieve the spool file DD names.

    \b
    You can specify one or more of the following optional query parameters:
    \b
    To identify the job in the request, use either the combination of the job name and job ID,
    or the job correlator, as follows:
    \b
    ./zcli.py jobs ddnames --job-name <job_name> --job-id <job_id>
    <job_name> <job_id> identifies the job for which the spool file DD Names are to be retrieved.
    \b
    ./zcli.py jobs ddnames --job-correlator <job_correlator>
    <job_correlator> identifies the job for which the spool file DD Names are to be listed.
    Specify the full job correlator for the job: The 31-byte system portion, a semicolon,
    and the user portion (up to 32 bytes). The correlator can be one that you obtained from the
    "job-correlator" property of the list subcommand in a returned JSON job document.
    \b
    """
    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-JOBS-000D job list entered with:")
    logging.debug(f"                       name:  {job_name}")
    logging.debug(f"                       jobid: {job_id}")
    logging.debug(f"              job-correlator: {job_correlator}")
    logging.debug(f"                       files: {files}")

    client = j.JOBS(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    if job_correlator == "":
        errors, response = client.get_files_by_jobname_jobid(
            jobname=job_name.upper(), jobid=job_id.upper(), verify=verify
        )
    else:
        errors, response = client.get_files_by_job_correlator(
            correlator=job_correlator.upper(), verify=verify
        )
    logging.debug("CMD-JOBS-000D Job list returned with:")
    logging.debug(f"                errors: {errors}")
    logging.debug(f"              response: {response}")

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        sys.stdout.write(f"{response.text}\n")


# ------------------------------------------------------------------------------#
# Define the jobs files subcommand                                             #
# ------------------------------------------------------------------------------#
@jobs_cli.command(name="files", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--job-id",
    "-ji",
    required=False,
    help="A Job ID.",
    default="*",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["job_correlator"],
    type=click.STRING,
)
@click.option(
    "--job-name",
    "-jn",
    required=False,
    help="The job name.",
    default="*",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["job_correlator"],
    type=click.STRING,
)
@click.option(
    "--job-correlator",
    "-jc",
    required=False,
    help="The user portion of the job correlator.",
    default="",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["jobid", "name"],
    type=click.STRING,
)
@click.option(
    "--file-id",
    "-fi",
    required=True,
    help="The id of the spool file to retrieveq.",
    type=click.STRING,
)
@click.pass_context
def files(
    ctx: click.Context, job_id: str, job_name: str, job_correlator: str, file_id: str
):
    """
    Use this command to retrieve a spool file.

    \b
    You can specify one or more of the following parameters:
    \b
    To identify the job in the request, use either the combination of the job name and job ID,
    or the job correlator, as follows:
    \b
    ./zcli.py jobs files --job-name <job_name> --job-id <job_id> --file-id <id>
    <job_name> <job_id> identifies the job.
    <id> is the file id of the spool file to be retrieved.
    \b
    ./zcli.py jobs files --job-correlator <job_correlator> --file-id <fileid>
    <job_correlator> identifies the job.
    <id> is the file id of the spool file to be retrieved.
    \b
    NOTE:
    Specify the full job correlator for the job: The 31-byte system portion, a semicolon,
    and the user portion (up to 32 bytes).
    \b
    """
    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-JOBS-000D files() entered with:")
    logging.debug(f"                    Job Name: {job_name}")
    logging.debug(f"                      Job ID: {job_id}")
    logging.debug(f"              Job Correlator: {job_correlator}")
    logging.debug(f"                     File ID: {file_id}")

    client = j.JOBS(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.get_job_file_by_id(
        fileid=file_id,
        jobname=job_name.upper(),
        jobid=job_id.upper(),
        correlator=job_correlator,
        verify=verify,
    )
    logging.debug("CMD-JOBS-000D files() returned with:")
    logging.debug(f"                errors: {errors}")
    logging.debug(f"              response: {response}")

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        sys.stdout.write(f"{response.text}\n")


# ------------------------------------------------------------------------------#
# Define the jobs jcl subcommand                                               #
# ------------------------------------------------------------------------------#
@jobs_cli.command(name="jcl", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--job-id",
    "-ji",
    required=False,
    help="A Job ID.",
    default="",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["job_correlator"],
    type=click.STRING,
)
@click.option(
    "--job-name",
    "-jn",
    required=False,
    help="The job name.",
    default="",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["job_correlator"],
    type=click.STRING,
)
@click.option(
    "--job-correlator",
    "-jc",
    required=False,
    help="The user portion of the job correlator.",
    default="",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["jobid", "name"],
    type=click.STRING,
)
@click.pass_context
def jcl(ctx: click.Context, job_id: str, job_name: str, job_correlator: str):
    """
    Use this command to retrieve the jobs JCL from JES spool.

    \b
    You can specify one or more of the following parameters:
    \b
    To identify the job in the request, use either the combination of the job name and job ID,
    or the job correlator, as follows:
    \b
    ./zcli.py jobs jcl --job-name <job_name> --job-id <job_id>
    <job_name> <job_id> identifies the job.
    \b
    ./zcli.py jobs jcl --job-correlator <job_correlator>
    <job_correlator> identifies the job.
    \b
    NOTE:
    Specify the full job correlator for the job: The 31-byte system portion, a semicolon,
    and the user portion (up to 32 bytes).
    \b
    """
    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-JOBS-000D jcl() entered with:")
    logging.debug(f"                    Job Name: {job_name}")
    logging.debug(f"                      Job ID: {job_id}")
    logging.debug(f"              Job Correlator: {job_correlator}")

    client = j.JOBS(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.get_job_jcl(
        jobname=job_name.upper(),
        jobid=job_id.upper(),
        correlator=job_correlator,
        verify=verify,
    )
    logging.debug("CMD-JOBS-000D jcl() returned with:")
    logging.debug(f"                errors: {errors}")
    logging.debug(f"              response: {response}")

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        sys.stdout.write(f"{response.text}\n")


# ------------------------------------------------------------------------------#
# Define the jobs submit subcommand                                            #
# ------------------------------------------------------------------------------#
@jobs_cli.command(name="submit", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--file-name",
    "-fn",
    required=True,
    help="Full file name containing z/OS Job JCL.",
    type=click.STRING,
)
@click.option(
    "--secondary-jes",
    "-sn",
    required=False,
    default="",
    help="Secondary JES subsystem name.",
    type=click.STRING,
)
@click.option(
    "--inline/--no-inline",
    required=False,
    default=True,
    help="Submit JCL inline.",
    type=click.BOOL,
)

@click.pass_context
def submit(
    ctx: click.Context,
    file_name: str,
    secondary_jes: str,
    inline: bool,
):
    """
    Use this command to submit a job to run on z/OS.

    \b
    To submit z/OS JCL contained in a file use the zcli jobs command as follows:
    ./zcli.py jobs submit --file-name <file_name> --no-inline
    \b
    Note: The --no-inline flag only works if zcli is running inside z/Unix!
          otherwise the default --inline must be used. In ths case zcli will
          read the file into memory and submit the JCL inline.
    \b
    If you want to submit the job to a secondary JES subsystem add the optional parameter:
    --secondary-jes <jes_name>
    to the request.
    \b
    """
    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-JOBS-000D job submit entered with:")
    logging.debug(f"                   file_name: {file_name}")
    logging.debug(f"                       inline: {inline}")
    logging.debug(f"               secondary_jes: {secondary_jes}")

    client = j.JOBS(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )

    errors, response = client.submit_job(
        file_name=file_name, jes_name=secondary_jes, verify=verify
    )

    logging.debug("CMD-JOBS-000D Job submit returned with:")
    logging.debug(f"                errors: {errors}")
    logging.debug(f"              response: {response}")

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        sys.stdout.write(f"{response.text}\n")


# ------------------------------------------------------------------------------#
# Define the jobs hold subcommand                                              #
# ------------------------------------------------------------------------------#
@jobs_cli.command(name="hold", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--job-name",
    "-jn",
    required=False,
    help="The job name.",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["job_correlator"],
    type=click.STRING,
)
@click.option(
    "--job-id",
    "-ji",
    required=False,
    help="A Job ID corresponding to job name.",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["job_correlator"],
    default="",
    show_default=True,
    type=click.STRING,
)
@click.option(
    "--job-correlator",
    "-jc",
    required=False,
    help="The user portion of the job correlator.",
    default="",
    show_default=True,
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["jobid", "name"],
    type=click.STRING,
)
@click.option(
    "--secondary-jes",
    "-sn",
    required=False,
    default="",
    show_default=True,
    help="Secondary JES subsystem name.",
    type=click.STRING,
)
@click.pass_context
def hold(
    ctx: click.Context,
    job_name: str = "",
    job_id: str = "",
    job_correlator: str = "",
    secondary_jes: str = "",
):
    """
    Use this command to hold a job.

    \b
    To hold z/OS job using job name and job id use the zcli jobs command as follows:
    ./zcli.py jobs hold --job-name <jobname> --job-id <jobid
    \b
    To hold z/OS job using the user portion of the job correlator use the zcli jobs
    command as follows:
    ./zcli.py jobs hold --job-correlator <correlator>
    \b
    If you want to hold a job on a secondary JES subsystem add the optional parameter:
    --secondary-jes <jes_name>
    to the request.
    \b
    """
    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-JOBS-000D hold() entered with:")
    logging.debug(f"                       Job Name: {job_name}")
    logging.debug(f"                         Job ID: {job_id}")
    logging.debug(f"                     Correlator: {job_correlator}")
    logging.debug(f"                  secondary_jes: {secondary_jes}")

    client = j.JOBS(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.hold_job(
        jobname=job_name, jobid=job_id, correlator=job_correlator, verify=verify
    )

    logging.debug("CMD-JOBS-000D hold() returned with:")
    logging.debug(f"                errors: {errors}")
    logging.debug(f"              response: {response}")

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        sys.stdout.write(f"{response.text}\n")


# ------------------------------------------------------------------------------#
# Define the jobs change class subcommand                                      #
# ------------------------------------------------------------------------------#
@jobs_cli.command(name="change-class", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--job-name",
    "-jn",
    required=False,
    help="The job name.",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["job_correlator"],
    type=click.STRING,
)
@click.option(
    "--job-id",
    "-ji",
    required=False,
    help="A Job ID corresponding to job name.",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["job_correlator"],
    default="",
    show_default=True,
    type=click.STRING,
)
@click.option(
    "--job-correlator",
    "-jc",
    required=False,
    help="The user portion of the job correlator.",
    default="",
    show_default=True,
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["jobid", "name"],
    type=click.STRING,
)
@click.option(
    "--new-class", "-nc", required=True, help="The new JES Jobclass to use.", type=click.STRING
)
@click.option(
    "--secondary-jes",
    "-sn",
    required=False,
    default="",
    show_default=True,
    help="Secondary JES subsystem name.",
    type=click.STRING,
)
@click.pass_context
def jobclass(
    ctx: click.Context,
    job_name: str = "",
    job_id: str = "",
    job_correlator: str = "",
    newclass: str = "",
    secondary_jes: str = "",
):
    """
    Use this command to change the class of a job on z/OS.

    \b
    To change the class of a job using Job Name and Job ID, use the zcli jobs command as follows:
    ./zcli.py jobs new-class --job-name <jobname> --job-id <jobid> --new-class <newclass>
    \b
    To change the class of a job using the user portion of the Job Correlator, use the zcli jobs
    command as follows:
    ./zcli.py jobs new-class --job-correlator <correlator> --new-class <newclass>
    \b
    If you want to change the class of a job on a secondary JES subsystem, add the optional parameter:
    --secondary-jes <jes_name>
    to the request.
    \b
    """
    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-JOBS-000D jobclass() entered with:")
    logging.debug(f"                       Job Name: {job_name}")
    logging.debug(f"                         Job ID: {job_id}")
    logging.debug(f"                     Correlator: {job_correlator}")
    logging.debug(f"                  New Job Class: {newclass}")
    logging.debug(f"                  secondary_jes: {secondary_jes}")

    client = j.JOBS(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.change_job_class(
        jobname=job_name,
        jobid=job_id,
        correlator=job_correlator,
        jobclass=newclass,
        verify=verify,
    )

    logging.debug("CMD-JOBS-000D jobclass() returned with:")
    logging.debug(f"                errors: {errors}")
    logging.debug(f"              response: {response}")

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        sys.stdout.write(f"{response.text}\n")


# ------------------------------------------------------------------------------#
# Define the jobs release subcommand                                           #
# ------------------------------------------------------------------------------#
@jobs_cli.command(name="release", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--job-name",
    "-jn",
    required=False,
    help="The job name.",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["job_correlator"],
    type=click.STRING,
)
@click.option(
    "--job-id",
    "-ji",
    required=False,
    help="A Job ID corresponding to job name.",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["job_correlator"],
    default="",
    show_default=True,
    type=click.STRING,
)
@click.option(
    "--job-correlator",
    "-jc",
    required=False,
    help="The user portion of the job correlator.",
    default="",
    show_default=True,
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["jobid", "name"],
    type=click.STRING,
)
@click.option(
    "--secondary-jes",
    "-sn",
    required=False,
    default="",
    show_default=True,
    help="Secondary JES subsystem name.",
    type=click.STRING,
)
@click.pass_context
def release(
    ctx: click.Context,
    job_name: str = "",
    job_id: str = "",
    job_correlator: str = "",
    secondary_jes: str = "",
):
    """
    Use this command to release a job.

    \b
    To submit z/OS JCL contained in a file use the zcli jobs command as follows:
    ./zcli.py jobs submit --file-name <file_name>
    \b
    If you want to submit the job to a secondary JES subsystem add the optional parameter:
    --secondary-jes <jes_name>
    to the request.
    \b
    """
    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-JOBS-000D release() entered with:")
    logging.debug(f"                       Job Name: {job_name}")
    logging.debug(f"                         Job ID: {job_id}")
    logging.debug(f"                     Correlator: {job_correlator}")
    logging.debug(f"                  secondary_jes: {secondary_jes}")

    client = j.JOBS(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    errors, response = client.release_job(
        jobname=job_name, jobid=job_id, correlator=job_correlator, verify=verify
    )

    logging.debug("CMD-JOBS-000D release() returned with:")
    logging.debug(f"                errors: {errors}")
    logging.debug(f"              response: {response}")

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        sys.stdout.write(f"{response.text}\n")


# ------------------------------------------------------------------------------#
# Define the jobs cancel subcommand                                            #
# ------------------------------------------------------------------------------#
@jobs_cli.command(name="cancel", cls=HelpColorsCommand, help_options_color="blue")
@click.option(
    "--job-name",
    "-jn",
    required=False,
    help="The job name.",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["job_correlator"],
    type=click.STRING,
)
@click.option(
    "--job-id",
    "-ji",
    required=False,
    help="A Job ID corresponding to job name.",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["job_correlator"],
    default="",
    show_default=True,
    type=click.STRING,
)
@click.option(
    "--job-correlator",
    "-jc",
    required=False,
    help="The user portion of the job correlator.",
    default="",
    show_default=True,
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["jobid", "name"],
    type=click.STRING,
)
@click.option(
    "--secondary-jes",
    "-sn",
    required=False,
    default="",
    show_default=True,
    help="Secondary JES subsystem name.",
    type=click.STRING,
)
@click.option(
    "--purge / --no-purge",
    required=False,
    default=False,
    show_default=True,
    help="Purge output of cancelled job.",
    type=click.BOOL,
)
@click.pass_context
def cancel(
    ctx: click.Context,
    job_name: str = "",
    job_id: str = "",
    job_correlator: str = "",
    secondary_jes: str = "",
    purge: bool = False,
):
    """
    Use this command to cancel a job on z/OS.

    \b
    To cancel a job by jobname and jobid:
    ./zcli.py jobs cancel --job-name <jobname> --job-id <job_id>
    \b
    To cancel a job by job correlator:
    ./zcli.py jobs cancel --job-correlator <jobname>
    \b
    If you want to cancel a job on a secondary JES subsystem add the optional parameter:
    --secondary-jes <jes_name>
    to the request.
    \b
    If you also want to purge the jobs output add the optional flag:
    --purge
    \b
    """
    verify = ctx.obj["VERIFY"]
    logging = ctx.obj["LOGGING"]

    logging.debug("CMD-JOBS-000D cancel() entered with:")
    logging.debug(f"                       Job Name: {job_name}")
    logging.debug(f"                         Job ID: {job_id}")
    logging.debug(f"                     Correlator: {job_correlator}")
    logging.debug(f"                  Secondary Jes: {secondary_jes}")
    logging.debug(f"                   Purge Output: {purge}")

    client = j.JOBS(
        hostname=ctx.obj["HOST_NAME"],
        protocol=ctx.obj["PROTOCOL"],
        port=ctx.obj["PORT"],
        username=ctx.obj["USER"],
        password=ctx.obj["PASSWORD"],
        cert_path=ctx.obj["CERT_PATH"],
    )
    if not purge:
        errors, response = client.cancel_job(
            jobname=job_name, jobid=job_id, correlator=job_correlator, verify=verify
        )
    else:
        errors, response = client.cancel_and_purge_job(
            jobname=job_name, jobid=job_id, correlator=job_correlator, verify=verify
        )

    logging.debug("CMD-JOBS-000D cancel() returned with:")
    logging.debug(f"                errors: {errors}")
    logging.debug(f"              response: {response}")

    if errors:
        sys.stderr.write(f"{str(errors)}\n")
    else:
        sys.stdout.write(f"{response.text}\n")
