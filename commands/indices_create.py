from .base import CreateBaseCommand


class IndicesCreateCommand(CreateBaseCommand):
    command_name = "elasticsearch:indices-create"

    def is_enabled(self):
        return True

    def run_request(self, index=None):
        if not index:
            self.show_input_panel(
                'Index name: ', self.settings.index, self.run)
            return

        options = dict(
            index=index
        )

        return self.client.indices.create(**options)
