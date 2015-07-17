from .base import CatBaseCommand


class CatAllocationCommand(CatBaseCommand):

    def run_request(self):
        options = dict(
            node_id="_all",
            params=dict(v=1)
        )

        response = self.client.cat.allocation(**options)
        self.show_output_panel(response)
