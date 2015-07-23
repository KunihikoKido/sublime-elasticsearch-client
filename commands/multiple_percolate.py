from .base import BaseCommand


class MultiplePercolateCommand(BaseCommand):
    command_name = "elasticsearch:multiple-percolate"

    def run_request(self):
        options = dict(
            index=self.settings.index,
            doc_type=self.settings.doc_type,
            body=self.get_text()
        )
        return self.client.mpercolate(**options)
