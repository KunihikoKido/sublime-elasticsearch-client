from .base import BaseCommand


class ClusterPutSettingsCommand(BaseCommand):

    def run_request(self):
        options = dict(
            body=self.get_text()
        )
        response = self.client.cluster.put_settings(**options)
        self.show_object_output_panel(response)
