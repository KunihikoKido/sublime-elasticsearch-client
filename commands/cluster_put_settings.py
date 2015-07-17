from .base import CreateBaseCommand


class ClusterPutSettingsCommand(CreateBaseCommand):

    def run_request(self):
        options = dict(
            body=self.get_text()
        )
        return self.client.cluster.put_settings(**options)
