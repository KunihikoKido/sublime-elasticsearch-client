from .base import BaseCommand


class ClusterGetSettingsCommand(BaseCommand):

    def is_enabled(self):
        return True

    def run_request(self):
        options = dict()
        return self.client.cluster.get_settings(**options)
