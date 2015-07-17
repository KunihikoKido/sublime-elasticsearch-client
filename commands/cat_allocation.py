from .base import CatBaseCommand


class CatAllocationCommand(CatBaseCommand):

    def run_request(self):
        options = dict(
            node_id="_all",
            params=dict(v=1)
        )

        return self.client.cat.allocation(**options)
