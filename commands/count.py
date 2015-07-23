from .base import BaseCommand


class CountCommand(BaseCommand):
    command_name = "elasticsearch:count"

    def is_enabled(self):
        return True

    def run_request(self, index=None):
        if not index:
            self.show_index_list_panel(self.run)
            return
        options = dict(
            index=index
        )

        return self.client.count(**options)
