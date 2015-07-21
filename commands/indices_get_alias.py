from .base import BaseCommand


class IndicesGetAliasCommand(BaseCommand):
    command_name = "elasticsearch:indices-get-alias"

    def is_enabled(self):
        return True

    def run_request(self, index=None, name=None):
        if not index or not name:
            self.show_alias_list_panel(self.run)
            return

        options = dict(
            index=index,
            name=name
        )

        return self.client.indices.get_alias(**options)
