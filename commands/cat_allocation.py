from .base import CatBaseCommand


class CatAllocationCommand(CatBaseCommand):
    command_name = "elasticsearch:cat-allocation"

    def run_request(self):
        options = dict(
            node_id="_all",
            params=dict(v=1)
        )

        return self.client.cat.allocation(**options)
