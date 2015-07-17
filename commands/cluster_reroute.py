from .base import CreateBaseCommand


class ClusterRerouteCommand(CreateBaseCommand):

    def run_request(self):
        options = dict(
            body=self.get_text()
        )
        return self.client.cluster.reroute(**options)
