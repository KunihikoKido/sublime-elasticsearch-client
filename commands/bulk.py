from .base import CreateBaseCommand


class BulkCommand(CreateBaseCommand):
    command_name = "elasticsearch:bulk"

    def is_enabled(self):
        if not self.get_text():
            return False
        return True

    def run_request(self):
        options = dict(
            index=self.settings.index,
            doc_type=self.settings.doc_type,
            body=self.get_text()
        )

        return self.client.bulk(**options)
