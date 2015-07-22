from .base import BaseCommand


class MultipleTermvectorsCommand(BaseCommand):
    command_name = "elasticsearch:multiple-termvectors"

    def run_request(self):
        options = dict(
            index=self.settings.index,
            doc_type=self.settings.doc_type,
            body=self.get_text()
        )
        return self.client.mtermvectors(**options)
