from .base import BaseCommand


class ClusterStatsCommand(BaseCommand):
    command_name = "elasticsearch:cluster-stats"

    def is_enabled(self):
        return True

    def run_request(self):
        options = dict()
        return self.client.cluster.stats(**options)
