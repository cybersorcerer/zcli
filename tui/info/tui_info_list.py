import json

from textual.app import App, ComposeResult
from textual.widgets import DataTable, Header, Footer, Label

COLUMNS_INFO: list = [
    ("Plugin Name", "Plugin Status", "Plugin Version"),
]

ROWS: list = [()]


class TableApp(App):
    TITLE = "z/OSMF Info"
    HOST_NAME: str = ""
    ZOS_VERSION: str = ""
    ZOSMF_VERSION: str = ""
    SAF_REALM: str = ""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label()
        yield Label(f" z/OSMF Host...: {self.HOST_NAME}")
        yield Label(f" z/OS Version..: {self.ZOS_VERSION}")
        yield Label(f" z/OSMF Version: {self.ZOSMF_VERSION}")
        yield Label(f" SAF Realm.....: {self.SAF_REALM}")
        yield Label()
        yield DataTable()
        yield Footer()

    def on_mount(self) -> None:
        self.theme = "textual-light"
        self.title = "z/OSMF Information"
        self.sub_title = f"Instance {self.HOST_NAME}"
        table = self.query_one(DataTable)
        table.show_row_labels = True
        table.zebra_stripes = True
        table.cursor_type = "row"
        table.add_columns(*COLUMNS_INFO[0])
        table.add_rows(ROWS[1:])

    def set_labels(self, info_list):
        self.HOST_NAME = info_list["zosmf_hostname"]
        self.ZOS_VERSION = info_list["zos_version"]
        self.ZOSMF_VERSION = info_list["zosmf_full_version"]
        self.SAF_REALM = info_list["zosmf_saf_realm"]

    def build_table(self, info_list):
        info_list = json.loads(info_list)
        self.set_labels(info_list)
        for entry in info_list["plugins"]:
            name: str = ""
            status: str = ""
            version: str = ""
            if "pluginDefaultName" in entry:
                name: str = entry["pluginDefaultName"]
            if "pluginStatus" in entry:
                status = entry["pluginStatus"]
            if "pluginVersion" in entry:
                version = entry["pluginVersion"]
            ROWS.append(
                [
                    name,
                    status,
                    version,
                ]
            )


def show_tui(info_list):
    app = TableApp()
    app.build_table(info_list)
    app.run()
