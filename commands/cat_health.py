from .base import CatBaseCommand


class CatHealthCommand(CatBaseCommand):

    def run_request(self):
        options = dict(
            params=dict(v=1)
        )

        response = self.client.cat.health(**options)
        self.show_output_panel(response)
