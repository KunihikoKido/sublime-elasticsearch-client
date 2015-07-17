from .base import BaseCommand


class ClusterPendingTasksCommand(BaseCommand):

    def is_enabled(self):
        return True

    def run_request(self):
        options = dict()
        return self.client.cluster.pending_tasks(**options)
