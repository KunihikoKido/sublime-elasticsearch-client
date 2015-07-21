from .base import CatBaseCommand


class CatPendingTasksCommand(CatBaseCommand):
    command_name = "elasticsearch:cat-pending-tasks"

    def run_request(self):
        options = dict(
            params=dict(v=1)
        )

        return self.client.cat.pending_tasks(**options)
