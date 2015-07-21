from .base import CatBaseCommand


class CatSegmentsCommand(CatBaseCommand):
    command_name = "elasticsearch:cat-segments"

    def run_request(self, index=None):
        if index is None:
            self.show_index_list_panel(self.run)
            return

        options = dict(
            index=index,
            params=dict(v=1)
        )

        return self.client.cat.segments(**options)
