from .base import CreateBaseCommand


class IndicesUpgradeCommand(CreateBaseCommand):
    command_name = "elasticsearch:indices-upgrade"

    def is_enabled(self):
        return True

    def run_request(self, index=None):
        if not index:
            self.show_index_list_panel(self.run)
            return

        options = dict(
            index=index
        )

        return self.client.indices.upgrade(**options)
