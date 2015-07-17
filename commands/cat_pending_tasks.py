from .base import CatBaseCommand


class CatPendingTasksCommand(CatBaseCommand):

    def run_request(self):
        options = dict(
            params=dict(v=1)
        )

        response = self.client.cat.pending_tasks(**options)
        self.show_output_panel(response)
