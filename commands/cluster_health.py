from .base import BaseCommand


class ClusterHealthCommand(BaseCommand):

    def is_enabled(self):
        return True

    def run_request(self):
        options = dict()
        response = self.client.cluster.health(**options)
        self.show_response(response)
