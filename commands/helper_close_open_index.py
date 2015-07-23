from .base import CreateBaseCommand


class HelperCloseOpenIndexCommand(CreateBaseCommand):
    command_name = "elasticsearch:helper-close-open-index"

    def is_enabled(self):
        return True

    def run_request(self, index=None):
        if not index:
            self.show_index_list_panel(self.run)
            return

        response_close = self.client.indices.close(index=index)
        response_open = self.client.indices.close(index=index)
        return dict(
            command=self.command_name,
            close=response_close, open=response_open)
