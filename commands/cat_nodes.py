from .base import CatBaseCommand


class CatNodesCommand(CatBaseCommand):

    def run_request(self):
        options = dict(
            params=dict(v=1)
        )

        response = self.client.cat.nodes(**options)
        self.show_output_panel(response)
