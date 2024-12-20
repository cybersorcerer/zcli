import json
from rich.text import Text

from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer
from textual.binding import Binding

COLUMNS_LIST: list = [
    ("Job-Name", "Job-ID", "Status", "Return-Code", "System", "Started", "Ended", "Owner", "Subsystem", "Type", "Correlator"),
]

COLUMNS_DDNAMES: list = [
    ("Job-Name", "Job-ID", "DD-Name", "File ID", "Step Name", "Recfm", "Lrecl", "Record Count", "Byte Count", "Class"),
]

ROWS: list = [()]
class TableApp(App):
    TITLE = "z/OS Jobs List"
    #BINDINGS = [
    #    Binding(
    #        key="enter", action="select_cursor", description="Select", show=True
    #    ),
    #    Binding(
    #        key="k", action="cursor_up", description="Cursor up", show=True
    #    ),
    #    Binding(
    #        key="j", action="cursor_down", description="Cursor down", show=True
    #    ),
    #    Binding(
    #        key="l", action="cursor_right", description="Cursor right", show=True
    #    ),
    #    Binding(
    #        "left", "cursor_left", "Cursor left", show=False
    #    ),
    #    Binding(
    #        "ctrl-u", "page_up", "Page up", show=False
    #    ),
    #    Binding(
    #        "ctrl-d", "page_down", "Page down", show=False
    #    ),
    #    Binding(
    #        "gg", "scroll_top", "Top", show=False
    #    ),
    #    Binding(
    #        "Shift-g", "scroll_bottom", "Bottom", show=False
    #    ),
    #]
    def compose(self) -> ComposeResult:
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.show_row_labels = True
        table.zebra_stripes = True
        table.cursor_type = 'row'
        table.add_columns(*COLUMNS_LIST[0])
        table.add_rows(ROWS[1:])

    def build_job_list_table (self, job_list):
        for job in json.loads(job_list):
            jobname: str = ''
            jobid: str =''
            status: str = ''
            retcode: str = ''
            execsystem: str = ''
            execstarted: str = ''
            execended: str = ''
            owner: str = ''
            subsystem: str = ''
            type: str = ''
            correlator: str = ''
            if 'jobname' in job:
                jobname: str = job['jobname']
            if 'jobid' in job:
                jobid = job['jobid']
            if 'status' in job:
                status = job['status']
            if 'retcode' in job:
                retcode = job['retcode']
            if 'exec-system' in job:
                execsystem = job['exec-system']
            if 'exec-started' in job:
                execstarted = job['exec-started']
            if 'exec-ended' in job:
                execended = job['exec-ended']
            if 'owner' in job:
                owner = job['owner']
            if 'subsystem' in job:
                subsystem = job['subsystem']
            if 'type' in job:
                type = job['type']
            if 'job-correlator' in job:
                correlator = job['job-correlator']
            ROWS.append([jobname, jobid, status, retcode, execsystem, execstarted, execended, owner, subsystem, type, correlator])

def show_tui(list):
    app = TableApp()
    app.build_job_list_table(list)
    app.run()

