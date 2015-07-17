from .base import CatBaseCommand


class CatFielddataCommand(CatBaseCommand):

    def run_request(self):
        options = dict(
            params=dict(v=1)
        )

        response = self.client.cat.fielddata(**options)
        self.show_output_panel(response)
