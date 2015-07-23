from .base import CreateBaseCommand


class ClusterRerouteCommand(CreateBaseCommand):
    command_name = "elasticsearch:cluster-reroute"

    def run_request(self):
        options = dict(
            body=self.get_text()
        )
        return self.client.cluster.reroute(**options)
