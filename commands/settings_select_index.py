from .base import SettingsBaseCommand


class SettingsSelectIndexCommand(SettingsBaseCommand):
    command_name = "elasticsearch:settings-select-index"

    def select_doc_type(self):
        self.window.run_command("settings_select_doc_type")

    def run(self, index=None):
        if not index:
            self.show_index_list_panel(self.run)
            return

        self.settings.set("index", index)
        self.save_settings()
        self.show_active_server()
        self.select_doc_type()
        self.track_command()
