from .base import BaseCommand


class NodesHotThreadsCommand(BaseCommand):
    command_name = "elasticsearch:nodes-hot-threads"

    def is_enabled(self):
        return True

    def run_request(self):
        options = dict()
        return self.client.nodes.hot_threads(**options)
