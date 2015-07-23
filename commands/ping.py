from .base import BaseCommand


class PingCommand(BaseCommand):
    command_name = "elasticsearch:ping"

    def is_enabled(self):
        return True

    def run_request(self):
        options = dict()
        return self.client.ping(**options)
