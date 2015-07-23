from .base import CatBaseCommand


class CatThreadPoolCommand(CatBaseCommand):
    command_name = "elasticsearch:cat-thread-pool"

    def run_request(self):
        options = dict(
            params=dict(v=1)
        )

        return self.client.cat.thread_pool(**options)
