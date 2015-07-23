from .base import BaseCommand


class CountPercolateCommand(BaseCommand):
    command_name = "elasticsearch:count-percolate"

    def run_request(self):
        options = dict(
            index=self.settings.index,
            doc_type=self.settings.doc_type,
            body=self.get_text()
        )

        return self.client.count_percolate(**options)
