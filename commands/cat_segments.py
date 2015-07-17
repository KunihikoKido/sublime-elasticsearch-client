from .base import CatBaseCommand


class CatSegmentsCommand(CatBaseCommand):

    def run_request(self, index=None):
        if index is None:
            self.show_index_list_panel(self.run_request)
            return

        options = dict(
            index=index,
            params=dict(v=1)
        )

        response = self.client.cat.segments(**options)
        self.show_output_panel(response)
