from .base import BaseCommand


class IndicesStatsCommand(BaseCommand):
    command_name = "elasticsearch:indices-stats"

    def is_enabled(self):
        return True

    def run_request(self, index=None):
        if index is None:
            self.show_index_list_panel(self.run)
            return

        options = dict(
            index=index,
            params=dict(human=True)
        )

        return self.client.indices.stats(**options)
