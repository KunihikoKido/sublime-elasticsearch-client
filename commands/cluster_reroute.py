from .base import BaseCommand


class ClusterRerouteCommand(BaseCommand):

    def run_request(self):
        options = dict(
            body=self.get_text()
        )
        response = self.client.cluster.reroute(**options)
        self.show_object_output_panel(response)
