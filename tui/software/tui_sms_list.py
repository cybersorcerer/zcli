import json
from rich.text import Text

from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer

COLUMNS_SWI: list = [
    ("Name", "system", "UUID", "Description", "CSI", "Target-Zone(s)", "Categories", "Info-retrieved", "Last-modified", "Modified-by", "Created", "Created-by", "Locked", "Locked-by", "URL"),
]

ROWS: list = [()]
class TableApp(App):
    TITLE = "Software Instance List"

    def compose(self) -> ComposeResult:
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        self.theme = "textual-light"
        table = self.query_one(DataTable)
        table.show_row_labels = True
        table.zebra_stripes = True
        table.cursor_type = 'row'
        table.add_columns(*COLUMNS_SWI[0])
        table.add_rows(ROWS[1:])

    def build_table (self, swi_list):
        swi_list = json.loads(swi_list)
        for instance in swi_list['swilist']:
            name: str = ''
            system: str =''
            description: str = ''
            csi: str = ''
            target_zones: str = ''
            categories: str = ''
            inforetrieved: str = ''
            last_modified: str = ''
            modified_by: str = ''
            created: str = ''
            created_by: str = ''
            locked: str = ''
            locked_by: str = ''
            url: str = ''
            uuid: str = ''
            if 'name' in instance:
                name: str = instance['name']
            if 'system' in instance:
                system = instance['system']
            if 'description' in instance and instance['description']:
                description = instance['description']
            if 'globalzone' in instance:
                csi = instance['globalzone']
            if 'targetzone' in instance:
                if instance['targetzones']:
                    for tz in instance['targetzones']:
                        target_zones = target_zones + tz + ' '
            if 'categories' in instance:
                if instance['categories']:
                    for cat in instance['categories']:
                        categories = categories + cat + ' '
            if 'productinforetrieved' in instance:
                inforetrieved = instance['productinforetrieved']
            if 'lastmodified' in instance:
                last_modified = instance['lastmodified']
            if 'modifiedby' in instance:
                modified_by = instance['modifiedby']
            if 'created' in instance:
                created = instance['created']
            if 'createdby' in instance:
                created_by = instance['createdby']
            if 'locked' in instance and instance['locked']:
                locked = instance['locked']
            if 'lockedby' in instance and instance['lockedby']:
                locked_by = instance['lockedby']
            if 'swiurl' in instance:
                url = instance['swiurl']
            if 'swiuuid' in instance:
                uuid = instance['swiuuid']
            ROWS.append([
                name,
                system,
                uuid,
                description,
                csi,
                target_zones,
                categories,
                inforetrieved,
                last_modified,
                modified_by,
                created,
                created_by,
                locked,
                locked_by,
                url,
            ])

def show_tui(swi_list):
    app = TableApp()
    app.build_table(swi_list)
    app.run()

