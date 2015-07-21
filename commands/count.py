from .base import BaseCommand


class CountCommand(BaseCommand):
    command_name = "elasticsearch:count"

    def run_request(self):
        options = dict(
            index=self.settings.index,
            doc_type=self.settings.doc_type,
            body=self.get_text()
        )

        return self.client.count(**options)
