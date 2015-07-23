from .base import SettingsBaseCommand


class SettingsShowActiveServerCommand(SettingsBaseCommand):
    command_name = "elasticsearch:settings-show-active-server"

    def run(self):
        self.show_object_output_panel(self.settings.active_server)
        self.track_command()
