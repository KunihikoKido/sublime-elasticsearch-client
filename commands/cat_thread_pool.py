from .base import CatBaseCommand


class CatThreadPoolCommand(CatBaseCommand):

    def run_request(self):
        options = dict(
            params=dict(v=1)
        )

        response = self.client.cat.thread_pool(**options)
        self.show_output_panel(response)
