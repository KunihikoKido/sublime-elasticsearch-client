from .base import BaseCommand


class SuggestCommand(BaseCommand):
    command_name = "elasticsearch:suggest"

    def run_request(self):
        options = dict(
            index=self.settings.index,
            body=self.get_text(),
            ignore=[404]
        )

        return self.client.suggest(**options)
