import sublime
from .base import BaseCommand
from ..panel import IndexListPanel


class IndicesGetCommand(BaseCommand):

    def is_enabled(self):
        return True

    def show_index_list_panel(self, callback):
        list_panel = IndexListPanel(self.window, self.client)
        list_panel.show(callback)

    def run_request(self, index=None):
        if index is None:
            return self.show_index_list_panel(self.run_request)

        options = dict(
            index=index
        )

        try:
            response = self.client.indices.get(**options)
        except Exception as e:
            return sublime.error_message("Error: {}".format(e))

        return self.show_response(response)
