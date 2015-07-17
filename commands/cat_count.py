from .base import CatBaseCommand


class CatCountCommand(CatBaseCommand):

    def run_request(self, index=None):
        if index is None:
            self.show_index_list_panel(self.run_request)
            return

        options = dict(
            index=index,
            params=dict(v=1)
        )

        response = self.client.cat.count(**options)
        self.show_output_panel(response)
