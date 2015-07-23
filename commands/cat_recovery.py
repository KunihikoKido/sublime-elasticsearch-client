from .base import CatBaseCommand


class CatRecoveryCommand(CatBaseCommand):
    command_name = "elasticsearch:cat-recovery"

    def run_request(self, index=None):
        if index is None:
            self.show_index_list_panel(self.run)
            return

        options = dict(
            index=index,
            params=dict(v=1)
        )

        return self.client.cat.recovery(**options)
