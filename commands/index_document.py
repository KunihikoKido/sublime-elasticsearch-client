from .base import CreateBaseCommand


class IndexDocumentCommand(CreateBaseCommand):
    command_name = "elasticsearch:index-document"

    def run_request(self, id=None):
        if id is None:
            self.show_input_panel(
                'Document Id (option): ', '', self.run)
            return

        options = dict(
            index=self.settings.index,
            doc_type=self.settings.doc_type,
            body=self.get_text(),
            id=id
        )

        return self.client.index(**options)
