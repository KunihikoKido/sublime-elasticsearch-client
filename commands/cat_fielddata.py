import sublime
from .base import BaseCommand


class CatFielddataCommand(BaseCommand):

    def is_enabled(self):
        return True

    def run_request(self):

        options = dict(
            params=dict(v=1)
        )

        try:
            response = self.client.cat.fielddata(**options)
        except Exception as e:
            return sublime.error_message("Error: {}".format(e))

        return self.show_output_panel(response)
