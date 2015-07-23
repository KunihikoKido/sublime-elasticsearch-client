from .base import BaseCommand


class NodesInfoCommand(BaseCommand):
    command_name = "elasticsearch:nodes-info"

    def is_enabled(self):
        return True

    def run_request(self):
        options = dict()
        return self.client.nodes.info(**options)
