from .base import BaseCommand


class InfoCommand(BaseCommand):
    command_name = "elasticsearch:info"

    def is_enabled(self):
        return True

    def run_request(self):
        options = dict()
        return self.client.info(**options)
