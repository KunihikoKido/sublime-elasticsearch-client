from .base import SettingsBaseCommand


class SettingsShowActiveServerCommand(SettingsBaseCommand):

    def run(self):
        self.show_object_output_panel(self.settings.active_server)
