import sublime
from .base import DeleteBaseCommand


class SnapshotDeleteRepositoryCommand(DeleteBaseCommand):
    command_name = "elasticsearch:snapshot-delete-repository"

    def is_enabled(self):
        return True

    def run_request(self, repository=None):
        if not repository:
            self.show_repository_list_panel(self.run)
            return

        options = dict(
            repository=repository
        )

        if sublime.ok_cancel_dialog("Are you sure you want to delete?", ok_title='Delete'):
            return self.client.snapshot.delete_repository(**options)
