from .base import BaseCommand


class ScrollCommand(BaseCommand):
    command_name = "elasticsearch:scroll"

    def is_enabled(self):
        return True

    def run_request(self, scroll_id=None):
        if not scroll_id:
            self.show_input_panel(
                'Scroll Id: ', '', self.run)
            return

        options = dict(
            scroll_id=scroll_id,
            params=dict(scroll=self.settings.scroll_size)
        )

        return self.client.scroll(**options)
