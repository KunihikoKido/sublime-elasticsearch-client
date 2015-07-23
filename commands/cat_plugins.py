from .base import CatBaseCommand


class CatPluginsCommand(CatBaseCommand):
    command_name = "elasticsearch:cat-plugins"

    def run_request(self):
        options = dict(
            params=dict(v=1)
        )

        return self.client.cat.plugins(**options)
