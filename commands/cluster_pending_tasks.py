from .base import BaseCommand


class ClusterPendingTasksCommand(BaseCommand):
    command_name = "elasticsearch:cluster-pending-tasks"

    def is_enabled(self):
        return True

    def run_request(self):
        options = dict()
        return self.client.cluster.pending_tasks(**options)
