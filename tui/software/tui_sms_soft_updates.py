import json
from rich.text import Text

from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer

COLUMNS_UPDATES: list = [
    ("Name", "Type", "FMID",  "Zone Status"),
]
ROWS: list = [()]
class TableApp(App):
    TITLE = "z/OS Software Updates"

    def compose(self) -> ComposeResult:
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        self.theme = "textual-light"
        table = self.query_one(DataTable)
        table.show_row_labels = True
        table.zebra_stripes = True
        table.cursor_type = 'row'
        table.add_columns(*COLUMNS_UPDATES[0])
        table.add_rows(ROWS[1:])
        print(self.active_bindings)

    def build_software_updates_table (self, update_list):
        software_updates = json.loads(update_list)
        for update in software_updates['updates']:
            name: str = ''
            typ: str = ''
            fmid: str = ''
            zone_status: str = ''
            if 'name' in update:
                if update['name'] != 'sysmods':
                    name: str = update['name']
                else:
                    continue
            if 'fmid' in update:
                fmid = update['fmid']
            if 'type' in update:
                typ = update['type']
            if 'zones' in update:
                for zone in update['zones']:
                    installed: str = ''
                    if zone['installed']:
                        installed = zone['installed']

                    zone_status: str = zone_status + zone['zone'] + ' - ' + zone['status'] + ' (' + installed + ') '
            ROWS.append([name, typ, fmid, zone_status])

def show_tui(software_updates):
    app = TableApp()
    app.build_software_updates_table(software_updates)
    app.run()

