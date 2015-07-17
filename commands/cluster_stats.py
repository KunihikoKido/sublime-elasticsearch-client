from .base import BaseCommand


class ClusterStatsCommand(BaseCommand):

    def is_enabled(self):
        return True

    def run_request(self):
        options = dict()
        response = self.client.cluster.stats(**options)
        self.show_response(response)
