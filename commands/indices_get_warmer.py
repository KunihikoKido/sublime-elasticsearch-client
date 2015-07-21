from .base import BaseCommand


class IndicesGetWarmerCommand(BaseCommand):
    command_name = "elasticsearch:indices-get-warmer"

    def is_enabled(self):
        return True

    def run_request(self, name=None):
        if not name:
            self.show_warmer_list_panel(self.run)
            return

        options = dict(
            index=self.settings.index,
            name=name
        )

        return self.client.indices.get_warmer(**options)
