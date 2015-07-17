from .base import CatBaseCommand


class CatThreadPoolCommand(CatBaseCommand):

    def run_request(self):
        options = dict(
            params=dict(v=1)
        )

        return self.client.cat.thread_pool(**options)
