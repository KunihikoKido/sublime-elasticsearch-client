from .base import CreateBaseCommand


class SnapshotCreateRepositoryCommand(CreateBaseCommand):
    command_name = "elasticsearch:snapshot-create-repository"

    def run_request(self, repository=None):
        if not repository:
            self.show_input_panel('Repository Name', '', self.run)
            return

        options = dict(
            repository=repository,
            body=self.get_text(),
            params=dict(verify=False)
        )

        return self.client.snapshot.create_repository(**options)
