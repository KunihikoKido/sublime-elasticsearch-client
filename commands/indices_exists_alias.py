from .base import BaseCommand


class IndicesExistsAliasCommand(BaseCommand):
    command_name = "elasticsearch:indices-exists-alias"

    def is_enabled(self):
        return True

    def run_request(self, name=None):
        if not name:
            self.show_input_panel('Alias Name: ', '', self.run)
            return

        options = dict(
            index=self.settings.index,
            name=name
        )

        return self.client.indices.exists_alias(**options)
