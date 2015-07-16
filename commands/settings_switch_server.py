from .base import BaseCommand


class SettingsSwitchServerCommand(BaseCommand):

    def is_enabled(self):
        return True

    def run(self, index=None):
        if index is None:
            return self.show_switch_server_list_panel(self.run)

        server = self.settings.servers[index]

        for key, value in server.items():
            self.settings.set(key, value)

        self.settings.save()

        self.show_active_server()
