from .base import CreateBaseCommand


class SnapshotRestoreCommand(CreateBaseCommand):
    command_name = "elasticsearch:snapshot-restore"

    def is_enabled(self):
        return True

    def close_indices(self, indices):
        for index in indices:
            self.client.indices.close(index=index)

    def open_indices(self, indices):
        for index in indices:
            self.client.indices.open(index=index)

    def restore(self, repository, snapshot):
        options = dict(repository=repository, snapshot=snapshot)
        return self.client.snapshot.restore(**options)

    def run_request(self, repository=None, snapshot=None, indices=None):
        if not repository:
            self.show_repository_list_panel(self.run)
            return

        if not snapshot:
            self.show_snapshot_list_panel(repository, self.run)
            return

        self.close_indices(indices)
        response = self.restore(repository, snapshot)
        self.open_indices(indices)
        return response
