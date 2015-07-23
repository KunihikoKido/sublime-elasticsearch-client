from .base import SettingsBaseCommand


class SettingsSelectDocTypeCommand(SettingsBaseCommand):
    command_name = "elasticsearch:settings-select-doc-type"

    def run(self, index=None, doc_type=None):
        if not doc_type:
            self.show_doc_type_list_panel(self.run)
            return

        self.settings.set("doc_type", doc_type)
        self.save_settings()
        self.show_active_server()
        self.track_command()
