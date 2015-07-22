from datetime import datetime
from .base import CreateBaseCommand


class SnapshotCreateCommand(CreateBaseCommand):
    command_name = "elasticsearch:snapshot-create"

    def is_enabled(self):
        return True

    def snapshot_name(self, prefix):
        now = datetime.now()
        return "{prefix}-{date:%Y%m%d%H%M}".format(
            prefix=prefix,
            date=now
        )

    def run_request(self, repository=None):
        if not repository:
            self.show_repository_list_panel(self.run)
            return

        index = self.settings.index
        options = dict(
            repository=repository,
            snapshot=self.snapshot_name(index),
            body=dict(indices=index)
        )

        return self.client.snapshot.create(**options)
