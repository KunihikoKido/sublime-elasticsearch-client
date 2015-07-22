from .base import BaseCommand


class SnapshotGetRepositoryCommand(BaseCommand):
    command_name = "elasticsearch:snapshot-get-repository"

    def is_enabled(self):
        return True

    def run_request(self, repository=None):
        if not repository:
            self.show_repository_list_panel(self.run)
            return

        options = dict(
            repository=repository
        )

        return self.client.snapshot.get_repository(**options)
