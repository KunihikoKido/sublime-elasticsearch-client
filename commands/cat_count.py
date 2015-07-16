import sublime
from .base import BaseCommand


class CatCountCommand(BaseCommand):

    def is_enabled(self):
        return True

    def run_request(self, index=None):
        if index is None:
            return self.show_index_list_panel(self.run_request)

        options = dict(
            index=index,
            params=dict(v=1)
        )

        try:
            response = self.client.cat.count(**options)
        except Exception as e:
            return sublime.error_message("Error: {}".format(e))

        return self.show_output_panel(response)
