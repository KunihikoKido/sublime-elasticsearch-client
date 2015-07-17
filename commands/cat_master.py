from .base import CatBaseCommand


class CatMasterCommand(CatBaseCommand):

    def run_request(self):
        options = dict(
            params=dict(v=1)
        )

        response = self.client.cat.master(**options)
        self.show_output_panel(response)
