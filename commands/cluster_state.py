from .base import BaseCommand


class ClusterStateCommand(BaseCommand):
    command_name = "elasticsearch:cluster-state"

    def is_enabled(self):
        return True

    def run_request(self):
        options = dict()
        return self.client.cluster.state(**options)
