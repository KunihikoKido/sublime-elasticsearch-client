from .base import BaseCommand


class IndicesGetCommand(BaseCommand):
    command_name = "elasticsearch:indices-get"

    def is_enabled(self):
        return True

    def run_request(self, index=None):
        if index is None:
            self.show_index_list_panel(self.run)
            return

        options = dict(
            index=index
        )

        return self.client.indices.get(**options)
