from .base import CatBaseCommand


class CatPendingTasksCommand(CatBaseCommand):

    def run_request(self):
        options = dict(
            params=dict(v=1)
        )

        return self.client.cat.pending_tasks(**options)
