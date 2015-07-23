from .base import CreateBaseCommand


class ClusterPutSettingsCommand(CreateBaseCommand):
    command_name = "elasticsearch:cluster-put-settings"

    def run_request(self):
        options = dict(
            body=self.get_text()
        )
        return self.client.cluster.put_settings(**options)
