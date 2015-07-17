from .base import BaseCommand


class ClusterHealthCommand(BaseCommand):

    def is_enabled(self):
        return True

    def run_request(self):
        options = dict()
        return self.client.cluster.health(**options)
