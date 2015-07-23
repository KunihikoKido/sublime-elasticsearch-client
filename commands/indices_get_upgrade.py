from .base import BaseCommand


class IndicesGetUpgradeCommand(BaseCommand):
    command_name = "elasticsearch:indices-get-upgrade"

    def is_enabled(self):
        return True

    def run_request(self, index=None):
        if not index:
            self.show_index_list_panel(self.run)
            return

        options = dict(
            index=index,
            params=dict(human=True)
        )

        return self.client.indices.get_upgrade(**options)
