from .base import SettingsBaseCommand


class SettingsSwitchServerCommand(SettingsBaseCommand):
    command_name = "elasticsearch:settings-switch-server"

    def run(self, index=None):
        if index is None:
            self.show_switch_server_list_panel(self.run)
            return

        server = self.settings.servers[index]

        for key, value in server.items():
            self.settings.set(key, value)

        self.save_settings()
        self.show_active_server()
        self.track_command()
