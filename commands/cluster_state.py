from .base import BaseCommand


class ClusterStateCommand(BaseCommand):

    def is_enabled(self):
        return True

    def run_request(self):
        options = dict()
        response = self.client.cluster.state(**options)
        self.show_response(response)
