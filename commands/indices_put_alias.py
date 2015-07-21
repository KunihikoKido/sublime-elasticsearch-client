from .base import CreateBaseCommand


class IndicesPutAliasCommand(CreateBaseCommand):
    command_name = "elasticsearch:indices-put-alias"

    def is_enabled(self):
        return True

    def run_request(self, name=None):
        if name is None:
            self.show_input_panel(
                'Alias Name: ', '', self.run)
            return

        options = dict(
            index=self.settings.index,
            name=name
        )

        return self.client.indices.put_alias(**options)
