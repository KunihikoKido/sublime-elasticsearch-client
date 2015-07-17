from .base import BaseCommand


class ClusterGetSettingsCommand(BaseCommand):

    def is_enabled(self):
        return True

    def run_request(self):
        options = dict()
        response = self.client.cluster.get_settings(**options)
        self.show_response(response)
