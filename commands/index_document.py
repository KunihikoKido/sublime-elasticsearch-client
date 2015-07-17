from .base import BaseCommand


class IndexDocumentCommand(BaseCommand):

    def run_request(self, id=None):
        if id is None:
            self.show_input_panel(
                'Document Id (option): ', '', self.run_request)
            return

        options = dict(
            index=self.settings.index,
            doc_type=self.settings.doc_type,
            body=self.get_text(),
            id=id
        )

        response = self.client.index(**options)
        self.show_object_output_panel(response)
