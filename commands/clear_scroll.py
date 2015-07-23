from .base import CreateBaseCommand


class ClearScrollCommand(CreateBaseCommand):
    command_name = "elasticsearch:clear-scroll"

    def is_enabled(self):
        return True

    def run_request(self, scroll_id=None):
        if not scroll_id:
            self.show_input_panel(
                'Scroll Id: ', '', self.run)
            return

        options = dict(
            scroll_id=scroll_id
        )

        return self.client.clear_scroll(**options)
