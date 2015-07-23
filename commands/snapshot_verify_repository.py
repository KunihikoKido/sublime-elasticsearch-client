from .base import BaseCommand


class SnapshotVerifyRepositoryCommand(BaseCommand):
    command_name = "elasticsearch:snapshot-verify-repository"

    def is_enabled(self):
        return True

    def run_request(self, repository=None):
        if not repository:
            self.show_repository_list_panel(self.run)
            return

        options = dict(
            repository=repository
        )

        return self.client.snapshot.verify_repository(**options)
