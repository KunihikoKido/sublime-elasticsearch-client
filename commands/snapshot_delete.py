import sublime
from .base import DeleteBaseCommand


class SnapshotDeleteCommand(DeleteBaseCommand):
    command_name = "elasticsearch:snapshot-delete"

    def is_enabled(self):
        return True

    def run_request(self, repository=None, snapshot=None, **kwargs):
        if not repository:
            self.show_repository_list_panel(self.run)
            return

        if not snapshot:
            self.show_snapshot_list_panel(repository, self.run)
            return

        options = dict(
            repository=repository,
            snapshot=snapshot
        )

        if sublime.ok_cancel_dialog("Are you sure you want to delete?", ok_title='Delete'):
            return self.client.snapshot.delete(**options)
