from .base import CatBaseCommand


class CatNodesCommand(CatBaseCommand):
    command_name = "elasticsearch:cat-nodes"

    def run_request(self):
        options = dict(
            params=dict(v=1)
        )

        return self.client.cat.nodes(**options)
