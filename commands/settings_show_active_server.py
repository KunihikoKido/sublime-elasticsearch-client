import json
from .base import BaseCommand


class SettingsShowActiveServerCommand(BaseCommand):

    def is_enabled(self):
        return True

    def run(self):
        options = dict(
            indent=4,
            ensure_ascii=False
        )

        self.show_output_panel(
            json.dumps(self.settings.active_server, **options),
            syntax="Packages/JavaScript/JSON.tmLanguage"
        )
