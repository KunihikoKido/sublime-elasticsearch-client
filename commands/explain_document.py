from .base import BaseCommand


class ExplainDocumentCommand(BaseCommand):
    command_name = "elasticsearch:explain-document"

    def run_request(self, id=None):
        if not id:
            self.show_input_panel('Document Id: ', '', self.run)
            return

        options = dict(
            index=self.settings.index,
            doc_type=self.settings.doc_type,
            body=self.get_text(),
            id=id
        )

        return self.client.explain(**options)
