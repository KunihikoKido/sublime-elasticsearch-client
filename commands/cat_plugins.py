from .base import CatBaseCommand


class CatPluginsCommand(CatBaseCommand):

    def run_request(self):
        options = dict(
            params=dict(v=1)
        )

        response = self.client.cat.plugins(**options)
        self.show_output_panel(response)
