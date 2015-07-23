from .base import BaseCommand


class GetMultipleDocumentsCommand(BaseCommand):
    command_name = "elasticsearch:get-multiple-document"

    def run_request(self):
        options = dict(
            index=self.settings.index,
            doc_type=self.settings.doc_type,
            body=self.get_text()
        )

        return self.client.mget(**options)
