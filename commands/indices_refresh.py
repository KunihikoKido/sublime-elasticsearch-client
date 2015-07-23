from .base import CreateBaseCommand


class IndicesRefreshCommand(CreateBaseCommand):
    command_name = "elasticsearch:indices-refresh"

    def is_enabled(self):
        return True

    def run_request(self, index=None):
        if not index:
            self.show_index_list_panel(self.run)
            return

        options = dict(
            index=self.settings.index
        )

        return self.client.indices.refresh(**options)
