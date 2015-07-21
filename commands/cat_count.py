from .base import CatBaseCommand


class CatCountCommand(CatBaseCommand):
    command_name = "elasticsearch:cat-count"

    def run_request(self, index=None):
        if index is None:
            self.show_index_list_panel(self.run)
            return

        options = dict(
            index=index,
            params=dict(v=1)
        )

        return self.client.cat.count(**options)
