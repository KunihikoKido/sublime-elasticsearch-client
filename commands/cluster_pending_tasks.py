from .base import BaseCommand


class ClusterPendingTasksCommand(BaseCommand):

    def is_enabled(self):
        return True

    def run_request(self):
        options = dict()
        response = self.client.cluster.pending_tasks(**options)
        self.show_response(response)
