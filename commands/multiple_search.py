from .base import BaseCommand


class MultipleSearchCommand(BaseCommand):
    command_name = "elasticsearch:multiple-search"

    def run_request(self):
        options = dict(
            index=self.settings.index,
            doc_type=self.settings.doc_type,
            body=self.get_text()
        )
        return self.client.msearch(**options)
