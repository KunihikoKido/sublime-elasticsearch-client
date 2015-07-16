import sublime
from .base import BaseCommand


class CatPendingTasksCommand(BaseCommand):

    def is_enabled(self):
        return True

    def run_request(self):

        options = dict(
            params=dict(v=1)
        )

        try:
            response = self.client.cat.pending_tasks(**options)
        except Exception as e:
            return sublime.error_message("Error: {}".format(e))

        return self.show_output_panel(response)
