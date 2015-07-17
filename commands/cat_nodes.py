from .base import CatBaseCommand


class CatNodesCommand(CatBaseCommand):

    def run_request(self):
        options = dict(
            params=dict(v=1)
        )

        return self.client.cat.nodes(**options)
