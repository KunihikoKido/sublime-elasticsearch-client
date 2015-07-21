from .base import BaseCommand


class IndicesExistsCommand(BaseCommand):
    command_name = "elasticsearch:indices-exists"

    def is_enabled(self):
        return True

    def run_request(self, index=None):
        if not index:
            self.show_input_panel('Index Name: ', '', self.run)
            return

        options = dict(
            index=index
        )

        return self.client.indices.exists(**options)
