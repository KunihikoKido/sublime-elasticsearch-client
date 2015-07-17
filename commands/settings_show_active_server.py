from .base import BaseCommand


class SettingsShowActiveServerCommand(BaseCommand):

    def is_enabled(self):
        return True

    def run(self):
        self.show_object_output_panel(self.settings.active_server)
