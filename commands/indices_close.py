from .base import BaseCommand


class IndicesCloseCommand(BaseCommand):

    def is_enabled(self):
        return True

    def run_request(self, index=None):
        if index is None:
            self.show_index_list_panel(self.run_request)
            return

        options = dict(
            index=index
        )

        response = self.client.indices.close(**options)
        self.show_object_output_panel(response)
