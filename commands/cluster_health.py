from .base import BaseCommand


class ClusterHealthCommand(BaseCommand):
    command_name = "elasticsearch:cluster-health"

    def is_enabled(self):
        return True

    def run_request(self):
        options = dict()
        return self.client.cluster.health(**options)
