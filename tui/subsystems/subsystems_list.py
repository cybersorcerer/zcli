import json

from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer

COLUMNS_SS: list = [
    (
        "Name", 
        "Active", 
        "Primary", 
        "Dynamic", 
        "Function-Codes", 
    ),
]

ROWS: list = [()]
class TableApp(App):
    TITLE = "z/OS Subsystems List"   

    def compose(self) -> ComposeResult:
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        self.theme = "textual-light"
        table = self.query_one(DataTable)
        table.show_row_labels = True
        table.zebra_stripes = True
        table.cursor_type = 'row'
        table.add_columns(*COLUMNS_SS[0])
        table.add_rows(ROWS[1:])

    def build_table (self, list):
        list = json.loads(list)
        if list['items']:
            for subsystem in list['items']:
                name: str = ''
                active: str =''
                primary: str = ''
                dynamic: str = ''
                function_codes: str = ''
                if 'subsys' in subsystem:
                    name: str = subsystem['subsys']
                if 'active' in subsystem:
                    active = str(subsystem['active'])
                if 'primary' in subsystem: 
                    primary = str(subsystem['primary'])
                if 'dynamic' in subsystem:
                    dynamic = str(subsystem['dynamic'])
                if 'funcs' in subsystem:
                    for func in subsystem['funcs']:
                        function_codes = function_codes + str(func) + ','
                ROWS.append([
                    name,
                    active,
                    primary,
                    dynamic,
                    function_codes,
                ])
        else:
            print('TUI-LIST-001I Nothing returned for your query')


def show_tui(list):
    app = TableApp()
    app.build_table(list)
    app.run()

