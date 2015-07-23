import sublime
from .base import DeleteBaseCommand


class NodesShutdownCommand(DeleteBaseCommand):
    command_name = "elasticsearch:nodes-shutdown"

    def is_enabled(self):
        return True

    def update_command_name(self, node_id):
        if node_id in ("_all", "_master", "_local"):
            self.command_name = "{base}-{node_id}".format(
                base=self.command_name,
                node_id=node_id[1:]
            )

    def run_request(self, node_id):
        self.update_command_name(node_id)

        if sublime.ok_cancel_dialog("Are you sure you want to shutdown?", ok_title='Shutdown'):
            options = dict()
            return self.client.nodes.shutdown(**options)
