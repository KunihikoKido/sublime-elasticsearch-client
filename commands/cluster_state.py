import sublime
from .base import BaseCommand


class ClusterStateCommand(BaseCommand):

    def is_enabled(self):
        return True

    def run_request(self):
        options = dict()

        try:
            response = self.client.cluster.state(**options)
        except Exception as e:
            return sublime.error_message("Error: {}".format(e))

        return self.show_response(response)
