import json
from rich.text import Text

from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer
from textual.binding import Binding, BindingsMap, BindingIDString, ActiveBinding

COLUMNS_UPDATES: list = [
    ("Name", "Hold Class", "Hold Symptom", "Held Sysmod", "FMID", "Resolver", "Target Zone(s)", "Description"),
]

ROWS: list = [()]
class TableApp(App):
    TITLE = "z/OS Missing Critical Updates"
    BINDINGS = [
        Binding(
            key="enter",
            action="select_cursor",
            description="Select",
            show=True,
            priority=True
        ),
        Binding(
            key="k",
            action="cursor_up",
            description="Cursor up",
            show=True,
            priority=True,
            system=True,
            tooltip='Press to move the cursor up one line'
        ),
        Binding(
            key="j",
            action="cursor_down",
            description="Cursor down",
            show=True,
            priority=True,
            system=True,
            tooltip='Press to move the cursor down one line'
        ),
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
    ]
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

    def build_missing_updates_table (self, update_list):
        missing_updates = json.loads(update_list)
        for update in missing_updates['missingcriticalupdates']:
            name: str = ''
            hold_class: str =''
            hold_symptom: str = ''
            held_sysmod: str = ''
            fmid: str = ''
            description: str = ''
            target_zones: str = ''
            resolver: str = ''
            if 'name' in update:
                name: str = update['name']
            if 'holdclass' in update:
                hold_class = update['holdclass']
            if 'holdsymptom' in update:
                hold_symptom = update['holdsymptom']
            if 'heldsysmod' in update:
                held_sysmod = update['heldsysmod']
            if 'fmid' in update:
                fmid = update['fmid']
            if 'fmiddesc' in update:
                description = update['fmiddesc']
            if 'resolvers' in update:
                if update['resolvers']:
                    for res in update['resolvers']:
                        rec_status: str = '(received)'
                        if not res['received']:
                            rec_status = "(not received)"
                        resolver = resolver + res['name'] + f'{rec_status} '
            if 'tgtzones' in update:
                for zone in update['tgtzones']:
                    target_zones = target_zones + zone + ' '
            ROWS.append([name, hold_class, hold_symptom, held_sysmod, fmid, resolver, target_zones, description])

def show_tui(missing_updates):
    app = TableApp()
    app.build_missing_updates_table(missing_updates)
    app.run()

